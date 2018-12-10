import thresholding
import Detect
import sys
import SmileDetection
import Eyebrows
import PyGame
import time
import cv2
import Reactions
import threading

# Camera settings go here
imageWidth = 640
imageHeight = 480
frameRate = 1
processingThreads = 1

# Shared values
global running
global cap
global frameLock
global processorPool
running = True
frameLock = threading.Lock()

# Setup the camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, imageWidth);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, imageHeight);
cap.set(cv2.CAP_PROP_FPS, frameRate);
if not cap.isOpened():
    cap.open()

# Image processing thread, self-starting
class ImageProcessor(threading.Thread):
    def __init__(self, name, autoRun=True):
        super(ImageProcessor, self).__init__()
        self.event = threading.Event()
        self.eventWait = (2.0 * processingThreads) / frameRate
        self.name = str(name)
        print
        'Processor thread %s started with idle time of %.2fs' % (self.name, self.eventWait)
        self.start()

    def run(self):
        # This method runs in a separate thread
        global running
        global frameLock
        global processorPool
        while running:
            # Wait for an image to be written to the stream
            self.event.wait(self.eventWait)
            if self.event.isSet():
                if not running:
                    break
                try:
                    self.ProcessImage(self.nextFrame)
                finally:
                    # Reset the event
                    self.nextFrame = None
                    self.event.clear()
                    # Return ourselves to the pool at the back
                    with frameLock:
                        processorPool.insert(0, self)
        print
        'Processor thread %s terminated' % (self.name)

    def ProcessImage(self, image):

        #Changes the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #loads the face cascade
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        PyGame.screen.fill((0, 0, 0))

        for (x, y, w, h) in faces:
            th = thresholding.getThDynamic(gray, y, y + h, x, x + w)
            extraImg = thresholding.setTh(gray.copy(), y, y + h, x, x + w, th - 20)
            extraImg = cv2.medianBlur(extraImg, 5)
            #cv2.imshow("FUCK", extraImg)
            browState = eb.getStateOfBrows(extraImg, b, y, y + h, x, x + w, 0)
            cv2.rectangle(gray, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)

            mouthMinX = int(x + (w / 4) - (w / 16))
            mouthMinY = int(y + 3 * (h / 4) - (h / 8))
            mouthMaxX = int(x + 3 * (w / 4) + (w / 16))
            mouthMaxY = int(y + 3 * (h / 4) + h / 8 + h / 16)
            mouthH = mouthMaxY - mouthMinY

            mouthYPosition = int(mouthMinY + (mouthH / 8) * 5)

            isSmiling, isFrowning = SmileDetection.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX,
                                                                mouthMaxY - mouthMinY)
            if isSmiling:
                #print('Smile detected directly')
                r.updateMouth(1)
                r.updateBrow(browState)
            elif isFrowning:
                r.updateMouth(2)
                r.updateBrow(browState)
            else:
                r.updateMouth(0)
                r.updateBrow(browState)
            r.getReaction()
            print("--------------------")


# Image capture thread, self-starting
class ImageCapture(threading.Thread):
    def __init__(self):
        super(ImageCapture, self).__init__()
        self.start()

    # Stream delegation loop
    def run(self):
        # This method runs in a separate thread
        global running
        global cap
        global processorPool
        global frameLock
        while running:
            # Grab the oldest unused processor thread
            with frameLock:
                if processorPool:
                    processor = processorPool.pop()
                else:
                    processor = None
            if processor:
                # Grab the next frame and send it to the processor
                success, frame = cap.read()
                if success:
                    processor.nextFrame = frame
                    processor.event.set()
                else:
                    print
                    'Capture stream lost...'
                    running = False
            else:
                # When the pool is starved we wait a while to allow a processor to finish
                time.sleep(0.01)
        print
        'Capture thread terminated'

# Create some threads for processing and frame grabbing
processorPool = [ImageProcessor(i + 1) for i in range(processingThreads)
                 ]
allProcessors = processorPool[:]
captureThread = ImageCapture()


#Initializes reactions eyebrows and blobs
r = Reactions.Reactions()
r.initMem()
eb = Eyebrows.Eyebrows()
b = Detect.BlobDetector()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')


# Main loop, basically waits until you press CTRL+C
# The captureThread gets the frames and passes them to an unused processing thread
try:
    print
    'Press CTRL+C to quit'
    while running:
        time.sleep(1)
except KeyboardInterrupt:
    print
    '\nUser shutdown'
except:
    e = sys.exc_info()
    print
    print
    e
    print
    '\nUnexpected error, shutting down!'

# Cleanup all processing threads
running = False
while allProcessors:
    # Get the next running thread
    with frameLock:
        processor = allProcessors.pop()
    # Send an event and wait until it finishes
    processor.event.set()
    processor.join()

# Cleanup the capture thread
captureThread.join()

# Cleanup the camera object
cap.release()

