import pydicom
import csv 
import numpy as np 


'''
This is the manual way of cropping the rt struct files

'''



path = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/RTSTRUCT_CT_20151217.dcm'
dcmobj = pydicom.dcmread(path)
dcmobj_copy = dcmobj.copy()

'''
work out how to delete points on certain slices in dicom 
'''

# there are 25 contours
#contours = dcmobj.ROIContourSequence

#deleting contours on certain slices

slice_threshold = 23

#name 
#print(dcmobj[0x3006,0x0020][0][0x3006, 0x0026])
#points
#25 contours
no_of_contours = len(dcmobj_copy[0x3006,0x0039][0][0x3006, 0x0040].value)
#print(dcmobj_copy[0x3006,0x0039][0][0x3006, 0x0040][0])

#CTV_names = ['']

# contour index
for c_i in np.arange(0,25):

    contour_name = dcmobj_copy[0x3006,0x0020][c_i][0x3006, 0x0026].value
    
    # slice index 
    for s_i in np.arange(0, 176):

        try:
            contours = dcmobj_copy[0x3006,0x0039][c_i][0x3006, 0x0040][s_i][0x3006,0x0050].value
        
            # decide on this threshold
            if int(contours[2]) < int(slice_threshold):
            #print(dcmobj_copy[0x3006,0x0039][0][0x3006, 0x0040][c_i][0x3006,0x0016])
                
                dcmobj_copy[0x3006,0x0039][c_i][0x3006, 0x0040][s_i][0x3006,0x0050].value = []
                dcmobj_copy[0x3006,0x0039][c_i][0x3006, 0x0040][s_i][0x3006,0x0046].value = '0'

        except:
            pass

        
   
dcmobj_copy.save_as('D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/test_RTSTRUCT_CT_20151217.dcm')


# write dicom header to csv

'''
newdcmobj = pydicom.dcmread('D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/test_RTSTRUCT_CT_20151217.dcm')
with open('mynew.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow("Group Elem Description VR value".split())
    for elem in newdcmobj:
        writer.writerow([
            f"{elem.tag.group:04X}", f"{elem.tag.element:04X}",
            elem.description(), elem.VR, str(elem.value)
        ])

'''


        

