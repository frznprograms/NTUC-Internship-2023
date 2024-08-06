import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 

grant = pd.read_csv('grantwages.csv')

grant = grant[['Company Name', 'Application No.', 'Coy Size', 'Outcome', 'Outcome\n[Wage Increment]',\
  '% of Wage Increment', 'Outcome\n[CDP]', 'Actual Outcome\n[Wage Increment]', 'Actual Outcome\n[CDP]']]

grant.columns = ['Company Name', 'Application No.', 'Coy Size', 'Final Outcome', 'Workers impacted by Wage Increment',\
  '% Wage Increment', 'Workers impacted by CDP', 'Actual Wage Increment', 'Actual CDP']

# print(grant['Final Outcome'].value_counts())
# print(grant['Company Name'].value_counts())

grant['Application No.'] = grant['Application No.'].str.strip().astype(str) 
grant['% Wage Increment'] = grant['% Wage Increment'].str.split('-').str[0]
grant['% Wage Increment'] = grant['% Wage Increment'].str.replace('%', '').astype(float)

grant = grant[grant['% Wage Increment'].notna()]
grant = grant.drop_duplicates(subset = 'Company Name')

# print(grant['% Wage Increment'].dtype) it's float64

# ---------------------------------------------------------------------------------------------------------------

def mark_wages(file, col, start, end): 
    res = []
    for i in range(start, end + 1): 
        res.append((i, len(file[file[col] > i])))
    return pd.DataFrame(res, columns = ['% Wage Increase', 'Number of Companies'])

wage_changes = mark_wages(grant, '% Wage Increment', 1, 8)
# print(wage_changes)

wage_changes_x = list(wage_changes['% Wage Increase'])
wage_changes_y = list(wage_changes['Number of Companies'])


sns.relplot(data = wage_changes, x = '% Wage Increase', y = 'Number of Companies', kind = 'line', \
            markers = True, dashes = False).\
                set(title = 'Change in Number of Eligible Companies as Minimum Wage Increment changes')
plt.show()


# ---------------------------------------------------------------------------------------------------------------



palette = {'1st': "blue", '2nd': 'orange'}
filtered_to_wages = grant[grant['Final Outcome'] != 'CDP']
sns.relplot(y = 'Workers impacted by Wage Increment', x = '% Wage Increment', data = filtered_to_wages, \
            kind = 'scatter', hue = 'Application No.', palette = palette).set(title = \
            'Overview of Wage Increments and Number of Workers who benefitted')
plt.show()


first_timers = grant[(grant['Final Outcome'] != 'CDP') & (grant['Application No.'] == '1st')]
#print(first_timers)

# deeper dive into first-time applicants 
first_timers_sorted = first_timers.sort_values(by = 'Workers impacted by Wage Increment', ascending = False)
# print(first_timers_sorted.head(10))

min = min(first_timers['Workers impacted by Wage Increment'])
max = max(first_timers['Workers impacted by Wage Increment'])

def mark_beneficiaries(file, col, start, end): 
    res = []
    for i in range(start, end + 1): 
        count = len(file[file[col] > i])
        res.append((i, count))
    return pd.DataFrame(res, columns=['Workers that benefitted', 'Number of Companies'])

thresholds = mark_beneficiaries(first_timers, 'Workers impacted by Wage Increment', int(min), int(max))

sns.relplot(data=thresholds, x='Workers that benefitted', y='Number of Companies', kind='line', \
            markers=True, dashes=False).\
    set(title='Change in Number of Eligible Companies as Minimum Beneficiaries increases')
plt.show()



second_timers = grant[(grant['Final Outcome'] != 'CDP') & (grant['Application No.'] != '1st')]
# print(second_timers)


# ---------------------------------------------------------------------------------------------------------------


# start fresh because I want all the duplicates just in case the company did two separate projects 
just_cdp = pd.read_csv('grantwages.csv')

just_cdp = just_cdp[['Company Name', 'Application No.', 'Coy Size', 'Outcome', 'Outcome\n[Wage Increment]',\
  '% of Wage Increment', 'Outcome\n[CDP]', 'Actual Outcome\n[Wage Increment]', 'Actual Outcome\n[CDP]']]

just_cdp.columns = ['Company Name', 'Application No.', 'Coy Size', 'Final Outcome', 'Workers impacted by Wage Increment',\
  '% Wage Increment', 'Workers impacted by CDP', 'Actual Wage Increment', 'Actual CDP']

just_cdp['Application No.'] = just_cdp['Application No.'].str.strip().astype(str) 
just_cdp['% Wage Increment'] = just_cdp['% Wage Increment'].str.split('-').str[0]
just_cdp['% Wage Increment'] = just_cdp['% Wage Increment'].str.replace('%', '').astype(float)

just_cdp = just_cdp[just_cdp['Workers impacted by CDP'].notna()]
just_cdp = just_cdp[(just_cdp['Final Outcome'] == 'CDP') | (just_cdp['Final Outcome'] == 'Wage Increment & CDP')]
just_cdp = just_cdp[['Company Name', 'Application No.', 'Coy Size', 'Final Outcome', 'Workers impacted by CDP']]
just_cdp['Coy Size'] = just_cdp['Coy Size'].str.replace(',' , '')
just_cdp['Coy Size'] = just_cdp['Coy Size'].str.strip().astype(float)

# add the proportion column 
just_cdp['Proportion'] = just_cdp['Workers impacted by CDP'] / just_cdp['Coy Size']

sns.set_palette('Blues')
g = sns.catplot(data = just_cdp, x = 'Proportion', y = 'Company Name', kind = 'bar', hue = 'Application No.').set(\
    title = 'CDP Companies by Proportion of Workers they trained')
g.ax.set_xticks([i / 100 for i in range(0, 31, 3)])

plt.show()
