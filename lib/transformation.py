from numpy import tan,deg2rad

def findLinePoints(line,img):
    [row,col] = img.shape
    X,Y = col-1,row-1
    centreR,centreC,orientation = line[0],line[1],line[2]
    centreX,centreY = centreC,row-centreR
    if (orientation<0):
        theta = 90+orientation
        slope = tan(deg2rad(theta))
    else:
        theta = 90+orientation
        slope = tan(deg2rad(theta))
        
    x1,x2 = 0,X
    y1,y2 = slope*(x1-centreX)+centreY,slope*(x2-centreX)+centreY
    
    r1,c1 = int(round(row-y1)),int(round(x1))
    r2,c2 = int(round(row-y2)),int(round(x2))
    
    return r1,c1,r2,c2
