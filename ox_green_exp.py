import pandas as pd 
import os 
from modules.yachtCharter import yachtCharter

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"

usd = 0.78
include = ["France", "China", 'Australia', "Spain", 'United Kingdom', 'United States', 
'South Korea', 'Canada', "Germany", "Mexico", "Japan"]

fillo = f"{data_path}20210310-Global-Recovery-Observatory-_-publicv3.xlsx"


## READ IN ORIGINAL DATSET
df = pd.read_excel(fillo, sheet_name="COVID-19 Measures")
df = df[:3701]
# df = df[['Country','Policy Archetype', 'Policy Name', 'Description', 'Total Value, Local Currency (billions)',
#        'Date', 'Source(s)', 'Clean archetype?', 'Total Value, USD (billions)']]
df = df[['Country','Policy Archetype', 'Policy Name', 'Description',
       'Date', 'Source(s)','Total Value, USD (billions)']]

## READ IN 20-21 BUDGET SPENDING

budget = f"{data_path}2021fedbudget.xlsx"
# ['Country', 'Policy Archetype', 'Policy Name', 'Description', 'Date',
#        'Source(s)', 'Total Value, USD (billions)', 'Type', 'Kind']

bud = pd.read_excel(budget)

bud['Total value, Local Currency'] = bud['Total Value, Local Currency (billions)'] * 1000000
bud['Total value, USD'] = bud['Total value, Local Currency'] * usd
bud['Total Value, USD (billions)'] = bud['Total value, USD']/1000000
bud['Description'] = ''

bud = bud[['Country','Policy Archetype', 'Policy Name', 
'Description', 'Date','Source(s)','Total Value, USD (billions)']]

## ADD BUDGET TO EXISTING DATSET

df = df.append(bud)

## GROUP BY TYPE OF PROJECT 

## INFRA

infra_projects = [('𝛽', "Communications infrastructure investment"), ('𝛾', "Traditional transport infrastructure investment"), 
('𝛿', "Clean transport infrastructure investment"), ('𝜀', "Traditional energy infrastructure investment"), 
('𝜂', "Clean energy infrastructure investment"), ('𝜃', "Local (project-based) infrastructure investment"), 
('𝜆', "Buildings upgrades and energy efficiency infrastructure investment"), ('𝜇', "Natural infrastructure and green spaces investment"),
 ('𝜋', "Other large-scale infrastructure investments")]

infra_icons = [x[0] for x in infra_projects]

infra = df.loc[df['Policy Archetype'].isin(infra_icons)].copy()

for thing in infra_projects:
    infra.loc[infra['Policy Archetype'] == thing[0], "Type"] = thing[1]


infra["Kind"] = "Infrastructure"

# grouped = infra.groupby(by=['Country', "Type", "Kind"])['Total Value, USD (billions)'].sum().reset_index()

## TAX

tax_measures = [("L","Income tax cuts"), 
("M", "VAT and other goods and services tax cuts"), ("N", "Business tax cuts"), ("O", "Business tax deferrals"),
("Q", "Other tax cuts and deferrals")]


tax_icons = [x[0] for x in tax_measures]

tax = df.loc[df['Policy Archetype'].isin(tax_icons)].copy()

for thing in tax_measures:
    tax.loc[tax['Policy Archetype'] == thing[0], "Type"] = thing[1]

tax = tax.sort_values(by='Total Value, USD (billions)', ascending=False)

tax["Kind"] = "Tax measures"

## Other 

other_measures = [("X", "Worker retraining and job creation"), ("H","Job continuation support"), ("G","Targeted welfare cash transfers")]

other_icons = [x[0] for x in other_measures]


other = df.loc[df['Policy Archetype'].isin(other_icons)].copy()

for thing in other_measures:
    other.loc[other['Policy Archetype'] == thing[0], "Type"] = thing[1]

other = other.sort_values(by='Total Value, USD (billions)', ascending=False)

other["Kind"] = "Transfers and job support"


other2_measures = [("B","Liquidity support for large businesses"),("C","Liquidity support for start-ups and SMEs")]

other2_icons = [x[0] for x in other2_measures]


other2 = df.loc[df['Policy Archetype'].isin(other2_icons)].copy()

for thing in other2_measures:
    other2.loc[other2['Policy Archetype'] == thing[0], "Type"] = thing[1]

other2 = other2.sort_values(by='Total Value, USD (billions)', ascending=False)

other2["Kind"] = "Liquidity support"

## BRING TOGETHER 

listo = [tax, other, other2, infra]

final = pd.concat(listo)

# final = final[['Country', 'Total Value, USD (billions)', 'Kind']]

grouped = final.groupby(by=['Country', 'Kind'])['Total Value, USD (billions)'].sum().reset_index()


sorted = grouped.sort_values(by="Total Value, USD (billions)", ascending=False)
print(sorted.loc[sorted['Kind'] =="Infrastructure"])

grouped = grouped.loc[grouped['Country'].isin(include)]

# print(grouped)

pivoted = grouped.pivot(index='Country', columns='Kind', values='Total Value, USD (billions)').reset_index()

# pivoted = new.pivot(index="date", columns="header")['count'].reset_index()

# print(pivoted)

pivoted['Color'] = "rgb(4, 109, 161)"

pivoted.loc[pivoted['Country'] == "Australia", 'Color'] = 'rgb(204, 10, 17)'

def makeDropChart(df):
	
    template = [
            {
                "title": "Government responses to the Covid pandemic",
                "subtitle": "Grouped by spending category, measured in billions of US dollars",
                "footnote": "",
                "source": "| Sources: Global Recovery Observatory, Oxford University Economic Recovery Project",
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
    dropdown = [{
        "data":"Infrastructure",
        "display":"Infrastructure"
    },{
        "data":"Liquidity support",
        "display":"Liquidity support"
    },{
        "data":"Tax measures",
        "display":"Tax measures"
    },{
        "data":"Transfers and job support",
        "display":"Transfers and job support"
    }]
    options = [{
        "enableShowMore":0
    }]


    yachtCharter(template=template, dropdown=dropdown, options=options, 
    labels=labels, data=chartData, chartId=[{"type":"horizontalbar"}], chartName="oz-covid-budget-comparison")

makeDropChart(pivoted)
