import numpy as np
import pandas as pd 

ctc_grant = pd.read_csv('CTC_grant.csv')
#print(ctc_grant) 

ctc_training = pd.read_csv('CTC_training.csv') 
#print(ctc_training.head())
#print(ctc_training['UEN Number'].value_counts())


''' Counting matches '''
ctc_training = ctc_training.drop_duplicates(subset = ['UEN Number', 'CompanyName'])
#print(len(ctc_training['UEN Number'].value_counts()))

ctc_grant["Match"] = ctc_grant["UEN Number"].isin(ctc_training["UEN Number"])
#print(ctc_grant)
#print(ctc_grant['Match'].value_counts())

''' ---- Function to determine if the CTC grant and CTC training lists overlap ---- '''
def match_or_not(file1, file2, col_name): 
    try: 
        data1 = pd.read_csv(file1)
        data2 = pd.read_csv(file2)
    
        data1['Match'] = data1[col_name].isin(data2[col_name])
        print(data1)

        return data1['Match'].value_counts()
    
    except TypeError: 
        return "File not found, check that the file name and directory is correct"

#print(match_or_not('CTC_grant.csv', 'CTC_training.csv', "UEN Number"))

''' ---- Function to set pathway for list of CTC training companies ---- '''
def set_pathway(file, reference): 
    file = pd.read_csv(file) 
    ref = pd.read_csv(reference)

    file['Pathway'] = np.where(file['UEN Number'].isin(ref['UEN Number']), '1a', '1b')
    print(file.head())

    return file 

#print(set_pathway('CTC_training.csv', 'CTC_grant.csv'))

''' ---- Verifying Grand Totals and Breakdown ---- '''
cass = pd.read_csv("Whitelisted.csv")
shane = pd.read_csv("Whitelist_shane.csv")
shane = set_pathway('Whitelist_shane.csv', 'CTC_grant.csv')
shane = shane.drop_duplicates(subset = ['UEN Number'])
# compiled list 
#print(shane)

# pathway breakdown 
#print(shane['Pathway'].value_counts())

''' ---- Changing Pathway to 1a, 1b and 1 ---- '''
ctc_training = pd.read_csv('CTC_training.csv')
ctc_grant = pd.read_csv('CTC_grant.csv')

shane = pd.read_csv('Whitelist_shane.csv')
shane = shane.drop_duplicates(subset = 'UEN Number')
#print(shane.head())

uen = 'UEN Number'
conditions = [(shane[uen].isin(ctc_grant[uen])) & (shane[uen].isin(ctc_training[uen])), 
            shane[uen].isin(ctc_grant[uen]), 
            shane[uen].isin(ctc_training[uen])
]
categories = ['1', '1a', '1b']
shane['Pathway'] = np.select(conditions, categories, default = np.nan)
shane.sort_values('Pathway', ascending = False)

#print(shane[shane['Pathway'] == '1'])
