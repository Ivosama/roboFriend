#loop through all the current values of the image, then apply the formula for the cumulative histogram and set the img values to the new values
import numpy as np
import cv2
import histogram
import cum_hist
import math

def equalizeHist(src):
    hist = histogram.histogram(src)
    cum_histogram = cum_hist.cumulative_histogram(hist)
    pixels = src.shape[0]*src.shape[1]
    for i in np.arange(src.shape[0]):
        for j in np.arange(src.shape[1]):
            a = src.item(i,j)
            b = np.round(cum_histogram[a] * 255.0 / pixels)
            src.itemset((i,j), b)

    return src