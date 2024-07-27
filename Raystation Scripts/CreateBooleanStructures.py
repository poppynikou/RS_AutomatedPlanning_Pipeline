# Script recorded 08 Apr 2024, 11:17:26

#   RayStation version: 14.0.100.0
#   Selected patient: ...

# Interpreter: CPython 3.8 (64-bit)
# Name: CreateStructures
# Comment: Post Process RTSTRUCT

from connect import *

# get patient

'''
patient_db = get_current("PatientDB")
patient_db.CreatePatient(LastName = '', FirstName = '', PatientID = '', BirthDate = '', Gender = '')
dicom_path = ''
patient.ImportDataFromPath(Path = dicom_path, CaseName  = 'Case 2', )

ui = get_current("ui")
ui.TabControl_ToolBar.ToolBarGroup.ToolBarGroup['PATIENT HANDLING'].Button_Open
'''


# import patients information 
case = get_current("Case")
examination = get_current("Examination")
patient_db = get_current("PatientDB")


def CreateROI(name, ROIType):
    ROI_object = case.PatientModel.CreateRoi(Name=name, Color="Pink", Type=ROIType, TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
    return ROI_object

def AlgebraROI(ROIObject, ROIAlgebra):
    
    with CompositeAction("'ROI algebra ('" + str(ROIAlgebra[2]['Expression_result']['Structure_Name']) + "')'"):
        ROIObject.SetAlgebraExpression(ExpressionA={ \
        'Operation': ROIAlgebra[0]['Expression_A']['Expression_type'], 'SourceRoiNames': ROIAlgebra[0]['Expression_A']['Structure_Name'], \
        'MarginSettings': { 'Type': ROIAlgebra[0]['Expression_A']['Margin_type'], 'Superior': ROIAlgebra[0]['Expression_A']['Margin_size'], 'Inferior': ROIAlgebra[0]['Expression_A']['Margin_size'], 'Anterior': ROIAlgebra[0]['Expression_A']['Margin_size'], 'Posterior': ROIAlgebra[0]['Expression_A']['Margin_size'], 'Right': ROIAlgebra[0]['Expression_A']['Margin_size'], 'Left': ROIAlgebra[0]['Expression_A']['Margin_size']} }, \
        ExpressionB={ 'Operation': ROIAlgebra[1]['Expression_B']['Expression_type'], 'SourceRoiNames': ROIAlgebra[1]['Expression_B']['Structure_Name'], \
        'MarginSettings': { 'Type': ROIAlgebra[1]['Expression_B']['Margin_type'], 'Superior': ROIAlgebra[1]['Expression_B']['Margin_size'], 'Inferior': ROIAlgebra[1]['Expression_B']['Margin_size'], 'Anterior': ROIAlgebra[1]['Expression_B']['Margin_size'], 'Posterior': ROIAlgebra[1]['Expression_B']['Margin_size'], 'Right': ROIAlgebra[1]['Expression_B']['Margin_size'], 'Left': ROIAlgebra[1]['Expression_B']['Margin_size']} }, \
        ResultOperation= ROIAlgebra[2]['Expression_result']['Expression_type'], \
        ResultMarginSettings={ 'Type': ROIAlgebra[2]['Expression_result']['Margin_type'], 'Superior': ROIAlgebra[2]['Expression_result']['Margin_size'], 'Inferior': ROIAlgebra[2]['Expression_result']['Margin_size'], 'Anterior': ROIAlgebra[2]['Expression_result']['Margin_size'], 'Posterior': ROIAlgebra[2]['Expression_result']['Margin_size'], 'Right': ROIAlgebra[2]['Expression_result']['Margin_size'], 'Left': ROIAlgebra[2]['Expression_result']['Margin_size']})
        ROIObject.UpdateDerivedGeometry(Examination=examination, Algorithm="Auto")

'''
ROIAlgebra = [ \
{'Expression_A': {'Expression_type': '', 'Structure_Name': '', 'Margin_type': '', 'Margin_size': ''}}, \
{'Expression_B': {'Expression_type': '', 'Structure_Name': '', 'Margin_type': '', 'Margin_size': ''}}, \
{'Expression_result': {'Expression_type': '', 'Structure_Name': '', 'Margin_type': '', 'Margin_size': ''}}]
'''    

## === Create correct CTVs === ## 

# create a croppped back CTV_lowdose to make sure it doesn't overlap with the CTV_highdose
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH'], 'Margin_type': 'Expand', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Subtraction', 'Structure_Name': 'CTVLOW_CROP_INTERMEDIATE', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# crop back from body 
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_CROP_INTERMEDIATE'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'PHYSTVLOW', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# crop back from body 
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'PHYSTVHIGH', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)


