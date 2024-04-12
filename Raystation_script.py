# Script recorded 08 Apr 2024, 11:17:26

#   RayStation version: 14.0.100.0
#   Selected patient: ...

# Interpreter: CPython 3.8 (64-bit)
# Name: CreateStructures
# Comment: Sort out planning structures 

from connect import *

'''
need to work out how to get the case you want
not just the current 
'''

case = get_current("Case")
examination = get_current("Examination")

'''
find couch structures somehow
'''
# this is hard coded, and need to option of defining air 
# I have emailed Josh about this 
with CompositeAction('Apply ROI changes (CouchSurface)'):
  case.PatientModel.RegionsOfInterest['CouchSurface'].SetRoiMaterial(Material=case.PatientModel.Materials[4])

with CompositeAction('Apply ROI changes (CouchInterior)'):
  case.PatientModel.RegionsOfInterest['CouchInterior'].SetRoiMaterial(Material=case.PatientModel.Materials[4])

with CompositeAction('Apply ROI changes (CouchRailLeft)'):
  case.PatientModel.RegionsOfInterest['CouchRailLeft'].SetRoiMaterial(Material=case.PatientModel.Materials[4])

with CompositeAction('Apply ROI changes (CouchRailRight)'):
  case.PatientModel.RegionsOfInterest['CouchRailRight'].SetRoiMaterial(Material=case.PatientModel.Materials[4])

'''
check if there exists a high dose CTV structure, and what it's called
'''

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

# check if CTV54 exists and create CTV_low
# check if CTV65 exists and create CTV_high
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV54'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': [], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'None', 'Structure_Name': 'CTV_lowdose_base', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV 65 combined'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': [], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'None', 'Structure_Name': 'CTV_highdose', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv") 
AlgebraROI(ROIObject, ROIAlgebra)

# create a croppped back CTV_lowdose to make sure it doesnt overlap with the CTV_highdose
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV_lowdose_base'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['CTV_highdose'], 'Margin_type': 'Expand', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Subtraction', 'Structure_Name': 'CTV_lowdose', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
with CompositeAction("'Delete ROIs ('" + str(ROIAlgebra[0]['Expression_A']['Structure_Name'][0]) + "')'"):
  case.PatientModel.RegionsOfInterest[str(ROIAlgebra[0]['Expression_A']['Structure_Name'][0])].DeleteRoi()

## === Create the OTVs === ## 


# expand CTV_highdose by 3mm
# make sure its cropped back from the body by 1mm 
# call it OTV_high
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV_highdose'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'OTV_high', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

# expand CTV_lowdose by 3mm
# make sure its cropped back from the body by 1mm and 1mm from the CTV_highdose
# call it OTV_low
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV_lowdose'], 'Margin_type': 'Expand', 'Margin_size': '0.3'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['BODY'], 'Margin_type': 'Contract', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Intersection', 'Structure_Name': 'OTV_low_intermediate', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)

ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['OTV_low_intermediate'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': ['OTV_high'], 'Margin_type': 'Expand', 'Margin_size': '0.1'}}, \
{'Expression_result':{ 'Expression_type': 'Subtraction', 'Structure_Name': 'OTV_low', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI(ROIAlgebra[2]['Expression_result']['Structure_Name'], "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)
#with CompositeAction("'Delete ROIs ('" + str(ROIAlgebra[0]['Expression_A']['Structure_Name'][0]) + "')'"):
#  case.PatientModel.RegionsOfInterest[str(ROIAlgebra[0]['Expression_A']['Structure_Name'][0])].DeleteRoi()

## === Create the STVs === ## 

