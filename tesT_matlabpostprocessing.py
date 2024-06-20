import pydicom as dcm
import os


path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/matlab_out/dicom_Img_1'



files = os.listdir(path)

for file in files:

    file_path = path + '/' + str(file)
    print(file_path)
    dicom_obj = dcm.dcmread(file_path)
    dicom_obj[0x010, 0x010].value = 'H&N 1'
    dicom_obj[0x010, 0x020].value = 'H&N 1'
    
    if dicom_obj[0x008, 0x060].value == 'CT':
        dicom_obj[0x028, 0x0101].value = 13

    dicom_obj.save_as(file_path)