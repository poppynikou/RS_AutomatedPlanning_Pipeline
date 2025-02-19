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


rois_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/STRUCTURES'

Structure_Set = StructureSet(rois_path, to_keep = ['BIN_BRAINSTEM'])#, 'BIN_CORD', 'BIN_CTV54', 'BIN_CTV65', 'BIN_NOBOLUS_BODY', 'BIN_PAROTIDL', 'BIN_PAROTIDR'])

new_rtstruct_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM/RTSTRUCT.dcm'
ref_rtstruct_path = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/RTSTRUCT_CT_20151217.dcm'
new_dicom_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM/1.dcm'
Img = Image(new_dicom_path, dtype = 'float32') #.astype("dcm")
Structure_Set.image = Img
Structure_Set.write(outname = new_rtstruct_path, voxel_size =voxel_size)#, header_source = ref_rtstruct_path)


rtstruct = pydicom.dcmread(new_rtstruct_path)
rtstruct[0x010, 0x010].value = 'H&N 1'
rtstruct[0x010, 0x020].value = 'H&N 1'
rtstruct.ApprovalStatus = 'UNAPPROVED'
rtstruct[0x010, 0x040].value = 'O'
rtstruct.add_new([0x0008, 0x1070], 'PN', "")
rtstruct.save_as(new_rtstruct_path)

rtstruct_file = open('rtstruct.txt', mode='w')
for header_data in rtstruct:
    rtstruct_file.write(str(header_data) + '\n' )

'''

path1 = 'D:/RBP_RS/UCLH/DICOM_pCT/HN_5/CT/CT_20160926_1.dcm'

dicom_object = pydicom.dcmread(path1)

dicom_file = open('ct.txt', mode='w')
for header_data in dicom_object:
    dicom_file.write(str(header_data) + '\n' )

path1 = 'D:/RBP_RS/UCLH/DICOM_RS/HN_11/RS.dcm'

dicom_object = pydicom.dcmread(path1)

dicom_file = open('rs.txt', mode='w')
for header_data in dicom_object:
    dicom_file.write(str(header_data) + '\n' )