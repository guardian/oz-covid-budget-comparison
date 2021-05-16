import pandas as pd 
import os 

here = os.path.dirname(__file__)
data_path = os.path.dirname(__file__) + "/data/"


fillo = f"{data_path}20210310-Global-Recovery-Observatory-_-publicv3.xlsx"

df = pd.read_excel(fillo, sheet_name="COVID-19 Measures")
df = df[:3701]
# df = df[['Country','Policy Archetype', 'Policy Name', 'Description', 'Total Value, Local Currency (billions)',
#        'Date', 'Source(s)', 'Clean archetype?', 'Total Value, USD (billions)']]
df = df[['Country','Policy Archetype', 'Policy Name', 'Description',
       'Date', 'Source(s)','Total Value, USD (billions)']]


infra_projects = [('𝛽', "Communications infrastructure investment"), ('𝛾', "Traditional transport infrastructure investment"), 
('𝛿', "Clean transport infrastructure investment"), ('𝜀', "Traditional energy infrastructure investment"), 
('𝜂', "Clean energy infrastructure investment"), ('𝜃', "Local (project-based) infrastructure investment"), 
('𝜆', "Buildings upgrades and energy efficiency infrastructure investment"), ('𝜇', "Natural infrastructure and green spaces investment"),
 ('𝜋', "Other large-scale infrastructure investments")]

infra_icons = [x[0] for x in infra_projects]

infra = df.loc[df['Policy Archetype'].isin(infra_icons)].copy()

for thing in infra_projects:
    infra.loc[infra['Policy Archetype'] == thing[0], "Type"] = thing[1]

include = ['Australia', 'United Kingdom', 'United States', 'South Korea', 'Canada', 'Peru', 'Israel', 'South Africa']

# print(infra['Country'].unique())
infra = infra.loc[infra['Country'].isin(include)]

infra["Kind"] = "Infrastructure"

grouped = infra.groupby(by=['Country', "Type", "Kind"])['Total Value, USD (billions)'].sum().reset_index()

# print(grouped)

tax_measures = [("L","Income tax cuts"), 
("M", "VAT and other goods and services tax cuts"), ("N", "Business tax cuts"), ("O", "Business tax deferrals"),
("Q", "Other tax cuts and deferrals")]

tax_icons = [x[0] for x in tax_measures]

tax = df.loc[df['Policy Archetype'].isin(tax_icons)].copy()

for thing in tax_measures:
    tax.loc[tax['Policy Archetype'] == thing[0], "Type"] = thing[1]



# tax = tax.loc[tax['Country'].isin(include)]
tax = tax.sort_values(by='Total Value, USD (billions)', ascending=False)

tax["Kind"] = "Tax"

# tax_grouped = tax.groupby(by=['Country', "Type", "Kind"])['Total Value, USD (billions)'].sum().reset_index()

# print(tax_grouped)

print(tax[['Country','Policy Name', 'Description',
       'Source(s)', 'Total Value, USD (billions)']].head(30))