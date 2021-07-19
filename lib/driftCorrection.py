import numpy
import cv2
from skimage.draw import circle_perimeter
from scipy import ndimage
from tqdm import tqdm

import fileIO
import imageProcess
import misc
import filters

class driftCorrection:
    
    def __init__(self,inputDir,sigma):
        self.sigma = sigma
        self.inputDir = inputDir
        self.imgDir = inputDir+'_Export/png_avg'
        self.npyDir = inputDir+'_Export/npy_avg'
        self.outputDir = inputDir+'_Export/output'
        self.outputImgDir = self.outputDir+'/images'
        self.outputDataDir = self.outputDir+'/data'
        self.outputPlotDir = self.outputDir+'/plots'
        self.driftParamsFile = self.outputDataDir+'/driftCorrectionParams.npy'
        self.driftParamsSmoothFile = self.outputDataDir+'/driftCorrectionSmoothParams.npy'
        
        fileIO.mkdir(self.outputDir)
        fileIO.mkdir(self.outputImgDir)
        fileIO.mkdir(self.outputImgDir+'/gImgCentre')
        fileIO.mkdir(self.outputDataDir)
        fileIO.mkdir(self.outputPlotDir)
        
        self.firstFrame,self.lastFrame = misc.findFirstLastFrames(self.imgDir)
        gImg = cv2.imread(self.imgDir+'/'+str(1).zfill(6)+'.png',0)
        [self.row,self.col] = gImg.shape
        
    def findDrift(self):
        centreRList,centreCList = [],[]
        for frame in tqdm(range(self.firstFrame,self.lastFrame+1)):
            gImg = cv2.imread(self.imgDir+'/'+str(frame).zfill(6)+'.png',0)
            bImg = gImg>=imageProcess.otsuThreshold(gImg)
            bImg = imageProcess.binary_erosion(bImg,iterations=10)
            bImg = filters.areaFilter(bImg)
            pixelsRC = numpy.nonzero(bImg)
            centreR,centreC = numpy.average(pixelsRC[0]),numpy.average(pixelsRC[1])
            centreRList.append(centreR)
            centreCList.append(centreC)
        numpy.save(self.driftParamsFile,numpy.column_stack((centreRList,centreCList)))
        
    def smoothDrift(self):
        driftParams = numpy.load(self.driftParamsFile)
        centreRList,centreCList = driftParams[:,0],driftParams[:,1]
        centreRList = ndimage.gaussian_filter1d(centreRList,sigma=self.sigma)
        centreCList = ndimage.gaussian_filter1d(centreCList,sigma=self.sigma)
        numpy.save(self.driftParamsSmoothFile,numpy.column_stack((centreRList,centreCList)))
        
    def generateImages(self,driftCorrectionParams,scale,radius):
        bImg = numpy.zeros([self.row,self.col],dtype='bool')
        for frame,centreR,centreC in tqdm(zip(list(range(self.firstFrame,self.lastFrame+1)),driftCorrectionParams[:,0],driftCorrectionParams[:,1])):
            gImg = cv2.imread(self.imgDir+'/'+str(frame).zfill(6)+'.png',0)
            bImg[:] = False
            rr,cc = circle_perimeter(int(round(centreR)),int(round(centreC)),radius,shape=[self.row,self.col])
            bImg[rr,cc] = True
            bImg = imageProcess.binary_dilation(bImg,iterations=8)
            bImg = bImg*255
            finalImg = numpy.maximum(gImg,bImg).astype('uint8')
            finalImg = cv2.resize(finalImg,(int(self.col*float(scale)),int(self.row*float(scale))),interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.outputImgDir+'/gImgCentre/'+str(frame).zfill(6)+'.png',finalImg)
############################################################
        
        
