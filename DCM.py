# -*- coding: utf-8 -*-

# Vutils for DICOM

import pydicom, glob
import numpy as np
import matplotlib.pyplot as plt
from . import File

def Load(filePath):
    return pydicom.dcmread(filePath) 

def Loadirectory(directory, ext="DCM"):

    pattern = File.Slash(directory)
    pattern += "*"

    if len(ext) != 0:
        pattern += "."
        pattern += ext

    return [Load(filePath) for filePath in glob.glob(pattern)]

def Store(filePath, DS, likeOriginal = True):
    pydicom.filewriter.write_file(filePath, DS, likeOriginal)
    return

def Save(filePath, DS):
    DS.save_as(filePath)
    return

def View(obj):

    theObjType = type(obj) 
    if theObjType is str:
        DS = Read(obj)
        plt.imshow(DS.pixel_array, cmap=plt.cm.bone)
        plt.show()
    elif theObjType is pydicom.dataset.FileDataset:
        plt.imshow(obj.pixel_array, cmap=plt.cm.bone)
        plt.show()
    elif theObjType is np.ndarray:
        plt.imshow(obj, cmap=plt.cm.bone)
        plt.show()
    else:
        print("ERROR: Unknown object type")

    return