import os
import shutil
import glob
import psycopg2
import getpass
import pandas as pd
from transform_data import transform_data
from Enervista import Enervista_transform

# Database connection details
DB_HOST = 'csbcd01.soest.hawaii.edu'  # db running on same machine as the script
DB_NAME = 'uhm2023'
DB_USER = getpass.getuser()

def process_files():
    inbox_folder = '/home/campusenergy/inbox'
    completed_folder = '/home/campusenergy/completed'
    
    # Ensure the completed folder exists
    os.makedirs(completed_folder, exist_ok=True)
    print ( "searching for files..." )

    csv_files = glob.glob(os.path.join(inbox_folder, '*.csv'))
    print ( "CSV found!", csv_files )

    for csv_file in csv_files:
        try:
            # Run the transformation
            if 'EnerVista' in csv_file:
                output_files = Enervista_transform(csv_file)
                print("EnerVista File")
                
            else:
                output_files = transform_data(csv_file)
                print("Communicator File")
            print ( "file found, moving files..." ) 
            # Move the processed file to the completed folder
            shutil.move(csv_file, os.path.join(completed_folder, os.path.basename(csv_file)))
            print ( "file moved successfully!" )

            # Upload the transformed files to the database
            for output_file in output_files:
                print ( "attempting upload..." )
                upload_to_database(output_file)
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            print(output_files)

def get_table_columns(conn, table_name):
    try:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table_name.split('.')[-1]}' AND table_schema = '{table_name.split('.')[0]}'
        """)
        columns = [row[0] for row in cur.fetchall()]
        cur.close()
        return columns
    except Exception as e:
        print(f"Error retrieving columns for table {table_name}: {e}")
        return None

def upload_to_database(file_path):
    
    print ( "mapping tables..." )
    # Map the file name prefix to the corresponding table name
    table_mapping = {
        'kW': 'aurora_v4.kw_communicator',
        'W-hours in the Interval, Received': 'aurora_v4.kwh_communicator'
        # Add other mappings here if needed
    }
    print ( "tables mapped successfully!" )

    # Extract the unit from the file name
    print ( "extracting units..." )
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    unit = file_name.split('_')[0]
    table_name = table_mapping.get(unit)
    print ( "unit extraction complete", unit )

    if not table_name:
        print(f"No table mapping found for file: {file_path}")
        return
    
    conn = None
    cur = None
    
    print ( "connecting to database..." )
    try:
        # Connect to the database using the .pgpass file for authentication
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER
            # No need to specify password here; it will be fetched from .pgpass
        )

        print ( "connection successful!" )
        # Get the columns from the table
        table_columns = get_table_columns(conn, table_name)
        
        if table_columns is None:
            print(f"Skipping upload due to error in retrieving columns for table {table_name}")
            return
        
        # Get the columns from the CSV file
        df = pd.read_csv(file_path)
        csv_columns = df.columns.tolist()
        
        # Check if the columns match
        if not all(col in table_columns for col in csv_columns):
            print(f"Column mismatch: Table columns {table_columns}, CSV columns {csv_columns}")
            return
        
        cur = conn.cursor()
        
        with open(file_path, 'r') as f:
            #next(f)  # Skip the header row
            cur.copy_expert(f"COPY {table_name} ({', '.join(csv_columns)}) FROM STDIN WITH CSV HEADER", f)
        
        conn.commit()
        print(f"Successfully uploaded {file_path} to table {table_name}")
    except Exception as e:
        print(f"Error uploading {file_path} to database: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    process_files()
