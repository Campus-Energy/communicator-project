import numpy as np
import pandas as pd


df = pd.read_csv('TEST BATCH_Scheduled_Report - TEST BATCH_Scheduled_Report.csv')

df = df.iloc[3:]

meter_id = df.iloc[0]
meter_id  = meter_id.tolist()
meter_id.pop(0)
meter_id = np.reshape(meter_id, (len(meter_id),1))



print(meter_id)