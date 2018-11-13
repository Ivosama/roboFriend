import cv2
import numpy as np
import sys

loadImg = cv2.imread('TestImage.png', cv2.IMREAD_REDUCED_COLOR_2)

cv2.imshow('fuck', loadImg)
cv2.imwrite('test.jpg', loadImg)
img = cv2.cvtColor(loadImg, cv2.COLOR_BGR2GRAY)



h, w = img.shape

objectImage = np.zeros((h, w, 1), np.uint8)


def thImage(img, th):
    height, width = img.shape

    for y in range(0, height):
        for x in range(0, width):
            if (img[y, x] > th):
                img[y, x] = 0
            else:
                img[y, x] = 255

    return img

def findAllObjects(yMin, yMax, xMin, xMax, blackTH, colorTH):
    objectCounter = 0

    for y in range(yMin, yMax):
        for x in range(xMin, xMax):
            if img[y, x] > blackTH:
                objectCounter += 20
                checkConnectivity(y, yMin, yMax, x, xMin, xMax, img[y, x], colorTH, objectCounter)



def checkConnectivity(y, yMin, yMax, x, xMin, xMax, color, colorTH, objectNumber):

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


img = thImage(img, 150)
cv2.imwrite('testTH.jpg', img)
cv2.imshow('INPUT', img)

print(h, w)
sys.setrecursionlimit(3000)
findAllObjects(1, h-1, 1, w-1, 0, 0)

cv2.imshow('OUTPUT', objectImage)
cv2.imwrite('testFinal.jpg', objectImage)

cv2.waitKey()