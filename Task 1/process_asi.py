#!/usr/bin/env python
# coding: utf-8

# # Task 1: Data Consolidation and Transformation

# In[227]:


import pandas as pd


# In[263]:


file_path = 'Table_1_Annual_Series_For_Principal_Characteristics_2019_2020.xlsx'
df = pd.read_excel(file_path, engine='openpyxl')


# In[264]:


df


# In[265]:


#Here, I'm looking for the 'CHARACTERISTICS' value in the 1st column
characteristics_indices = [i for i, x in enumerate(df['Unnamed: 0']) if x == 'CHARACTERISTICS']


# In[266]:


#divide main df into multiple dfs
for i in range(len(characteristics_indices)):
    start_row = characteristics_indices[i]
    if i < len(characteristics_indices) - 1:
        end_row = characteristics_indices[i + 1]
    else:
        end_row = len(df)
    table_name = f'table_{i+1}'
    table_dict[table_name] = df.iloc[start_row:end_row]


# In[267]:


#dropping top 2 rows
for key in table_dict.keys():
    table_dict[key] = table_dict[key].rename(columns=table_dict[key].iloc[0]).drop(table_dict[key].index[0:2])


# In[276]:


#All tables have 'PROFITS' values in the last column, so we are dropping rows that come after that
for key in table_dict.keys():
    # Convert 'CHARACTERISTICS' column to string type
    table_dict[key]['CHARACTERISTICS'] = table_dict[key]['CHARACTERISTICS'].astype(str)
    
    mask = table_dict[key]['CHARACTERISTICS'].str.contains('PROFITS')
    if any(mask):
        table_dict[key] = table_dict[key].loc[:mask.idxmax()]


# In[269]:


#Drop the column where the entire column is null
    table_dict[key] = table_dict[key].dropna(axis=1, how='all')


# In[270]:


#reshape the dataframe as we want only three columns
for key in table_dict.keys():
    table_dict[key] = pd.melt(table_dict[key], id_vars=['CHARACTERISTICS'], var_name='year', value_name='value')


# In[275]:


for key in table_dict.keys():
    print(table_dict[key])


# In[272]:


combined_df = pd.concat(list(table_dict.values()), ignore_index=True)


# In[274]:


combined_df.to_csv('Table_1_Annual_Series_For_Principal_Characteristics_2019_2020.csv',index=False)


# In[ ]:




