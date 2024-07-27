import pandas as pd
import os
import numpy as np 

path_to_csv = os.getcwd() +  '/RSAnalysis/RSPlan1.csv'

results = pd.read_csv(path_to_csv, header = 0)

Patients = np.unique(results['Patient'].tolist())
UCLH_Patients = ['UCLH_HN_10', 'UCLH_HN_11', 'UCLH_HN_12', 'UCLH_HN_13', 'UCLH_HN_18', 'UCLH_HN_19' , 'UCLH_HN_5']
GSTT_Patients = ['GSTT_HN_1','GSTT_HN_10','GSTT_HN_15', 'GSTT_HN_22','GSTT_HN_5','GSTT_HN_7','GSTT_HN_8']
No_Patients = len(Patients)
No_UCLH_Patients = len(UCLH_Patients)
No_GSTT_Patients = len(GSTT_Patients)
Structures = np.unique(results['Structure'].tolist())
No_Structures = len(Structures)
CTV_Stuctures = Structures[4:8]
No_CTV_Stuctures = 4
No_Serial_OARs = 2
No_Parallel_OARs = 2
# calculate for both GSTT and UCLH patients together
# and then seperate

# Nominal re-calc stats 
#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------
# FOUR FIELD PLAN ALL 
print('---Four field Plan ALL ---')

# calc % of patients with four field plan which adhered to all nominal criteria  
# for all structures
total = 0
for patient in Patients:
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Nominal_Pass_Rate'].tolist()) == No_Structures:
        total = total +1 
print('% Passed of all Patients: ' + str(np.round(total/No_Patients * 100, 2))+ '%')



# calc % of patients with four field plan which adhered to all nominal criteria  
# for the ctvs
total = 0
CTV_HIGH_D99 = []
CTV_HIGH_D95 = []
CTV_LOW_D99 = []
CTV_LOW_D95 = []
for patient in Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][4:8]['Nominal_Pass_Rate'].tolist()) == No_CTV_Stuctures:
        total = total +1 

    else:
        Difference = 5850- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[4]
        CTV_HIGH_D99.append(np.abs(Difference)/100)
        Difference = 6180 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[5]
        CTV_HIGH_D95.append(np.abs(Difference)/100)
        Difference = 4860 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[6]
        CTV_LOW_D99.append(np.abs(Difference)/100)
        Difference = 5130 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[7]
        CTV_LOW_D95.append(np.abs(Difference)/100)

