import os
import shutil
import glob
import psycopg2
import getpass
from transform_data import transform_data

# Database connection details
DB_HOST = 'localhost' # db running on same machine as the script
DB_NAME = 'uhm2023'
DB_USER = getpass.getuser()

def process_files():
    inbox_folder = '/path/to/inbox'
    completed_folder = '/path/to/completed'
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

def upload_to_database(file_path):
    # Map the file name prefix to the corresponding table name
    table_mapping = {
        'kW': 'kw',
        'kWh': 'kwh'
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
            user=DB_USER
        )
        cur = conn.cursor()
        
        with open(file_path, 'r') as f:
            next(f)  # Skip the header row
            cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", f)
        
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