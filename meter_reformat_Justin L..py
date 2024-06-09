import pandas as pd
# import geopandas as gpd

def create_dicts_from_csv(file_path, key_row, header_row):

    data = pd.read_csv(file_path)
    
    # Extract each unique meter_id in the specified row
    unique_keys = data.iloc[key_row].unique()
    
    # Create an empty dictionary to store the results
    result_dict = {}
    
    # Iterate through each unique key
    for unique_key in unique_keys:
        #Make a dictionary titled with the meter_id for each unqiue meter_id
        result_dict[unique_key] = {}
        
        # Store each column that has the meter_id at the top of it's row, in prep for data extraction
        columns = data.columns[data.iloc[key_row] == unique_key]
        
        # Populate the inner dictionary with headers as keys and column values as values
        for col in columns:
            #Store the type of data for each column as a key (kw, amp, watts, volts, etc)
            header = data.iloc[header_row][col]
            #Take every other value in that column and store it in a list
            values = data[col][header_row+1:].tolist()
            #Add the values to the dictionary under the path "meter_id/type_of_data/value" in the dictionary
            result_dict[unique_key][header] = values
    
    return result_dict

file_path = 'TEST BATCH_Scheduled_Report - TEST BATCH_Scheduled_Report.csv'
key_row = 3  # specify the row number for dictionary names (meter_id)
header_row = 4  # specify the row number for dictionary keys (types of units)



#Run the function
result_dict = create_dicts_from_csv(file_path, key_row, header_row)


#For formatting purposes when printing the result, only displays the first 3 values of each key in a dictionary
import json
limited_result_dict = {k: {hk: hv[:3] for hk, hv in v.items()} for k, v in result_dict.items()}
print(json.dumps(limited_result_dict, indent=2))
