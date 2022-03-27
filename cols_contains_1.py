
import pandas as pd

def find_contents(specified_column, substring_columns, excel_filename, results_filename=None):
    """Useful when needing to know if contents in one or more columns also appear in a specified column.\n
    Searches specified column for contents in other column(s).\n
    substring_columns is a list of one or more column names appearing in excel_filename.\n
    Argument results_filename is optional. If not given, then no excel file will be created.
    """
    
    df_main_file = pd.read_excel(excel_filename)
    
    print(df_main_file)
    
    # Get a list of unique search values.
    df_search_cols = df_main_file[substring_columns]       
    search_values = []
    for col in substring_columns:
        df_temp_sv = df_search_cols[col].drop_duplicates()
        for elements in list(df_temp_sv):
            search_values.append(elements)
    
    print(search_values)
    
    big_found_list = []
    df_results = pd.DataFrame()
    for s in search_values:
        print(f"Searching for '{s}'.")
        df_temp_search = df_main_file[df_main_file[specified_column].str.contains(s)]
        # print(df_temp_search)
        df_results = df_results.append(df_temp_search)
        found_list = [s for x in range(len(list(df_temp_search[specified_column])))]
        big_found_list.append(found_list)
        
        # Add Results column to allow for grouping.
        found_col = []
        for small_list in big_found_list:
            for s in small_list:
                found_col.append(s)
        df_results['Results'] = found_col
    
    # Clean up df_results.
    df_results = df_results.sort_values(by=[specified_column]).reset_index()
    df_results = df_results.drop(columns=substring_columns)    
    
    if results_filename != None:
        with pd.ExcelWriter(results_filename) as writer:
            df_results.to_excel(writer, index=False)       
        

    return df_results
    

a = find_contents('Foo', ['Search_1', 'Search_2'], 'contains_file.xlsx', 'results.xlsx')

print(a)
print(type(a))