print('% Passed of CTVs: ' + str(np.round(total/No_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
print('CTV High D99 Failure: ' + str(np.round(np.mean(CTV_HIGH_D99),2)) + ' +/- ' + str(np.round(np.std(CTV_HIGH_D99))))
print('CTV High D95 Failure: ' + str(np.round(np.mean(CTV_HIGH_D95),2)) + ' +/- ' + str(np.round(np.std(CTV_HIGH_D95))))
print('CTV Low D99 Failure: ' + str(np.round(np.mean(CTV_LOW_D99),2)) + ' +/- ' + str(np.round(np.std(CTV_LOW_D99))))
print('CTV Low D95 Failure: ' + str(np.round(np.mean(CTV_LOW_D95),2)) + ' +/- ' + str(np.round(np.std(CTV_LOW_D95))))


# calc % of patients with four field plan which adhered to all nominal criteria  
# for the serial oars
total = 0
BRAINSTEM = []
CORD = []
for patient in Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][0:2]['Nominal_Pass_Rate'].tolist()) == No_Serial_OARs:
        total = total +1 

    else:
        Difference = 5400- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[0]
        BRAINSTEM.append(np.abs(Difference)/100)
        Difference = 4800 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[1]
        CORD.append(np.abs(Difference)/100)

print('% Passed of Serial OARS: ' + str(np.round(total/No_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
if len(BRAINSTEM) != 0:
    print('Brainstem Failure: ' + str(np.round(np.mean(BRAINSTEM),2)) + ' +/- ' + str(np.round(np.std(BRAINSTEM),2)))
if len(CORD) !=0:
    print('Cord Failure: ' + str(np.round(np.mean(CORD),2)) + ' +/- ' + str(np.round(np.std(CORD),2)))

# calc % of patients with four field plan which adhered to all nominal criteria  
# for the parallel oars
total = 0
PAROTIDL = []
PAROTIDR = []
for patient in Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][2:4]['Nominal_Pass_Rate'].tolist()) == No_Parallel_OARs:
        total = total +1 

    else:
        Difference = 2400- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[2]
        PAROTIDL.append(np.abs(Difference)/100)
        Difference = 2400 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[3]
        PAROTIDR.append(np.abs(Difference)/100)

print('% Passed of Parallel OARS: ' + str(np.round(total/No_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
# of the ones which did not pass, how many Gy did they not pass by?
if len(PAROTIDL) != 0:
    print('Parotid L Failure: ' + str(np.round(np.mean(PAROTIDL),2)) + ' +/- ' + str(np.round(np.std(PAROTIDL),2)))
if len(PAROTIDR) !=0:
    print('Parotid R Failure: ' + str(np.round(np.mean(PAROTIDR),2)) + ' +/- ' + str(np.round(np.std(PAROTIDR),2)))


#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------
# FOUR FIELD PLAN GSTT  
print('---Four field Plan GSTT ---')

# calc % of patients with four field plan which adhered to all nominal criteria  
# for all structures
total = 0
for patient in GSTT_Patients:
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Nominal_Pass_Rate'].tolist()) == No_Structures:
        total = total +1 
print('% Passed of GSTT Patients: ' + str(np.round(total/No_GSTT_Patients * 100, 2))+ '%')



# calc % of patients with four field plan which adhered to all nominal criteria  
# for the ctvs
total = 0
CTV_HIGH_D99 = []
CTV_HIGH_D95 = []
CTV_LOW_D99 = []
CTV_LOW_D95 = []
for patient in GSTT_Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][4:8]['Nominal_Pass_Rate'].tolist()) == No_CTV_Stuctures:
        total = total +1 

    else:
        Difference = 5850- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[4]
        CTV_HIGH_D99.append(np.abs(Difference)/100)
        Difference = 6180 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[5]
        CTV_HIGH_D95.append(np.abs(Difference)/100)
        Difference = 4860 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[6]
        CTV_LOW_D99.append(np.abs(Difference)/100)
        Difference = 5130 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[7]
        CTV_LOW_D95.append(np.abs(Difference)/100)

print('% Passed of CTVs: ' + str(np.round(total/No_GSTT_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
if len(CTV_HIGH_D99) != 0:
    print('CTV High D99 Failure: ' + str(np.round(np.mean(CTV_HIGH_D99),2)) + ' +/- ' + str(np.round(np.std(CTV_HIGH_D99))))
if len(CTV_HIGH_D95) != 0:
    print('CTV High D95 Failure: ' + str(np.round(np.mean(CTV_HIGH_D95),2)) + ' +/- ' + str(np.round(np.std(CTV_HIGH_D95))))
if len(CTV_LOW_D99) != 0:
    print('CTV Low D99 Failure: ' + str(np.round(np.mean(CTV_LOW_D99),2)) + ' +/- ' + str(np.round(np.std(CTV_LOW_D99))))
if len(CTV_LOW_D95) != 0:
    print('CTV Low D95 Failure: ' + str(np.round(np.mean(CTV_LOW_D95),2)) + ' +/- ' + str(np.round(np.std(CTV_LOW_D95))))


# calc % of patients with four field plan which adhered to all nominal criteria  
# for the serial oars
total = 0
BRAINSTEM = []
CORD = []
for patient in GSTT_Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][0:2]['Nominal_Pass_Rate'].tolist()) == No_Serial_OARs:
        total = total +1 

    else:
        Difference = 5400- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[0]
        BRAINSTEM.append(np.abs(Difference)/100)
        Difference = 4800 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[1]
        CORD.append(np.abs(Difference)/100)

print('% Passed of Serial OARS: ' + str(np.round(total/No_GSTT_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
if len(BRAINSTEM) != 0:
    print('Brainstem Failure: ' + str(np.round(np.mean(BRAINSTEM),2)) + ' +/- ' + str(np.round(np.std(BRAINSTEM),2)))
if len(CORD) !=0:
    print('Cord Failure: ' + str(np.round(np.mean(CORD),2)) + ' +/- ' + str(np.round(np.std(CORD),2)))

# calc % of patients with four field plan which adhered to all nominal criteria  
# for the parallel oars
total = 0
PAROTIDL = []
PAROTIDR = []
for patient in GSTT_Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][2:4]['Nominal_Pass_Rate'].tolist()) == No_Parallel_OARs:
        total = total +1 

    else:
        Difference = 2400- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[2]
        PAROTIDL.append(np.abs(Difference)/100)
        Difference = 2400 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[3]
        PAROTIDR.append(np.abs(Difference)/100)

print('% Passed of Parallel OARS: ' + str(np.round(total/No_GSTT_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
# of the ones which did not pass, how many Gy did they not pass by?
if len(PAROTIDL) != 0:
    print('Parotid L Failure: ' + str(np.round(np.mean(PAROTIDL),2)) + ' +/- ' + str(np.round(np.std(PAROTIDL),2)))
if len(PAROTIDR) !=0:
    print('Parotid R Failure: ' + str(np.round(np.mean(PAROTIDR),2)) + ' +/- ' + str(np.round(np.std(PAROTIDR),2)))




#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------
# FOUR FIELD PLAN UCLH  
print('---Four field Plan UCLH ---')

# calc % of patients with four field plan which adhered to all nominal criteria  
# for all structures
total = 0
for patient in UCLH_Patients:
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Nominal_Pass_Rate'].tolist()) == No_Structures:
        total = total +1 
print('% Passed of UCLH Patients: ' + str(np.round(total/No_UCLH_Patients * 100, 2))+ '%')



# calc % of patients with four field plan which adhered to all nominal criteria  
# for the ctvs
total = 0
CTV_HIGH_D99 = []
CTV_HIGH_D95 = []
CTV_LOW_D99 = []
CTV_LOW_D95 = []

for patient in UCLH_Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][4:8]['Nominal_Pass_Rate'].tolist()) == No_CTV_Stuctures:
        total = total +1 

    else:
        
        Difference = 5850- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[4]
        CTV_HIGH_D99.append(np.abs(Difference)/100)
        Difference = 6180 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[5]
        CTV_HIGH_D95.append(np.abs(Difference)/100)
        Difference = 4860 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[6]
        CTV_LOW_D99.append(np.abs(Difference)/100)
        Difference = 5130 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[7]
        CTV_LOW_D95.append(np.abs(Difference)/100)

print('% Passed of CTVs: ' + str(np.round(total/No_UCLH_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
if len(CTV_HIGH_D99) !=0:
    print('CTV High D99 Failure: ' + str(np.round(np.mean(CTV_HIGH_D99),2)) + ' +/- ' + str(np.round(np.std(CTV_HIGH_D99))))
if len(CTV_HIGH_D95) !=0:
    print('CTV High D95 Failure: ' + str(np.round(np.mean(CTV_HIGH_D95),2)) + ' +/- ' + str(np.round(np.std(CTV_HIGH_D95))))
if len(CTV_LOW_D99) !=0:
    print('CTV Low D99 Failure: ' + str(np.round(np.mean(CTV_LOW_D99),2)) + ' +/- ' + str(np.round(np.std(CTV_LOW_D99))))
if len(CTV_LOW_D95) !=0:
    print('CTV Low D95 Failure: ' + str(np.round(np.mean(CTV_LOW_D95),2)) + ' +/- ' + str(np.round(np.std(CTV_LOW_D95))))


# calc % of patients with four field plan which adhered to all nominal criteria  
# for the serial oars
total = 0
BRAINSTEM = []
CORD = []
for patient in UCLH_Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][0:2]['Nominal_Pass_Rate'].tolist()) == No_Serial_OARs:
        total = total +1 

    else:
        Difference = 5400- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[0]
        BRAINSTEM.append(np.abs(Difference)/100)
        Difference = 4800 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[1]
        CORD.append(np.abs(Difference)/100)

print('% Passed of Serial OARS: ' + str(np.round(total/No_UCLH_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
if len(BRAINSTEM) != 0:
    print('Brainstem Failure: ' + str(np.round(np.mean(BRAINSTEM),2)) + ' +/- ' + str(np.round(np.std(BRAINSTEM),2)))
if len(CORD) !=0:
    print('Cord Failure: ' + str(np.round(np.mean(CORD),2)) + ' +/- ' + str(np.round(np.std(CORD),2)))

# calc % of patients with four field plan which adhered to all nominal criteria  
# for the parallel oars
total = 0
PAROTIDL = []
PAROTIDR = []
for patient in UCLH_Patients:
    
    if np.sum(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) ][2:4]['Nominal_Pass_Rate'].tolist()) == No_Parallel_OARs:
        total = total +1 

    else:
        Difference = 2400- results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[2]
        PAROTIDL.append(np.abs(Difference)/100)
        Difference = 2400 - results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient))]['Dose_Nominal'].tolist()[3]
        PAROTIDR.append(np.abs(Difference)/100)

print('% Passed of Parallel OARS: ' + str(np.round(total/No_UCLH_Patients * 100, 2))+ '%')

# of the ones which did not pass, how many Gy did they not pass by?
# of the ones which did not pass, how many Gy did they not pass by?
if len(PAROTIDL) != 0:
    print('Parotid L Failure: ' + str(np.round(np.mean(PAROTIDL),2)) + ' +/- ' + str(np.round(np.std(PAROTIDL),2)))
if len(PAROTIDR) !=0:
    print('Parotid R Failure: ' + str(np.round(np.mean(PAROTIDR),2)) + ' +/- ' + str(np.round(np.std(PAROTIDR),2)))








# Robustness re-calc stats 
#---------------------

# calc % of patients with Star plan which adhered to all robustness criteria  
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
print('---Robustness Four Field Plan ALL ---')
Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in Patients:
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()) == No_Structures:
        Robustness100 = Robustness100 +1 
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()) == No_Structures:
        Robustness95 = Robustness95 +1 
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()) == No_Structures:
        Robustness90 = Robustness90 +1 

print('100% Robustness Passed of all Patients: ' + str(np.round(Robustness100/No_Patients * 100, 2))+ '%')
print('95% Robustness Passed of all Patients: ' + str(np.round(Robustness95/No_Patients * 100, 2))+ '%')
print('90% Robustness Passed of all Patients: ' + str(np.round(Robustness90/No_Patients * 100, 2))+ '%')



# calc % of patients with Star plan which adhered to all robustness criteria for CTVs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range

Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness90 = Robustness90 + 1 

print('100% Robustness CTV High Passed of all Patients: ' + str(np.round(Robustness100/No_Patients * 100, 2))+ '%')
print('95% Robustness CTV High Passed of all Patients: ' + str(np.round(Robustness95/No_Patients * 100, 2))+ '%')
print('90% Robustness CTV High Passed of all Patients: ' + str(np.round(Robustness90/No_Patients * 100, 2))+ '%')


Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness90 = Robustness90 + 1 

print('100% Robustness CTV Low Passed of all Patients: ' + str(np.round(Robustness100/No_Patients * 100, 2))+ '%')
print('95% Robustness CTV Low Passed of all Patients: ' + str(np.round(Robustness95/No_Patients * 100, 2))+ '%')
print('90% Robustness CTV Low Passed of all Patients: ' + str(np.round(Robustness90/No_Patients * 100, 2))+ '%')


Difference_CTVHIGHD99 = []
Difference_CTVHIGHD95 = []
Difference_CTVLOWD99 = []
Difference_CTVLOW95 = []
for patient in Patients:
    
    WorstCase_CTVHIGHD99 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_HIGH_D99') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVHIGHD99) != 0:
        Difference_CTVHIGHD99.append(np.absolute(5850 - WorstCase_CTVHIGHD99[0])/100)
    WorstCase_CTVHIGHD95 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_HIGH_D95') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVHIGHD95) != 0:
        Difference_CTVHIGHD95.append(np.absolute(6180 - WorstCase_CTVHIGHD95[0])/100)
    WorstCase_CTVLOWD99 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_LOW_D99') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVLOWD99) != 0:
        Difference_CTVLOWD99.append(np.absolute(6180 - WorstCase_CTVLOWD99[0])/100)
    WorstCase_CTVLOWD95 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_LOW_D95') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVLOWD95) != 0:
        Difference_CTVLOW95.append(np.absolute(6180 - WorstCase_CTVLOWD95[0])/100)


if not len(Difference_CTVHIGHD99) ==0:
    print('CTV High D99 Worst Case All Patients: ' + str(np.round(np.mean(Difference_CTVHIGHD99),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVHIGHD99),2)))
if not len(Difference_CTVHIGHD95) ==0:
    print('CTV High D95 Worst Case All Patients: ' + str(np.round(np.mean(Difference_CTVHIGHD95),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVHIGHD95),2)))
