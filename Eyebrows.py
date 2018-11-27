
import cv2
import numpy as np
import thresholding
import MedianGBlur
import Detect
import sys


class Eyebrows:

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

    def getStateOfBrows(self, img, blobDetector, yMin, yMax, xMin, xMax, posTH):

        h = yMax - yMin
        w = xMax - xMin

        sizeX = int(3*w / 4)
        sizeY = int(h / 6)

        yCenter = int(yMin + (2 * h / 8))
        yStart = int(yCenter - sizeY)
        yEnd = int(yCenter + sizeY)

        xCenter = int(xMin + (w / 2))
        xStart = int(xCenter - (sizeX/2))
        xEnd = int(xCenter + (sizeX/2))

        img = self.placeBarsOnBrows(img, yMin, yMax, xMin, xMax, 40, 5)

        objectImg = blobDetector.getObjectImage(img, yStart, yEnd, xStart, xEnd, 0, 0)
        objects = blobDetector.getBlobIDsInArea(objectImg, yStart, yEnd, xStart, xEnd)
        objects.pop(0)
        """
        
        """

        objects = blobDetector.getClosestBlobs(img, objects, yMin, yMax, xMin, xMax, yCenter, xCenter, 4)
        if objects:

            left = 0
            leftCenter = 0

            right = 0
            rightCenter = 0
            positions = []

            xMinCurrent = xMax
            xMaxCurrent = xMin
            currentLowest = 0
            currentHighest = 0

            tempCenter = xMax

            if len(objects) == 4:

                for i in range(0, len(objects)):

                    blobNum = objects[i]
                    pos = blobDetector.getCenterOfBlob(objectImg, blobNum, yMin, yMax, xMin, xMax)
                    positions.append(pos)

                    if pos[0] <= xMinCurrent:
                        xMinCurrent = pos[0]
                        left = i

                    if pos[0] >= xMaxCurrent:
                        xMaxCurrent = pos[0]
                        right = i

                for i in range(0, len(objects)):
                    if i != left:
                        if i != right:
                            if positions[i][0] <= tempCenter:
                                leftCenter = i

                for i in range(0, len(objects)):
                    if i != left:
                        if i != right:
                            if i != leftCenter:
                                rightCenter = i

                rightState = 0
                leftState = 0

                if positions[right][1] <= positions[rightCenter][1] - posTH:
                    if positions[left][1] <= positions[leftCenter][1] - posTH:
                        print(positions[right][1])
                        print(positions[rightCenter][1])
                        rightState = 1
                        leftState = 1

                if positions[right][1] >= positions[rightCenter][1] + posTH:
                    if positions[left][1] >= positions[leftCenter][1] + posTH:
                        rightState = 2
                        leftState = 2

                if positions[right][1] < positions[rightCenter][1] + posTH:
                    if positions[right][1] > positions[rightCenter][1] - posTH:
                        rightState = 0

                if positions[left][1] < positions[leftCenter][1] + posTH:
                    if positions[left][1] > positions[leftCenter][1] - posTH:
                        leftState = 0

                print("Right ")
                print(rightState)
                print("Left ")
                print(leftState)


        return img


    def getBlobInSide(self, positions, side):

        currentClosest = 0
        closestDist = 1000

        for i in range(0, len(positions)):
                if side == 0:
                    if positions[i][0] < closestDist:
                        currentClosest = i
                        closestDist = positions[0]


########## END OF CLASS ###########
"""
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
blobDetector = Detect.BlobDetector()
brows = Eyebrows()

sys.setrecursionlimit(5000)

while True:
    ret, frame = cap.read()
    #frame = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    editedImage = np.zeros((gray.shape[0], gray.shape[1]), np.uint8)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #editedImage = gray
        editedImage = MedianGBlur.medianBlur(gray, editedImage, 3, x, y, w, h)
        editedImage = blobDetector.thImage(editedImage, 40)
        editedImage = brows.getStateOfBrows(editedImage, blobDetector, y, y+h, x, x+h, 1)
        #editedImage = brows.placeBarsOnBrows(editedImage, y, y + h, x, x + w, 50, 10)
        #editedImage = thresholding.th(editedImage, x, y, (w + x), (h + y), 0)
        #editedImage = blobDetector.getObjectImage(editedImage, y, y+h, x, x+w, 50, 100)

    cv2.imshow("imshow", editedImage)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""
