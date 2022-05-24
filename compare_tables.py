import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_left = pd.DataFrame(data={
    'Col_1': [1,2,3,0,4,9,22], # Merging left_on.
    'Col_2': [5,6,7,4,5,0,31], 
    'Col_5': [0,2,3,0,-1,8,4]                             
    })

# print(df_left)
# print(f'df_left shape: {df_left.shape}')

df_right = pd.DataFrame(data={
    'Col_3': [1,2,10,4,8,9,22,0,24], # Merging right_on.
    'Col_4': [5,6,7,4,5,0,40,0,70],       
    })

# print(df_right)
# print(f'df_right shape: {df_right.shape}')


df_merge = pd.merge(df_left, df_right, how='inner', left_on=['Col_1'], right_on=['Col_3'])

# print(df_merge)
# print(f'df_merge shape: {df_merge.shape}')

excluded_dict = {'Excluded_Left': None, 'Excluded_Right': None, 'Row': None}

print("df_left checks:")

left_list = list(df_left['Col_1'])
merged_left = list(df_merge['Col_1'])

excluded_left_list = []
left_row_excluded_list = []
for i in left_list:
    if i in merged_left:
        print(f'{i} appears in the merged DataFrame.')
    else:
        print(f'{i} does not appear in the merged DataFrame.')
        excluded_left_list.append(i)
        left_row_excluded_list.append(left_list.index(i))

excluded_dict['Excluded_Left'] = excluded_left_list
excluded_dict['Row'] = left_row_excluded_list

print(excluded_dict)

print("\n")


print("df_right checks:")

right_list = list(df_right['Col_3'])
merged_right = list(df_merge['Col_3'])

excluded_right_list = []
right_row_excluded_list = []
for i in right_list:
    if i in merged_right:
        print(f'{i} appears in the merged DataFrame.')
    else:
        print(f'{i} does not appear in the merged DataFrame.')
        excluded_right_list.append(i)
        right_row_excluded_list.append(right_list.index(i))

excluded_dict['Excluded_Right'] = excluded_right_list
excluded_dict['Row']+= right_row_excluded_list

# Remove duplicates from excluded_dict['Row'].
excluded_dict['Row'] = sorted(list(set(excluded_dict['Row'])))
print(excluded_dict)


# Find the excluded rows.
df_excluded_rows_left = pd.DataFrame()
for i in excluded_dict['Excluded_Left']:
    df_temp = df_left.query(f'Col_1 == {i}').copy()
    df_temp['Table_Excluded'] = 'Left'
    # print(df_temp)
    df_excluded_rows_left = df_excluded_rows_left.append(df_temp)

print("Printing df_excluded_rows_left:")    
print(df_excluded_rows_left)

# print("\n")

df_excluded_rows_right = pd.DataFrame()
for i in excluded_dict['Excluded_Right']:
    df_temp = df_right.query(f'Col_3 == {i}').copy()
    df_temp['Table_Excluded'] = 'Right'
    df_excluded_rows_right = df_excluded_rows_right.append(df_temp)

print("Printing df_excluded_rows_right:")
print(df_excluded_rows_right)
    
print("\n")

# Creating a DataFrame from excluded_dict will require columns of same length.
print(excluded_dict)

len_left = len(excluded_dict['Excluded_Left'])
print(f'len_left is: {len_left}')

len_right = len(excluded_dict['Excluded_Right'])
print(f'len_right is: {len_right}')

if len_left - len_right == 0:
    pass
elif len_left - len_right < 0:
    excluded_dict['Excluded_Left'] += [np.nan]*abs(len_left - len_right)
elif len_left - len_right > 0:
    excluded_dict['Excluded_Right'] += [np.nan]*abs(len_left - len_right)

print(excluded_dict)


df_excluded = pd.DataFrame()
df_excluded = df_excluded.append(df_excluded_rows_left)
df_excluded = df_excluded.append(df_excluded_rows_right)
df_excluded['Row_Number'] = df_excluded.index
# print(df_excluded)
# print("\n")


df_excluded.set_index(keys=['Table_Excluded'], inplace=True)
print(df_left)
print(f'df_left shape is {df_left.shape}')
print("\n")

print(df_right)
print(f'df_right shape is {df_right.shape}')
print("\n")

print(df_merge)
print(f'df_merge shape is {df_merge.shape}')
print("\n")

print(df_excluded)
print(f'df_excluded shape is {df_excluded.shape}')
print("\n")

print("Rows number(s) excluded when merging df_left and df_right, with left_on=['Col_1'] and right_on=['Col_3']:")
for i in sorted(list(set(list(df_excluded['Row_Number'])))):
    print(i)

print("\n")
print(excluded_dict)
df_excluded_simple = pd.DataFrame(data=excluded_dict)
print("Printing df_excluded_simple:")
print(df_excluded_simple)

print("\n")

df_excluded_group = df_excluded[['Row_Number']].copy()
df_excluded_group.reset_index(inplace=True)
df_excluded_group.rename(columns={'Row_Number': 'Row_Count'}, inplace=True)
df_excluded_group = df_excluded_group.groupby(by=['Table_Excluded']).count()
df_excluded_group['Tables_Merged'] = df_excluded_group.index

print("Number of rows excluded by table:")
print(df_excluded_group)



# Plot the number of rows excluded by table.
plt.style.use('seaborn')
fig, ax = plt.subplots()
ax = df_excluded_group.plot.bar(x='Tables_Merged', y='Row_Count',
                                rot=0,
                                color=['orange', 'blue'],
                                title='Count of Rows Excluded',
                                legend=False)                          

# Set the gridlines.
ax.grid(visible=True, which='both', axis='both', color='black', alpha=0.2)

plt.savefig('count_excluded.png')
                                


