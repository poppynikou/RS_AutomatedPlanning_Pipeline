
from skrt import Image, StructureSet
import os 

'''
ref_dicom_path = 'D:/UCLH_HN/HN_1/CT_20151217/DICOM/'
ref_rtstruct_path = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/RTSTRUCT_CT_20151217.dcm'

Img = Image(ref_dicom_path, dtype = 'float32').astype("dcm")
new_dicom_path = 'D:/test_dcm_0911/CT.nii.gz'
#Img.write(outname = new_dicom_path,  modality = 'CT')

T = 'T:/UCLH_MODELS/PATIENTSPACE_REGS/HN_1/CBCT_20160115/deformation_field_CBCT_20160115.nii.gz'

reg_resample = 'C:/Users/poppy/Documents/Nifty/niftyreg_install/bin/reg_resample.exe'

resampled_img = 'D:/test_dcm_0911/model_CT.nii.gz'
command = reg_resample + ' -ref ' + new_dicom_path + ' -flo ' + new_dicom_path + ' -trans ' + T + ' -res ' + resampled_img + ' -inter 3 -pad -1000'
#os.system(command)

Img = Image(resampled_img, dtype = 'float32')
new_dicom_path = 'D:/test_dcm_0911/DICOM/*.dcm'
#Img.write(outname = new_dicom_path,  modality = 'CT')

ref_img = 'D:/test_dcm_0911/CT.nii.gz'
float_img  = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/BIN_BRAINSTEM_CT_20151217.nii.gz'
resampled_img = 'D:/test_dcm_0911/structures/BRAINSTEM.nii.gz'
command = reg_resample + ' -ref ' + ref_img + ' -flo ' + float_img + ' -trans ' + T + ' -res ' + resampled_img + ' -inter 0 -pad 0'
#os.system(command)




Structure_Set = StructureSet(resampled_img, to_keep = ['BRAINSTEM'])#, 'BIN_CORD', 'BIN_CTV54', 'BIN_CTV65', 'BIN_NOBOLUS_BODY', 'BIN_PAROTIDL', 'BIN_PAROTIDR'])
Img = Image(new_dicom_path, dtype = 'float32').astype("dcm")
Structure_Set.image = Img
new_rtstruct_path = 'D:/test_dcm_0911/DICOM/RTSTRUCT.dcm'
Structure_Set.write(outname = new_rtstruct_path, header_source = new_dicom_path)


'''
import pydicom 

new_dicom_path = 'D:/test_dcm_0911/DICOM/'
for dicom in os.listdir(new_dicom_path):
    
    dicom_object = pydicom.dcmread(new_dicom_path + '/' + str(dicom))


    dicom_object[0x010, 0x010].value = 'H&N 1'
    dicom_object[0x010, 0x020].value = 'H&N 1'
    dicom_object[0x010, 0x040].value = 'O'

    try: 
        dicom_object.ApprovalStatus = 'UNAPPROVED'
    except:
        pass
    
    pydicom.dcmwrite(new_dicom_path + '/'  + str(dicom), dicom_object)