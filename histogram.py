import numpy as np

#Creates a histogram of the image
def histogram(img):
    height = img.shape[0]
    width = img.shape[1]

    hist = np.zeros(256) #initially fills the histogram with 0

    for i in np.arange(height):
        for j in np.arange(width):
            a = img.item(i, j)
            hist[a] += 1

    return hist