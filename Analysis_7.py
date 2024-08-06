import pandas as pd 

unionised_co = pd.read_excel('Unionised Companies.xlsx', header = 0)
#print(unionised_co)
lhub_list = pd.read_excel('LHub list.xlsx', header = 2)
lhub_list = lhub_list[['Company Name', 'UEN Number']]
lhub_list = lhub_list.dropna(subset = ['UEN Number'])
#print(len(lhub_list))


e2i_ccp = pd.read_excel('e2i CCP.xlsx')
e2i_ccp = e2i_ccp[['Company Name', 'UEN Number']].drop_duplicates(subset = 'UEN Number')
#print(len(e2i_ccp))


e2i_ct = pd.read_excel('e2i Career Trial.xlsx')
e2i_ct = e2i_ct.dropna(subset = 'Conversion Rate*')[['Company Name', 'UEN Number', 'Conversion Rate*']]
e2i_ct = e2i_ct.drop_duplicates(subset = 'UEN Number')
#print(e2i_ct) 
#print(len(e2i_ct))


unionised_co = unionised_co[['Name of Company', 'UEN Number']]
#print(unionised_co) 


compiled_list = lhub_list.merge(e2i_ccp, how = 'outer', on = 'UEN Number')
compiled_list = compiled_list.merge(e2i_ct, how = 'outer', on = 'UEN Number')
compiled_list['Company Name'] = compiled_list['Company Name_x'].combine_first(compiled_list['Company Name_y']).combine_first(compiled_list['Company Name'])
compiled_list.drop(columns=['Company Name_x', 'Company Name_y'], inplace=True)
compiled_list = compiled_list[['UEN Number', 'Company Name']].drop_duplicates(subset = 'UEN Number')
#print(compiled_list)
#print(len(compiled_list))


verified_co = compiled_list.merge(unionised_co, how = 'inner', on = 'UEN Number')
#print(verified_co)
 


''' ###### Double Checks ###### '''
verified_lhub = lhub_list.merge(unionised_co, how = 'inner', on = 'UEN Number')
#print(len(verified_lhub))

verified_e2i_ccp = e2i_ccp.merge(unionised_co, how = 'inner', on = 'UEN Number')
#print(len(verified_e2i_ccp))

verified_ct = e2i_ct.merge(unionised_co, how = 'inner', on = 'UEN Number')
#print(len(verified_ct))
