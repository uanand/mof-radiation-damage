import os


def mkdir(dirName):
    if (os.path.exists(dirName) == False):
        os.makedirs(dirName)