if not len(Difference_CTVLOWD99) ==0:
    print('CTV Low D99 Worst Case All Patients: ' + str(np.round(np.mean(Difference_CTVLOWD99),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVLOWD99),2)))
if not len(Difference_CTVLOW95) ==0:
    print('CTV Low D95 Worst Case All Patients: ' + str(np.round(np.mean(Difference_CTVLOW95),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVLOW95),2)))



# calc % of patients with Star plan which adhered to all robustness criteria for serial OARs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range


Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness90 = Robustness90 + 1 

print('100% Robustness Serial OARs Passed of all Patients: ' + str(np.round(Robustness100/No_Patients * 100, 2))+ '%')
print('95% Robustness Serial OARs Passed of all Patients: ' + str(np.round(Robustness95/No_Patients * 100, 2))+ '%')
print('90% Robustness Serial OARs Passed of all Patients: ' + str(np.round(Robustness90/No_Patients * 100, 2))+ '%')

Difference_BS = []
Difference_SC = []
for patient in Patients:
    
    WorstCase_BS = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'BRAINSTEM') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_BS) != 0:
        Difference_BS.append(np.absolute(5400 - WorstCase_BS[0])/100) 
    WorstCase_SC = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CORD') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_SC) != 0:
        Difference_SC.append(np.absolute(4800 - WorstCase_SC[0])/100)

