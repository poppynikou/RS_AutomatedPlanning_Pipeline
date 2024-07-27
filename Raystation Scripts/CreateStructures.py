from skrt import Image, StructureSet
import pydicom
from ROIclass import * 
import os 

'''
This assumes that in the patient folder there is:
- pCT
- text file containing the affine/rigid transformation from patient space -> model space 
but it assumes that the rigid transformation just accounts for small miss-alignments, not large ones
'''

path_to_patients = 'D:/RBP_RS/UCLH/DICOM_pCT/'
patients = ['HN_10']
#os.listdir(path_to_patients)

for patient in patients:

    path_csv = os.getcwd() + '\Contour_Naming_Schema.csv'
    rtstruct_path = [path_to_patients + str(patient) + '/' + file for file in os.listdir(path_to_patients + str(patient)) if file.startswith('RTSTRUCT')][0]
    RS_rtstruct_path = 'D:/RBP_RS/TEST.dcm'
    #UCLH/DICOM_RS/'+str(patient)+'/RS.dcm'
    img_path = path_to_patients + str(patient) + '/CT/'
    text_file_path = 'D:/RBP_RS/UCLH/DICOM_pCT/'+str(patient)+'/InitAlignment_atlas.txt'

    # defined in atlas space
    atlas_x_cut = 260
    atlas_z_chin = 71
    #atlas_z_shoulder = 50
    atlas_y_spinalcord = 200

    ROIobj = ROI()
    ROIobj.import_Img(img_path)
    ((x_min, x_max), (y_min,y_max), (z_min, z_max)) = ROIobj.get_Img_extents()

    alignment = ROIobj.get_atlas_alignment(text_file_path)
    ROIobj.define_atlas_alignment(alignment, [1,1,1])

    x_cut = ROIobj.calc_atlas_xslice_in_dicom(atlas_x_cut)
    z_chin = ROIobj.calc_atlas_zslice_in_dicom(atlas_z_chin)
    #z_shoulder = ROIobj.calc_atlas_zslice_in_dicom(atlas_z_shoulder)
    z_shoulder = ROIobj.get_shoulder_slice_in_dicom(path_csv, rtstruct_path, img_path)
    y_cut = ROIobj.calc_atlas_yslice_indicom(atlas_y_spinalcord)

    newnames = ['CTVHIGH_ANT', 'CTVLOW_ANT']
    rois_to_keep, names = ROIobj.get_rois_CTVs(path_csv, newnames)
    structure_set1 = ROIobj.import_and_filter(rtstruct_path, names)
    structure_set1 = ROIobj.crop(structure_set1, newnames, limits = [None, None,[int(z_min), z_chin]])

    newnames = ['CTVHIGH_POS', 'CTVLOW_POS']
    rois_to_keep, names = ROIobj.get_rois_CTVs(path_csv, newnames)
    structure_set2 = ROIobj.import_and_filter(rtstruct_path, names)
    structure_set2 = ROIobj.crop(structure_set2, newnames, limits = [None, None,[z_shoulder, int(z_max)]])

    newnames = ['CTVLOWTemp']
    rois_to_keep, names = ROIobj.get_rois_lowdoseCTV(path_csv, newnames)
    structure_set3 = ROIobj.import_and_filter(rtstruct_path, names)
    newnames = ['CTVHIGHTemp']
    rois_to_keep, names = ROIobj.get_rois_highdoseCTV(path_csv, newnames)
    structure_set4 = ROIobj.import_and_filter(rtstruct_path, names)
    total_structure_set_CTV_total = ROIobj.add_structure_sets([structure_set3, structure_set4])
    total_structure_set_CTV_total = total_structure_set_CTV_total.combine_rois(name = 'CTVTOTAL', intersection = False)
    new_structure_set1 = StructureSet()
    new_structure_set1.add_roi(total_structure_set_CTV_total)

    newnames = ['CTV_LAO']
    CTV_HIGH_TOTAL = new_structure_set1.get_roi('CTVTOTAL')
    print(CTV_HIGH_TOTAL)
    # its because crop is a function you made 
    # and crop is also a function of StructureSet() by scikit-rt
    structure_set5 = new_structure_set1.crop(CTV_HIGH_TOTAL, newnames, limits = [[x_cut, x_max], [y_min, y_cut], None])

    newnames = ['CTV_RAO']
    structure_set6 = new_structure_set1.crop(total_structure_set_CTV_total, newnames, limits = [[x_min, x_cut], [y_min,y_cut], None])

    newnames = ['CTV_RPO']
    structure_set17 = new_structure_set1.crop(total_structure_set_CTV_total, newnames, limits = [[x_min, x_cut], [y_min,y_cut], [z_shoulder, int(z_max)]])

    newnames = ['CTV_LPO']
    structure_set18 = new_structure_set1.crop(total_structure_set_CTV_total, newnames, limits = [[x_cut, x_max], [y_min, y_cut], [z_shoulder, int(z_max)]])

    rois_to_keep, names = ROIobj.get_rois_all(path_csv)
    structure_set20 = ROIobj.import_and_filter(rtstruct_path, names)
    total_structure_set = ROIobj.add_structure_sets([structure_set20, structure_set1, structure_set2,  structure_set5, structure_set6, structure_set17, structure_set18])
    ROIobj.save_rtstruct(total_structure_set, RS_rtstruct_path, rtstruct_path)

    ROIobj.remove_approval(RS_rtstruct_path)

