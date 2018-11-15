
import cv2
import numpy as np
import thresholding
import MedianGBlur
import Detect
import sys





class Eyebrows:

    from Detect import BlobDetector

    import cv2
    import numpy as np

    b = BlobDetector()

    def getStateOfBrows(self, img, blobDetector, yMin, yMax, xMin, xMax):

        h = yMax - yMin
        w = xMax - xMin

        sizeX = int(3*w / 5)
        sizeY = int(h / 8)

        yStart = int(yMin + (2 * h / 7) - sizeY)
        yEnd = int(yMin + (2 * h / 7) + sizeY)

        xStart = int(xMin + (w/2) - (sizeX/2))
        xEnd = int(xMin + (w/2) + (sizeX/2))

        img = self.placeBarsOnBrows(img, yMin, yMax, xMin, xMax, 50, 5)

        tempImg = img

        objectImg = blobDetector.getObjectImage(tempImg, yStart, yEnd, xStart, xEnd, 0, 0)
        objects = blobDetector.getBlobIDsInArea(objectImg, yStart, yEnd, xStart, xEnd)

        for i in range (0, len(objects)):
            oH, oW = blobDetector.getCenterOfBlob(objectImg, objects[i])
            print (objects[i])

        return img


    def placeBarsOnBrows(self, img, yMin, yMax, xMin, xMax, sizeY, sizeX):
        width = (xMax - xMin) / 3
        height = (yMax - yMin) / 8

        #Left brow bar
        for y in range (int(yMin + height), int(yMin + height + sizeY)):
            for x in range (int(xMin + width - (sizeX / 2)), int(xMin + width + (sizeX / 2))):
                if y < yMax:
                    if x < xMax:
                        img[y, x] = 0

        #Right brow bar
        for y in range (int(yMin + height), int(yMin + height + sizeY)):
            for x in range (int(xMin + (width*2) - (sizeX / 2)), int(xMin + (width*2) + (sizeX / 2))):
                if y < yMax:
                    if x < xMax:
                        img[y, x] = 0

        return img


cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
blobDetector = Detect.BlobDetector()
brows = Eyebrows()

sys.setrecursionlimit(3000)

while True:
    ret, frame = cap.read()
    #frame = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    editedImage = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #editedImage = gray
        editedImage = MedianGBlur.medianBlur(gray, editedImage, 3, x, y, w, h)
        editedImage = blobDetector.thImage(editedImage, 60)
        editedImage = brows.getStateOfBrows(editedImage, blobDetector, y, y+h, x, x+h)
        #editedImage = brows.placeBarsOnBrows(editedImage, y, y + h, x, x + w, 50, 10)
        #editedImage = thresholding.th(editedImage, x, y, (w + x), (h + y), 0)
        #editedImage = blobDetector.getObjectImage(editedImage, y, y+h, x, x+w, 50, 100)

    cv2.imshow("imshow", editedImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()