if not len(Difference_BS) ==0:
    print('Brainstem Worst Case All Patients: ' + str(np.round(np.mean(Difference_BS),2)) + ' +/- ' + str(np.round(np.std(Difference_BS),2)))
if not len(Difference_SC) ==0:
    print('Spinal Cord Worst Case All Patients: ' + str(np.round(np.mean(Difference_SC),2)) + ' +/- ' + str(np.round(np.std(Difference_SC),2)))



# calc % of patients with Star plan which adhered to all robustness criteria for parallel OARs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range


Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness90 = Robustness90 + 1 

print('100% Robustness Parallel OARs Passed of all Patients: ' + str(np.round(Robustness100/No_Patients * 100, 2))+ '%')
print('95% Robustness Parallel OARs Passed of all Patients: ' + str(np.round(Robustness95/No_Patients * 100, 2))+ '%')
print('90% Robustness Parallel OARs Passed of all Patients: ' + str(np.round(Robustness90/No_Patients * 100, 2))+ '%')

Difference_PAROTIDR = []
Difference_PAROTIDL = []

for patient in Patients:

    WorstCase_PAROTIDR = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'PAROTIDR') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_PAROTIDR) != 0:
        Difference_PAROTIDR.append(np.absolute(2400 - WorstCase_PAROTIDR[0])/100)
    WorstCase_PAROTIDL = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'PAROTIDL') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_PAROTIDL) != 0:
        Difference_PAROTIDL.append(np.absolute(2400 - WorstCase_PAROTIDL[0])/100)

