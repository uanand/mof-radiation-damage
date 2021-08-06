import os
import sys
import pandas
import numpy

sys.path.append(os.path.abspath('./lib'))
import dataPrep
import driftCorrection
import orderedParameter
import utils


excelFile = 'analysisLog.xlsx'
df = pandas.read_excel(excelFile,names=['inputDir','fps','pixelSize','flux'])
df.dropna(subset=['inputDir'],inplace=True)


for inputDir,fps,pixelSize,flux in df.values:
    print ('Processing %s' %(inputDir))
    
    # dp = dataPrep.dataPrep(inputDir)
    # dp.convertGatanMovie()
    # dp.averageFrames(dp.outputPNGDir,dp.outputPNGDir+'_avg',20,'png')
    # dp.averageFrames(dp.outputNPYDir,dp.outputNPYDir+'_avg',10,'npy')
    # dp.averageFrames(dp.outputPNGDir,dp.outputDir,dp.numFrames,'png')
    # dp.rmdir(dp.outputPNGDir)
    # dp.rmdir(dp.outputNPYDir)
    
    # drift = driftCorrection.driftCorrection(inputDir,sigma=10)
    # drift.findDrift()
    # drift.smoothDrift()
    # drift.generateImages(numpy.load(drift.driftParamsSmoothFile),scale=0.25,radius=100)
    
    # utils.makeBeamBlockerMask(inputDir+'_Export/000001.png',inputDir+'_Export/beamBlockerMask.png')
    
    op = orderedParameter.orderedParameter(inputDir,inputDir+'_Export/output/data/driftCorrectionSmoothParams.npy',inputDir+'_Export/beamBlockerMask.png',pixelSize)
    op.calculateOP(distanceRangePixel=[100,1000],stepSize=100)
    op.calculateOP(distanceRangePixel=[100,1000],stepSize=50)
    
    op.linePlot(array=inputDir+'_Export/output/data/meanArr-100_1000_100.npy',saveFile=inputDir+'_Export/output/plots/meanArr-100_1000_100.png')
    op.linePlot(array=inputDir+'_Export/output/data/medianArr-100_1000_100.npy',saveFile=inputDir+'_Export/output/plots/medianArr-100_1000_100.png')
    op.linePlot(array=inputDir+'_Export/output/data/stdArr-100_1000_100.npy',saveFile=inputDir+'_Export/output/plots/stdArr-100_1000_100.png')
    op.linePlot(array=inputDir+'_Export/output/data/ordParamArr_mean-100_1000_100.npy',saveFile=inputDir+'_Export/output/plots/ordParamArr_mean-100_1000_100.png')
    op.linePlot(array=inputDir+'_Export/output/data/ordParamArr_median-100_1000_100.npy',saveFile=inputDir+'_Export/output/plots/ordParamArr_median-100_1000_100.png')
    
    op.linePlot(array=inputDir+'_Export/output/data/meanArr-100_1000_50.npy',saveFile=inputDir+'_Export/output/plots/meanArr-100_1000_50.png')
    op.linePlot(array=inputDir+'_Export/output/data/medianArr-100_1000_50.npy',saveFile=inputDir+'_Export/output/plots/medianArr-100_1000_50.png')
    op.linePlot(array=inputDir+'_Export/output/data/stdArr-100_1000_50.npy',saveFile=inputDir+'_Export/output/plots/stdArr-100_1000_50.png')
    op.linePlot(array=inputDir+'_Export/output/data/ordParamArr_mean-100_1000_50.npy',saveFile=inputDir+'_Export/output/plots/ordParamArr_mean-100_1000_50.png')
    op.linePlot(array=inputDir+'_Export/output/data/ordParamArr_median-100_1000_50.npy',saveFile=inputDir+'_Export/output/plots/ordParamArr_median-100_1000_50.png')
