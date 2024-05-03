# Script recorded 08 Apr 2024, 11:17:26

#   RayStation version: 14.0.100.0
#   Selected patient: ...

# Interpreter: CPython 3.8 (64-bit)
# Name: CreateStructures
# Comment: Post Process RTSTRUCT

from connect import *

'''
need to work out how to get the case you want
not just the current 
'''

case = get_current("Case")
examination = get_current("Examination")


# sets the couch material correctly 


patient_db = get_current("PatientDB")
Templates = patient_db.GetTemplateMaterials()

for i in Templates:
    if i.Material.Name == "Adipose":
        SelectedMaterial = i.Material

case.PatientModel.RegionsOfInterest['CouchSurface'].SetRoiMaterial(Material=SelectedMaterial)
case.PatientModel.RegionsOfInterest['CouchInterior'].SetRoiMaterial(Material=SelectedMaterial)
case.PatientModel.RegionsOfInterest['CouchRailLeft'].SetRoiMaterial(Material=SelectedMaterial)
case.PatientModel.RegionsOfInterest['CouchRailRight'].SetRoiMaterial(Material=SelectedMaterial)



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



# create a croppped back CTV_lowdose to make sure it doesnt overlap with the CTV_highdose
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH'], 'Margin_type': 'Expand', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Subtraction', 'Structure_Name': 'CTVLOW_CROP_INTERMEDIATE', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_CROP_INTERMEDIATE'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'CTVLOW_OPT', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
with CompositeAction('Delete ROIs (CTVLOW_CROP_INTERMEDIATE)'):
  case.PatientModel.RegionsOfInterest['CTVLOW_CROP_INTERMEDIATE'].DeleteRoi()

## === Create the OTVs === ## 


# expand CTV_highdose by 3mm
# make sure its cropped back from the body by 1mm 
# call it OTV_high
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'OTVHIGH', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)


# expand CTV_lowdose by 3mm
# make sure its cropped back from the body by 1mm and 1mm from the CTV_highdose
# call it OTV_low
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_OPT'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'OTVLOW_INTERMEDIATE', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['OTVLOW_INTERMEDIATE'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['OTVHIGH'], 'Margin_type': 'Expand', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Subtraction', 'Structure_Name': 'OTVLOW', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
with CompositeAction('Delete ROIs (OTVLOW_INTERMEDIATE)'):
  case.PatientModel.RegionsOfInterest['OTVLOW_INTERMEDIATE'].DeleteRoi()


## === Create the STVs === ## 

# creatve CTV_ant
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_ANT'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_ANT'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'CTV_ANT', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)


# creatve STV_ant
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV_ANT'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result': {'Expression_type': 'Intersection', 'Structure_Name': 'STV_ANT', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
with CompositeAction('Delete ROIs (CTV_ANT)'):
  case.PatientModel.RegionsOfInterest['CTV_ANT'].DeleteRoi()

# creatve CTV_pos
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_POS'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_POS'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'CTV_POS', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_pos
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV_POS'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result': {'Expression_type': 'Intersection', 'Structure_Name': 'STV_POS', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
with CompositeAction('Delete ROIs (CTV_POS)'):
  case.PatientModel.RegionsOfInterest['CTV_POS'].DeleteRoi()

# creatve CTV_left
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_L'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_L'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'CTV_LEFT', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_left
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV_LEFT'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result': {'Expression_type': 'Intersection', 'Structure_Name': 'STV_L', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
with CompositeAction('Delete ROIs (CTV_LEFT)'):
  case.PatientModel.RegionsOfInterest['CTV_LEFT'].DeleteRoi()

# creatve CTV_right
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTVLOW_R'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTVHIGH_R'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'Union', 'Structure_Name': 'CTV_R', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# creatve STV_right
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV_R'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result': {'Expression_type': 'Intersection', 'Structure_Name': 'STV_R', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
with CompositeAction('Delete ROIs (CTV_R)'):
  case.PatientModel.RegionsOfInterest['CTV_R'].DeleteRoi()



case.PatientModel.RegionsOfInterest['CTVHIGH'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVHIGH_R'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVHIGH_L'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVHIGH_ANT'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVHIGH_POS'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVLOW'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVLOW_OPT'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVLOW_R'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVLOW_L'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVHIGH_ANT'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVLOW_ANT'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['CTVLOW_POS'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['OTVHIGH'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['OTVLOW'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STVHIGH'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STVHIGH_R'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STVHIGH_L'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STVHIGH_ANT'].Type = "Ctv"
case.PatientModel.RegionsOfInterest['STVHIGH_POS'].Type = "Ctv"

case.PatientModel.RegionsOfInterest['CTVHIGH'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVHIGH_R'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVHIGH_L'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVHIGH_ANT'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVHIGH_POS'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVLOW'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVLOW_OPT'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVLOW_R'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVLOW_L'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVHIGH_ANT'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVLOW_ANT'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['CTVLOW_POS'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['OTVHIGH'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['OTVLOW'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STVHIGH'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STVHIGH_R'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STVHIGH_L'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STVHIGH_ANT'].OrganData.OrganType = "Target"
case.PatientModel.RegionsOfInterest['STVHIGH_POS'].OrganData.OrganType = "Target"


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