if not len(Difference_PAROTIDR) ==0:
    print('PAROTIDR Worst Case All Patients: ' + str(np.round(np.mean(Difference_PAROTIDR),2)) + ' +/- ' + str(np.round(np.std(Difference_PAROTIDR),2)))
if not len(Difference_PAROTIDL) ==0:
    print('PAROTIDL Worst Case All Patients: ' + str(np.round(np.mean(Difference_PAROTIDL),2)) + ' +/- ' + str(np.round(np.std(Difference_PAROTIDL),2)))





# calc % of patients with Star plan which adhered to all robustness criteria  
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
print('---Robustness Four Field Plan GSTT ---')
Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in GSTT_Patients:
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()) == No_Structures:
        Robustness100 = Robustness100 +1 
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()) == No_Structures:
        Robustness95 = Robustness95 +1 
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()) == No_Structures:
        Robustness90 = Robustness90 +1 

print('100% Robustness Passed of GSTT Patients: ' + str(np.round(Robustness100/No_GSTT_Patients * 100, 2))+ '%')
print('95% Robustness Passed of GSTT Patients: ' + str(np.round(Robustness95/No_GSTT_Patients * 100, 2))+ '%')
print('90% Robustness Passed of GSTT Patients: ' + str(np.round(Robustness90/No_GSTT_Patients * 100, 2))+ '%')



# calc % of patients with Star plan which adhered to all robustness criteria for CTVs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range

Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in GSTT_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness90 = Robustness90 + 1 

print('100% Robustness CTV High Passed of GSTT Patients: ' + str(np.round(Robustness100/No_GSTT_Patients * 100, 2))+ '%')
print('95% Robustness CTV High Passed of GSTT Patients: ' + str(np.round(Robustness95/No_GSTT_Patients * 100, 2))+ '%')
print('90% Robustness CTV High Passed of GSTT Patients: ' + str(np.round(Robustness90/No_GSTT_Patients * 100, 2))+ '%')



Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in GSTT_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness90 = Robustness90 + 1 

print('100% Robustness CTV Low Passed of GSTT Patients: ' + str(np.round(Robustness100/No_GSTT_Patients * 100, 2))+ '%')
print('95% Robustness CTV Low Passed of GSTT Patients: ' + str(np.round(Robustness95/No_GSTT_Patients * 100, 2))+ '%')
print('90% Robustness CTV Low Passed of GSTT Patients: ' + str(np.round(Robustness90/No_GSTT_Patients * 100, 2))+ '%')


Difference_CTVHIGHD99 = []
Difference_CTVHIGHD95 = []
WorstCase_CTVLOWD99 = []
WorstCase_CTVLOWD95 = []

