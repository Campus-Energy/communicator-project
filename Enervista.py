import pandas as pd
import os



def Enervista_transform(file_path):
    # Create a list to hold the transformed DataFrames
    df = pd.read_csv(file_path, skiprows=1)  # Skip the first row if it's not a header

    # Convert the "Time" column to datetime format, assuming the date is present
    df['Time'] = pd.to_datetime(df['Time'], format='%b %d %y %H:%M')

    # Filter the DataFrame for 15-minute intervals
    df = df[df['Time'].dt.minute % 15 == 0]
    transformed_dataframes = []

    # Loop through columns starting from the second one to create separate DataFrames
    for column in df.columns[1:]:
        # Create a new DataFrame with the Time, Meter_ID, and Data_Values columns
        transformed_df = pd.DataFrame({
            'datetime': df['Time'],
            'meter_name': column,
            'meter_reading': df[column]
        })
        transformed_dataframes.append(transformed_df)


    combined_df = pd.concat(transformed_dataframes, ignore_index=True)
    # combined_df.to_csv('combined_transformed_dataframes.csv')


    # Define the output directory one level higher and named 'ready-for-upload'
    output_dir = os.path.abspath(os.path.join(os.path.dirname(file_path), '..', 'ready-for-upload'))
    # Create the directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    output_files = []
    filename = os.path.join(output_dir, f'EnerVistakW_Report.csv')
    combined_df.to_csv(filename, index=False)
    output_files.append(filename)
    print(f"Saved DataFrame for key EnerVistakW to '{filename}'")
    
    return output_files



if __name__ == '__main__':
    import argparse
    # Parse the input arguments
    parser = argparse.ArgumentParser(description="Transform data from a CSV file.")
    parser.add_argument('file', type=str, help='Path to the input CSV file.')
    args = parser.parse_args()
    
    # Transform the data
    Enervista_transform(args.file)