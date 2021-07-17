import os
import sys
import pandas

sys.path.append(os.path.abspath('./lib'))
import dataPrep


excelFile = 'analysisLog.xlsx'
df = pandas.read_excel(excelFile,names=['inputDir','fps','pixelSize','flux'])
df.dropna(subset=['inputDir'],inplace=True)


for inputDir,fps,pixelSize,flux in df.values:
    dp = dataPrep.dataPrep(inputDir)
    # dp.convertGatanMovie()
    dp.averageFrames(dp.outputPNGDir,dp.outputPNGDir+'_avg',20,'png')
    dp.averageFrames(dp.outputNPYDir,dp.outputNPYDir+'_avg',10,'npy')
    dp.averageFrames(dp.outputPNGDir,dp.outputDir,dp.numFrames,'png')
    
    
    
