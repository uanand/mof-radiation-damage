import numpy
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

import fileIO
import misc

class orderedParameter:
    
    def __init__(self,inputDir,driftCorrectionFile,maskFile,pixelSize):
        self.inputDir = inputDir
        self.pixelSize = pixelSize
        self.imgDir = inputDir+'_Export/png_avg'
        self.npyDir = inputDir+'_Export/npy_avg'
        self.outputDir = inputDir+'_Export/output'
        self.outputImgDir = self.outputDir+'/images'
        self.outputDataDir = self.outputDir+'/data'
        self.outputPlotDir = self.outputDir+'/plots'
        
        self.firstFrame,self.lastFrame = misc.findFirstLastFrames(self.imgDir)
        self.mask = cv2.imread(self.inputDir+'_Export/beamBlockerMask.png',0).astype('bool')
        self.driftCorrectionParams = numpy.load(driftCorrectionFile)
        
        gImg = numpy.load(self.npyDir+'/000001.npy')
        [self.row,self.col] = gImg.shape
        
        rr = numpy.arange(self.row)
        cc = numpy.arange(self.col)
        self.CC,self.RR = numpy.meshgrid(rr,cc)
        
        
    def calculateOP(self,distanceRangePixel,stepSize):
        print ('Calculate ordered paramter')
        opImgDir = self.outputImgDir+'/orderedParamerter-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)
        fileIO.mkdir(opImgDir)
        counter = 0
        
        distanceArr,qArr = [],[]
        for distance in range(distanceRangePixel[0],distanceRangePixel[1]+1,stepSize):
            meanDistance = (distance+distance+stepSize)/2.0
            qDistance = 10/(meanDistance*self.pixelSize)
            distanceArr.append(meanDistance)
            qArr.append(qDistance)
        self.distanceArr = numpy.asarray(distanceArr)
        self.qArr = numpy.asarray(qArr)
        
        minCount = 1e10
        for frame in tqdm(range(self.firstFrame,self.lastFrame+1)):
            imgNPY = numpy.load(self.npyDir+'/'+str(frame).zfill(6)+'.npy')
            count = imgNPY[self.mask==True]
            minCount = min(minCount,count.min())
            
        for frame,centreR,centreC in tqdm(zip(range(self.firstFrame,self.lastFrame+1),self.driftCorrectionParams[:,0],self.driftCorrectionParams[:,1])):
            distanceMesh = numpy.sqrt((self.RR-centreR)**2 + (self.CC-centreC)**2)
            meanArr,medianArr,stdArr,ordParamArr_mean,ordParamArr_median = [],[],[],[],[]
            imgNPY = numpy.load(self.npyDir+'/'+str(frame).zfill(6)+'.npy')-minCount
            
            for distance in range(distanceRangePixel[0],distanceRangePixel[1]+1,stepSize):
                distanceMask = numpy.logical_and(numpy.logical_and(distanceMesh>=distance,distanceMesh<distance+stepSize),self.mask)
                count = imgNPY[distanceMask==True]
                avgCount = numpy.mean(count)
                medianCount = numpy.median(count)
                stdCount = numpy.std(count)
                meanArr.append(avgCount)
                medianArr.append(medianCount)
                stdArr.append(stdCount)
                ordParamArr_mean.append(stdCount/avgCount)
                ordParamArr_median.append(stdCount/medianCount)
                
                if (frame==self.firstFrame):
                    gImg = cv2.imread(self.imgDir+'/000001.png',0)
                    finalImg = numpy.maximum(gImg,distanceMask*200)
                    counter += 1
                    cv2.imwrite(opImgDir+'/'+str(counter).zfill(3)+'.png',finalImg)
                    
            meanArr = numpy.asarray(meanArr)
            medianArr = numpy.asarray(medianArr)
            stdArr = numpy.asarray(stdArr)
            ordParamArr_mean = numpy.asarray(ordParamArr_mean)
            ordParamArr_median = numpy.asarray(ordParamArr_median)
            
            if (frame==self.firstFrame):
                self.meanArr = meanArr.copy()
                self.medianArr = medianArr.copy()
                self.stdArr = stdArr.copy()
                self.ordParamArr_mean = ordParamArr_mean.copy()
                self.ordParamArr_median = ordParamArr_median.copy()
            else:
                self.meanArr = numpy.row_stack((self.meanArr,meanArr))
                self.medianArr = numpy.row_stack((self.medianArr,medianArr))
                self.stdArr = numpy.row_stack((self.stdArr,stdArr))
                self.ordParamArr_mean = numpy.row_stack((self.ordParamArr_mean,ordParamArr_mean))
                self.ordParamArr_median = numpy.row_stack((self.ordParamArr_median,ordParamArr_median))
                
        numpy.save(self.outputDataDir+'/distanceArr-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)+'.npy',self.distanceArr)
        numpy.save(self.outputDataDir+'/qArr-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)+'.npy',self.qArr)
        numpy.save(self.outputDataDir+'/meanArr-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)+'.npy',self.meanArr)
        numpy.save(self.outputDataDir+'/medianArr-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)+'.npy',self.medianArr)
        numpy.save(self.outputDataDir+'/stdArr-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)+'.npy',self.stdArr)
        numpy.save(self.outputDataDir+'/ordParamArr_mean-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)+'.npy',self.ordParamArr_mean)
        numpy.save(self.outputDataDir+'/ordParamArr_median-'+str(distanceRangePixel[0])+'_'+str(distanceRangePixel[1])+'_'+str(stepSize)+'.npy',self.ordParamArr_median)
        
        
    def linePlot(self,array,saveFile):
        print ('Plotting %s' %(array))
        data = numpy.load(array)
        [row,col] = data.shape
        
        if ('100_1000_100' in saveFile):
            fig = plt.figure(figsize=(15,1))
            for i in range(col):
                ax = fig.add_subplot(1,10,i+1)
                print (i,data[:,i].min(),data[:,i].max())
                ax.plot(data[:,i])
                ax.set_xticks([])
                ax.set_yticks([])
            plt.savefig(saveFile,format='png')
            plt.close()
            
        if ('100_1000_50' in saveFile):
            fig = plt.figure(figsize=(15,3))
            for i in range(col):
                ax = fig.add_subplot(2,10,i+1)
                print (i,data[:,i].min(),data[:,i].max())
                ax.plot(data[:,i])
                ax.set_xticks([])
                ax.set_yticks([])
            plt.savefig(saveFile,format='png')
            plt.close()
            
        # fig = plt.figure(figsize=(10,1))
        # for i in range(col):
            # ax = fig.add_subplot(1,col,i+1)
            # plotData = numpy.reshape(data[:,i],(row,1))
            # ax.imshow(plotData,aspect='auto',cmap='jet')
            # ax.set_xticks([])
            # ax.set_yticks([])
        # plt.show()
        
        
