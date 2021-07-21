import os
import numpy
import cv2
import shutil
import hyperspy.api as hs
from tqdm import tqdm
from os.path import join

import fileIO
import imageProcess

class dataPrep:
    
    def __init__(self,inputDir,minPercentile=0.1,maxPercentile=99.9):
        self.inputDir = inputDir
        self.outputDir = inputDir+'_Export'
        self.outputPNGDir = self.outputDir+'/png'
        self.outputNPYDir = self.outputDir+'/npy'
        
        self.minPercentile = 0.1
        self.maxPercentile = 99.9
        
        self.inputFileList = self.getFiles(path=self.inputDir,extension='dm4')
        self.numFrames = numpy.size(self.inputFileList)
        
        fileIO.mkdir(self.outputDir)
        fileIO.mkdir(self.outputPNGDir)
        fileIO.mkdir(self.outputNPYDir)
        
    def getFiles(self,path,extension):
        inputFileList=[]
        for root,dirs,files in os.walk(path):
            for name in files:
                if name.endswith((extension)):
                    inputFileList.append(join(root,name))
        inputFileList = numpy.sort(inputFileList,kind='mergesort')
        return inputFileList
    
    def convertGatanMovie(self):
        print ('Converting gatan movie - %s' %(self.inputDir))
        minCount,maxCount = 1e10,-1e10
        for inputFile,frame in tqdm(zip(self.inputFileList,list(range(1,self.numFrames+1)))):
            f = hs.load(inputFile)
            gImg = f.data
            lowLimit,highLimit = numpy.percentile(gImg,float(self.minPercentile)),numpy.percentile(gImg,float(self.maxPercentile))
            minCount = min(minCount,lowLimit)
            maxCount = max(maxCount,highLimit)
            numpy.save(self.outputNPYDir+'/'+str(frame).zfill(6)+'.npy',gImg)
            
        for inputFile,frame in tqdm(zip(self.inputFileList,list(range(1,self.numFrames+1)))):
            f = hs.load(inputFile)
            gImg = f.data
            lowLimit,highLimit = numpy.percentile(gImg,float(self.minPercentile)),numpy.percentile(gImg,float(self.maxPercentile))
            gImg[gImg<=lowLimit] = lowLimit
            gImg[gImg>=highLimit] = highLimit
            gImg = imageProcess.normalize(gImg,min=(gImg.min()-minCount)/(maxCount-minCount)*255,max=(gImg.max()-minCount)/(maxCount-minCount)*255)
            cv2.imwrite(self.outputPNGDir+'/'+str(frame).zfill(6)+'.png',gImg)
            
    def averageFrames(self,path,outputDir,numFramesToAvg,extension,movingAvgFlag=True):
        print ('Averaging image sequence - %s' %(path))
        fileIO.mkdir(outputDir)
        avgFrameList = []
        firstFrame,lastFrame = 1,self.numFrames
        for frame1 in range(int(firstFrame),int(lastFrame+1)):
            if (frame1+numFramesToAvg<=lastFrame+1):
                frameList = []
                for frame2 in range(frame1,frame1+numFramesToAvg):
                    frameList.append(frame2)
                avgFrameList.append(frameList)
                
        if (extension=='png'):
            for frameList in tqdm(avgFrameList):
                outputFile = outputDir+'/'+str(frameList[0]).zfill(6)+'.png'
                for frame in frameList:
                    inputFile = path+'/'+str(frame).zfill(6)+'.png'
                    gImg = cv2.imread(inputFile,0)
                    if (frame==frameList[0]):
                        avgImg = gImg.copy()
                        avgImg = avgImg.astype('double')
                    else:
                        avgImg = avgImg+gImg
                avgImg = (avgImg/numFramesToAvg).astype('uint8')
                avgImg = imageProcess.normalize(avgImg)
                cv2.imwrite(outputFile,avgImg)
        elif (extension=='npy'):
            for frameList in tqdm(avgFrameList):
                outputFile = outputDir+'/'+str(frameList[0]).zfill(6)+'.npy'
                for frame in frameList:
                    inputFile = path+'/'+str(frame).zfill(6)+'.npy'
                    gImg = numpy.load(inputFile)
                    if (frame==frameList[0]):
                        avgImg = gImg.copy()
                        avgImg = avgImg.astype('double')
                    else:
                        avgImg = avgImg+gImg
                avgImg = avgImg/numFramesToAvg
                numpy.save(outputFile,avgImg)
                
    def rmdir(self,path):
        print ('Delete directory - %s' %(path))
        shutil.rmtree(path)
    
