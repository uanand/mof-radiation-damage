import cv2
import numpy
from skimage import filters as flt
import matplotlib.pyplot as plt

import imageProcess
import filters
import imageDraw

############################################################
def makeBeamBlockerMask(inputImg,maskImg):
    img = cv2.imread(inputImg,0)
    gradImg = flt.sobel(img)
    bImg = gradImg>numpy.percentile(gradImg,99.5)
    bImg = filters.areaFilter(bImg)
    labelImg,numLabel,dictionary = imageProcess.regionProps(bImg)
    line1 = [dictionary['centroid'][0][0],dictionary['centroid'][0][1],dictionary['orientation'][0]]
    line2 = [dictionary['centroid'][1][0],dictionary['centroid'][1][1],dictionary['orientation'][1]]
    bImg = imageDraw.fillBetweenLines([line1,line2],bImg)
    bImg = imageProcess.binary_dilation(bImg,iterations=25)
    bImg = numpy.logical_not(bImg)
    cv2.imwrite(maskImg,bImg*255)
    
    plt.figure()
    plt.subplot(121), plt.imshow(img)
    plt.subplot(122), plt.imshow(bImg)
    plt.show()
    
    return None
############################################################
