import pandas as pd 
import os 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"


fillo = f"{data_path}CESI_16.xlsx"

df = pd.read_excel(fillo)

df = df[:168]

include = ['Australia', 'United States', 'New Zealand', 'UK']

# print(df['Country'].unique())

# print(df)

print(df.loc[df['Country'].isin(include)])

sorted = df.sort_values(by='fiscal_16', ascending=False)
print(sorted.head(20))