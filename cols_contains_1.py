
import pandas as pd

df_contains = pd.read_excel('contains_file.xlsx')

df_results = pd.DataFrame()
for i in list(df_contains['col_1']):
    df_row = df_contains[df_contains['col_0'].str.contains(i)].loc[df_contains['col_1']==i]
    df_results = df_results.append(df_row)

with pd.ExcelWriter('temp_contains.xlsx') as writer:
    df_results.to_excel(writer)
             
