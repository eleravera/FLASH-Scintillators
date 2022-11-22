from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import scipy
from scipy.optimize import curve_fit
import glob


def openImage(path):
    im = Image.open(path)
    return np.array(im, dtype= np.int32)

def plotImage(imArray, bounds=[None, None]):
    if bounds==[None, None]:
        vmin, vmax = np.quantile(imArray, [0.02, 0.98])
    fig, ax = plt.subplots(1,1)
    show=ax.imshow(imArray, vmin=vmin, vmax=vmax)
    fig.colorbar(show)
    return 

def histImage(imArray, bins=None):
    if bins==None:
        vmin, vmax = np.quantile(imArray, [0.002, 0.998])
        bins=np.linspace(vmin-0.5, vmax+0.5, int(vmax-vmin+2) )
    fig, ax = plt.subplots(1,1)
    ax.hist(imArray[200,:], bins=bins, alpha=0.4)
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
    return imArray1-imArray2

def diffImDark(dict, imDark ):
    imDiff = []
    for key in dict:
        im = dict[key]
        d = diffImage(im, imDark)
        imDiff.append(d)
    return imDiff