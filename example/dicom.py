from PyVutils import DCM

DS = DCM.Load("data/CT_small.dcm") # load a dicom file

print(DS) # view dicom tags

DCM.View(DS) # view pixel data as an image

'''
<data/CT_small-pixel_data.png>
'''