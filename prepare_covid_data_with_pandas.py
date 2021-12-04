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

df = pd.read_csv('RKI_COVID19_history.csv', index_col=8, nrows=1000)

print(df.head(10))

