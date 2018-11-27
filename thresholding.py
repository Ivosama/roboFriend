# Thresholding code for fixing image n' stuff
import numpy as np
import cv2
import math







# Thresholding using gray scale image and a dynamically calulated threshold from image
def th(img, stX, stY, endX, endY, thMod):
    height, width = img.shape
    bI = np.ones((height, width), np.uint8)
    sumPix = 0

    # Calculated the sum of the pixels in the detected face image square thingy
    for i in range(stY, endY):
        for j in range(stX, endX):
            sumPix += img.item(i, j)

    # Now calculates the prefered thresholding value from sum of pixels divided by the resolution
    TVa = sumPix / ((endX - stX) * (endY - stY)) + thMod

    # Loop through image and set the pixels to be either black or white
    for i in range(stY, endY):
        for j in range(stX, endX):
            if img.item(i, j) >= TVa:
                bI[i, j] = 0
            elif img.item(i, j) < TVa:
                bI[i, j] = 255
    #print(TVa)
    return bI

# Thresholding version 2, uses HSL image for getting brightness (L) value of frame. Input frame, not gray-scale
def thHSL(img, stX, stY, endX, endY, thMod):
    # Create HSL and Grayscale images of input frame
    imgHSL = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Create new np.ones copy based on height and width of image
    height, width = imgGray.shape
    bI = np.ones((height, width), np.uint8)
    # Split HSL image into the individual channels, LChan is used
    HChan, SChan, LChan = cv2.split(imgHSL)
    TVa = 70
    # Loop through image and set the pixels to be either black or white based on brightness which sets th value
    for i in range(stY, endY):
        for j in range(stX, endX):
            if LChan[i,j] > 100:
                TVa = 100 + thMod
            elif LChan[i,j] > 40 & LChan[i,j] < 50:
                TVa = 60 + thMod
            elif LChan[i,j] > 50 & LChan[i,j] < 60:
                TVa = 70 + thMod
            elif LChan[i,j] > 60 & LChan[i,j] < 70:
                TVa = 80 + thMod
            else:
                TVa = 5 + thMod

            if imgGray.item(i, j) >= TVa:
                bI[i, j] = 0
            elif imgGray.item(i, j) < TVa:
                bI[i, j] = 255
    return bI

# Thresholding version 3, it splits the image in top and bottom and does thresholding on both individually
def thSplit(img, stX, stY, endX, endY, thModT, thModB):
    height, width = img.shape
    bI = np.ones((height, width), np.uint8)
    sumPix1 = 0
    sumPix2 = 0

    # Top part of face
    for i in range(stY,  math.floor((endY - stY) / 2 + stY)):
        for j in range(stX, endX):
            sumPix1 += img.item(i, j)

    TVa1 = sumPix1 / (math.floor((endY - stY) / 2) * (endX - stX)) + thModT

    for i in range(stY, math.floor((endY - stY) / 2 + stY)):
        for j in range(stX, endX):
            if img.item(i, j) >= TVa1:
                bI[i, j] = 0
            elif img.item(i, j) < TVa1:
                bI[i, j] = 255


    # Bottom part of face
    for i in range(math.floor((endY - stY) / 2 + stY), endY):
        for j in range(stX, endX):
            sumPix2 += img.item(i, j)

    TVa2 = sumPix2 / (math.floor((endY - stY) / 2) * (endX - stX)) + thModB

    for i in range(math.floor((endY - stY) / 2 + stY), endY):
        for j in range(stX, endX):
            if img.item(i, j) >= TVa2:
                bI[i, j] = 0
            elif img.item(i, j) < TVa2:
                bI[i, j] = 255

    return bI