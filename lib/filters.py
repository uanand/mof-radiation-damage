import imageProcess
import numpy
from skimage.measure import label, regionprops

def areaFilter(bImg):
    labelImg = label(bImg)
    numLabel = labelImg.max()
    props = regionprops(labelImg)
    bImg[:] = False
    
    areaList = []
    for i in range(numLabel):
        areaList.append(props[i].area)
    areaList = sorted(areaList,reverse=True)
    areaList = areaList[:2]
    
    for i in range(numLabel):
        area = props[i].area
        if (area==areaList[0] or area==areaList[1]):
            bImgN = labelImg==i+1
            bImg = numpy.logical_or(bImg,bImgN)
    return bImg
