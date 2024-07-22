#Importing libraries that will be used, run commands below in terminal line to install
# -pip install numpy, -pip install pandas
import numpy as np
import pandas as pd

#Read the csv and turn it into a dataframe
#Replace the stuff in quotes with your path to the file
df = pd.read_csv('PHASE THREE_Hourly_Report3_202407051700.csv', skiprows=4, header=None)
df = df.dropna(how="all")
df = df.dropna(how="all",axis=1)



#Cut out the uneeded first 3 rows of the csv

#Uncomment code below if you wanna see the csv without the first 3 rows, or print() it ig
# df.to_csv('Check_Me_Out')

#Finds where the '0' values are in the dataframe and stores the rows and cols in a list
zero_positions = np.where(df == '0.00')
zero_positions = list(zip(zero_positions[0], zero_positions[1]))
#Same thing as '0' but for NaN's
nan_positions = np.where(df.isna())
nan_positions = list(zip(nan_positions[0], nan_positions[1]))
#Puts them into a tuple containing the positions in (row,col) format
# combined_positions = list(zip(zero_positions[0], zero_positions[1])) + list(zip(nan_positions[0], nan_positions[1]))

#Store the datetime values
column_a_series = df.iloc[:,0]
column_a_series = column_a_series[2:]
#Reformat the datetime into year/month/day military time
# datetime_series = pd.to_datetime(column_a_series)
# column_a_series = datetime_series.apply(lambda x: x.strftime('%Y/%m/%d %H:%M'))
# column_a_series = formatted_dates.tolist()




#Runs for loop that reads the [(row,col), (row,col), ...] data in combined_positions
def thing(positions):
    a = pd.DataFrame(columns=['Datetime', 'meter_id', 'Value','type'])
    data = {'Datetime': [], 'meter_id': [], 'Value': [], 'type': []}
    for row,col in positions:
        #Take the datetime on the row correspeonding to the row the '0' or NaN was found
        day = column_a_series.iloc[row-2]
        #Take the meter_id
        meter = df.iloc[0, col]
        #Take the type of data it is
        value = df.iloc[1,col]
        #Return the value of that cell
        ty = df.iloc[row,col]
        
    
    
        #Add the data to the dictionary with the key
        data['Datetime'].append(day)
        data['meter_id'].append(meter)
        data['Value'].append(value)
        data['type'].append(ty)

    #Add the dictionary data to the dataframe
    a = pd.concat([a, pd.DataFrame(data)], ignore_index=True)
    #Fill the NaN data (Blank data) with a string placeholder 'NaN' so it appears on the csv
    a['type'] = a['type'].fillna('NaN')


    duplicates_mask = a.duplicated(subset='meter_id', keep=False)

# Add the mask as a column to the DataFrame for sorting
    a['Is_Duplicate'] = duplicates_mask

# Sort by the duplicate mask first and then by the 'Age' column
    sorted_df = a.sort_values(by=['Is_Duplicate', 'meter_id'], ascending=[False, True])

# Drop the helper column if needed
    a = sorted_df.drop(columns='Is_Duplicate')

    return a



thing(zero_positions).to_csv("Integrity check 0's 3,3.csv")
thing(nan_positions).to_csv("Integrity check nan's 3,3.csv")



# grouped = a.groupby('Value')
# dfs = {Value: group.reset_index(drop=True) for Value, group in grouped}
# for Value, dataframe in dfs.items():
#     # dataframe.to_csv(Value)
#     print(f"DataFrame for {Value}:")
#     print(dataframe)
#     print("\n")

#Uncomment below if you wanna print the dataframe
# print(a)

#Create the csv
