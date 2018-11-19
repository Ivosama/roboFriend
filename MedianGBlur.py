import cv2
import numpy as np
import matplotlib.pyplot as plt
import statistics

def medianBlur(src, outputImage, searchDistance, faceX, faceY, faceW, faceH):
    # swag boi dolla dolla bill$ holla at me
    height, width = src.shape
    outputImage = np.zeros((height, width), np.uint8)
    for y in range(1 + faceY + searchDistance, faceY+faceH - 1 - searchDistance):
        for x in range(1 + faceX + searchDistance, faceX+faceW - 1 - searchDistance):
            surroundingPixels = []
            startY = y-searchDistance
            startX = x-searchDistance
            for searchY in range(y+searchDistance+1-startY):
                for searchX in range(x+searchDistance+1-startX):
                    surroundingPixels.append(src[startY + searchY, startX + searchX])

            #outputImage[y, x] = np.median(surroundingPixels)

            outputImage[y, x] = statistics.median(surroundingPixels);


    return outputImage