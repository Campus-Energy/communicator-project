import numpy as np
import pandas as pd
import os

def transform_data(file_path):
    # Read the data from the CSV file, skipping the first 4 rows which contain metadata
    df = pd.read_csv(file_path, skiprows=4, header=None)
    df = df.dropna(how='all')


    # Get the second row after the skipped rows which contains 'Time Stamp' in the first column and units of measure in subsequent columns
    second_row_after_skip = df.iloc[1]
    # Get the unique units of measure
    unique_values = second_row_after_skip[1:].unique()
    # Store first row values which contain 'Time Stamp' and meter IDs
    first_row = df.iloc[0]

    # Create a dictionary to store the transformed dataframes
    transformed_dataframes = {}

    # Iterate over the unique units of measure
    for value in unique_values:
        # Select columns with the same units of measure as the current unique_value
        columns_to_include = df.columns[(second_row_after_skip == value).values]
        # Include the first column which contains the datetime values and the columns with the same units of measure
        columns_to_include = [0] + list(columns_to_include)
        # Save included columns to a new dataframe
        df_subset = df.iloc[[0] + list(range(2, len(df))), columns_to_include]
        # Rename the first column to 'datetime'
        df_subset.rename(columns={0: 'datetime'}, inplace=True)
        # Rename the columns to the values in the first row
        df_subset.columns = ['datetime'] + first_row[columns_to_include[1:]].tolist()
        # Get the datetime column
        datetime_col = df_subset['datetime']
        # Melt the dataframe to have a single column for meter_id and another for meter_reading
        df_melted = df_subset.iloc[1:].melt(id_vars=['datetime'], var_name='meter_id', value_name='meter_reading')
        df_melted['meter_reading'] = df_melted['meter_reading'].astype(str).str.strip().str.replace(r'[^\d.]+', '', regex=True)
        df_melted['meter_reading'] = pd.to_numeric(df_melted['meter_reading'], errors='coerce')

        # Convert the meter readings to the appropriate units
        if value == 'Watts, 3-Ph total':
            df_melted['meter_reading'] = df_melted['meter_reading'] / 1000
            transformed_dataframes['kW'] = df_melted
        elif value == 'W-hours, Total':
            df_melted['meter_reading'] = df_melted['meter_reading'] / 1000
            transformed_dataframes['kWh'] = df_melted
        else:
            transformed_dataframes[value] = df_melted

    # Define the output directory one level higher and named 'ready-for-upload'
    output_dir = os.path.abspath(os.path.join(os.path.dirname(file_path), '..', 'ready-for-upload'))
    # Create the directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the transformed dataframes to CSV files
    output_files = []
    print(transformed_dataframes.items())
    
    for key, dataframe in transformed_dataframes.items():
        if ( dataframe.empty ):
            pass
        else:
        # Get the first and last datetime values
            print( "getting datetimes..." )
        
            print( "\n\tsearching for start date... " )
            first_datetime = dataframe['datetime'].iloc[0]
            print( "\n\tstart date found\n\t", first_datetime )
        
            print( "\n\tsearching for end date..." )
            last_datetime = dataframe['datetime'].iloc[-1]
            print( "\n\tend date found...\n\t", last_datetime )
        
        # Format the datetime values to avoid invalid characters
            first_datetime_str = pd.to_datetime(first_datetime).strftime('%Y-%m-%d_%H-%M-%S')
            last_datetime_str = pd.to_datetime(last_datetime).strftime('%Y-%m-%d_%H-%M-%S')
        
        # Format the filename with the unit and datetime range
            filename = os.path.join(output_dir, f'{key}_{first_datetime_str}_{last_datetime_str}.csv')
            dataframe.to_csv(filename, index=False)
            output_files.append(filename)
            print(f"Saved DataFrame for key '{key}' to '{filename}'")
    
    return output_files

transform_data("PHASE TWO_Scheduled_Report2_202406300000.csv")