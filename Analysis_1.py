import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt  


ctc_training = pd.read_csv('CTC_training.csv', encoding = 'latin-1', low_memory = False)
#print(ctc_training.head(10))

full_list = pd.read_csv('212k_magic.csv', encoding = 'latin-1', low_memory = False)
#print(full_list.columns)

full_list.fillna(0)
filtered_to_2023 = full_list[full_list['BatchStartDate'].str.contains('2023', na = False)]
# print(filtered_to_2023['CompanyName'].value_counts())
# USE THIS AS THE BASE DATASET  

# replace all sc and pr values as local, the rest fall under others 
rs = 'residentialstatus'
conditions = [(filtered_to_2023[rs] == 'SC') , filtered_to_2023[rs] == 'PR', (filtered_to_2023[rs] != 'SC') & (filtered_to_2023[rs] != 'PR') ]
categories = ['Local', 'Local', 'Others']
filtered_to_2023[rs] = np.select(conditions, categories, default = np.nan)
#print(filtered_to_2023[['UEN Number', 'CompanyName', rs, 'coursehour']])


by_coursehours = filtered_to_2023[['UEN Number', 'CompanyName', rs, 'coursehour']]

# remove all the duplicates and just look at the companies themselves 
by_coursehours = by_coursehours.drop_duplicates(subset = ['UEN Number', 'CompanyName', 'coursehour'])
#print(by_coursehours)



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
print(new_df)

# adding the proportion of locals to the total number of people trained 
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

def mark_threshold_hours(file, col, start, end): 
    res = []
    for i in range(start, end + 1): 
        res.append((i, len(file[file[col] > i])))
    return pd.DataFrame(res, columns = ['Threshold', "Number of companies"])

coursehour_df = mark_threshold_hours(by_coursehours, 'coursehour', 8, 40)
#print(coursehour_df)
hours_x = list(coursehour_df['Threshold'])
hours_y = list(coursehour_df['Number of companies'])



# Plotting a figure with multiple axes 
fig = plt.figure() 
fig.add_subplot(111)
ax1 = fig.add_subplot(111, label = 'Line 1', frame_on = False)    
ax2 = fig.add_subplot(111, label = 'Line 2', frame_on = False)
#ax3 = fig.add_subplot(111, label = 'Line 3', frame_on = False)

ax1.plot(x_values, y_values, 'bo-', color = 'C0')
ax1.set_xlabel("Threshold by Locals Trained", color="C0")
ax1.set_ylabel("Number of Companies", color="C0")
ax1.xaxis.set_ticks(np.linspace(0, 1, num = 10))
ax1.tick_params(axis='x', colors="C0")
ax1.tick_params(axis='y', colors="C0")

ax2.plot(hours_x, hours_y, 'ro-', color="C1")
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('Threshold by Hours Trained', color="C1") 
ax2.set_ylabel('Number of Companies', color="C1")       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors="C1")
ax2.tick_params(axis='y', colors="C1")


plt.show()


print(filtered_to_2023.groupby('CompanyName')['coursetitle'].value_counts())



''' -------- Annex --------'''
# full list of all programmes featured in the long list 
#print(full_list['coursetitle'].value_counts())
