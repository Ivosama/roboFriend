

class BlobDetector:


    import cv2
    import numpy as np
    import sys

    h = 2
    w = 2

    img = np.zeros((h, w, 1), np.uint8)

    objectImage = np.zeros((h, w, 1), np.uint8)

    #def __init__(self):


    def setImage(self, image):
        self.img = image
        self.h, self.w = img.shape
        self.objectImage = np.zeros((h, w, 1), np.uint8)


    """
    def getBlobID(self, image, xMin, xMax, yMin, yMax):
        
        currentID = 0
        
        blob1Counter = 0
        blob2Counter = 0
        blob3Counter = 0
        
        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                if image[y,x] != 0:
    """

    def getBlobIDsInArea(self, image, yMin, yMax, xMin, xMax):
        objectCounter = 0
        objectIDs = [0]

        for y in range (yMin, yMax):
            for x in range (xMin, xMax):
                currentID = image[y, x]
                if currentID != 0:
                    isInArray = 0
                    for i in range(0, objectIDs):
                        if currentID == objectIDs[i]:
                            isInArray = 1

                    if isInArray == 0:
                        objectIDs.append(currentID)

        return objectIDs


    def getCenterOfBlob(self, image, blobID):
        h, w = image.shape

        xMin = w
        xMax = 0
        yMin = h
        yMax = 0

        for y in range(0, h):
            for x in range(0, w):
                if image[y,x] == blobID:
                    if x < xMin:
                        xMin = x
                    if x > xMax:
                        xMax = x
                    if y < yMin:
                        yMin = y
                    if y > yMax:
                        yMax = y

        return (xMin + xMax) / 2, (yMin + yMax) / 2

    def thImage(self, img, th):
        height, width = img.shape

        for y in range(0, height):
            for x in range(0, width):
                if (img[y, x] > th):
                    img[y, x] = 0
                else:
                    img[y, x] = 255

        return img

    def getObjectImage(self, image, yMin, yMax, xMin, xMax, blackTH, colorTH):

        self.setImage(self, image)

        objectCounter = 0

        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                if img[y, x] > blackTH:
                    objectCounter += 20
                    checkConnectivity(y, yMin, yMax, x, xMin, xMax, img[y, x], colorTH, objectCounter)

        return self.objectImage

    """
    def findAllObjects(self, image, yMin, yMax, xMin, xMax, blackTH, colorTH):

        self.setImage(self, image)

        objectCounter = 0

        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                if img[y, x] > blackTH:
                    objectCounter += 20
                    checkConnectivity(y, yMin, yMax, x, xMin, xMax, img[y, x], colorTH, objectCounter)
    """


    def checkConnectivity(self, y, yMin, yMax, x, xMin, xMax, color, colorTH, objectNumber):

        img[y, x] = 0
        objectImage[y, x] = objectNumber

        if x + 1 < xMax:
            right = img[y, x + 1]
            if right <= color + colorTH:
                if right >= color - colorTH:
                    checkConnectivity(y, yMin, yMax, x + 1, xMin, xMax, color, colorTH, objectNumber)

        if y + 1 < yMax:
            bottom = img[y + 1, x]
            if bottom <= color + colorTH:
                if bottom >= color - colorTH:
                    checkConnectivity(y + 1, yMin, yMax, x, xMin, xMax, color, colorTH, objectNumber)

        if x - 1 > xMin:
            left = img[y, x - 1]
            if left <= color + colorTH:
                if left >= color - colorTH:
                    checkConnectivity(y, yMin, yMax, x - 1, xMin, xMax, color, colorTH, objectNumber)

        if y - 1 > yMin:
            top = img[y - 1, x]
            if top <= color + colorTH:
                if top >= color - colorTH:
                    checkConnectivity(y - 1, yMin, yMax, x, xMin, xMax, color, colorTH, objectNumber)

