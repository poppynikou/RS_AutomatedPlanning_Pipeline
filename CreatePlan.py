# Script recorded 03 May 2024, 14:48:12

#   RayStation version: 14.0.100.0
#   Selected patient: ...

# Interpreter: CPython 3.8 (64-bit)
# Name: CreatePlan
# Comment: Create treatment plan

from connect import *


db = get_current("PatientDB")
TemplateTreatmentOptimization_fourfield = db.LoadTemplateOptimizationFunctions(templateName = 'FOURFIELD_HN', lockMode = 'Read')
TemplateClinicalGoals = db.LoadTemplateClinicalGoals(templateName = 'HN_CG_AUTO', lockMode = 'Read')

case = get_current("Case")
examination = get_current("Examination")

# set the rsp curve of the CT 
examination.EquipmentInfo.SetImagingSystemReference(ImagingSystemName="Philips 7500 UCH HU2RSP")

retval_0 = case.AddNewPlan(PlanName="FOURFIELD_HN", PlannedBy="POPPY_AUTO", Comment="", ExaminationName="CT 1", IsMedicalOncologyPlan=False, AllowDuplicateNames=False)
retval_1 = retval_0.AddNewBeamSet(Name="FOURFIELD_HN", ExaminationName="CT 1", MachineName="Gantry 1", Modality="Protons", TreatmentTechnique="ProtonPencilBeamScanning", PatientPosition="HeadFirstSupine", NumberOfFractions=30, CreateSetupBeams=False, UseLocalizationPointAsSetupIsocenter=False, UseUserSelectedIsocenterSetupIsocenter=False, Comment="", RbeModelName="Constant 1.1", EnableDynamicTrackingForVero=False, NewDoseSpecificationPointNames=[], NewDoseSpecificationPoints=[], MotionSynchronizationTechniqueSettings={ 'DisplayName': None, 'MotionSynchronizationSettings': None, 'RespiratoryIntervalTime': None, 'RespiratoryPhaseGatingDutyCycleTimePercentage': None, 'MotionSynchronizationTechniqueType': "Undefined" }, Custom=None, ToleranceTableLabel=None)
retval_1.SetAutoScaleToPrimaryPrescription(AutoScale=False)

plan_info = case.QueryPlanInfo(Filter = {'Name': 'FOURFIELD_HN'})
plan = case.LoadPlan(PlanInfo = plan_info[0])


beam_set = get_current("BeamSet")

#find the isocentre
sub_structure_set = beam_set.DependentSubStructureSet
stv_center = sub_structure_set.RoiStructures['STV_TOTAL'].GetCenterOfRoi()
iso_position = {'x':stv_center.x, 'y':stv_center.y, 'z':stv_center.z}
iso_data = beam_set.CreateDefaultIsocenterData(Position=iso_position)

#creatt the beam set 
beam_set.CreatePBSIonBeam(Name = "ANT", GantryAngle=0, CouchRotationAngle=0, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)
beam_set.CreatePBSIonBeam(Name = "POS", GantryAngle=180, CouchRotationAngle=0, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)
beam_set.CreatePBSIonBeam(Name = "LAO", GantryAngle=45, CouchRotationAngle=0, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)
beam_set.CreatePBSIonBeam(Name = "RAO", GantryAngle=315, CouchRotationAngle=0, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)

plan.PlanOptimizations[0].ResetOptimization()
plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template = TemplateTreatmentOptimization_fourfield, AssociatedRoisAndPois={'STR_RAO': "STV_RAO", 'STV_LAO': "STV_LAO", 'STV_POS': "STV_POS", 'STV_ANT': "STV_ANT", 'BODY': "BODY", 'OTVHIGH': "OTVHIGH", 'OTVLOW': "OTVLOW", 'BRAINSTEM': "BRAINSTEM", 'CORD': "CORD", 'PAROTIDL': "PAROTIDL", 'PAROTIDR': "PAROTIDR" })
plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

# if you want to keep it going:
plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

# compute the final dose 
beam_set.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="IonMonteCarlo", ForceRecompute=False, RunEntryValidation=True)

# calculate the final clinical goals 
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template = TemplateClinicalGoals, AssociatedRoisAndPois={ 'CTVHIGH': "PHYSTVHIGH", 'CTVLOW': "PHYSTVLOW", 'BRAINSTEM': "BRAINSTEM", 'CORD': "CORD", 'PAROTIDL': "PAROTIDL", 'PAROTIDR': "PAROTIDR" })

#plan.TreatmentCourse.GoalEvaluation()