for patient in GSTT_Patients:
    
    WorstCase_CTVHIGHD99 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_HIGH_D99') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVHIGHD99) !=0:
        Difference_CTVHIGHD99.append(np.absolute(5850 - WorstCase_CTVHIGHD99[0])/100)
    WorstCase_CTVHIGHD95 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_HIGH_D95') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVHIGHD95) != 0:
        Difference_CTVHIGHD95.append(np.absolute(6180 - WorstCase_CTVHIGHD95[0])/100)
    WorstCase_CTVLOWD99 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_LOW_D99') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVLOWD99) !=0:
        Difference_CTVLOWD99.append(np.absolute(4860 - WorstCase_CTVLOWD99[0])/100)
    WorstCase_CTVLOWD95 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_LOW_D95') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVLOWD95) != 0:
        Difference_CTVLOW95.append(np.absolute(5130 - WorstCase_CTVLOWD95[0])/100)

if not len(Difference_CTVHIGHD99) ==0:
    print('CTV High D99 Worst Case of GSTT Patients: ' + str(np.round(np.mean(Difference_CTVHIGHD99),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVHIGHD99),2)))
if not len(Difference_CTVHIGHD95) ==0:
    print('CTV High D95 Worst Case of GSTT Patients: ' + str(np.round(np.mean(Difference_CTVHIGHD95),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVHIGHD95),2)))
if not len(Difference_CTVLOWD99) ==0:
    print('CTV Low D99 Worst Caseof GSTT Patients: ' + str(np.round(np.mean(Difference_CTVLOWD99),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVLOWD99),2)))
if not len(Difference_CTVLOW95) ==0:
    print('CTV Low D95 Worst Case of GSTT Patients:' + str(np.round(np.mean(Difference_CTVLOW95),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVLOW95),2)))

# calc % of patients with Star plan which adhered to all robustness criteria for serial OARs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range


Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in GSTT_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness90 = Robustness90 + 1 

print('100% Robustness Serial OARs Passed of GSTT Patients: ' + str(np.round(Robustness100/No_GSTT_Patients * 100, 2))+ '%')
print('95% Robustness Serial OARs Passed of GSTT Patients: ' + str(np.round(Robustness95/No_GSTT_Patients * 100, 2))+ '%')
print('90% Robustness Serial OARs Passed of GSTT Patients: ' + str(np.round(Robustness90/No_GSTT_Patients * 100, 2))+ '%')




Difference_BS = []
Difference_SC = []
for patient in GSTT_Patients:
    
    WorstCase_BS = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'BRAINSTEM') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_BS) !=0:
        Difference_BS.append(np.absolute(5400 - WorstCase_BS[0])/100)
    WorstCase_SC = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CORD') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_SC) !=0:
        Difference_SC.append(np.absolute(4800 - WorstCase_SC[0])/100)

if not len(Difference_BS) ==0:
    print('Brainstem Worst Case All Patients: ' + str(np.round(np.mean(Difference_BS),2)) + ' +/- ' + str(np.round(np.std(Difference_BS),2)))
if not len(Difference_SC) ==0:
    print('Spinal Cord Worst Case All Patients: ' + str(np.round(np.mean(Difference_SC),2)) + ' +/- ' + str(np.round(np.std(Difference_SC),2)))





# calc % of patients with Star plan which adhered to all robustness criteria for parallel OARs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range


Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in GSTT_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness90 = Robustness90 + 1 

print('100% Robustness Parallel OARs Passed of GSTT Patients: ' + str(np.round(Robustness100/No_GSTT_Patients * 100, 2) )+ '%')
print('95% Robustness Parallel OARs Passed of GSTT Patients: ' + str(np.round(Robustness95/No_GSTT_Patients * 100, 2))+ '%')
print('90% Robustness Parallel OARs Passed of GSTT Patients: ' + str(np.round(Robustness90/No_GSTT_Patients * 100, 2))+ '%')

Difference_PAROTIDR = []
Difference_PAROTIDL = []

for patient in GSTT_Patients:
    WorstCase_PAROTIDR = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'PAROTIDR') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_PAROTIDR) !=0:
        Difference_PAROTIDR.append(np.absolute(2400 - WorstCase_PAROTIDR[0])/100)
    WorstCase_PAROTIDL = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'PAROTIDL') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_PAROTIDL) !=0:
        Difference_PAROTIDL.append(np.absolute(2400 - WorstCase_PAROTIDL[0])/100)

