import cv2
import numpy as np
import PyGame
import SmileDetection
import eyes

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
awake = cv2.imread('TestImages/awake.jpg')
sleep = cv2.imread('TestImages/sleeprobo.jpg')


while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    PyGame.screen.fill((0, 0, 0))

    if (len(faces)>=1):
        cv2.imshow("Awake", awake)
        cv2.destroyWindow("Sleep")
    elif (len(faces)== 0):
        cv2.imshow("Sleep", sleep)
        cv2.destroyWindow("Awake")

    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)

        mouthMinX = int(x + (w / 4) - (w / 16))
        mouthMinY = int(y + 3 * (h / 4) - (h / 8))
        mouthMaxX = int(x + 3 * (w / 4) + (w / 16))
        mouthMaxY = int(y + 3 * (h / 4) + h / 8 + h / 16)
        mouthH = mouthMaxY - mouthMinY

        mouthYPosition = int(mouthMinY + (mouthH / 8) * 5)
        if SmileDetection.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX, mouthMaxY - mouthMinY):
            PyGame.happyFace()
        else:
            PyGame.sadFace()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()