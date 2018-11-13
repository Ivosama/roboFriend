# Thresholding code for fixing image n' stuff
import numpy as np
import cv2


def thresholding(img, stX, stY, endX, endY):
    height, width = img.shape
    bI = np.ones((height, width), np.uint8)
    sumPix = 0

    # Calculated the sum of the pixels in the detected face image square thingy
    for i in range(stY, endY):
        for j in range(stX, endX):
            sumPix += img.item(i, j)

    # Now calculates the prefered thresholding value from sum of pixels divided by the resolution
    TVa = sumPix / ((endX - stX) * (endY - stY))

    # Loop through image and set the pixels to be either black or white
    for i in range(stY, endY):
        for j in range(stX, endX):
            if img.item(i, j) >= TVa:
                bI[i, j] = 255
            elif img.item(i, j) < TVa:
                bI[i, j] = 0

    cv2.imshow('Thresholded Image', bI)
    print(TVa)