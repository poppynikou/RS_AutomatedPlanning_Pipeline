from skrt import Image, StructureSet
import pydicom 
import os 
from pydicom.uid import UID

'''
import nibabel as nib 
import numpy as np 

input_nii_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/CT_resampled.nii.gz'

nifti_obj = nib.load(input_nii_path)
img = np.array(nifti_obj.get_fdata(), dtype = np.float32)

img[np.isnan(img)] = -1000

NewNiftiObj = nib.Nifti1Image(img, nifti_obj.affine, nifti_obj.header)
mask_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/CT_resampled.nii.gz'
nib.save(NewNiftiObj, mask_path)
'''

import nibabel as nib 
path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/CT_resampled.nii.gz'

Img = Image(path, dtype = 'float32', default_intensity = [-1189, 3700]).astype("dcm")
voxel_size = Img.get_voxel_size()


new_dicom_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM'
ref_dicom_path = 'D:/UCLH_HN/HN_1/CT_20151217/DICOM/CT_20151217_1.dcm'
Img.write(outname = new_dicom_path,  modality = 'CT')#, header_source = ref_dicom_path)#, voxel_size =voxel_size)


for dicom in os.listdir(new_dicom_path):

    dicom_object = pydicom.dcmread(new_dicom_path + '/' + str(dicom))

    if dicom_object[0x008, 0x060].value == 'CT':

        dicom_object[0x020, 0x000d].value = UID("1.2.826.0.1.3680043.2.135.736382.57774833.7.1543497167.516.1")
        dicom_object[0x010, 0x010].value = 'H&N 1'
        dicom_object[0x010, 0x020].value = 'H&N 1'
        pydicom.dcmwrite(new_dicom_path + '/'  + str(dicom), dicom_object)


rois_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/STRUCTURES'

Structure_Set = StructureSet(rois_path, to_keep = ['BIN_BRAINSTEM', 'BIN_CORD', 'BIN_CTV54', 'BIN_CTV65', 'BIN_NOBOLUS_BODY', 'BIN_PAROTIDL', 'BIN_PAROTIDR'])

new_rtstruct_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM/RTSTRUCT.dcm'
ref_rtstruct_path = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/RTSTRUCT_CT_20151217.dcm'
Img = Image(new_dicom_path, dtype = 'float32', default_intensity = [-1189, 3700]).astype("dcm")
Structure_Set.image = Img
Structure_Set.write(outname = new_rtstruct_path, header_source =  ref_rtstruct_path, voxel_size =voxel_size)

rtstruct = pydicom.dcmread(new_rtstruct_path)
rtstruct.ApprovalStatus = 'NOT APPROVED'
rtstruct.save_as(new_rtstruct_path)


'''
for dicom in os.listdir(new_dicom_path):

    new_dicom_obj = pydicom.dcmread(new_dicom_path + '/' + str(dicom))

    if new_dicom_obj[0x008, 0x060].value == 'CT':

        new_dicom_obj[0x028, 0x0030].value = [9.76562e-1, 9.76562e-1]
        new_dicom_obj[0x020, 0x0032].value[1] = new_dicom_obj[0x028, 0x0030].value[1] * -1
        new_dicom_obj[0x020, 0x0037].value = [1, 0, 0, 0, 1, 0]

        pydicom.dcmwrite(new_dicom_path + '/'  + str(dicom), new_dicom_obj)
'''


'''
import pydicom as dcm
import csv 
import nibabel as nib 

#new_dicom_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM/1.dcm'
#ref_dicom_path = 'D:/UCLH_HN/HN_1/CT_20151217/DICOM/CT_20151217_1.dcm'

new_dicom_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/CT_resampled.nii.gz'
ref_dicom_path = 'D:/UCLH_HN/HN_1/CT_20151217/NIFTI/CT_20151217.nii.gz'

#new_dicom = dcm.dcmread(new_dicom_path)
new_dicom_obj = nib.load(new_dicom_path)
new_dicom = new_dicom_obj.header

newdicom_file = open('newnifti.txt', mode='w')
for header_data in new_dicom:
    newdicom_file.write(str(header_data) + '\n' )

#ref_dicom = dcm.dcmread(ref_dicom_path)
ref_dicom_obj = nib.load(ref_dicom_path)
ref_dicom = ref_dicom_obj.header

refdicom_file = open('refnifti.txt', mode='w')
for header_data in ref_dicom:
    refdicom_file.write(str(header_data) + '\n' )

'''

