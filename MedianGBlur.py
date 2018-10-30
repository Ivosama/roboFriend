# Don't get confused there's nothing median about this function
import cv2
import numpy as np

startImg = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_GRAYSCALE)


def medianBlur(src, searchDistance):
    # swag boi dolla dolla bill$ holla at me
    height, width = src.shape
    outputImage = np.zeros((height, width, 1), np.uint8)
    for y in range(1 + searchDistance, height - 1 - searchDistance):
        for x in range(1 + searchDistance, width - 1 - searchDistance):
            surroundingPixels = []
            startY = y-searchDistance
            startX = x-searchDistance
            for searchY in range(y+searchDistance+1-startY):
                for searchX in range(x+searchDistance+1-startX):
                    surroundingPixels.append(src[startY + searchY, startX + searchX])

            outputImage[y, x] = np.median(surroundingPixels)

    return outputImage

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    editedImage = medianBlur(frame, 3)
    #editedImage = cv2.medianBlur(frame, 5)
    cv2.imshow("preview", editedImage)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")