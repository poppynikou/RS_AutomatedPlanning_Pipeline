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
atlas_z_chin = 71
atlas_z_shoulder = 50
atlas_y_spinalcord = 200

ROIobj = ROI()
ROIobj.import_Img(img_path)
((x_min, x_max), (y_min,y_max), (z_min, z_max)) = ROIobj.get_Img_extents()

#alignment = ROIobj.get_atlas_alignment(text_file_path)
ROIobj.define_atlas_alignment([-1,3,-7], [1,1,-1])

x_cut = ROIobj.calc_atlas_xslice_in_dicom(atlas_x_cut)
z_chin = ROIobj.calc_atlas_zslice_in_dicom(atlas_z_chin)
z_shoulder = ROIobj.calc_atlas_zslice_in_dicom(atlas_z_shoulder)
y_cut = ROIobj.calc_atlas_yslice_indicom(atlas_y_spinalcord)

newnames = ['CTVHIGH_ANT', 'CTVLOW_ANT']
rois_to_keep, names = ROIobj.get_rois_CTVs(path_csv, newnames)
structure_set = ROIobj.import_and_filter(rtstruct_path, names)
structure_set = ROIobj.crop(structure_set, newnames, limits = [None, None,[int(z_min), z_chin]])

newnames = ['CTVHIGH_POS', 'CTVLOW_POS']
rois_to_keep, names = ROIobj.get_rois_CTVs(path_csv, newnames)
structure_set2 = ROIobj.import_and_filter(rtstruct_path, names)
structure_set2 = ROIobj.crop(structure_set2, newnames, limits = [None, None,[z_shoulder, int(z_max)]])

newnames = ['CTVLOW_R']
rois_to_keep, names = ROIobj.get_rois_lowdoseCTV(path_csv, newnames)
structure_set3 = ROIobj.import_and_filter(rtstruct_path, names)
structure_set3 = ROIobj.crop(structure_set3, newnames, limits = [[x_cut, x_max], None, None])

newnames = ['CTVLOW_L']
rois_to_keep, names = ROIobj.get_rois_lowdoseCTV(path_csv, newnames)
structure_set4 = ROIobj.import_and_filter(rtstruct_path, names)
structure_set4 = ROIobj.crop(structure_set4, newnames, limits = [[x_min, x_cut], None, None])


newnames = ['CTVHIGH_R1']
rois_to_keep, names = ROIobj.get_rois_highdoseCTV(path_csv, newnames)
structure_set5 = ROIobj.import_and_filter(rtstruct_path, names)
structure_set5 = ROIobj.crop(structure_set5, newnames, limits = [[x_cut, x_max], None, None])

newnames = ['CTVHIGH_R2']
rois_to_keep, names = ROIobj.get_rois_highdoseCTV(path_csv, newnames)
structure_set6 = ROIobj.import_and_filter(rtstruct_path, names)
structure_set6 = ROIobj.crop(structure_set6, newnames, limits = [[x_min,x_cut], [y_min, y_cut], None])

total_structure_set_CTV_highdose_right = ROIobj.add_structure_sets([structure_set5, structure_set6])
ROI_total_structure_set_CTV_highdose_right = total_structure_set_CTV_highdose_right.combine_rois(name = 'CTVHIGH_R', intersection = False)
new_structure_set = StructureSet()
new_structure_set.add_roi(ROI_total_structure_set_CTV_highdose_right)


newnames = ['CTVHIGH_L1']
rois_to_keep, names = ROIobj.get_rois_highdoseCTV(path_csv, newnames)
structure_set8 = ROIobj.import_and_filter(rtstruct_path, names)
structure_set8 = ROIobj.crop(structure_set8, newnames, limits = [[x_min, x_cut], None, None])

newnames = ['CTVHIGH_L2']
rois_to_keep, names = ROIobj.get_rois_highdoseCTV(path_csv, newnames)
structure_set9 = ROIobj.import_and_filter(rtstruct_path, names)
structure_set9 = ROIobj.crop(structure_set9, newnames, limits = [[x_cut,x_max], [y_min,y_cut], None])

total_structure_set_CTV_highdose_left = ROIobj.add_structure_sets([structure_set8, structure_set9])
ROI_total_structure_set_CTV_highdose_left = total_structure_set_CTV_highdose_left.combine_rois(name = 'CTVHIGH_L', intersection = False)
new_structure_set2 = StructureSet()
new_structure_set2.add_roi(ROI_total_structure_set_CTV_highdose_left)


rois_to_keep, names = ROIobj.get_rois_all(path_csv)
structure_set20 = ROIobj.import_and_filter(rtstruct_path, names)
total_structure_set = ROIobj.add_structure_sets([structure_set20, structure_set, structure_set2, structure_set3, structure_set4, new_structure_set, new_structure_set2])
ROIobj.save_rtstruct(total_structure_set, RS_rtstruct_path, rtstruct_path)


ROIobj.remove_approval(RS_rtstruct_path)