import cv2
import numpy as np
import thresholding
import MedianGBlur
import Detect
import sys
import eyes
import SmileDetection
import PyGame
import cum_hist as ch
import histogram as hg
import FrownDetection
import SmileDetectionOLD
import SmileDetectionEVENOLDER

eyes = eyes.Eyes()

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
blobDetector = Detect.BlobDetector()
sys.setrecursionlimit(5000)

while True:
    ret, frame = cap.read()
    #frame = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.imread("TestImages/Peter.png", cv2.IMREAD_GRAYSCALE)
    editedImage = np.zeros((gray.shape[0], gray.shape[1]), np.uint8)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    PyGame.screen.fill((0, 0, 0))

    for (x, y, w, h) in faces:
        #cv2.imwrite("TestImages/NightSmile.png", gray)
        cv2.rectangle(editedImage, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
        editedImage = eyes.drawSquaresOnEyes(gray, x, y, w, h)

        mouthMinX = int(x + (w / 4) - (w / 16))
        mouthMinY = int(y + 3 * (h / 4) - (h / 8))
        mouthMaxX = int(x + 3 * (w / 4) + (w / 16))
        mouthMaxY = int(y + 3 * (h / 4) + h / 8 + h / 16)
        mouthH = mouthMaxY - mouthMinY

        mouthYPosition = int(mouthMinY + (mouthH / 8) * 5)
        isSmiling, isFrowning = SmileDetection.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX, mouthMaxY - mouthMinY)
        #isSmiling = SmileDetectionEVENOLDER.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX, mouthMaxY - mouthMinY)
        if isSmiling:
            cv2.imshow("Smile", gray)
            PyGame.happyFace()
        elif isFrowning:
            cv2.imshow("Frown", gray)
            PyGame.sadFace()
        else:
            cv2.imshow("Normal", gray)

        #sys.exit("Yote")
        #editedImage = MedianGBlur.medianBlur(gray, editedImage, 3, x, y, w, h)
        #editedImage = thresholding.th(editedImage, x, y, (w + x), (h + y), 40)
        #editedImage = blobDetector.thImage(editedImage, 40)
        #editedImage = thresholding.th(gray, x, y, (w+x), (h+y), -45)
        #editedImage = thresholding.thSplit(gray, x, y, (w+x), (h+y), 0, 0)
        #editedImage = thresholding.thHSL(frame, x, y, (w + x), (h + y), 0)
        #editedImage = blobDetector.getObjectImage(editedImage, y, y+h, x, x+w, 50, 100)

    #print(SmileDetection.getHistogramMedian(gray))

    #cv2.imshow("imshow", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()