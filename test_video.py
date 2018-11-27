# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import Detect
import sys
import eyes
import SmileDetection
import PyGame
import time
import cv2
import io

eyes = eyes.Eyes()
blobDetector = Detect.BlobDetector()
sys.setrecursionlimit(5000)

# Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.color_effects = (128, 128)  # his sets the channels to capture only black and white
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        eyes.drawSquaresOnEyes(gray, x, y, w, h)

        mouthMinX = int(x + (w / 4) - (w / 16))
        mouthMinY = int(y + 3 * (h / 4) - (h / 8))
        mouthMaxX = int(x + 3 * (w / 4) + (w / 16))
        mouthMaxY = int(y + 3 * (h / 4) + h / 8 + h / 16)
        mouthH = mouthMaxY - mouthMinY

        mouthYPosition = int(mouthMinY + (mouthH / 8) * 5)
        if SmileDetection.mouthSmiling(gray, mouthMinX, mouthMinY, mouthMaxX - mouthMinX, mouthMaxY - mouthMinY):
            cv2.imshow("Smile", gray)
            PyGame.happyFace()
        else:
            PyGame.sadFace()

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break