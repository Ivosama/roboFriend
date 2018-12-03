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
r = Reactions.Reactions()
r.initMem()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eb = Eyebrows.Eyebrows()
    b = Detect.BlobDetector()
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    PyGame.screen.fill((0, 0, 0))

    for (x, y, w, h) in faces:
        th = thresholding.getThDynamic(gray, y, y + h, x, x + w)
        extraImg = thresholding.setTh(gray.copy(), y, y + h, x, x + w, th / 3 + 10)
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
            r.updateMouth(1)
            r.updateBrow(browState)
        else:
            r.updateMouth(0)
            r.updateBrow(browState)
    r.getReaction()


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()