
import xml.etree.ElementTree as ET 
import pandas as pd

file = 'CDID_SDMX Output_Development.xml'
output_file = 'v4-MQ10.csv'

# Reading in the data
tree = ET.parse(file)
root = tree.getroot()

rows = [] # to be populated with separate dicts for each row of data
for elem in root[1]:
    my_dict = elem.attrib.copy()
    for subelem in elem:
        for key in subelem.attrib:
            my_dict[key] = subelem.attrib[key]  
        rows.append(my_dict)
        my_dict = elem.attrib.copy()
            
# data into a pandas dataframe
df = pd.DataFrame(rows)

###### Next part is more CMD specific ######

print(df.columns) # shows list of columns/dimensions

# removing columns that have only one variable per dimension
# some of these may need to be kept in if its decided that they are actually needed
# CDID also removed as this isnt used in CMD
columns_to_remove = [
        'ACCOUNTING_ENTRY', 'ACTIVITY', 'CDID', 'CONF_STATUS', 'COUNTERPART_AREA', 'COUNTERPART_SECTOR',
        'DECIMALS', 'EXPENDITURE', 'INSTR_ASSET', 'OBS_STATUS', 'PRICES', 'REF_SECTOR', 'STO',
        'TABLE_IDENTIFIER', 'TRANSFORMATION', 'UNIT_MEASURE', 'UNIT_MULT'
        ]

# dropping columns
df = df.drop(columns_to_remove, axis=1)

# Transforming data in a v4 format - format used for CMD
# observation followed by code-label columns for each dimension

#renaming columns to start
df = df.rename(columns={
        'OBS_VALUE':'v4_0', # obs column is renamed this for v4 format
        'TIME_PERIOD':'Time', 
        'ADJUSTMENT':'Adjustment',
        'FREQ':'Freq',
        'REF_AREA':'RefArea'
        }
    )

# creating new columns for the 'codes' for each dimension
df['calendar-years'] = df['Time'] # using an existing code list
# CMD also requires a geography - will assume to use 'United Kingdom'
df['Geography'] = 'United Kingdom'
df['uk-only'] = 'K02000001' # ONS geography code

# code lists for below dont exist so giving generic names for now
df['adjustment_codelist'] = df['Adjustment'] 
df['freq_codelist'] = df['Freq']
df['refarea_codelist'] = df['RefArea']


# re-ordering columns
# code column goes before label column
df = df[[
        'v4_0', 'calendar-years', 'Time', 'uk-only', 'Geography', 'adjustment_codelist', 'Adjustment',
        'freq_codelist', 'Freq', 'refarea_codelist', 'RefArea'
        ]]

df.to_csv(output_file, index=False)