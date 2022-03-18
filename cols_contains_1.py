
import pandas as pd

df_contains = pd.read_excel('contains_file.xlsx')

big_found_list = []
df_results = pd.DataFrame()
# Search only once for each value in the Search column.
for i in sorted(list(set(list(df_contains['Search'])))):
    print(f"Searching for '{i}'.")
    df_row = df_contains[df_contains['Chairs'].str.contains(i)]
    df_results = df_results.append(df_row)
    found_list = [i for x in range(len(list(df_row['Chairs'])))]
    big_found_list.append(found_list)

# Add Results column to allow for grouping.
found_col = []
for small_list in big_found_list:
    for s in small_list:
        found_col.append(s)
df_results['Results'] = found_col


# Clean up df_results.
df_results = df_results.sort_values(by=['Chairs']).reset_index(drop=True)
df_results = df_results.drop(columns=['Search'])

print(df_results)

with pd.ExcelWriter('excel_contains.xlsx') as writer:
    df_results.to_excel(writer, index=False)
             
