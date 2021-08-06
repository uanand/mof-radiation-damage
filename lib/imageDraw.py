from skimage.draw import polygon

import transformation


############################################################
def fillBetweenLines(lines,bImg):
    line1 = lines[0]
    line2 = lines[1]
    r1_1,c1_1,r1_2,c1_2 = transformation.findLinePoints(line1,bImg)
    r2_1,c2_1,r2_2,c2_2 = transformation.findLinePoints(line2,bImg)
    rr,cc = polygon([r1_1,r1_2,r2_2,r2_1],[c1_1,c1_2,c2_2,c2_1])
    bImg[:] = False
    bImg[rr,cc] = True
    return bImg
    