if not len(Difference_PAROTIDR) ==0:
    print('PAROTIDR Worst Case All Patients: ' + str(np.round(np.mean(Difference_PAROTIDR),2)) + ' +/- ' + str(np.round(np.std(Difference_PAROTIDR),2)))
if not len(WorstCase_PAROTIDL) ==0:
    print('PAROTIDL Worst Case All Patients: ' + str(np.round(np.mean(Difference_PAROTIDL),2)) + ' +/- ' + str(np.round(np.std(Difference_PAROTIDL),2)))





# calc % of patients with Star plan which adhered to all robustness criteria  
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
print('---Robustness Four Field Plan UCLH ---')
Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in UCLH_Patients:
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()) == No_Structures:
        Robustness100 = Robustness100 +1 
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()) == No_Structures:
        Robustness95 = Robustness95 +1 
    if len(results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()) == No_Structures:
        Robustness90 = Robustness90 +1 

print('100% Robustness Passed of GSTT Patients: ' + str(np.round(Robustness100/No_UCLH_Patients * 100, 2))+ '%')
print('95% Robustness Passed of GSTT Patients: ' + str(np.round(Robustness95/No_UCLH_Patients * 100, 2))+ '%')
print('90% Robustness Passed of GSTT Patients: ' + str(np.round(Robustness90/No_UCLH_Patients * 100, 2))+ '%')



# calc % of patients with Star plan which adhered to all robustness criteria for CTVs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range

Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in UCLH_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:8] == 'CTV_HIGH']
    if len(CTV_Pass_Structures) == 2:
        Robustness90 = Robustness90 + 1 

print('100% Robustness CTV High Passed of GSTT Patients: ' + str(np.round(Robustness100/No_UCLH_Patients * 100, 2))+ '%')
print('95% Robustness CTV High Passed of GSTT Patients: ' + str(np.round(Robustness95/No_UCLH_Patients * 100, 2))+ '%')
print('90% Robustness CTV High Passed of GSTT Patients: ' + str(np.round(Robustness90/No_UCLH_Patients * 100, 2))+ '%')



Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in UCLH_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    CTV_Pass_Structures = [structure for structure in Pass_structures if structure[0:7] == 'CTV_LOW']
    if len(CTV_Pass_Structures) == 2:
        Robustness90 = Robustness90 + 1 

print('100% Robustness CTV Low Passed of GSTT Patients: ' + str(np.round(Robustness100/No_UCLH_Patients * 100, 2))+ '%')
print('95% Robustness CTV Low Passed of GSTT Patients: ' + str(np.round(Robustness95/No_UCLH_Patients * 100, 2))+ '%')
print('90% Robustness CTV Low Passed of GSTT Patients: ' + str(np.round(Robustness90/No_UCLH_Patients * 100, 2))+ '%')


Difference_CTVHIGHD99 = []
Difference_CTVHIGHD95 = []
WorstCase_CTVLOWD99 = []
WorstCase_CTVLOWD95 = []

for patient in UCLH_Patients:
    
    WorstCase_CTVHIGHD99 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_HIGH_D99') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVHIGHD99) !=0:
        Difference_CTVHIGHD99.append(np.absolute(5850 - WorstCase_CTVHIGHD99[0])/100)
    WorstCase_CTVHIGHD95 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_HIGH_D95') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVHIGHD95) != 0:
        Difference_CTVHIGHD95.append(np.absolute(6180 - WorstCase_CTVHIGHD95[0])/100)
    WorstCase_CTVLOWD99 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_LOW_D99') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVLOWD99) !=0:
        Difference_CTVLOWD99.append(np.absolute(4860 - WorstCase_CTVLOWD99[0])/100)
    WorstCase_CTVLOWD95 = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CTV_LOW_D95') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_CTVLOWD95) != 0:
        Difference_CTVLOW95.append(np.absolute(5130 - WorstCase_CTVLOWD95[0])/100)

if not len(Difference_CTVHIGHD99) ==0:
    print('CTV High D99 Worst Case of GSTT Patients: ' + str(np.round(np.mean(Difference_CTVHIGHD99),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVHIGHD99),2)))
if not len(Difference_CTVHIGHD95) ==0:
    print('CTV High D95 Worst Case of GSTT Patients: ' + str(np.round(np.mean(Difference_CTVHIGHD95),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVHIGHD95),2)))
if not len(Difference_CTVLOWD99) ==0:
    print('CTV Low D99 Worst Caseof GSTT Patients: ' + str(np.round(np.mean(Difference_CTVLOWD99),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVLOWD99),2)))