for i in range(0,8):
    # Access the first clinical goal defined for the plan
    goal = plan.TreatmentCourse.EvaluationSetup.EvaluationFunctions[i]

    # Access the current value of the goal on the total plan dose
    # of the current plan
    value_plan = goal.GetClinicalGoalValue()

    print(value_plan)


# create plan number 2 

case = get_current("Case")
examination = get_current("Examination")
db = get_current("PatientDB")
TemplateTreatmentOptimization_star = db.LoadTemplateOptimizationFunctions(templateName = 'STAR_HN', lockMode = 'Read')

retval_0 = case.AddNewPlan(PlanName="STAR_HN", PlannedBy="POPPY_AUTO", Comment="", ExaminationName="CT 1", IsMedicalOncologyPlan=False, AllowDuplicateNames=False)
retval_1 = retval_0.AddNewBeamSet(Name="STAR_HN", ExaminationName="CT 1", MachineName="Gantry 1", Modality="Protons", TreatmentTechnique="ProtonPencilBeamScanning", PatientPosition="HeadFirstSupine", NumberOfFractions=30, CreateSetupBeams=False, UseLocalizationPointAsSetupIsocenter=False, UseUserSelectedIsocenterSetupIsocenter=False, Comment="", RbeModelName="Constant 1.1", EnableDynamicTrackingForVero=False, NewDoseSpecificationPointNames=[], NewDoseSpecificationPoints=[], MotionSynchronizationTechniqueSettings={ 'DisplayName': None, 'MotionSynchronizationSettings': None, 'RespiratoryIntervalTime': None, 'RespiratoryPhaseGatingDutyCycleTimePercentage': None, 'MotionSynchronizationTechniqueType': "Undefined" }, Custom=None, ToleranceTableLabel=None)
retval_1.SetAutoScaleToPrimaryPrescription(AutoScale=False)

plan_info = case.QueryPlanInfo(Filter = {'Name': 'STAR_HN'})
plan = case.LoadPlan(PlanInfo = plan_info[0])


beam_set = get_current("BeamSet")

#find the isocentre
sub_structure_set = beam_set.DependentSubStructureSet
stv_center = sub_structure_set.RoiStructures['STV_TOTAL'].GetCenterOfRoi()
iso_position = {'x':stv_center.x, 'y':stv_center.y, 'z':stv_center.z}
iso_data = beam_set.CreateDefaultIsocenterData(Position=iso_position)

#creatt the beam set 
beam_set.CreatePBSIonBeam(Name = "RPO", GantryAngle=260, CouchRotationAngle=30, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)
beam_set.CreatePBSIonBeam(Name = "LPO", GantryAngle=100, CouchRotationAngle=330, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)
beam_set.CreatePBSIonBeam(Name = "LAO", GantryAngle=25, CouchRotationAngle=0, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)
beam_set.CreatePBSIonBeam(Name = "RAO", GantryAngle=335, CouchRotationAngle=0, ArcRotationDirection="None", ArcStopGantryAngle=None, SnoutId="S1", SpotTuneId="4.0", RangeShifter=None, MinimumAirGap=40, MetersetRateSetting="", IsocenterData=iso_data, Description="",  CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)

plan.PlanOptimizations[0].ResetOptimization()
plan.PlanOptimizations[0].ApplyOptimizationTemplate(Template = TemplateTreatmentOptimization_star, AssociatedRoisAndPois={'STR_RAO': "STV_RAO", 'STV_LAO': "STV_LAO", 'STV_RPO': "STV_RPO", 'STV_LPO': "STV_LPO", 'BODY': "BODY", 'OTVHIGH': "OTVHIGH", 'OTVLOW': "OTVLOW", 'BRAINSTEM': "BRAINSTEM", 'CORD': "CORD", 'PAROTIDL': "PAROTIDL", 'PAROTIDR': "PAROTIDR" })
plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

# if you want to keep it going:
plan.PlanOptimizations[0].RunOptimization(ScalingOfSoftMachineConstraints=None)

# compute the final dose 
beam_set.ComputeDose(ComputeBeamDoses=True, DoseAlgorithm="IonMonteCarlo", ForceRecompute=False, RunEntryValidation=True)

# calculate the final clinical goals 
plan.TreatmentCourse.EvaluationSetup.ApplyClinicalGoalTemplate(Template = TemplateClinicalGoals, AssociatedRoisAndPois={ 'CTVHIGH': "PHYSTVHIGH", 'CTVLOW': "PHYSTVLOW", 'BRAINSTEM': "BRAINSTEM", 'CORD': "CORD", 'PAROTIDL': "PAROTIDL", 'PAROTIDR': "PAROTIDR" })

