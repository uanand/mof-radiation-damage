import numpy
from scipy import ndimage
from skimage import measure

def normalize(gImg, min=0, max=255):
    if (gImg.max() > gImg.min()):
        gImg = 1.0*(max-min)*(gImg - gImg.min())/(gImg.max() - gImg.min())
        gImg=gImg+min
    elif (gImg.max() > 0):
        gImg[:] = max
    gImg=gImg.astype('uint8')
    return gImg


#######################################################################
# OTSU THRESHOLD FOR GRAYSCALE IMAGES
#######################################################################
def otsuThreshold(img, bins=256):
    hist, bins = numpy.histogram(img.flatten(), bins=bins, range=(0,255))
    totalPixels = hist.sum()
    
    currentMax = 0
    threshold = 0
    sumTotal, sumForeground, sumBackground = 0., 0., 0.
    weightBackground, weightForeground = 0., 0.
    
    for i,t in enumerate(hist):
        sumTotal += i * hist[i]
    for i,t in enumerate(hist):
        weightBackground += hist[i]
        if(weightBackground==0):
            continue
        weightForeground = totalPixels - weightBackground
        if (weightForeground==0):
            break
            
        sumBackground += i*hist[i]
        sumForeground = sumTotal-sumBackground
        meanB = sumBackground/weightBackground
        meanF = sumForeground/weightForeground
        varBetween = weightBackground*weightForeground
        varBetween *= (meanB-meanF)*(meanB-meanF)
        if(varBetween>currentMax):
            currentMax = varBetween
            threshold = i
    return threshold
#######################################################################


#######################################################################
# FIND OUT THE REGION PROPERTIES OF CONNECTED OBJECTS IN A BINARY IMAGE
#######################################################################
def regionProps(bImg,structure=[[1,1,1],[1,1,1],[1,1,1]]):
    [labelImg,numLabel] = ndimage.label(bImg,structure=structure)
    [row,col] = bImg.shape
    dictionary = {}
    dictionary['id'] = []
    dictionary['area'] = []
    dictionary['centroid'] = []
    dictionary['orientation'] = []
    
    for i in range(1,numLabel+1):
        bImgLabelN = labelImg==i
        ####
        dictionary['id'].append(i)
        ####
        Area = bImgLabelN.sum()
        dictionary['area'].append(Area)
        ####
        pixelsRC = numpy.nonzero(bImgLabelN)
        centerRC = [numpy.average(pixelsRC[0]), numpy.average(pixelsRC[1])]
        dictionary['centroid'].append(centerRC)
        ####
        regions = measure.regionprops(bImgLabelN.astype('uint8'))
        for props in regions:
            dictionary['orientation'].append(numpy.rad2deg(props.orientation))
            
    return labelImg,numLabel,dictionary
#######################################################################


#######################################################################
# BINARY OPENING OPERATION
#######################################################################
def binary_opening(bImg, iterations=1):
    bImg = ndimage.binary_erosion(bImg, iterations=iterations)
    bImg = ndimage.binary_dilation(bImg, iterations=iterations)
    return bImg
#######################################################################


#######################################################################
# BINARY CLOSING OPERATION
#######################################################################
def binary_closing(bImg, iterations=1):
    bImg = ndimage.binary_dilation(bImg, iterations=iterations)
    bImg = ndimage.binary_erosion(bImg, iterations=iterations)
    return bImg
#######################################################################


#######################################################################
# BINARY DILATION OPERATION
#######################################################################
def binary_dilation(bImg, iterations=1):
    bImg = ndimage.binary_dilation(bImg, iterations=iterations)
    return bImg
#######################################################################


############################################################
# BINARY EROSION OPERATION
############################################################
def binary_erosion(bImg, iterations=1):
    bImg = ndimage.binary_erosion(bImg, iterations=iterations)
    return bImg
############################################################
