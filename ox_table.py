import pandas as pd 
import os 
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

usd = 0.78

fillo = f"{data_path}20210310-Global-Recovery-Observatory-_-publicv3.xlsx"


## READ IN ORIGINAL DATSET
df = pd.read_excel(fillo, sheet_name="COVID-19 Measures")
df = df[:3701]
# df = df[['Country','Policy Archetype', 'Policy Name', 'Description', 'Total Value, Local Currency (billions)',
#        'Date', 'Source(s)', 'Clean archetype?', 'Total Value, USD (billions)']]
df = df[['Country','Policy Archetype', 'Policy Name', 'Description',
       'Date', 'Source(s)','Total Value, USD (billions)']]

## READ IN 20-21 BUDGET SPENDING

budget = f"{data_path}2021ozfedaggregatedspending.xlsx"
# ['Country', 'Policy Archetype', 'Policy Name', 'Description', 'Date',
#        'Source(s)', 'Total Value, USD (billions)', 'Type', 'Kind']

bud = pd.read_excel(budget)

bud['Total value, Local Currency'] = bud['Total Value, Local Currency (billions)'] * 1000000
bud['Total value, USD'] = bud['Total value, Local Currency'] * usd
bud['Total Value, USD (billions)'] = bud['Total value, USD']/1000000
bud['Description'] = 'More than 60 projects, including $2 billion for the Melbourne intermodal terminal, $2.6 billion and $2 billion for the Anzac and Great Western Highways'

bud = bud[['Country','Policy Archetype', 'Policy Name', 
'Description', 'Date','Source(s)','Total Value, USD (billions)']]


## ADD UK, US AND KOREA

uuk = f"{data_path}2021addedspending.xlsx"
uuk = pd.read_excel(uuk)

uuk['Description'] = ''
uuk = uuk[['Country','Policy Archetype', 'Policy Name', 
'Description', 'Date','Source(s)','Total Value, USD (billions)']]
uuk = uuk[:19]

## ADD BUDGET TO EXISTING DATSET

df = df.append(bud)
df = df.append(uuk)



infra_projects = [('𝛾', "Traditional transport infrastructure investment"), 
('𝛿', "Clean transport infrastructure investment"), ('𝜀', "Traditional energy infrastructure investment"), 
('𝜂', "Clean energy infrastructure investment"), ('𝜃', "Local (project-based) infrastructure investment"), 
('𝜆', "Buildings upgrades and energy efficiency infrastructure investment"), ('𝜇', "Natural infrastructure and green spaces investment"),
 ('𝜋', "Other large-scale infrastructure investments")]

infra_icons = [x[0] for x in infra_projects]

tax_measures = [("L","Income tax cuts"), 
("M", "VAT and other goods and services tax cuts"), ("N", "Business tax cuts"), ("O", "Business tax deferrals"),
("Q", "Other tax cuts and deferrals")]

tax_icons = [x[0] for x in tax_measures]

other_measures = [("F", "Direct provision of basic needs"), ("R", "Targeted recovery cash transfers"), 
("X", "Worker retraining and job creation"), ("H","Job continuation support"), ("G","Targeted welfare cash transfers")]

other_icons = [x[0] for x in other_measures]

together = infra_icons + tax_icons + other_icons

# print(together)

df['Total Value, USD (billions)'] = pd.to_numeric(df['Total Value, USD (billions)'])

df = df.sort_values(by='Total Value, USD (billions)', ascending=False)

df = df.loc[df['Policy Archetype'].isin(infra_icons)]

df = df[:50]

# print(df[['Country','Policy Archetype', 'Policy Name','Total Value, USD (billions)']])
# df = df[['Country','Policy Name', 
# 'Description','Total Value, USD (billions)']]

# df.loc[df['Description'].isna(), "Description"] = ' '

df = df[['Country','Policy Name','Total Value, USD (billions)']]

print(df)

def makeTable(df):
	
    template = [
            {
                "title": "Major global infrastructure programs",
                "subtitle": f"50 of the largest infrastructure programs announced during the Covid-19 pandemic",
                "footnote": "",
                "source": "Global Recovery Observatory, Oxford University Economic Recovery Project, all Street Journal, International Monetary Fund, government websites",
                "yScaleType":"",
                "minY": "0",
                "maxY": "",
                "x_axis_cross_y":"",
                "periodDateFormat":"",
                "margin-left": "50",
                "margin-top": "30",
                "margin-bottom": "20",
                "margin-right": "10"
            }
        ]
    key = []
    # labels = []
    df.fillna("", inplace=True)
    chartData = df.to_dict('records')
    labels = []


    yachtCharter(template=template, dropdown=[],labels=labels, data=chartData, chartId=[{"type":"table"}], 
    options=[{"colorScheme":"guardian","format": "scrolling","enableSearch": "FALSE","enableSort": "FALSE", "enableShowMore":1}], chartName="big-infrastructure-programs")

makeTable(df)