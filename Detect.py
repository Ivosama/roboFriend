class BlobDetector:
    import cv2
    import numpy as np
    import sys

    h = 2
    w = 2

    img = np.zeros((h, w, 1), np.uint8)

    objectImage = np.zeros((h, w, 1), np.uint8)

    # def __init__(self):

    def setImage(self, image):
        self.img = image
        self.h, self.w = self.img.shape
        self.objectImage = self.np.zeros((self.h, self.w, 1), self.np.uint8)

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

        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                currentID = image[y, x]
                if currentID != 0:
                    isInArray = 0
                    for i in range(0, len(objectIDs)):
                        if currentID == objectIDs[i]:
                            isInArray = 1

                    if isInArray == 0:
                        objectIDs.append(currentID)

        return objectIDs

    def getClosestBlobs(self, img, blobs, pointY, pointX, amount):

        furthestID = 0
        furthestDist = 0

        if blobs:
            if len(blobs) > amount:
                for i in range (0, len(blobs)):
                    x, y = self.getCenterOfBlob(img, i)
                    distX = abs(pointX - x)
                    distY = abs(pointY - y)
                    dist = distX + distY

                    if dist > furthestDist:
                        furthestDist = dist
                        furthestID = i
                blobs.pop(furthestID)
                blobs = self.getClosestBlobs(img, blobs, pointY, pointX, amount)

        return blobs



    def eliminateFurthestBlob(self, img, blobs, pointY, pointX):
        if len(blobs) > 4:
            furthestBLob = 0
            furthestDist = 0
            for i in range (0, len(blobs)):
                x, y = self.getCenterOfBlob(img, blobs[i])
                dist = int(abs((x + y) - (pointX + pointY)))
                if dist > furthestDist:
                    furthestDist = dist
                    furthestBLob = i
            blobs.pop(furthestBLob)
            return blobs
        else:
            return blobs


    def getCenterOfBlob(self, image, blobID):
        h = image.shape[0]
        w = image.shape[1]

        xMin = w
        xMax = 0
        yMin = h
        yMax = 0

        for y in range(0, h):
            for x in range(0, w):
                if image[y, x] == blobID:
                    if x < xMin:
                        xMin = x
                    if x > xMax:
                        xMax = x
                    if y < yMin:
                        yMin = y
                    if y > yMax:
                        yMax = y

        return int((xMin + xMax) / 2), int((yMin + yMax) / 2)

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

        self.setImage(image)

        objectCounter = 0

        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                if self.img[y, x] > blackTH:
                    objectCounter += 1
                    self.checkConnectivity(y, yMin, yMax, x, xMin, xMax, self.img[y, x], colorTH, objectCounter)

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

        self.img[y, x] = 0
        self.objectImage[y, x] = objectNumber
        searchDistance = 1

        if x + searchDistance < xMax:
            right = self.img[y, x + 1]
            if right <= color + colorTH:
                if right >= color - colorTH:
                    self.checkConnectivity(y, yMin, yMax, x + 1, xMin, xMax, color, colorTH, objectNumber)

        if y + searchDistance < yMax:
            bottom = self.img[y + 1, x]
            if bottom <= color + colorTH:
                if bottom >= color - colorTH:
                    self.checkConnectivity(y + 1, yMin, yMax, x, xMin, xMax, color, colorTH, objectNumber)

        if x - searchDistance > xMin:
            left = self.img[y, x - 1]
            if left <= color + colorTH:
                if left >= color - colorTH:
                    self.checkConnectivity(y, yMin, yMax, x - 1, xMin, xMax, color, colorTH, objectNumber)

        if y - searchDistance > yMin:
            top = self.img[y - 1, x]
            if top <= color + colorTH:
                if top >= color - colorTH:
                    self.checkConnectivity(y - 1, yMin, yMax, x, xMin, xMax, color, colorTH, objectNumber)