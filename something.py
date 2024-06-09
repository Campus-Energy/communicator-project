#Importing libraries that will be used, run commands below in terminal line to install
# -pip install numpy, -pip install pandas
import numpy as np
import pandas as pd

#Read the csv and turn it into a dataframe
#Replace the stuff in quotes with your path to the file
df = pd.read_csv('TEST BATCH_Scheduled_Report - TEST BATCH_Scheduled_Report.csv')

#Cut out the uneeded first 3 rows of the csv
df = df.iloc[3:]

#Uncomment code below if you wanna see the csv without the first 3 rows, or print() it ig
# df.to_csv('Check_Me_Out')

#Finds where the '0' values are in the dataframe and stores the rows and cols in a list
zero_positions = np.where(df == '0')
#Same thing as '0' but for NaN's
nan_positions = np.where(df.isna())
#Puts them into a tuple containing the positions in (row,col) format
combined_positions = list(zip(zero_positions[0], zero_positions[1])) + list(zip(nan_positions[0], nan_positions[1]))

#Store the datetime values
column_a_series = df['TEST BATCH Scheduled Report']
column_a_series = column_a_series[2:]
#Reformat the datetime into year/month/day military time
datetime_series = pd.to_datetime(column_a_series)
column_a_series = datetime_series.apply(lambda x: x.strftime('%Y/%m/%d %H:%M'))
# column_a_series = formatted_dates.tolist()




#Create an empty dataframe to with 4 column titles to turn into a csv later
a = pd.DataFrame(columns=['Datetime', 'meter_id', 'Value','type'])

#Create a dictionary to store data to concat to the dataframe later, creates less problems when uploading directly
data = {'Datetime': [], 'meter_id': [], 'Value': [], 'type': []}

#Runs for loop that reads the [(row,col), (row,col), ...] data in combined_positions
for row,col in combined_positions:
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

grouped = a.groupby('Value')
dfs = {Value: group.reset_index(drop=True) for Value, group in grouped}
for Value, dataframe in dfs.items():
    # dataframe.to_csv(Value)
    print(f"DataFrame for {Value}:")
    print(dataframe)
    print("\n")

#Uncomment below if you wanna print the dataframe
# print(a)

#Create the csv
# a.to_csv("zero_values.csv")
