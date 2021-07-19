from os import listdir
from os.path import join,isfile

############################################################
# FIND THE FIRST FRAME AND LAST FRAME IN A DIRECTORY
############################################################
def findFirstLastFrames(path,extension='png'):
    fileList1 = [f for f in listdir(path) if isfile(join(path,f))]
    fileList = []
    for fileName in fileList1:
        if ('.'+extension in fileName):
            fileList.append(fileName)
    firstFrame,lastFrame = 1e10,-1e10
    for fileName in fileList:
        name = int(fileName.split('.'+extension)[0])
        if (name<firstFrame):
            firstFrame = name
        if (name>lastFrame):
            lastFrame = name
    return (int(firstFrame),int(lastFrame))
############################################################
