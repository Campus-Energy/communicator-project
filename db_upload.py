import os
import shutil
import glob
import psycopg2
import getpass
import pandas as pd
from transform_data import transform_data

# Database connection details
DB_HOST = 'localhost'  # db running on same machine as the script
DB_NAME = 'uhm2023'
DB_USER = getpass.getuser()
DB_PASSWORD = getpass.getpass(prompt='Enter database password: ')

def process_files():
    inbox_folder = '/home/lydia/inbox'
    completed_folder = '/home/lydia/completed'
    
    # Ensure the completed folder exists
    os.makedirs(completed_folder, exist_ok=True)
    
    csv_files = glob.glob(os.path.join(inbox_folder, '*.csv'))

    for csv_file in csv_files:
        try:
            # Run the transformation
            output_files = transform_data(csv_file)
            
            # Move the processed file to the completed folder
            shutil.move(csv_file, os.path.join(completed_folder, os.path.basename(csv_file)))
            
            # Upload the transformed files to the database
            for output_file in output_files:
                upload_to_database(output_file)
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

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
    # Map the file name prefix to the corresponding table name
    table_mapping = {
        'kW': 'aurora_v4.kw_communicator',
        'kWh': 'aurora_v4.kwh_communicator'
        # Add other mappings here if needed
    }
    
    # Determine the table based on the file name prefix
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    table_name = table_mapping.get(file_name)
    
    if not table_name:
        print(f"No table mapping found for file: {file_path}")
        return
    
    conn = None
    cur = None
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
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
            next(f)  # Skip the header row
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