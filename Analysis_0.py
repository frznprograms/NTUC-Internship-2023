import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

''' ---- Changing Pathway to 1a, 1b and 1 ---- '''
ctc_training = pd.read_csv('CTC_training.csv')
ctc_grant = pd.read_csv('CTC_grant.csv')

shane = pd.read_csv('Whitelist_shane.csv')
shane = shane.drop_duplicates(subset = 'UEN Number')
print(shane.head())

uen = 'UEN Number'
conditions = [(shane[uen].isin(ctc_grant[uen])) & (shane[uen].isin(ctc_training[uen])), 
            shane[uen].isin(ctc_grant[uen]), 
            shane[uen].isin(ctc_training[uen])
]
categories = ['1', '1a', '1b']
shane['Pathway'] = np.select(conditions, categories, default = np.nan)

#print(shane)
#print(shane['Pathway'].value_counts())

def new_cat_col(file, categories, conditions, column, def_value): 
    try: 
        file[column] = np.select(conditions, categories, default = def_value)
        print(file.head())
        return file[column].value_counts() 
    except TypeError:
        print("Have you imported numpy and are you working on a pandas datframe?")
        return 'Check your file name and directory'


''' ---- Threshold Testing ---- '''   
#print(ctc_training.info())
#print(ctc_training.loc[:, 'coursehour'])
# different main levels can be 8, 16, 24

# filtering in pandas
condition = ctc_training['coursehour'] > 24
# print(len(ctc_training[condition]))

def num_companies(start, end, file, col):
    file = pd.read_csv(file)
    res = [] 
    for i in range(start, end + 1):
        res.append((i, len(file[file[col] == i])))
    return pd.DataFrame(res, columns = ['Hours trained', 'Number of Eligible Companies'])

test2 = num_companies(8, 40, 'CTC_training.csv', 'coursehour')
#print(test2)

w = list(test2['Hours trained'])
z = list(test2['Number of Eligible Companies'])

test2.plot(x = 'Hours trained', y = 'Number of Eligible Companies', kind = 'bar', rot = 90, 
           title = 'Number of Companies by Hours Trained')

plt.show()


def threshold_map(start, end, file, col): 
    file = pd.read_csv(file)
    res = []
    for i in range(start, end + 1): 
        res.append((i, len(file[file[col] > i])))
    return pd.DataFrame(res, columns = ['Threshold', "Number of companies"])

test = threshold_map(8, 40, 'CTC_training.csv', 'coursehour')
#print(test)


x = list(test['Threshold'])
y = list(test['Number of companies'])

plt.plot(x, y, 'bo-')
plt.xlabel('Threshold by Training Hours')
plt.ylabel('Number of Eligible Companies')
plt.title('Change in Eligible Companies as Threshold Shifts')

plt.text(9, 240, 'x = 9, 237')
plt.text(10, 190, 'x = 10, \ny = 208')
plt.text(15, 197, 'x = 15, y = 194')
plt.text(17, 134, 'x = 16, y = 131')
plt.text(21, 90, 'x = 23, \ny = 109')
plt.text(20, 67, 'x = 24, y = 67')
plt.text(31, 55, 'x = 31, y = 52')
plt.text(32, 34, 'x = 32, y = 31')

plt.show()


df = ctc_training[ctc_training['coursehour'] > 40]
