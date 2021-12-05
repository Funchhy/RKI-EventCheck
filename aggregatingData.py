import csv
import pandas as pd
import numpy as np
import datetime

csvName = 'RKI_COVID19_history_2021_cut.csv'
allFields = ['IdBundesland','IdLandkreis','AnzahlFall','AnzahlTodesfall','Refdatum']
fields = ['IdLandkreis','AnzahlFall','Refdatum']

df = pd.read_csv(csvName)

#Convert String to Refdatum
df['Refdatum']= pd.to_datetime(df['Refdatum'])

aggregated_df = df.groupby(['IdLandkreis',
                 'Refdatum'], as_index=False).agg({'AnzahlFall': 
                 ['sum']}).reset_index

# Misaligned Header, which i manually set in the csv File now
# there is one more line with blank - blank - sum
# Becuz of the groupby operator above
aggregated_df.to_csv('aggregatedCovid.csv', encoding='utf-8')

