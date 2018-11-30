import cv2
import numpy as np

import cum_hist as ch
import histogram as hg
import thresholding

def getHistogramMedian(src):
    histogram = hg.histogram(src)
    cumHist = ch.cumulative_histogram(histogram)
    histogramMedian = np.median(cumHist)
    # print(histogramMedian)
    if histogramMedian in cumHist:
        for yikers in range(0, len(cumHist) - 1):
            if cumHist[yikers] <= histogramMedian + 1 and cumHist[yikers] >= histogramMedian - 1:
                histogramMedian = yikers
                break
    else:
        histogramMedian = find_nearest(cumHist, histogramMedian)

    return histogramMedian


def deleteWhiteSides(edited, rectX, rectY, rectW, rectH):
    deleteFromLeft = 0
    for i in range(rectX, rectX + rectW):
        whiteInX = False
        for j in range(rectY, rectY + rectH):
            pixVal = edited[j, i]
            if pixVal == 255:
                whiteInX = True

        if not whiteInX:
            break
        deleteFromLeft += 1

    for xd in range(rectX, deleteFromLeft + rectX):
        for y in range(rectY, rectY + rectH):
            edited[y, xd] = 0

    deleteFromRight = 0
    for i in range(rectX + rectW, rectX):
        whiteInX = False
        for j in range(rectY, rectY + rectH):
            pixVal = edited[j, i]
            if pixVal == 255:
                whiteInX = True

        if not whiteInX:
            break
        deleteFromRight += 1

    for xd in range(rectX - deleteFromRight, rectX):
        for y in range(rectY, rectY + rectH):
            edited[y, xd] = 0

    #cv2.imshow('Thresholded Image', edited)
    return edited, deleteFromLeft, deleteFromRight


