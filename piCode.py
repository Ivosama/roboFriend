""" File for running the code on the Raspberry Pi"""
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import thresholding
import Detect
import sys
import eyes
import SmileDetection
import Eyebrows
import PyGame
import time
import cv2
import io
import Reactions

blobDetector = Detect.BlobDetector()
sys.setrecursionlimit(5000)

# Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.color_effects = (128, 128)  # his sets the channels to capture only black and white
camera.framerate = 1
rawCapture = PiRGBArray(camera, size=(640, 480))

# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# allow the camera to warmup
time.sleep(0.1)

r = Reactions.Reactions()
r.initMem()


# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    eb = Eyebrows.Eyebrows()
    b = Detect.BlobDetector()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    PyGame.screen.fill((0,0,0))

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    PyGame.neutralFace()

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        th = thresholding.getThDynamic(gray, y, y + h, x, x + w)
        extraImg = thresholding.setTh(gray.copy(), y, y + h, x, x + w, th / 3 + 10)
        extraImg = cv2.medianBlur(extraImg, 5)
        browState = eb.getStateOfBrows(extraImg, b, y, y + h, x, x + w, 0)

        mouthMinX = int(x + (w / 4) - (w / 16))
        mouthMinY = int(y + 3 * (h / 4) - (h / 8))
        mouthMaxX = int(x + 3 * (w / 4) + (w / 16))
        mouthMaxY = int(y + 3 * (h / 4) + h / 8 + h / 16)
        mouthH = mouthMaxY - mouthMinY

        mouthYPosition = int(mouthMinY + (mouthH / 8) * 5)

        isSmiling, isFrowning = SmileDetection.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX,
                                                            mouthMaxY - mouthMinY)
        if isSmiling:
            r.updateMouth(1)
            r.updateBrow(browState)
        elif isFrowning:
            r.updateMouth(2)
            r.updateBrow(browState)
        else:
            r.updateMouth(0)
            r.updateBrow(browState)

        rawCapture.flush()
        r.getReaction()

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if cv2.waitKey(1) and 0xFF == ord ('q'):
        break