from skrt import Image, StructureSet


path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/CT_resampled.nii.gz'
Img = Image(path)
voxel_size = Img.get_voxel_size()

new_dicom_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM'
ref_dicom_path = 'D:/UCLH_HN/HN_1/CT_20151217/DICOM/CT_20151217_1.dcm'
Img.write(outname = new_dicom_path, header_source = ref_dicom_path, modality = 'CT')#, voxel_size =voxel_size)

'''
rois_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/STRUCTURES'
Structure_Set = StructureSet(rois_path)

new_rtstruct_path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM/RTSTRUCT.dcm'
ref_rtstruct_path = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/RTSTRUCT_CT_20151217.dcm'
Structure_Set.image = Img
Structure_Set.write(outname = new_rtstruct_path, header_source =  ref_rtstruct_path)#, voxel_size =voxel_size)
'''