if not len(Difference_CTVLOW95) ==0:
    print('CTV Low D95 Worst Case of GSTT Patients:' + str(np.round(np.mean(Difference_CTVLOW95),2)) + ' +/- ' + str(np.round(np.std(Difference_CTVLOW95),2)))

# calc % of patients with Star plan which adhered to all robustness criteria for serial OARs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range


Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in UCLH_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    SerialOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['BRAINSTEM', 'CORD']]
    if len(SerialOAR_Pass_Structures) == No_Serial_OARs:
        Robustness90 = Robustness90 + 1 

print('100% Robustness Serial OARs Passed of GSTT Patients: ' + str(np.round(Robustness100/No_UCLH_Patients * 100, 2))+ '%')
print('95% Robustness Serial OARs Passed of GSTT Patients: ' + str(np.round(Robustness95/No_UCLH_Patients * 100, 2))+ '%')
print('90% Robustness Serial OARs Passed of GSTT Patients: ' + str(np.round(Robustness90/No_UCLH_Patients * 100, 2))+ '%')




Difference_BS = []
Difference_SC = []
for patient in UCLH_Patients:
    
    WorstCase_BS = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'BRAINSTEM') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_BS) !=0:
        Difference_BS.append(np.absolute(5400 - WorstCase_BS[0])/100)
    WorstCase_SC = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'CORD') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_SC) !=0:
        Difference_SC.append(np.absolute(4800 - WorstCase_SC[0])/100)

if not len(Difference_BS) ==0:
    print('Brainstem Worst Case All Patients: ' + str(np.round(np.mean(Difference_BS),2)) + ' +/- ' + str(np.round(np.std(Difference_BS),2)))
if not len(Difference_SC) ==0:
    print('Spinal Cord Worst Case All Patients: ' + str(np.round(np.mean(Difference_SC),2)) + ' +/- ' + str(np.round(np.std(Difference_SC),2)))





# calc % of patients with Star plan which adhered to all robustness criteria for parallel OARs
# calc % of patients with Star plan which adhered to robustness criteria at > 95% 
# calc % of patients with Star plan which adhered to robustness criteria at > 90%
# calc difference in dose between target and worst case scenario, report in Gy mean and range


Robustness100 = 0
Robustness95 = 0
Robustness90 = 0
for patient in UCLH_Patients:
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] == 100)]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness100 = Robustness100 + 1
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(95))]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness95 = Robustness95 + 1 
    Pass_structures = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Robustness_Pass_Rate'] > int(90))]['Structure'].tolist()
    ParallelOAR_Pass_Structures = [structure for structure in Pass_structures if structure in ['PAROTIDR', 'PAROTIDL']]
    if len(ParallelOAR_Pass_Structures) == No_Parallel_OARs:
        Robustness90 = Robustness90 + 1 

print('100% Robustness Parallel OARs Passed of GSTT Patients: ' + str(np.round(Robustness100/No_UCLH_Patients * 100, 2) )+ '%')
print('95% Robustness Parallel OARs Passed of GSTT Patients: ' + str(np.round(Robustness95/No_UCLH_Patients * 100, 2))+ '%')
print('90% Robustness Parallel OARs Passed of GSTT Patients: ' + str(np.round(Robustness90/No_UCLH_Patients * 100, 2))+ '%')

Difference_PAROTIDR = []
Difference_PAROTIDL = []

for patient in UCLH_Patients:
    WorstCase_PAROTIDR = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'PAROTIDR') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_PAROTIDR) !=0:
        Difference_PAROTIDR.append(np.absolute(2400 - WorstCase_PAROTIDR[0])/100)
    WorstCase_PAROTIDL = results.loc[(results['Plan'] == 'FOUR_FIELD') & (results['Patient'] == str(patient)) & (results['Structure'] == 'PAROTIDL') & (results['Robustness_Pass_Rate'] != 100)]['Worst_Case_Scenario'].tolist()
    if len(WorstCase_PAROTIDL) !=0:
        Difference_PAROTIDL.append(np.absolute(2400 - WorstCase_PAROTIDL[0])/100)

if not len(Difference_PAROTIDR) ==0:
    print('PAROTIDR Worst Case All Patients: ' + str(np.round(np.mean(Difference_PAROTIDR),2)) + ' +/- ' + str(np.round(np.std(Difference_PAROTIDR),2)))
if not len(WorstCase_PAROTIDL) ==0:
    print('PAROTIDL Worst Case All Patients: ' + str(np.round(np.mean(Difference_PAROTIDL),2)) + ' +/- ' + str(np.round(np.std(Difference_PAROTIDL),2)))



