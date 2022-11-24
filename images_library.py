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

def checkSaturation(imArray, saturation=2**16-1):
    args=np.argwhere(imArray>=saturation)
    if len(args)!=0:
        print("CCD saturate in %d pixels; the max value recorded is %d" % (len(args), imArray.max() ))
    return

def plotImage(imArray, bounds=[None, None], title=''):
    if bounds==[None, None]:
        vmin, vmax = np.quantile(imArray, [0.02, 0.98])
    else: 
        vmin=bounds[0]
        vmax=bounds[1]
    fig, ax = plt.subplots(1,1, figsize=(3,3))
    show=ax.imshow(imArray, vmin=vmin, vmax=vmax)
    fig.colorbar(show)
    fig.suptitle(title)    
    return

def histImage(imArray, bins, title =""):
    fig, ax = plt.subplots(1,1, figsize=(3,3))
    ax.hist(np.concatenate(imArray), bins=bins, alpha=0.4)
    fig.suptitle(title)    
    return 

def histImageROI(imArray, ROI, bins, title=""):
    #if bins==None: 
    #    vmin, vmax = np.quantile(imArray, [0.1, 0.9])
    #    bins=np.linspace(vmin-0.5, vmax+0.5, int(vmax-vmin+2) )
    fig, ax = plt.subplots(1,1, figsize=(3,3))
    ax.hist(imArray[ROI], bins=bins, alpha=0.4)
    fig.suptitle(title)    
    return 

def defineROI(x, y, centerX, centerY, r=12):
    d=np.sqrt ((x-centerX)**2 + (y-centerY)**2)
    roi=d<r
    return roi

def applySquareROI(imArray, centerX, centerY, r=12 ):
    return imArray[centerX-r:centerX+r, centerY-r:centerY+r]

def fillDict(nameDict, fileList, word, notWord):
    keys=[]
    for f in fileList:
        excludeWord = f.find(notWord)
        dictIndex = f.find(word)
        if (dictIndex>0) * (excludeWord<0):
            dictKey = f[dictIndex:-4]
            keys.append(dictKey)
            nameDict[dictKey] = openImage(f)
            print("Added an image to the dictionary with key: %s" %(dictKey))
    return keys

def diffImage(imArray1, imArray2): 
    return imArray1-imArray2

def diffImDark(dict, imDark ):
    imDiff = []
    for key in dict:
        im = dict[key]
        d = diffImage(im, imDark)
        imDiff.append(d)
    return imDiff