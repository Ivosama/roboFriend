# Don't get confused there's nothing median about this function
import cv2
import numpy as np
import matplotlib.pyplot as plt
import statistics

startImg = cv2.imread("TestImages/Straight Outta CREATE 2.png", cv2.IMREAD_GRAYSCALE)
# Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def medianBlur(src, outputImage, searchDistance, faceX, faceY, faceW, faceH):
    # swag boi dolla dolla bill$ holla at me
    height, width = src.shape
    #outputImage = np.zeros((height, width, 1), np.uint8)
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

"""
def integralImage(src):
    height, width = src.shape
    outputImage = np.zeros((height, width, 1), np.uint8)
    s = np.zeros((height, width, 1), np.uint8)
    outputImage[0, 0] = src[0, 0]
    s[0, 0] = src[0, 0]
    for x in range(1, width):
        for y in range(1, height):
            s[y, x] = s[y-1, x] + src[y, x]
            outputImage[y, x] = outputImage[y, x-1] + s[y, x]
            #print(outputImage[y, x])

    return outputImage
"""

def summed_area_table(img):

    table = np.zeros_like(img).astype(int)
    #print(table)

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):

            if (row > 0) and (col > 0):
                table[row, col] = (img[row, col] +
                                   table[row, col - 1] +
                                   table[row - 1, col] -
                                   table[row - 1, col - 1])
            elif row > 0:
                table[row, col] = img[row, col] + table[row - 1, col]
            elif col > 0:
                table[row, col] = img[row, col] + table[row, col - 1]
            else:
                table[row, col] = img[row, col]

    return table


startPosition = 700
sumOfOriginal = startImg[startPosition, startPosition]+startImg[startPosition+1, startPosition]+startImg[startPosition, startPosition+1]+startImg[startPosition+1, startPosition+1]
print(sumOfOriginal)
#ii = summed_area_table(startImg)
ii = startImg.cumsum(axis=0).cumsum(axis=1)
sumOfII = ii[startPosition+1, startPosition+1] + ii[startPosition, startPosition] - ii[startPosition, startPosition+1] - ii[startPosition+1, startPosition]
print(sumOfII)
#print(ii)

def histogram(img):
    height = img.shape[0]
    width = img.shape[1]

    hist = np.zeros(256)

    for i in np.arange(height):
        for j in np.arange(width):
            a = img.item(i, j)
            hist[a] += 1

    return hist


def cumulative_histogram(hist):
    cum_hist = hist.copy()

    for i in np.arange(1, 256):
        cum_hist[i] = cum_hist[i - 1] + cum_hist[i]

    return cum_hist


#cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    medianBlurred = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)

    faces = face_cascade.detectMultiScale(frame, 1.1, 5)
    for (x, y, w, h) in faces:
        #cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        medianBlurred = medianBlur(frame, medianBlurred, 3, x, y, w, h)
        #print("xd")

    cv2.imshow("Output", medianBlurred)
    #editedImage = medianBlur(frame, 0)
    #editedImageCV = cv2.medianBlur(frame, 9)
    #cv2.imshow("preview", editedImage)
    #cv2.imshow("preview cv", editedImageCV)
    #plt.plot(cumulative_histogram(histogram(frame)))
    #plt.show();
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")