## === Create the OTVs === ## 
# expand CTV_highdose by 3mm
# make sure its cropped back from the body by 1mm 
# call it OTV_high
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['PHYSTVHIGH'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'OTVHIGH', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# expand CTV_lowdose by 3mm
# make sure its cropped back from the body by 1mm and 1mm from the CTV_highdose
# call it OTV_low
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['PHYSTVLOW'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'OTVLOW_INTERMEDIATE', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['OTVLOW_INTERMEDIATE'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['OTVHIGH'], 'Margin_type': 'Expand', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Subtraction', 'Structure_Name': 'OTVLOW', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)


## === Create the STVs === ## 

# creatve STV_ANT
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_ANT'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_ANT'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'STV_ANT', 'Margin_type': 'Expand', 'Margin_size': '0.3'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_POS
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_POS'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_POS'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'STV_POS', 'Margin_type': 'Expand', 'Margin_size': '0.3'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

#create STV_Total
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['STV_POS'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['STV_ANT'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'STV_TOTAL', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_LAO
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_LAO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_LAO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'STV_LAO', 'Margin_type': 'Expand', 'Margin_size': '0.3'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_LPO
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_LPO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_LPO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'STV_LPO', 'Margin_type': 'Expand', 'Margin_size': '0.3'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_RAO
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_RAO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_RAO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'STV_RAO', 'Margin_type': 'Expand', 'Margin_size': '0.3'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_RPO
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_RPO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_RPO'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'STV_RPO', 'Margin_type': 'Expand', 'Margin_size': '0.3'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)




# delete all the structures created which you don't need
case.PatientModel.RegionsOfInterest['CTVLOW_CROP_INTERMEDIATE'].DeleteRoi()
case.PatientModel.RegionsOfInterest['OTVLOW_INTERMEDIATE'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVHIGH'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVLOW'].DeleteRoi()

case.PatientModel.RegionsOfInterest['CTVHIGH_RAO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVHIGH_LAO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVHIGH_RPO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVHIGH_LPO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVHIGH_ANT'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVHIGH_POS'].DeleteRoi()

case.PatientModel.RegionsOfInterest['CTVLOW_RAO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVLOW_LAO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVLOW_RPO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVLOW_LPO'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVLOW_ANT'].DeleteRoi()
case.PatientModel.RegionsOfInterest['CTVLOW_POS'].DeleteRoi()

# assign all the structures to the appropriate types 
case.PatientModel.RegionsOfInterest['PHYSTVHIGH'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['PHYSTVLOW'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['OTVHIGH'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['OTVLOW'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STV_RAO'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STV_LAO'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STV_RPO'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STV_LPO'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STV_ANT'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STV_POS'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STV_TOTAL'].Type = "Ctv"

case.PatientModel.RegionsOfInterest['PHYSTVHIGH'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['PHYSTVLOW'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['OTVHIGH'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['OTVLOW'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STV_RAO'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STV_LAO'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STV_RPO'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STV_LPO'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STV_ANT'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STV_POS'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STV_TOTAL'].OrganData.OrganType = "Target"

case.PatientModel.RegionsOfInterest['BODY'].Type = "External"
case.PatientModel.RegionsOfInterest['BODY'].SetAsExternal()
case.PatientModel.RegionsOfInterest['BODY'].OrganData.OrganType = "OrganAtRisk"


case.PatientModel.RegionsOfInterest['BRAINSTEM'].Type = "Organ"
case.PatientModel.RegionsOfInterest['BRAINSTEM'].OrganData.OrganType = "OrganAtRisk"
case.PatientModel.RegionsOfInterest['CORD'].Type = "Organ"
case.PatientModel.RegionsOfInterest['CORD'].OrganData.OrganType = "OrganAtRisk"
case.PatientModel.RegionsOfInterest['PAROTIDL'].Type = "Organ"
case.PatientModel.RegionsOfInterest['PAROTIDL'].OrganData.OrganType = "OrganAtRisk"
case.PatientModel.RegionsOfInterest['PAROTIDR'].Type = "Organ"
case.PatientModel.RegionsOfInterest['PAROTIDR'].OrganData.OrganType = "OrganAtRisk"


# sets the couch material correctly 
Templates = patient_db.GetTemplateMaterials()
for i in Templates:
    if i.Material.Name == "Air":
        SelectedMaterial = i.Material

case.PatientModel.RegionsOfInterest['CouchSurface'].SetRoiMaterial(Material=SelectedMaterial)
case.PatientModel.RegionsOfInterest['CouchInterior'].SetRoiMaterial(Material=SelectedMaterial)
case.PatientModel.RegionsOfInterest['CouchRailLeft'].SetRoiMaterial(Material=SelectedMaterial)
case.PatientModel.RegionsOfInterest['CouchRailRight'].SetRoiMaterial(Material=SelectedMaterial)

case.PatientModel.RegionsOfInterest['CouchSurface'].Type = "Support"
case.PatientModel.RegionsOfInterest['CouchInterior'].Type = "Support"
case.PatientModel.RegionsOfInterest['CouchRailLeft'].Type = "Support"
case.PatientModel.RegionsOfInterest['CouchRailRight'].Type = "Support"
case.PatientModel.RegionsOfInterest['CouchSurface'].OrganData.OrganType = "Other"
case.PatientModel.RegionsOfInterest['CouchInterior'].OrganData.OrganType = "Other"
case.PatientModel.RegionsOfInterest['CouchRailLeft'].OrganData.OrganType = "Other"
case.PatientModel.RegionsOfInterest['CouchRailRight'].OrganData.OrganType = "Other"
