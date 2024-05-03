# Script recorded 03 May 2024, 14:48:12

#   RayStation version: 14.0.100.0
#   Selected patient: ...

from connect import *

case = get_current("Case")
plan = get_current("Plan")
beam_set = get_current("BeamSet")
db = get_current("PatientDB")
examination = get_current("Examination")

# set the rsp curve of the CT 
examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName="Philips 7500 UCH HU2RSP")

retval_0 = case.AddNewPlan(PlanName="TEST_03052024", PlannedBy="POPPY_AUTO", Comment="", ExaminationName="CT 1", IsMedicalOncologyPlan=False, AllowDuplicateNames=False)
retval_1 = retval_0.AddNewBeamSet(Name="TEST_03052024", ExaminationName="CT 1", MachineName="Gantry 1", Modality="Protons", TreatmentTechnique="ProtonPencilBeamScanning", PatientPosition="HeadFirstSupine", NumberOfFractions=30, CreateSetupBeams=False, UseLocalizationPointAsSetupIsocenter=False, UseUserSelectedIsocenterSetupIsocenter=False, Comment="", RbeModelName="Constant 1.1", EnableDynamicTrackingForVero=False, NewDoseSpecificationPointNames=[], NewDoseSpecificationPoints=[], MotionSynchronizationTechniqueSettings={ 'DisplayName': None, 'MotionSynchronizationSettings': None, 'RespiratoryIntervalTime': None, 'RespiratoryPhaseGatingDutyCycleTimePercentage': None, 'MotionSynchronizationTechniqueType': "Undefined" }, Custom=None, ToleranceTableLabel=None)
retval_1.SetAutoScaleToPrimaryPrescription(AutoScale=False)

plan.PlanOptimizations[0].ResetOptimization()
plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template=db.TemplateTreatmentOptimizations['HN_AUTO'], AssociatedRoisAndPois={ 'BODY': "BODY", 'OTVHIGH': "OTVHIGH", 'OTVLOW': "OTVLOW", 'BRAINSTEM': "BRAINSTEM", 'CORD': "CORD", 'PAROTIDL': "PAROTIDL", 'PAROTIDR': "PAROTIDR" })
plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

# if you want to keep it going:
plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

# compute the final dose 
beam_set.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="IonMonteCarlo", ForceRecompute=False, RunEntryValidation=True)

# calculate the final clinical goals 
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template=db.TemplateTreatmentOptimizations['HN_CG_AUTO'], AssociatedRoisAndPois={ 'CTVHIGH': "CTVHIGH", 'CTVLOW': "CTVLOW", 'BRAINSTEM': "BRAINSTEM", 'CORD': "CORD", 'PAROTIDL': "PAROTIDL", 'PAROTIDR': "PAROTIDR" })

plan.TreatmentCourse.GoalEvaluation()
