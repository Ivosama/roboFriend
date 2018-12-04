
import cv2
import numpy as np
import thresholding
import MedianGBlur
import Detect
import sys


class Eyebrows:

    def placeBarsOnBrows(self, img, yMin, yMax, xMin, xMax, sizeY, sizeX):
        width = (xMax - xMin) / 3 #starting point of bars x axis
        height = (yMax - yMin) / 8 #starting point of bars y axis

        #Draw left brow bar
        for y in range (int(yMin + height), int(yMin + height + sizeY)):
            for x in range (int(xMin + width - (sizeX / 2)), int(xMin + width + (sizeX / 2))):
                if y < yMax:
                    if x < xMax:
                        img[y, x] = 0

        #Draw right brow bar
        for y in range (int(yMin + height), int(yMin + height + sizeY)):
            for x in range (int(xMin + (width*2) - (sizeX / 2)), int(xMin + (width*2) + (sizeX / 2))):
                if y < yMax:
                    if x < xMax:
                        img[y, x] = 0

        return img

    def getStateOfBrows(self, img, blobDetector, yMin, yMax, xMin, xMax, posTH): # Args : image, blobDetector-object, start Y, end Y, start X, end X, position TH (position tolerance)

        h = yMax - yMin # Height of brow area
        w = xMax - xMin # width of brow area

        state = 0 # Browstate  -  Returns 0 for neutral, 1 for happy, 2 for angry

        sizeX = int(3*w / 4) # width of brow detection area
        sizeY = int(h / 6) # half height of brow detection area

        yCenter = int(yMin + (2 * h / 8)) # Center of brow detection area
        yStart = int(yCenter - sizeY) # starting point of brow detection area
        yEnd = int(yCenter + sizeY)  # end point of brow detection area

        xCenter = int(xMin + (w / 2)) # center of brow detection x
        xStart = int(xCenter - (sizeX/2)) # start of brow detection area on x axis
        xEnd = int(xCenter + (sizeX/2)) # end of brow detection area on x axis

        img = self.placeBarsOnBrows(img, yMin, yMax, xMin, xMax, 40, 5) # Modify image by placing bars on brows

        objectImg = blobDetector.getObjectImage(img, yStart, yEnd, xStart, xEnd, 0, 0) # Do BLOB-detection in brow area, save as new image
        objects = blobDetector.getBlobIDsInArea(objectImg, yStart, yEnd, xStart, xEnd) # Get the BLOB-IDs of detected BLOBs in area
        objects.pop(0)
        """
        
        """

        objects = blobDetector.getClosestBlobs(img, objects, yMin, yMax, xMin, xMax, yCenter, xCenter, 4) # Discard furthest dots from center of brow area untill 4 are left
        if objects:

            left = 0 # Temporary assignemnt of leftmost dot
            leftCenter = 0 # Left center eyebrow dot

            right = 0 # Rightmost dot
            rightCenter = 0 # Right center dot
            positions = [] # Array for storing the positions of the individual blobs

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

                    if pos[0] <= xMinCurrent: # Find and set the leftmost brow
                        xMinCurrent = pos[0]
                        left = i

                    if pos[0] >= xMaxCurrent: # Find and set the rightmost brow
                        xMaxCurrent = pos[0]
                        right = i

                for i in range(0, len(objects)):
                    if i != left:
                        if i != right:
                            if positions[i][0] <= tempCenter:
                                leftCenter = i # Find and set the inner left brow

                for i in range(0, len(objects)):
                    if i != left:
                        if i != right:
                            if i != leftCenter:
                                rightCenter = i # Find last dot, and set as right center

                rightState = 0 # Temp state of right eyebrow
                leftState = 0 # Temp state of left eyebrow

                if positions[right][1] <= positions[rightCenter][1] - posTH: # If the outhermost dots are lower than the inner dots
                    if positions[left][1] <= positions[leftCenter][1] - posTH:
                        rightState = 1 # Set state of brows to be happy
                        leftState = 1

                if positions[right][1] >= positions[rightCenter][1] + posTH: # If the outermost dots are higher than the inner dots
                    if positions[left][1] >= positions[leftCenter][1] + posTH:
                        rightState = 2 # Set state of brows to be angry
                        leftState = 2

                if positions[right][1] < positions[rightCenter][1] + posTH: # If brows are at same height
                    if positions[right][1] > positions[rightCenter][1] - posTH: # Or at least within posTH tolerances
                        rightState = 0 # Set state of brows as neutral

                if positions[left][1] < positions[leftCenter][1] + posTH: # Same as above
                    if positions[left][1] > positions[leftCenter][1] - posTH:
                        leftState = 0

                state = int((rightState + leftState) / 2)
                print("Eyebrow detector state: " + str(state))
                #print("Right ")
                #print(rightState)
                #print("Left ")
                #print(leftState)


        return state


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
