import imageProcess
import numpy

def areaFilter(bImg):
    labelImg,numLabel,dictionary = imageProcess.regionProps(bImg)
    bImg[:] = False
    
    regionAreaList = dictionary['area']
    regionAreaList = sorted(regionAreaList,reverse=True)
    regionAreaList = regionAreaList[:2]
    for label,area in zip(range(1,numLabel+1),dictionary['area']):
        if (area==regionAreaList[0] or area==regionAreaList[1]):
            bImgN = labelImg==label
            bImg = numpy.logical_or(bImg,bImgN)
    return bImg
