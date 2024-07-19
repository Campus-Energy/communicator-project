import numpy as np
import pandas as pd
import os

def transform_data(file_path):
    # read the data from the CSV file, skipping the first 4 rows which contain metadata
    df = pd.read_csv(file_path, skiprows=4, header=None)

    # get the second row after the skipped rows which contains 'Time Stamp' in the first column and units of measure in
    # subsequent columns
    second_row_after_skip = df.iloc[1]
    # get the unique units of measure
    unique_values = second_row_after_skip[1:].unique()
    # store first row values which contain 'Time Stamp' and meter IDs
    first_row = df.iloc[0]

    # create a dictionary to store the transformed dataframes
    transformed_dataframes = {}

    # iterate over the unique units of measure
    for value in unique_values:
        # select columns with the same units of measure as the current unique_value
        columns_to_include = df.columns[(second_row_after_skip == value).values]
        # include the first column which contains the datetime values and the columns with the same units of measure
        columns_to_include = [0] + list(columns_to_include)
        # save included columns to a new dataframe
        df_subset = df.iloc[[0] + list(range(2, len(df))), columns_to_include]
        # rename the first column to 'datetime'
        df_subset.rename(columns={0: 'datetime'}, inplace=True)
        # rename the columns to the values in the first row
        df_subset.columns = ['datetime'] + first_row[columns_to_include[1:]].tolist()
        # get the datetime column
        datetime_col = df_subset['datetime']
        # melt the dataframe to have a single column for meter_id and another for meter_reading
        df_melted = df_subset.iloc[1:].melt(id_vars=['datetime'], var_name='meter_id', value_name='meter_reading')
        df_melted['meter_reading'] = df_melted['meter_reading'].str.strip().str.replace(r'[^\d.]+', '', regex=True)
        df_melted['meter_reading'] = pd.to_numeric(df_melted['meter_reading'], errors='coerce')

        # convert the meter readings to the appropriate units
        if value == 'Watts, 3-Ph total':
            df_melted['meter_reading'] = df_melted['meter_reading'] / 1000
            transformed_dataframes['kW'] = df_melted
        elif value == 'W-hours, Total':
            df_melted['meter_reading'] = df_melted['meter_reading'] / 1000
            transformed_dataframes['kWh'] = df_melted
        else:
            transformed_dataframes[value] = df_melted

        # define the output directory one level higher and named 'ready-for-upload'
    output_dir = os.path.abspath(os.path.join(os.path.dirname(file_path), '..', 'ready-for-upload'))
    # create the directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # save the transformed dataframes to CSV files
    output_files = []
    for key, dataframe in transformed_dataframes.items():
        filename = os.path.join(output_dir, f'{key}.csv')
        dataframe.to_csv(filename, index=False)
        output_files.append(filename)
        print(f"Saved DataFrame for key '{key}' to '{filename}'")
    
    return output_files

if __name__ == '__main__':
    import argparse
    # parse the input arguments
    parser = argparse.ArgumentParser(description="Transform data from a CSV file.")
    parser.add_argument('file', type=str, help='Path to the input CSV file.')
    args = parser.parse_args()
    
    # transform the data
    transform_data(args.file)