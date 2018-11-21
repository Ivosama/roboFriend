import cv2
import numpy as np
import thresholding
import MedianGBlur
import Detect
import sys

class Eyes:

    def drawSquaresOnEyes(self, img, x, y, w, h):

        if (w > 210 or w < 190):
            if (w > 210):
                scalar = 1.03
                #scalar = w / 230 #I need to find how to assign a max value for the scalar
                xStart = np.math.floor((x + (x + w) / 10) / scalar)
                yStart = np.math.floor(y + (h / 3.7))
                xEnd = np.math.floor((x + (x + w) / 4) / scalar)
                yEnd = np.math.floor(y + (h / 2))

                cv2.rectangle(img, (xStart, yStart), (xEnd, yEnd), (255, 0, 0), 3)

            if (w < 190):
                scalar = 1.105
                #scalar = w / 190 #I need to find how to assign a max value for the scalar

                xStart = np.math.floor((x + (x + w) / 10) / scalar)
                yStart = np.math.floor(y + (h / 3.7))
                xEnd = np.math.floor((x + (x + w) / 4) / scalar)
                yEnd = np.math.floor(y + (h / 2))

                cv2.rectangle(img, (xStart, yStart), (xEnd, yEnd), (255, 0, 0), 3)

        """
        xStart = np.math.floor((x + (x + w) / 10) / scalar)
        yStart = np.math.floor(y + (h / 3.7))
        xEnd = np.math.floor((x + (x + w) / 4) / scalar)
        yEnd = np.math.floor(y + (h / 2))
        """



    """
    def getStateOfEyes (self, img, blobDetector, yMin, yMax, xMin, xMax):


        objectImg = blobDetector.getObjectImage(img, yStart, yEnd, xStart, xEnd, 0, 0)
        objects = blobDetector.getBlobIDsInArea(objectImg, yStart, yEnd, xStart, xEnd)
        objects = blobDetector.getClosestBlobs(img, objects, yMin, yMax, xMin, xMax, yCenter, xCenter, 4)
        if objects:

            for i in range(0, len(objects)):
                print(objects[i])

        return img
"""

#### Class Test ####

"""
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
blobDetector = Detect.BlobDetector()
sys.setrecursionlimit(5000)

while True:
    ret, frame = cap.read()
    # frame = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    editedImage = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)


    for (x, y, w, h) in faces:
        cv2.rectangle(editedImage, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
        print(x, "x")
        print(y, "y")
        print(w, "w")
        print(h, "h")
        for (x, y, w, h) in faces:  # gotta add a scalar

            scalar = 1
            if (w > 210 or w < 190):
                if (w > 210):
                    scalar = 1.03
                    # scalar = w / 230 #I need to find how to assign a max value for the scalar

                if (w < 190):
                    scalar = 1.105
                    # scalar = w / 190 #I need to find how to assign a max value for the scalar

            print(scalar)
            xStart = np.math.floor((x + (x + w) / 10) / scalar)
            yStart = np.math.floor(y + (h / 3.7))
            xEnd = np.math.floor((x + (x + w) / 4) / scalar)
            yEnd = np.math.floor(y + (h / 2))

            cv2.rectangle(gray, (xStart, yStart), (xEnd, yEnd), (255, 0, 0), 3)

            # editedImage = MedianGBlur.medianBlur(gray, editedImage, 3, x, y, w, h)
            # editedImage = thresholding.th(editedImage, x, y, (w + x), (h + y), 40)
            # editedImage = blobDetector.thImage(editedImage, 40)
            # editedImage = blobDetector.getObjectImage(editedImage, y, y+h, x, x+w, 50, 100)

            cv2.imshow("imshow", gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

"""