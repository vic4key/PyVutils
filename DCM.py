# -*- coding: utf-8 -*-

# Vutils for DICOM

import pydicom, glob
import numpy as np
from . import File

def Load(filePath, force=True):
    return pydicom.dcmread(filePath, force=force)

def Loadirectory(pattern, extensions = [], force=True):

    list_ds = []
    def callback(filePath, fileDirectory, fileName):
        try:
            list_ds.append(Load(filePath, force))
        except: print(f"Error when loading '{filePath}'")
        return
    File.LSRecursive(pattern, callback, extensions)

    dict_series = {}
    if len(list_ds) > 0:
        for ds in list_ds:
            try:
                series_instance_uid = str(ds[0x0020, 0x000E].value) # Series Instance UID
                if not series_instance_uid in dict_series.keys():        
                    dict_series[series_instance_uid] = []
                dict_series[series_instance_uid].append(ds)
            except: print(f"Error when grouping '{ds.filename}'")

    return dict_series

def Store(filePath, DS, likeOriginal = True):
    pydicom.filewriter.write_file(filePath, DS, likeOriginal)
    return

def Save(filePath, DS):
    DS.save_as(filePath)
    return

def View(obj):

    import matplotlib.pyplot as plt

    theObjType = type(obj)
    if theObjType is str:
        DS = Load(obj)
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