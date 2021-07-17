import numpy

def normalize(gImg, min=0, max=255):
    if (gImg.max() > gImg.min()):
        gImg = 1.0*(max-min)*(gImg - gImg.min())/(gImg.max() - gImg.min())
        gImg=gImg+min
    elif (gImg.max() > 0):
        gImg[:] = max
    gImg=gImg.astype('uint8')
    return gImg
