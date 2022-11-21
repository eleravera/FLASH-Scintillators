from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import scipy
from scipy.optimize import curve_fit
import glob


def openImage(path):
    im = Image.open(path)
    return np.array(im)

def plotImage(imArray, vmin=2000, vmax=2300):
    fig, ax = plt.subplots(1,1)
    ax.imshow(imArray, vmin=vmin, vmax=vmax)
    return 

def findROI(imArray, x, y, centerX, centerY, r=12, default_value=100):
    d=np.sqrt ((x-centerX)**2 + (y-centerY)**2)
    roi=d<r
    imArray[~roi]=default_value
    return imArray, roi

def fillDict(nameDict, fileList, word):
    for f in fileList:
        dictIndex = f.find(word)
        if dictIndex>0:
            dictKey = f[dictIndex:-4]
            nameDict[dictKey] = openImage(f)
            print("Added an image to the dictionary with key: %s" %(dictKey))
    return 

def diffImage(imArray1, imArray2): 
    return np.abs(imArray1-imArray2)

def diffImDark(dict, imDark ):
    imDiff = []
    for key in dict:
        im = dict[key]
        d = diffImage(im, imDark)
        imDiff.append(d)
    return imDiff