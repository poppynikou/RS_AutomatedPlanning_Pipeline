from skrt import Image, StructureSet
import pydicom
from ROIclass import * 
import os 

def replace_dicom_tag(dicom_obj, tag, value):

    if tag in dicom_obj:

        dicom_obj[tag].value = value


centres = ['UCLH']#,'GSTT']

for centre in centres:
    
    data_path = 'D:/RBP_RS/'+str(centre)+'/DICOM_RS/'
    patients = ['HN_10']
    #os.listdir(data_path)

    for patient in patients:

        patient_path = data_path + str(patient)
        
        for (root,dirs,files) in os.walk(patient_path):
             
            for file in files:
                
                dicom_path = root + '/' + str(file)
                
                dicom_object = pydicom.dcmread(dicom_path)

                # date DA type 
                replace_dicom_tag(dicom_object, (0x008, 0x012), '20240623')
                replace_dicom_tag(dicom_object, (0x008, 0x020), '20240623')
                replace_dicom_tag(dicom_object, (0x008, 0x021), '20240623')
                replace_dicom_tag(dicom_object, (0x008, 0x022), '20240623')
                replace_dicom_tag(dicom_object, (0x008, 0x023), '20240623')
                replace_dicom_tag(dicom_object, (0x3006, 0x008), '20240623')

                # time TM type
                replace_dicom_tag(dicom_object, (0x008, 0x013), '090000')
                replace_dicom_tag(dicom_object, (0x008, 0x030), '090000')
                replace_dicom_tag(dicom_object, (0x008, 0x031), '090000')
                replace_dicom_tag(dicom_object, (0x008, 0x032), '090000')
                replace_dicom_tag(dicom_object, (0x008, 0x033), '090000')
                replace_dicom_tag(dicom_object, (0x3006, 0x009), '090000')
                
                # names 
                replace_dicom_tag(dicom_object, (0x010, 0x010), str(centre) + '_' + str(patient))
                replace_dicom_tag(dicom_object, (0x010, 0x020), str(centre) + '_' + str(patient))

                # patient sex 
                replace_dicom_tag(dicom_object, (0x010, 0x040), 'O')

                # series number
                replace_dicom_tag(dicom_object, (0x020, 0x011), '1')
                replace_dicom_tag(dicom_object, (0x020, 0x012), '1')
                
                # approval status
                replace_dicom_tag(dicom_object, (0x300e, 0x002), 'UNAPPROVED')
                # description of series
                replace_dicom_tag(dicom_object, (0x3006, 0x002), 'RS')
                replace_dicom_tag(dicom_object, (0x008, 0x103e), 'RS')

                pydicom.dcmwrite(dicom_path, dicom_object)
                          


'''
This bit of code lets you save the dicom files as a txt so you can check
Not all dicom files have all the tags listed above 
Some may have more?

path1 = 'D:/RBP_RS/UCLH/DICOM_pCT/HN_19/CT/CT.HN19.Image 1.dcm'

dicom_object = pydicom.dcmread(path1)

dicom_file = open('ct.txt', mode='w')
for header_data in dicom_object:
    dicom_file.write(str(header_data) + '\n' )

path1 = 'D:/RBP_RS/GSTT/DICOM_RS/HN_1/RS.dcm'

dicom_object = pydicom.dcmread(path1)

dicom_file = open('rs.txt', mode='w')
for header_data in dicom_object:
    dicom_file.write(str(header_data) + '\n' )


'''