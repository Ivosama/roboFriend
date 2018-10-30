# Don't get confused there's nothing median about this function
import cv2
import numpy as np

startImg = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_GRAYSCALE)

cv2.medianBlur()

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

editedImage = medianBlur(startImg, 3)

cv2.imshow("Output", editedImage)
cv2.waitKey()