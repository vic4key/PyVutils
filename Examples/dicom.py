import PyVutils as vu

data_set = vu.load_dicom("data/CT_small.dcm") # load a dicom file
print(data_set)  # view dicom tags
vu.view_dicom_image(data_set)  # view pixel data as an image

'''
<data/CT_small-pixel_data.png>
'''