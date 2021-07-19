import os
import sys
import pandas
import numpy

sys.path.append(os.path.abspath('./lib'))
import dataPrep
import driftCorrection


excelFile = 'analysisLog.xlsx'
df = pandas.read_excel(excelFile,names=['inputDir','fps','pixelSize','flux'])
df.dropna(subset=['inputDir'],inplace=True)


for inputDir,fps,pixelSize,flux in df.values:
    dp = dataPrep.dataPrep(inputDir)
    dp.convertGatanMovie()
    dp.averageFrames(dp.outputPNGDir,dp.outputPNGDir+'_avg',20,'png')
    dp.averageFrames(dp.outputNPYDir,dp.outputNPYDir+'_avg',10,'npy')
    dp.averageFrames(dp.outputPNGDir,dp.outputDir,dp.numFrames,'png')
    
    drift = driftCorrection.driftCorrection(inputDir,sigma=10)
    drift.findDrift()
    drift.smoothDrift()
    drift.generateImages(numpy.load(drift.driftParamsSmoothFile),scale=0.25,radius=100)
    
    
    
