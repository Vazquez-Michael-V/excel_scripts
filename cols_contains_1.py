
import pandas as pd

def cols_substring(col_to_search, col_substring, cols_substring_filename, cols_substring_output_filename=None):
    """Checks if a column contains a substring from another column. \n
    'col_to_search' will be searched for substrings in 'col_substring'. \n
    'cols_substring_filename' (required argument) is the excel file to be read, and
    'cols_substring_output_filename' (optional argument) is the excel file that will print the results of the
    substring search. If 'cols_substring_output_filename' is not specified, then no excel file will be output.   
    """
    
    df_contains = pd.read_excel(cols_substring_filename)
    
    big_found_list = []
    df_results = pd.DataFrame()
    # Search only once for each value in the Search column.
    for i in sorted(list(set(list(df_contains[col_substring])))):
        print(f"Searching for '{i}'.")
        df_row = df_contains[df_contains[col_to_search].str.contains(i)]
        df_results = df_results.append(df_row)
        found_list = [i for x in range(len(list(df_row[col_to_search])))]
        big_found_list.append(found_list)
    
    # Add Results column to allow for grouping.
    found_col = []
    for small_list in big_found_list:
        for s in small_list:
            found_col.append(s)
    df_results['Results'] = found_col
    
    
    # Clean up df_results.
    df_results = df_results.sort_values(by=[col_to_search]).reset_index(drop=True)
    df_results = df_results.drop(columns=[col_substring])    
    
    if cols_substring_output_filename != None:
        with pd.ExcelWriter(cols_substring_output_filename) as writer:
            df_results.to_excel(writer, index=False)

    return df_results
    
        
a = cols_substring('Chairs', 'Search', 'contains_file.xlsx', 'excel_contains.xlsx')

print(a)
print(type(a))
