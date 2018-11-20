import cv2
import numpy as np
import thresholding
import MedianGBlur
import Detect
import sys
import eyes

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
blobDetector = Detect.BlobDetector()
eyes = eyes.Eyes()
sys.setrecursionlimit(5000)

while True:
    ret, frame = cap.read()
    #frame = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    editedImage = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(editedImage, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)

        editedImage = eyes.drawSquaresOnEyes(gray, x, y, w, h)
        #editedImage = MedianGBlur.medianBlur(gray, editedImage, 3, x, y, w, h)
        #editedImage = thresholding.th(editedImage, x, y, (w + x), (h + y), 40)
        #editedImage = blobDetector.thImage(editedImage, 40)
        #editedImage = blobDetector.getObjectImage(editedImage, y, y+h, x, x+w, 50, 100)

    cv2.imshow("imshow", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()