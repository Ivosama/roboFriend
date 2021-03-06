""" File which is testable on a computer with a webcam or other connected camera """

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


cap = cv2.VideoCapture(0)
sys.setrecursionlimit(5000)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
r = Reactions.Reactions()
r.initMem()

eb = Eyebrows.Eyebrows()
b = Detect.BlobDetector()

while True:
    ret, frame = cap.read()
    print(len(frame))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    PyGame.screen.fill((0, 0, 0))

    for (x, y, w, h) in faces:
        th = thresholding.getThDynamic(gray, y, y + h, x, x + w)
        extraImg = thresholding.setTh(gray.copy(), y, y + h, x, x + w, th - 20)
        extraImg = cv2.medianBlur(extraImg, 5)
        cv2.imshow("FUCK", extraImg)
        browState = eb.getStateOfBrows(extraImg, b, y, y + h, x, x + w, 0)
        cv2.rectangle(gray, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)

        mouthMinX = int(x + (w / 4) - (w / 16))
        mouthMinY = int(y + 3 * (h / 4) - (h / 8))
        mouthMaxX = int(x + 3 * (w / 4) + (w / 16))
        mouthMaxY = int(y + 3 * (h / 4) + h / 8 + h / 16)
        mouthH = mouthMaxY - mouthMinY

        mouthYPosition = int(mouthMinY + (mouthH / 8) * 5)

        isSmiling, isFrowning = SmileDetection.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX, mouthMaxY - mouthMinY)
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


    # Allow the program to be closed with the key, q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()