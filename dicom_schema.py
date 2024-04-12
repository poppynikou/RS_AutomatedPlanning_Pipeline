from skrt import Image, StructureSet
import pydicom
from ROIclass import * 
import os 

'''
This assumes that in the patient folder there is:

- pCT
- text file containing the affine/rigid transformation from patient space -> model space 

'''

path_csv = os.getcwd() + '\Contour_Naming_Schema.csv'
rtstruct_path = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/RTSTRUCT_CT_20151217.dcm'
RS_rtstruct_path = 'D:/UCLH_HN/HN_1/CT_20151217/STRUCTURES/RS_RTSTRUCT_CT_20151217.dcm'
img_path = 'D:/UCLH_HN/HN_1/CT_20151217/DICOM'
text_file_path = ''

# defined in atlas space
atlas_x_cut = 260
atlas_z_chin= 71
atlas_z_shoulder = 50



ROIobj = ROI()
ROIobj.import_Img(img_path)
((x_min, x_max), (y_min,y_max), (z_min, z_max)) = ROIobj.get_Img_extents()

alignment = ROIobj.get_atlas_alignment(text_file_path)
ROIobj.define_atlas_alignment(alignment, [1,1,-1])

x_cut = ROIobj.calc_atlas_xslice_in_dicom(atlas_x_cut)
z_chin = ROIobj.calc_atlas_zslice_in_dicom(atlas_z_chin)
z_shoulder = ROIobj.calc_atlas_zslice_in_dicom(atlas_z_shoulder)

rois_to_keep, names = ROIobj.get_rois_all(path_csv, ['CTV_lowdose_ant', 'CTV_highdose_ant'])
structure_set = ROIobj.import_and_filter_CTVs(rtstruct_path, rois_to_keep, names)
structure_set = ROIobj.crop_z(structure_set, names, [int(z_min), z_chin])

rois_to_keep, names = ROIobj.get_rois_all(path_csv, ['CTV_lowdose_pos', 'CTV_highdose_pos'])
structure_set2 = ROIobj.import_and_filter_CTVs(rtstruct_path, rois_to_keep, names)
structure_set2 = ROIobj.crop_z(structure_set2, names, [z_shoulder, int(z_max)])

rois_to_keep, names = ROIobj.get_rois_all(path_csv, ['CTV_lowdose_right', 'CTV_highdose_right'])
structure_set3 = ROIobj.import_and_filter_CTVs(rtstruct_path, rois_to_keep, names)
structure_set3 = ROIobj.crop_x(structure_set3, names, [x_cut, x_max])

rois_to_keep, names = ROIobj.get_rois_all(path_csv, ['CTV_lowdose_left', 'CTV_highdose_left'])
structure_set4 = ROIobj.import_and_filter_CTVs(rtstruct_path, rois_to_keep, names)
structure_set4 = ROIobj.crop_x(structure_set4, names, [x_min, x_cut])

rois_to_keep, names = ROIobj.get_rois_all(path_csv)
structure_set5 = ROIobj.import_and_filter_CTVs(rtstruct_path, rois_to_keep, names)
total_structure_set = ROIobj.add_structure_sets([structure_set, structure_set2, structure_set3, structure_set4, structure_set5])
ROIobj.save_rtstruct(total_structure_set, RS_rtstruct_path, rtstruct_path)
