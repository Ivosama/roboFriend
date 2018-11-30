import cv2
import numpy as np
import PyGame
import SmileDetection
import eyes
import sys
import Eyebrows
import Detect
import pygame
import thresholding
import Reactions
import SmileDetectionEVENOLDER

cap = cv2.VideoCapture(0)
sys.setrecursionlimit(3000)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
awake = cv2.imread('TestImages/awake.jpg')
sleep = cv2.imread('TestImages/sleeprobo.jpg')
#
r = Reactions.Reactions()
r.initMem()




def getThDynamic(img, yMin, yMax, xMin, xMax):
    valueCounter = 0
    pixelCounter = 0
    #print(yMin, yMax, xMin, xMax)

    valueCounter = np.sum(img)
    pixelCounter = np.size(img)
    print (valueCounter / pixelCounter)

    """
        for y in range (yMin, yMax):
        for x in range (xMin, xMax):
            valueCounter += img[y, x]
            pixelCounter += 1

    """

    if pixelCounter != 0:
        return valueCounter / pixelCounter
    else:
        return 0

def setTh(img, yMin, yMax, xMin, xMax, th):
    for y in range (yMin, yMax):
        for x in range (xMin, xMax):
            if img[y, x] >= th:
                img[y, x] = 0
            else:
                img[y, x] = 255

    return img

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eb = Eyebrows.Eyebrows()
    b = Detect.BlobDetector()
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    PyGame.screen.fill((0, 0, 0))

    if (len(faces)>=1):
        cv2.imshow("Awake", awake)
        cv2.destroyWindow("Sleep")
    elif (len(faces)== 0):
        cv2.imshow("Sleep", sleep)
        cv2.destroyWindow("Awake")

    for (x, y, w, h) in faces:
        th = getThDynamic(gray, y, y + h, x, x + w)
        extraImg = setTh(gray.copy(), y, y + h, x, x + w, th / 3 + 10)
        extraImg = cv2.medianBlur(extraImg, 5)
        browState = eb.getStateOfBrows(extraImg, b, y, y + h, x, x + w, 0)
        cv2.rectangle(gray, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)

        mouthMinX = int(x + (w / 4) - (w / 16))
        mouthMinY = int(y + 3 * (h / 4) - (h / 8))
        mouthMaxX = int(x + 3 * (w / 4) + (w / 16))
        mouthMaxY = int(y + 3 * (h / 4) + h / 8 + h / 16)
        mouthH = mouthMaxY - mouthMinY

        mouthYPosition = int(mouthMinY + (mouthH / 8) * 5)

        if SmileDetectionEVENOLDER.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX, mouthMaxY - mouthMinY):
            PyGame.happyFace()
            print("true")
        else:
            PyGame.angryFace()
            print("false")

        cv2.imshow("Smile", gray)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()