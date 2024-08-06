import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt  


ctc_training = pd.read_csv('CTC_training.csv', encoding = 'latin-1', low_memory = False)
full_list = pd.read_csv('212k_magic.csv', encoding = 'latin-1', low_memory = False)
#print(ctc_training.head())

# companies filtered by whether they did any training in 2023 
full_list.fillna(0)
filtered_to_2023 = full_list[full_list['BatchStartDate'].str.contains('2023', na = False)]
# print(filtered_to_2023['CompanyName'].value_counts())

rs = 'residentialstatus'
conditions = [(filtered_to_2023[rs] == 'SC') , filtered_to_2023[rs] == 'PR', (filtered_to_2023[rs] != 'SC') & (filtered_to_2023[rs] != 'PR') ]
categories = ['Local', 'Local', 'Others']
filtered_to_2023[rs] = np.select(conditions, categories, default = np.nan)

by_coursehours = filtered_to_2023[['UEN Number', 'CompanyName', rs, 'coursehour']]
#print(by_coursehours)

# remove all the duplicates and just look at the companies themselves 
by_coursehours = by_coursehours.drop_duplicates(subset = ['UEN Number', 'CompanyName', 'coursehour'])
#print(by_coursehours)


ctc_reduced = ctc_training[['UEN Number', 'CompanyName']]
ctc_reduced.drop_duplicates(subset = 'UEN Number')
ctc_reduced['Overlap'] = ctc_reduced['UEN Number'].isin(by_coursehours['UEN Number'])
#print(ctc_reduced['Overlap'].value_counts()) 


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

workers_and_coursehours = new_df.merge(by_coursehours, on = 'UEN Number')
workers_and_coursehours = workers_and_coursehours.drop(['residentialstatus', 'CompanyName'], axis = 1)
#print(workers_and_coursehours)


seq = [round(elem, 2) for elem in list(np.linspace(0.5, 1, num = 10)) ]
#print(seq)
seq2 = list(range(8, 56, 8))

# making scatter plot to see if there can be a relationship 
def threshold_scatter(seq, seq2): 
    res = [] 
    for flo in seq: 
        for num in seq2: 
            res.append(((flo, num), len(workers_and_coursehours[(workers_and_coursehours['Prop'] > flo) \
                                                   & (workers_and_coursehours['coursehour'] > num)])))
    return pd.DataFrame(res, columns = ['Thresholds', 'Number of companies'])

hourpropdf = threshold_scatter(seq, seq2)
hourpropdf = hourpropdf.iloc[0: 54, :]
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
