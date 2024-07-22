import pandas as pd
# import geopandas as gpd




file_path = 'TEST BATCH_Scheduled_Report - TEST BATCH_Scheduled_Report.csv'
key_row = 3  # specify the row number for dictionary names (meter_id)
header_row = 4  # specify the row number for dictionary keys (types of units)

data = pd.read_csv(file_path)

titles = ['datetime', 'meter_id']

    
# Extract each unique meter_id in the specified row
unique_keys = data.iloc[key_row].unique()
    
# Create an empty dictionary to store the results
result_dict = {}
    
    # Iterate through each unique key
for unique_key in unique_keys:
    #Make a dictionary titled with the meter_id for each unqiue meter_id
    result_dict[unique_key] = {}
        
    # Store each column that has the meter_id at the top of it's row, in prep for data extraction
    column_names = data.columns[data.iloc[key_row] == unique_key]

        
    # Populate the inner dictionary with headers as keys and column values as values
    for col in column_names:
        #Store the type of data for each column as a key (kw, amp, watts, volts, etc)
        header = data.iloc[header_row][col]
        titles.append(header)
        #Take every other value in that column and store it in a list
        values = data[col][header_row+1:].tolist()
        #Add the values to the dictionary under the path "meter_id/type_of_data/value" in the dictionary
        result_dict[unique_key][header] = values
    

holder = result_dict['Time Stamp']
datetime = []
for key, val in holder.items():
    datetime.append(val)


del result_dict['Time Stamp']

        
column_names = []
[column_names.append(x) for x in titles if x not in column_names]
column_names.remove('Time Stamp')

df = pd.DataFrame(columns=column_names)

      
for meter_id, nested_dict in result_dict.items():
        #nested_dict is datatype and value (key and value)
        storage_dict = {key: [] for key in column_names}
        [storage_dict['datetime'].append(x) for x in datetime]
        for key, value in nested_dict.items():
            for x in value:
                storage_dict[key].append(x)
        [storage_dict['meter_id'].append(meter_id) for z in range(len(value))]
        # dict_df = pd.DataFrame({ key:pd.Series(value) for key, value in storage_dict.items() })




# dict_df.to_csv("view_test.csv")

                
    
import json

# Display each dictionary individually
for unique_key, nested_dict in result_dict.items():
    print(f"Dictionary for key: {unique_key}")
    limited_dict = {hk: hv[:3] for hk, hv in nested_dict.items()}
    print(json.dumps(limited_dict, indent=2))
    print("\n" + "-"*50 + "\n")
