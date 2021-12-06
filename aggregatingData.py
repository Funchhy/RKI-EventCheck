import csv
import pandas as pd
import numpy as np
import datetime

csvName = 'csv_data/RKI_COVID19_history_2021_cut_new.csv'
allFields = ['IdBundesland','IdLandkreis','AnzahlFall','AnzahlTodesfall','Refdatum']
fields = ['IdLandkreis','AnzahlFall','Refdatum']

df = pd.read_csv(csvName)

#Convert String to Refdatum
df['Refdatum']= pd.to_datetime(df['Refdatum'])

# Aggregate by if IdLandkreis and Refdatum match
aggregated_df = df.groupby(['IdLandkreis','Refdatum'], as_index=False).agg({'AnzahlFall':['sum']})
# Reset Index since groupby introduces new line with "sum" in it
aggregated_df.reset_index
# Rename Columns to create original header
aggregated_df.columns = ['IdLandkreis','Refdatum','AnzahlFall']

aggregated_df.to_csv('csv_data/aggregatedCovid_new.csv', encoding='utf-8')

