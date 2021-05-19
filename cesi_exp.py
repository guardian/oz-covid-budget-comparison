import pandas as pd 
import os 
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

include = ["France", "China", 'Australia', "Spain", 'UK', 'United States', 
'South Korea', 'Canada', "Germany", "Mexico", "Japan", "New Zealand"]
fillo = f"{data_path}CESI_16.xlsx"

df = pd.read_excel(fillo)

df = df[:168]

df = df.loc[df['Country'].isin(include)]
df = df[['Country', 'fiscal_16']]
df.columns = ['Country', "Fiscal response as % of GDP"]
df = df.sort_values(by="Fiscal response as % of GDP", ascending=False)

df['Color'] = "rgb(4, 109, 161)"

df.loc[df['Country'] == "Australia", 'Color'] = 'rgb(204, 10, 17)'
df.loc[df['Country'] == "Australia", 'Fiscal response as % of GDP'] = '14.7'
# print(df.loc[df['Country'] == "Australia"])
# 14.7
def makeDropChart(df):
	
    template = [
            {
                "title": "Government Covid spending as % of GDP",
                "subtitle": "Comparing the federal government's Covid economic support estimate with the COVID-19 Economic Stimulus Index",
                "footnote": "",
                "source": "COVID-19 Economic Stimulus Index - Ceyhun Elgin, Gokce Basbug, Abdullah Yalaman; Australian federal government budget website",
                "dateFormat": "%Y-%m-%d",
                "minY": "0",
                "maxY": "",
                "xAxisDateFormat":"%b %d",
                # "tooltip":"<strong>{{#formatDate}}{{data.Date}}{{/formatDate}}</strong><br/>{{group}}: {{groupValue}}<br/>Total: {{total}}",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10"
            }
        ]
    key = []
    periods = []
    # labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    labels = []
    # dropdown = [{
    #     "data":"Infrastructure",
    #     "display":"Infrastructure"
    # },{
    #     "data":"Liquidity support",
    #     "display":"Liquidity support"
    # },{
    #     "data":"Tax measures",
    #     "display":"Tax measures"
    # },{
    #     "data":"Transfers and job support",
    #     "display":"Transfers and job support"
    # }]
    dropdown = []
    options = [{
        "enableShowMore":0
    }]


    yachtCharter(template=template, dropdown=dropdown, options=options, 
    labels=labels, data=chartData, chartId=[{"type":"horizontalbar"}], chartName="oz-covid-budget-gdp-comparison")

makeDropChart(df)