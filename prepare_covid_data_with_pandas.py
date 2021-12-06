# Daniel Németh RKI Event Checker
# RKI History analyzer
import csv
import pandas as pd
import datetime

# csv too large with unrestricted nrows
# df = pd.read_csv('RKI_COVID19_history.csv', index_col=8, nrows=1000)

# All Fields:
# ['FID', 'IdBundesland', 'Bundesland','Landkreis',
# 'Altersgruppe', 'Geschlecht', 'AnzahlFall', 'AnzahlTodesfall',
# 'Refdatum']
fields = ["IdLandkreis", "IdBundesland", "AnzahlFall",
          "AnzahlTodesfall", "Refdatum"]

# read Csv in Chunks
def chunkedCSVReaderWithFields(fields, csvName):
    tp = pd.read_csv(csvName, iterator=True, chunksize=1000,
                     usecols=fields)
    return pd.concat(tp)

df = chunkedCSVReaderWithFields(fields, 'csv_data/RKI_COVID19_history.csv')

#Only keep 2021 Data / Omit everything that is earlier than 2021
df['Refdatum']= pd.to_datetime(df['Refdatum'])
df.drop(df[df['Refdatum'] < datetime.datetime(2021,1,1)].index, inplace=True)

#df = df.set_index('Refdatum')
print(df.iloc[500000:500005])

#Final: Only 2021 and columns: "IdLandkreis", "IdBundesland", "AnzahlFall",
#                              "AnzahlTodesfall", "Refdatum"
df.to_csv('csv_data/RKI_COVID19_history_2021_cut_new.csv', encoding='utf-8')