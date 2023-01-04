# -*- coding: utf-8 -*-

# Vutils for DICOM

import pydicom, glob
import numpy as np
from . import FS

def load_dicom(file_path, force=True):
    return pydicom.dcmread(file_path, force=force)

def load_dicom_directory(pattern, extensions = [], force=True):

    list_ds = []
    def callback(file_path, file_directory, file_name):
        try:
            list_ds.append(load_dicom(file_path, force))
        except: print(f"Error when loading '{file_path}'")
        return
    File.recursive_directory(pattern, callback, extensions)

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

def store_dicom_file(file_path, data_set, like_original = True):
    pydicom.filewriter.write_file(file_path, data_set, like_original)
    return

def save_dicom_file(file_path, data_set):
    data_set.save_as(file_path)
    return

def view_dicom_image(any_obj):

    import matplotlib.pyplot as plt

    obj_type = type(any_obj)
    if obj_type is str:
        DS = load_dicom(any_obj)
        plt.imshow(DS.pixel_array, cmap=plt.cm.bone)
        plt.show()
    elif obj_type is pydicom.dataset.FileDataset:
        plt.imshow(any_obj.pixel_array, cmap=plt.cm.bone)
        plt.show()
    elif obj_type is np.ndarray:
        plt.imshow(any_obj, cmap=plt.cm.bone)
        plt.show()
    else:
        print("ERROR: Unknown object type")

    return