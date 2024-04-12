

from connect import *

case = get_current("Case")
examination = get_current("Examination")



def CreateROI(name, ROIType):
    ROIObject = case.PatientModel.CreateRoi(Name=name, Color="Pink", Type=ROIType, TissueName=None, RbeCellTypeName=None, RoiMaterial=None)
    return ROIObject

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




# check if CTV54 exists and create CTV_low
# check if CTV65 exists and create CTV_high
ROIAlgebra = [{'Expression_A': {'Expression_type': 'Union', 'Structure_Name': ['CTV54'], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_B': {'Expression_type': 'Union', 'Structure_Name': [], 'Margin_type': 'Expand', 'Margin_size': '0'}}, \
{'Expression_result': {'Expression_type': 'None', 'Structure_Name': 'CTV_lowdose_base', 'Margin_type': 'Expand', 'Margin_size': '0'}}]
ROIObject = CreateROI("CTV_lowdose_base", "Ptv")
AlgebraROI(ROIObject, ROIAlgebra)


