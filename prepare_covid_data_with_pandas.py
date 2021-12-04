# Daniel Németh RKI Event Checker

#Status Update Checker 
""""
import requests, json
url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/rki_key_data_v/FeatureServer/0/query?"
parameter = {
'referer':'https://www.mywebapp.com',
    'user-agent':'python-requests/2.9.1',
    'where': '1=1', # Alle Status-Datensätze
    'outFields': '*', # Rückgabe aller Felder
    'returnGeometry': False, # Keine Geometrien
    'f':'json', # Rückgabeformat, hier JSON
'cacheHint': True # Zugriff über CDN anfragen
}
result = requests.get(url=url, params=parameter) #Anfrage absetzen
resultjson = json.loads(result.text) # Das Ergebnis JSON als Python Dictionary laden
print(resultjson['features'])
"""

#RKI History analyzer
import csv
import pandas as pd
import datetime

# csv too large with unrestricted nrows
#df = pd.read_csv('RKI_COVID19_history.csv', index_col=8, nrows=1000)

#['FID', 'IdBundesland', 'Bundesland','Landkreis',
#'Altersgruppe', 'Geschlecht', 'AnzahlFall', 'AnzahlTodesfall', 'Meldedatum']

fields = ["IdLandkreis", "IdBundesland", "Altersgruppe", "Geschlecht", "AnzahlFall",
          "AnzahlTodesfall", "Meldedatum"]

def chunkedCSVReaderWithFields(fields, csvName):
    tp = pd.read_csv(csvName, iterator=True, chunksize=1000, usecols=fields)
    return pd.concat(tp)

# read Csv in Chunks
#tp = pd.read_csv('RKI_COVID19_history.csv', iterator=True, chunksize=1000, usecols=fields)
df = chunkedCSVReaderWithFields(fields, 'RKI_COVID19_history.csv')
df['Meldedatum']= pd.to_datetime(df['Meldedatum'])

# pseudo: if df['Meldedatum'] < 2021-01-01, omit Data.
df.drop(df[df['Meldedatum'] < datetime.datetime(2021,1,1)].index, inplace=True)

#df = df.set_index('Meldedatum')
print(df.iloc[500000:500005])

#Initialize with first Landkreis and first date of year
cumulatingLandkreis = '1001'
cumulatingTimestamp = datetime.datetime(2021,11,30)
cumulatingBundesland = '1'
cases = 0
deaths = 0

# Cumulate cases per day, ignoring sex and age groups
with open('RKI_COVID19_history_2021_cut.csv', mode='w', newline='') as ags_file:
        ags_writer = csv.writer(ags_file, delimiter=',')
        ags_writer.writerow(["IdBundesland"+','+"IdLandkreis"
                                        +','+"AnzahlFall"
                                        +','+"AnzahlTodesfall"+','
                                        +"Meldedatum"])

        for i, row in df.iterrows():
            #Save current AGS to check
            currentLandkreis = row['IdLandkreis']
            currentTimestamp = row['Meldedatum']
            currentBundesland = row['IdBundesland']
            if(currentLandkreis == cumulatingLandkreis):
                if(currentTimestamp == cumulatingTimestamp):
                    #cumulate Values
                    cases = cases+ int(row['AnzahlFall'])
                    deaths = deaths+ int(row['AnzahlTodesfall'])
                else:
                    #Add Row to new CSV File
                    ags_writer.writerow([str(cumulatingBundesland)+','+
                                        str(cumulatingLandkreis)+','+str(cases)
                                        +','+str(deaths)+','+(str(cumulatingTimestamp))[0:9]])
                    cumulatingTimestamp = currentTimestamp
                    cases= int(row['AnzahlFall'])
                    deaths = int(row['AnzahlTodesfall'])
            else:
                cumulatingBundesland = currentBundesland
                cumulatingLandkreis = currentLandkreis
#df.to_csv('pandasCovid.csv', encoding='utf-8')