""" Python code example: DICOM import to a new patient """
import platform
from connect import get_current

def import_from_file_to_a_new_patient(path, patient_id):
    """ DICOM import to a new patient from file """

    patient_db = get_current('PatientDB')

    # Query patients from path by Patient ID
    matching_patients = patient_db.QueryPatientsFromPath(Path = path, SearchCriterias = {'PatientID' : patient_id})

    assert len(matching_patients) == 1, 'Found more than 1 patient with ID {}'.format(patient_id)
    matching_patient = matching_patients[0]

    # Query all the studies of the matching patient
    studies = patient_db.QueryStudiesFromPath(Path = path, SearchCriterias = matching_patient)

    # Query all the series from all the matching studies
    series = []
    for study in studies:
        series += patient_db.QuerySeriesFromPath(Path = path, SearchCriterias = study)

    # Filter queried series to only contain CT series
    series_to_import = [s for s in series if s['Modality'] == 'CT']

    # Import the CT series
    warnings = patient_db.ImportPatientFromPath(Path = path, SeriesOrInstances = series_to_import)

    return warnings




if __name__ == '__main__':
    file_path = ''
    patientID_RS = ''
    import_from_file_to_a_new_patient(file_path, patientID_RS)






