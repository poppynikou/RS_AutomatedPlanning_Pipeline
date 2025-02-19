from skrt import Image, StructureSet
import pydicom
import pandas as pd 
import numpy as np 
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

class ROI():


    def __init__(self):

        return 

    def define_atlas_alignment(self, shifts, quaternion_signs):

        '''
        shifts: [x_shift, y_shift,z_shift]
        in slices which align to the UCLH atlas
        quaternion_signs: [x_q, y_q, z_q]
        whether to add/subtract slices in each direction
        '''

        self.shifts = shifts
        self.quaternion_signs = quaternion_signs

    
    def calc_atlas_xslice_in_dicom(self, atlas_slice): 

        nifti_slice = atlas_slice + self.quaternion_signs[0]*self.shifts[0]
        #print(self.Img_extent[0])
        dicom_distance = self.Img_extent[0][0] + (nifti_slice * self.voxel_size[0])

        return dicom_distance

    def calc_atlas_zslice_in_dicom(self, atlas_slice):

        # atlas extent
        atlas_extent = -152.5
        
        shift = +self.shifts[2] + atlas_extent - self.Img_extent[2][0]

        # in the atlas space
        distance_from_zero = atlas_slice * self.voxel_size[2]

        #print(self.Img_extent[2])
        dicom_distance = self.Img_extent[2][0] + shift + distance_from_zero 

       

        return dicom_distance
    

    

    def calc_atlas_yslice_indicom(self, atlas_slice):

        nifti_slice = atlas_slice + self.quaternion_signs[1]*self.shifts[1]
        #print(self.Img_extent[2])
        dicom_distance = self.Img_extent[1][0] + (nifti_slice * self.voxel_size[1])

        return dicom_distance
    

    def import_and_filter(self, path, names):

        structure_set = StructureSet(path)
        roi_list = structure_set.get_roi_names()
        list_rois_to_keep = [item for key in names.keys() for item in names[key]]

        # assumes there are only two CTV structures 
        rois_to_remove = [roi for roi in roi_list if roi not in list_rois_to_keep]
        
        structure_set.filter_rois(to_keep = list_rois_to_keep, to_remove = rois_to_remove)

        structure_set.rename_rois(names)

        
        return structure_set
    
    def get_shoulder_slice_in_dicom(self, csv_path, rtstruct_path, img_path):
        # I tried to use the atlas to define the shoulder slice 
        # but found that it didnt work too well, because people's necks are very different lengths/sizes

        rois_to_keep, names = self.get_rois_BODY(csv_path, ['BODY'])

        structure_set = self.import_and_filter(rtstruct_path, names)

        structure_set.set_image(img_path)
        body_roi = structure_set.get_roi('BODY')
        mask = body_roi.get_mask()

        # calculate volume of body mask 
        volumes = np.array([np.sum(mask[:,:,i]) for i in np.arange(0, np.shape(mask)[2])])
        

        # the neck is about 20% the volume of the shoulder region 
        inv_volumes = volumes*-1 
        scaled_inv_voles = inv_volumes/inv_volumes[0]
        shoulder_slice = np.where(scaled_inv_voles <0.2)[0][0]

        dicom_distance = self.Img_extent[2][0] + (shoulder_slice * self.voxel_size[2])

        return dicom_distance




    def import_Img(self, path):

        self.Img = Image(path)
        self.voxel_size = self.Img.get_voxel_size()
        self.Img_extent =self.Img.get_extents()

    def get_Img_extents(self):
        
        return self.Img_extent

    def crop(self, structure_set, names, limits = []):

        # in the z axis it crops the points
        # in the x,y axis it creates a mask and then crops 

        structure_set.crop(xlim = limits[0], ylim= limits[1], zlim=limits[2])

        # need to re-set this otherwise it will over-write the original structure in the list
        for structure in names:
            structure_set[str(structure)].number = None
        
        return structure_set
    

    def remove_approval(self, path):

        rtstruct = pydicom.dcmread(path)
        rtstruct.ApprovalStatus = 'NOT APPROVED'
        rtstruct.save_as(path)

    def save_rtstruct(self, structureset, path, ref_path):

        structureset.image = self.Img
        structureset.write(outname = path, header_source =  ref_path, voxel_size =self.voxel_size)


    def add_structure_sets(self, structure_sets):

        '''
        structure_sets: [] list of structure sets to add to eachother
        '''
        total_structure_set = structure_sets[0]
        for s_i, structure_set in enumerate(structure_sets):
            if s_i < len(structure_sets)-1:
                total_structure_set = total_structure_set.__add__(structure_sets[s_i+1])

        return total_structure_set
    

    def get_rois_all(self, csv_path):

        contournames = pd.read_csv(csv_path, header =0, dtype = str)

        rois_to_keep = list(contournames.columns.values)

        names = {}
        for roi in rois_to_keep:

            #print(r)
            names[roi] = list(contournames.loc[:,roi].dropna())

        return rois_to_keep, names

    def get_rois_CTVs(self, csv_path, new_names):

        contournames = pd.read_csv(csv_path, header =0, dtype = str)
        rois_to_keep = list(contournames.columns.values)[0:2]
        names = {}
        if new_names == None:
            for roi in rois_to_keep:

                #print(r)
                names[roi] = list(contournames.loc[:,roi].dropna())
        
        else:
            for r_index, roi in enumerate(new_names):
                # assumes ctvs are stored first and second 
                
                #print(r)
                names[roi] = list(contournames.loc[:,rois_to_keep[r_index]].dropna())

        return rois_to_keep, names
    
    def get_rois_highdoseCTV(self, csv_path, new_names):
    
        contournames = pd.read_csv(csv_path, header =0, dtype = str)
        rois_to_keep = [list(contournames.columns.values)[0]]

        names = {}
        if new_names == None:
            for roi in rois_to_keep:

                #print(r)
                names[roi] = list(contournames.loc[:,roi].dropna())
        
        else:
            for r_index, roi in enumerate(new_names):
                # assumes ctvs are stored first and second 
                
                #print(r)
                names[roi] = list(contournames.loc[:,rois_to_keep[r_index]].dropna())

        return rois_to_keep, names
    
    def get_rois_lowdoseCTV(self, csv_path, new_names):
    
        contournames = pd.read_csv(csv_path, header =0, dtype = str)
        rois_to_keep = [list(contournames.columns.values)[1]]

        names = {}
        if new_names == None:
            for roi in rois_to_keep:

                #print(r)
                names[roi] = list(contournames.loc[:,roi].dropna())
        
        else:
            for r_index, roi in enumerate(new_names):
                # assumes ctvs are stored first and second 
                
                #print(r)
                names[roi] = list(contournames.loc[:,rois_to_keep[r_index]].dropna())

        return rois_to_keep, names
    
    def get_rois_BODY(self, csv_path, new_names):
        
        contournames = pd.read_csv(csv_path, header =0, dtype = str)
        rois_to_keep = [list(contournames.columns.values)[6]]

        names = {}
        if new_names == None:
            for roi in rois_to_keep:

                #print(r)
                names[roi] = list(contournames.loc[:,roi].dropna())
        
        else:
            for r_index, roi in enumerate(new_names):
                # assumes ctvs are stored first and second 
                
                #print(r)
                names[roi] = list(contournames.loc[:,rois_to_keep[r_index]].dropna())

        return rois_to_keep, names
    

    def get_atlas_alignment(self, text_file):


        text_info = np.loadtxt(text_file, dtype='i', delimiter=' ', converters=float)

        x_shift, y_shift, z_shift = text_info[0,3], text_info[1,3], text_info[2,3]
        #print(x_shift, y_shift, z_shift)

        return [x_shift, y_shift, z_shift]
    
    def get_quaternion(self):
        
        # not sure where this comes from exactly ]

        
        return
        