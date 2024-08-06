import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt  


ctc_training = pd.read_csv('CTC_training.csv', encoding = 'latin-1', low_memory = False)
full_list = pd.read_csv('212k_magic.csv', encoding = 'latin-1', low_memory = False)
#print(ctc_training.head())

# companies filtered by whether they did any training in 2023 
full_list.fillna(0)
filtered_to_2023 = full_list[full_list['BatchStartDate'].str.contains('2023', na = False)]
print(filtered_to_2023.columns)

rs = 'residentialstatus'
conditions = [(filtered_to_2023[rs] == 'SC') , filtered_to_2023[rs] == 'PR', (filtered_to_2023[rs] != 'SC') & (filtered_to_2023[rs] != 'PR') ]
categories = ['Local', 'Local', 'Others']
filtered_to_2023[rs] = np.select(conditions, categories, default = np.nan)

locals_only = filtered_to_2023[filtered_to_2023['residentialstatus'] == 'Local']
locals_only = locals_only[['UEN Number', 'CompanyName', 'traineeunid', 'residentialstatus', 'coursehour']]
#print(locals_only)

by_hours = locals_only[locals_only['coursehour'] >= 48]
#print(by_hours.groupby('CompanyName')['traineeunid'].value_counts().reset_index())

# by_hours_grouped = by_hours.groupby('CompanyName')['traineeunid'].value_counts().reset_index()
#print(len(by_hours_grouped.drop_duplicates(subset = 'CompanyName')))

def mark_threshold(data, col, start, end): 
    res = [] 
    for i in range(start, end + 1): 
        data1 = data[data[col] >= i].drop_duplicates(subset = 'CompanyName')
        res.append((i, len(data1)))
    return pd.DataFrame(res, columns = ['Threshold', 'Number of Companies'])

df_hours = mark_threshold(locals_only, 'coursehour', 8, 48)
#print(df_hours)
hours_x = list(df_hours['Threshold'])
hours_y = list(df_hours['Number of Companies'])

plt.plot(hours_x, hours_y, 'co-')
plt.title('Change in number of Eligible Companies as Min Training Hours changes')
plt.xlabel('Minimum Training Hours')
plt.ylabel('Number of Eligible Companies')
plt.show()

########################################################################################################

# isolate all the company UENs 
uens = filtered_to_2023['UEN Number'].value_counts()
#print(uens)

def get_locals(uens):
    res = []
    for uen in uens.index:
        working_file = filtered_to_2023[filtered_to_2023['UEN Number'] == uen]
        count = (working_file['residentialstatus'] == 'Local').sum()
        res.append(count)
    return res  

locals = get_locals(uens) 
# adding new column to the new dataframe 
new_df = pd.DataFrame(uens).reset_index()
new_df.columns = ['UEN Number', 'Grand_Total']
new_df['Locals'] = pd.Series(locals)
#print(new_df)

# adding the proportion 
new_df['Prop'] = new_df['Locals'] / new_df['Grand_Total']
#print(new_df)

#random numbers from 0 to 1, 50 even intervals 
seq = np.linspace(0, 1.1, num = 50)
#print(type(seq))

def mark_threshold(file, col, sequence): 
    res = []
    for i in sequence: 
        res.append((i, len(file[file[col] > i])))
    return pd.DataFrame(res, columns = ['Threshold', "Number of Companies"])

#print(mark_threshold(new_df, 'Prop', seq).iloc[0:23, :])
res_df = mark_threshold(new_df, 'Prop', seq).iloc[0:44, :]
#print(res_df)
x_values = list(res_df['Threshold'])
y_values = list(res_df['Number of Companies'])

plt.plot(x_values, y_values, 'co-')
plt.title('Change in number of Eligible Companies as Min Local Workforce Ratio changes')
plt.xlabel('Minimum Local Workforce Ratio')
plt.ylabel('Number of Eligible Companies')
plt.show()

prophours = locals_only.merge(new_df, on = 'UEN Number', how = 'left')
#print(prophours)
seq = [round(elem, 2) for elem in list(np.linspace(0.5, 1, num = 10)) ]
#print(seq)
seq2 = list(range(8, 56, 8))

def threshold_scatter(seq, seq2): 
    res = [] 
    for flo in seq: 
        for num in seq2: 
            res.append(((flo, num), len(prophours[(prophours['Prop'] > flo) \
                                                   & (prophours['coursehour'] > num)].drop_duplicates(\
                                                        subset = 'CompanyName'))))
    return pd.DataFrame(res, columns = ['Thresholds', 'Number of companies'])

hourpropdf = threshold_scatter(seq, seq2)
#print(hourpropdf)
x = [str(t) for t in hourpropdf['Thresholds']]
y = list(hourpropdf['Number of companies'])


plt.scatter(x, y, s = 40, alpha = 0.5, data = hourpropdf)
plt.xticks(rotation = 90)
plt.xlabel('Threshold Boundaries as (Proportion of Locals, Course Hours)')
plt.ylabel('Number of Companies')
plt.title('Change in number of Eligible Companies as Threshold Changes')
for i, txt in enumerate(y):
    plt.annotate(txt, (x[i], y[i]))

plt.show() 
