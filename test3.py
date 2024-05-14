from pydicom.dataset import Dataset, FileMetaDataset
import nibabel as nib 
import numpy as np 
from pydicom.uid import UID, ExplicitVRLittleEndian

path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/CT_resampled.nii.gz'

nifti_object = nib.load(path)
data = nifti_object.get_fdata()
data = np.array(data, dtype = np.float32)

ds = Dataset()
ds.add_new([0x7fe0, 0x010], 'OW', data)
ds.add_new([0x010, 0x010], 'PN', 'H&N 1')
ds.add_new([0x010, 0x020], 'LO', 'H&N 1')

ds.add_new([0x018, 0x050], 'D.S', '2.5')
ds.add_new([0x018, 0x5100], 'CS', 'HFS')
ds.add_new([0x020, 0x037], 'DS', [1, 0, 0, 0, 1, 0])
ds.add_new([0x028, 0x010], 'US', 512)
ds.add_new([0x028, 0x011], 'US', 512)
ds.add_new([0x028, 0x030], 'DS', [9.76562e-1, 9.76562e-1])
ds.add_new([0x028, 0x1050], 'DS', '40.0')
ds.add_new([0x028, 0x1051], 'DS', '300.0')
ds.add_new([0x028, 0x1052], 'DS', '-1024.0')
ds.add_new([0x028, 0x1053], 'DS', '1.0')


file_meta = FileMetaDataset()
file_meta.MediaStorageSOPClassUID = UID("1.2.840.10008.5.1.4.1.1.2")
file_meta.MediaStorageSOPInstanceUID = UID("1.2.826.0.1.3680043.2.135.736382.57774833.7.1543497167")
file_meta.ImplementationClassUID = UID("1.2.826.0.1.3680043.2.135")
file_meta.TransferSyntaxUID = ExplicitVRLittleEndian


# Add the file meta information
ds.file_meta = file_meta

path = 'D:/UCLH_MODELS/PATIENTSPACE_REGS/CBCT_20160115/DICOM'
ds.save_as(path)#, enforce_file_format=True)