# Script recorded 03 May 2024, 14:48:12

#   RayStation version: 14.0.100.0
#   Selected patient: ...

from connect import *

case = get_current("Case")
plan = get_current("Plan")
beam_set = get_current("BeamSet")
db = get_current("PatientDB")


retval_0 = case.AddNewPlan(PlanName="TEST_03052024", PlannedBy="POPPY_AUTO", Comment="", ExaminationName="CT 1", IsMedicalOncologyPlan=False, AllowDuplicateNames=False)

retval_1 = retval_0.AddNewBeamSet(Name="TEST_03052024", ExaminationName="CT 1", MachineName="Gantry 1", Modality="Protons", TreatmentTechnique="ProtonPencilBeamScanning", PatientPosition="HeadFirstSupine", NumberOfFractions=30, CreateSetupBeams=False, UseLocalizationPointAsSetupIsocenter=False, UseUserSelectedIsocenterSetupIsocenter=False, Comment="", RbeModelName="Constant 1.1", EnableDynamicTrackingForVero=False, NewDoseSpecificationPointNames=[], NewDoseSpecificationPoints=[], MotionSynchronizationTechniqueSettings={ 'DisplayName': None, 'MotionSynchronizationSettings': None, 'RespiratoryIntervalTime': None, 'RespiratoryPhaseGatingDutyCycleTimePercentage': None, 'MotionSynchronizationTechniqueType': "Undefined" }, Custom=None, ToleranceTableLabel=None)

