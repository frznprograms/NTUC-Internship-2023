import pandas as pd 
import numpy as np 

''' ---- Changing Pathway to 1a, 1b and 1 ---- '''
ctc_training = pd.read_csv('CTC_training.csv')
ctc_grant = pd.read_csv('CTC_grant.csv')

shane = pd.read_csv('Whitelist_shane.csv')
shane = shane.drop_duplicates(subset = 'UEN Number')


uen = 'UEN Number'
conditions = [(shane[uen].isin(ctc_grant[uen])) & (shane[uen].isin(ctc_training[uen])), 
            shane[uen].isin(ctc_grant[uen]), 
            shane[uen].isin(ctc_training[uen])
]
categories = ['1', '1a', '1b']
shane['Pathway'] = np.select(conditions, categories, default = np.nan)
shane.sort_values('Pathway', ascending = False)

shane = shane[shane['Pathway'] == '1']

magic = pd.read_csv('212k_magic.csv', encoding = 'latin-1', low_memory = False)
magic = magic.drop_duplicates(subset = 'UEN Number')

olderworkers = shane.merge(magic, how = 'inner', on = 'UEN Number')
olderworkers = olderworkers[['UEN Number', 'Company Name', 'Union Cluster', 'Union']]
olderworkers['Trained with LHub/e2i'] = 'Yes'
olderworkers['Trained Older Workers'] = np.nan
#print(olderworkers.head())


olderworkers.to_excel("/Users/shaneryan_1/Documents/NTUC/NTUC Pathway 1 Analysis/older_workers.xlsx", \
                         sheet_name='older workers', index=False)


reset_magic = pd.read_csv('212k_magic.csv', encoding = 'latin-1', low_memory = False)
reset_magic = reset_magic.drop_duplicates(subset = 'traineeunid')

by_trainees = reset_magic.merge(shane[['UEN Number']], how = 'inner', on = 'UEN Number')
by_trainees = by_trainees[['UEN Number', 'CompanyName', 'Union Cluster', 'Union', 'traineeunid']]

by_company = by_trainees.groupby(['UEN Number', 'CompanyName', 'Union Cluster', 'Union'])['traineeunid'].value_counts()
by_company = pd.DataFrame(by_company)
by_company.rename(columns = {'count' : 'Count'}, inplace = True)

table = pd.pivot_table(by_company, values=['Count'], index=['UEN Number', 'CompanyName', 'Union Cluster', 'Union'], aggfunc='cumsum')
#print(table)


table.to_excel("/Users/shaneryan_1/Documents/NTUC/NTUC Pathway 1 Analysis/by_company.xlsx", \
                         sheet_name='by company')
