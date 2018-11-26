import cv2
import numpy as np

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
awake = cv2.imread('TestImages/awake.jpg')
sleep = cv2.imread('TestImages/sleeprobo.jpg')


while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    editedImage = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    if (len(faces)>=1):
        cv2.imshow("Awake", awake)
        cv2.destroyWindow("Sleep")
    elif (len(faces)== 0):
        cv2.imshow("Sleep", sleep)
        cv2.destroyWindow("Awake")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()