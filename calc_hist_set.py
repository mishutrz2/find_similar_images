# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 22:18:57 2021

@author: mircea.brisan
"""

import matplotlib.pyplot as plt
import numpy as np
from skimage import color
from skimage.feature import local_binary_pattern
import os

def calc_set():

    resourcesPath = os.path.join(os.getcwd(), 'resources')
    histograms = []
    myfiles = []

    for file in os.listdir(os.path.join(resourcesPath, 'img')):
        if file.endswith('.JPG') or file.endswith('.jpg'):
            img = plt.imread(os.path.join(resourcesPath, 'img', file))
            img = color.rgb2gray(img)
            img_lbp = local_binary_pattern(img,16,2,'default')
            #plt.figure(), plt.imshow(img_lbp)
            histogram = np.histogram(img_lbp, bins=256, density=True)
            histograms.append(histogram[0])
            myfiles.append(os.path.join(resourcesPath, 'img', file))

    histograms = np.array(histograms)
    myfiles = np.array(myfiles)

    np.savetxt(os.path.join(resourcesPath, 'histograms.csv'), histograms, delimiter=',')
    np.save(os.path.join(resourcesPath, 'myfiles.npy'), myfiles)
    print("-histogram set updated-")