def rapidSmileCascade(src, rectX, rectY, rectW, rectH, histogramMedian):
    """
    :param src: The input image, for best results it should be median blurred with cv2 radius 3 and histogram equalized
    :param rectX: The top left x of the rectangle to search through
    :param rectY: The top left Y of the rectangle to search through
    :param rectW: The width of the search area
    :param rectH: The height of the search area
    :return: Returns true or false depending on whether the smile passes the tests or not
    To look at what is happening, uncomment the commented parts at the bottom of each stage.
    This will show the rectangles that the program is testing and searching through
    """
    cumSumTable = src.cumsum(axis=0).cumsum(axis=1)
    searchRectH = int(np.ceil(rectH/8))
    searchRectW = int(np.ceil((rectW/8)*6))
    smileDetected = False
    frownDetected = False
    bottomOfLip = src.shape[0]
    normalisedLighting = histogramMedian/127
    #imageCopy = src.copy()
    #cv2.rectangle(imageCopy, (rectX, rectY), (rectX+searchRectW, rectY+searchRectH), (255, 0, 0), 1)
    #cv2.imshow("Size of search rectangle", imageCopy)

    for y in range(rectY+int(rectH/3), rectY+(rectH-searchRectH)-1):
        for x in range(rectX+searchRectW, rectX+rectW-1):
            searchRectH = int(np.ceil(rectH / 8))
            searchRectW = int(np.ceil((rectW / 8) * 6))
            originalSearchW = searchRectW
            searchRectArea = searchRectH * searchRectW


            bottomRightTop = cumSumTable[y, x]
            topRightTop = cumSumTable[y-searchRectH, x]
            topLeftTop = cumSumTable[y-searchRectH, x-searchRectW]
            bottomLeftTop = cumSumTable[y, x-searchRectW]
            topColourSum = (bottomRightTop-topRightTop-bottomLeftTop+topLeftTop)/searchRectArea

            bottomRightBottom = cumSumTable[y+searchRectH, x]
            topRightBottom = cumSumTable[y, x]
            topLeftBottom = cumSumTable[y, x-searchRectW]
            bottomLeftBottom = cumSumTable[y+searchRectH, x-searchRectW]
            bottomColourSum = (bottomRightBottom-topRightBottom-bottomLeftBottom+topLeftBottom)/searchRectArea

            if (bottomColourSum-topColourSum) > normalisedLighting*40:
                #print(topColourSum)
                #print(bottomColourSum)
                #cv2.rectangle(imageCopy, (x-searchRectW, y), (x, y), (255, 0, 0), 2)
                #cv2.imshow("Bottom Lip", imageCopy)
                bottomOfLip = y

    for y in range(rectY+int(rectH/3), rectY+(rectH-searchRectH)-1):
        for x in range(rectX+searchRectW, rectX+rectW-1):
            searchRectH = int(np.ceil(rectH / 8))
            searchRectW = int(np.ceil((rectW / 8) * 6))
            originalSearchW = searchRectW
            searchRectArea = searchRectH * searchRectW


            bottomRightTop = cumSumTable[y, x]
            topRightTop = cumSumTable[y-searchRectH, x]
            topLeftTop = cumSumTable[y-searchRectH, x-searchRectW]
            bottomLeftTop = cumSumTable[y, x-searchRectW]
            topColourSum = (bottomRightTop-topRightTop-bottomLeftTop+topLeftTop)/searchRectArea

            bottomRightBottom = cumSumTable[y+searchRectH, x]
            topRightBottom = cumSumTable[y, x]
            topLeftBottom = cumSumTable[y, x-searchRectW]
            bottomLeftBottom = cumSumTable[y+searchRectH, x-searchRectW]
            bottomColourSum = (bottomRightBottom-topRightBottom-bottomLeftBottom+topLeftBottom)/searchRectArea

            if (topColourSum-bottomColourSum) < -normalisedLighting*30:
                searchRectX = int(x-(searchRectW/8)*5)
                searchRectW = int(searchRectW/8)
                searchRectX += searchRectW

                bottomRightTop = cumSumTable[y, searchRectX]
                topRightTop = cumSumTable[y - searchRectH, searchRectX]
                topLeftTop = cumSumTable[y - searchRectH, searchRectX - searchRectW]
                bottomLeftTop = cumSumTable[y, searchRectX - searchRectW]
                topColourSum = (bottomRightTop - topRightTop - bottomLeftTop + topLeftTop) / searchRectArea

                bottomRightBottom = cumSumTable[y + searchRectH, searchRectX]
                topRightBottom = cumSumTable[y, searchRectX]
                topLeftBottom = cumSumTable[y, searchRectX - searchRectW]
                bottomLeftBottom = cumSumTable[y + searchRectH, searchRectX - searchRectW]
                bottomColourSum = (bottomRightBottom - topRightBottom - bottomLeftBottom + topLeftBottom) / searchRectArea

                #cv2.rectangle(imageCopy, (searchRectX - searchRectW, y - searchRectH * 2),(searchRectX, y - searchRectH), (255, 0, 0), 2)
                #cv2.imshow("Next Rectangle", imageCopy)

                if bottomColourSum - topColourSum > normalisedLighting*6:
                    searchRectX = int(x-(originalSearchW/5))
                    #searchRectW = int(searchRectW / 8)

                    bottomRightTop = cumSumTable[y-searchRectH, searchRectX]
                    topRightTop = cumSumTable[y - searchRectH*2, searchRectX]
                    topLeftTop = cumSumTable[y - searchRectH*2, searchRectX - searchRectW]
                    bottomLeftTop = cumSumTable[y - searchRectH, searchRectX - searchRectW]
                    topColourSum = (bottomRightTop - topRightTop - bottomLeftTop + topLeftTop) / searchRectArea

                    bottomRightRight = cumSumTable[y-searchRectH, searchRectX + searchRectW]
                    topRightRight = cumSumTable[y - searchRectH*2, searchRectX + searchRectW]
                    topLeftRight = cumSumTable[y - searchRectH*2, searchRectX]
                    bottomLeftRight = cumSumTable[y - searchRectH, searchRectX]
                    rightColourSum = (bottomRightRight - topRightRight - bottomLeftRight + topLeftRight) / searchRectArea

                    bottomRightLeft = cumSumTable[y - searchRectH, searchRectX-searchRectW]
                    topRightLeft = cumSumTable[y - searchRectH * 2, searchRectX-searchRectW]
                    topLeftLeft = cumSumTable[y - searchRectH * 2, searchRectX - searchRectW*2]
                    bottomLeftLeft = cumSumTable[y - searchRectH, searchRectX - searchRectW*2]
                    leftColourSum = (bottomRightLeft - topRightLeft - bottomLeftLeft + topLeftLeft) / searchRectArea

                    #cv2.rectangle(imageCopy, (searchRectX - searchRectW, y - searchRectH * 2),(searchRectX, y - searchRectH), (255, 0, 0), 2)
                    #cv2.imshow("Next Rectangle", imageCopy)
                    #print(rightColourSum - topColourSum)
                    #print(leftColourSum - topColourSum)

                    if abs(rightColourSum - topColourSum) > normalisedLighting*3 and abs(leftColourSum - topColourSum) > normalisedLighting*0.6 and y < bottomOfLip:
                        #print("LUL")
                        smileDetected = True

    if smileDetected == False and bottomOfLip == src.shape[0]:
        for y in range(rectY + int(rectH / 3), rectY + (rectH - searchRectH) - 1):
            for x in range(rectX + searchRectW, rectX + rectW - 1):
                searchRectH = int(np.ceil(rectH / 8))
                searchRectW = int(np.ceil((rectW / 8) * 6))
                originalSearchW = searchRectW
                searchRectArea = searchRectH * searchRectW

                bottomRightTop = cumSumTable[y, x]
                topRightTop = cumSumTable[y - searchRectH, x]
                topLeftTop = cumSumTable[y - searchRectH, x - searchRectW]
                bottomLeftTop = cumSumTable[y, x - searchRectW]
                topColourSum = (bottomRightTop - topRightTop - bottomLeftTop + topLeftTop) / searchRectArea

                bottomRightBottom = cumSumTable[y + searchRectH, x]
                topRightBottom = cumSumTable[y, x]
                topLeftBottom = cumSumTable[y, x - searchRectW]
                bottomLeftBottom = cumSumTable[y + searchRectH, x - searchRectW]
                bottomColourSum = (
                                              bottomRightBottom - topRightBottom - bottomLeftBottom + topLeftBottom) / searchRectArea

                # cv2.rectangle(imageCopy, (x-searchRectW, y - searchRectH),(x, y), (255, 0, 0), 2)
                # cv2.imshow("Next Rectangle", imageCopy)
                # print(topColourSum-bottomColourSum)

                if (topColourSum - bottomColourSum) < -normalisedLighting * 10:
                    mouthStraightish = True
                    searchRectW = int(searchRectW / 8)
                    # searchRectX += searchRectW
                    for xLineSegmenter in range(5):
                        searchRectX = int(x - (originalSearchW / 9) * (2 + xLineSegmenter))
                        bottomRightTop = cumSumTable[y, searchRectX]
                        topRightTop = cumSumTable[y - searchRectH, searchRectX]
                        topLeftTop = cumSumTable[y - searchRectH, searchRectX - searchRectW]
                        bottomLeftTop = cumSumTable[y, searchRectX - searchRectW]
                        topColourSum = (bottomRightTop - topRightTop - bottomLeftTop + topLeftTop) / searchRectArea

                        bottomRightBottom = cumSumTable[y + searchRectH, searchRectX]
                        topRightBottom = cumSumTable[y, searchRectX]
                        topLeftBottom = cumSumTable[y, searchRectX - searchRectW]
                        bottomLeftBottom = cumSumTable[y + searchRectH, searchRectX - searchRectW]
                        bottomColourSum = (
                                                      bottomRightBottom - topRightBottom - bottomLeftBottom + topLeftBottom) / searchRectArea

                        # cv2.rectangle(imageCopy, (searchRectX - searchRectW, y - searchRectH),(searchRectX, y), (255, 0, 0), 2)
                        # cv2.imshow("Next Rectangle", imageCopy)
                        # print(topColourSum - bottomColourSum)
                        if topColourSum - bottomColourSum < normalisedLighting * -2:
                            mouthStraightish = False
                    # print(mouthStraightish)
                    if mouthStraightish:
                        searchRectX = int(x - (originalSearchW / 9) * 7)  # The right side of mouth
                        searchRectW *= 2
                        searchRectH *= 2

                        bottomRightTop = cumSumTable[y, searchRectX]
                        topRightTop = cumSumTable[y - searchRectH, searchRectX]
                        topLeftTop = cumSumTable[y - searchRectH, searchRectX - searchRectW]
                        bottomLeftTop = cumSumTable[y, searchRectX - searchRectW]
                        topColourSum = (bottomRightTop - topRightTop - bottomLeftTop + topLeftTop) / searchRectArea

                        bottomRightBottom = cumSumTable[y + searchRectH, searchRectX]
                        topRightBottom = cumSumTable[y, searchRectX]
                        topLeftBottom = cumSumTable[y, searchRectX - searchRectW]
                        bottomLeftBottom = cumSumTable[y + searchRectH, searchRectX - searchRectW]
                        bottomColourSum = (
                                                      bottomRightBottom - topRightBottom - bottomLeftBottom + topLeftBottom) / searchRectArea

                        # cv2.rectangle(imageCopy, (searchRectX - searchRectW, y), (searchRectX, y + searchRectH), (255, 0, 0), 2)
                        # cv2.imshow("Next Rectangle", imageCopy)
                        # print(rightColourSum - topColourSum)
                        # print(leftColourSum - topColourSum)
                        if bottomColourSum - topColourSum > normalisedLighting * 2:
                            if bottomOfLip == src.shape[0]:
                                frownDetected = True
                                print("LUL")

    return smileDetected, frownDetected #int(bottomOfLip), topOfLip


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def mouthSmiling(src, rectX, rectY, rectW, rectH):
    """
    :param src: Input image
    :param rectX: Face cascade x
    :param rectY: Face cascade y
    :param rectW: Face cascade w
    :param rectH: Face cascade h
    :return: True for if smile is detected, otherwise false
    First the area is median blurred (I tested originally with cv2 radius 3), then histogram equalized.
    Poul's dynamic thresholding applied
    Using the thresholded image, sides are deleted that are hopefully the background
    Then a cascade is run on the resulting dimensions
    """
    src = cv2.medianBlur(src, 3)
    src = cv2.equalizeHist(src)
    edited = thresholding.th(src, rectX, rectY, rectX+rectW, rectY+rectH, -45)

    histogram = hg.histogram(src)
    cumHist = ch.cumulative_histogram(histogram)
    histogramMedian = np.median(cumHist)
    #print(histogramMedian)
    if histogramMedian in cumHist:
        for yikers in range(0, len(cumHist)-1):
            if cumHist[yikers] <= histogramMedian+1 and cumHist[yikers] >= histogramMedian-1:
                histogramMedian = yikers
                break
    else:
        histogramMedian = find_nearest(cumHist, histogramMedian)

    #print(histogramMedian)
    """
    histogramMedians.append(histogramMedian)
    if len(histogramMedians) > 10:
        print(np.mean(histogramMedians))
    """
    edited, deleteFromLeft, deleteFromRight = deleteWhiteSides(edited, rectX, rectY, rectW, rectH)
    if deleteFromRight > rectW/3:
        deleteFromRight = 0
    if deleteFromLeft > rectW/3:
        deleteFromLeft = 0
    smileDetected = rapidSmileCascade(src, rectX+deleteFromLeft, rectY, rectW-deleteFromRight, rectH, histogramMedian)
    return smileDetected