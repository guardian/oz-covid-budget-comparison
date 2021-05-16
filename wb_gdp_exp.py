import pandas as pd 
import os 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

fillo = f"{data_path}"

wb = f"{data_path}WDI_csv/WDIData.csv"

wb = pd.read_csv(wb)

# print(wb)
# print(wb.columns)

# print(wb['Country Name'].unique())

oz = wb.loc[wb['Country Name'] == 'Australia'].copy()

print(oz['Indicator Name'].unique())