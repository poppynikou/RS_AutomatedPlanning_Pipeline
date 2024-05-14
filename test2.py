import pydicom as dcm

ref_dicom_path = 'D:/UCLH_HN/HN_1/CT_20151217/DICOM/CT_20151217_1.dcm'

new_dicom = dcm.dcmread(ref_dicom_path)

print(new_dicom.file_meta[0x002, 0x002].value)

'''
newdicom_file = open('newnifti.txt', mode='w')
for header_data in new_dicom:
    newdicom_file.write(str(header_data) + '\n' )

'''
