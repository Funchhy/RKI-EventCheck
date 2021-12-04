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
""""
#Cut Rows and Columns which are not needed from Big csv File into
#new csv File
with open('RKI_COVID19_history.csv', newline='') as csvfile:
     datareader = csv.reader(csvfile, delimiter=',')
     counter = 0

     with open('RKI_COVID19_history_modified.csv', mode='w', newline='') as mod_file:
         mod_writer = csv.writer(mod_file, delimiter=',')

         #Writing the Header of the new csv File
         mod_writer.writerow(['FID', 'IdBundesland', 'Bundesland','Landkreis',
          'Altersgruppe', 'Geschlecht', 'AnzahlFall', 'AnzahlTodesfall', 'Meldedatum'])
         for row in datareader:
             #Check Date as Inclusion Criterion (only 2021 Data should be considered)
             if(counter > 0):
                 if(int(row[8][0:4]) >= 2021 and counter > 0):
                     #Add Row to new CSV File
                     mod_writer.writerow((row[0:9]))
             counter = counter+1
             if(counter % 100000 == 0):
                 print(counter)

             #if(counter > 1000):
             #    break
"""
            
with open('RKI_COVID19_history_modified.csv', newline='') as csvfile:
     datareader = csv.reader(csvfile, delimiter=',')
     counter = 0

     with open('RKI_COVID19_history_modified_landkreiseCut.csv', mode='w', newline='') as ags_file:
         ags_writer = csv.writer(ags_file, delimiter=',')

         #Writing the Header of the new csv File
         ags_writer.writerow(['Bundesland','Landkreis', 
         'AnzahlFall', 'AnzahlTodesfall', 'Meldedatum'])
         
         #Initialize with first Landkreis and first date of year
         cumulatingLandkreis = 'SK Flensburg'
         cumulatingTimestamp = '2021/01/01 00:00:00'
         cumulatingBundesland = 'Schleswig-Holstein'
         cases = 0
         deaths = 0
         for row in datareader:
             #Save current AGS to check
             if(counter > 3):
                 #counter > 3 to skip header line in CSV File and first entries
                 #since first entries are not sorted by date in csv file
                 currentLandkreis = row[3]
                 currentTimestamp = row[8]
                 currentBundesland = row[2]
                 if(currentLandkreis == cumulatingLandkreis):
                     if(currentTimestamp == cumulatingTimestamp):
                         #cumulate Values
                         cases = cases+ int(row[6])
                         deaths = deaths+ int(row[7])
                     else:
                         #Add Row to new CSV File
                         ags_writer.writerow([cumulatingBundesland+','+cumulatingLandkreis+","+str(cases)
                         +','+str(deaths)+','+cumulatingTimestamp])
                         cumulatingTimestamp = currentTimestamp
                         cases= int(row[6])
                         deaths = int(row[7])
                 else:
                     cumulatingBundesland = currentBundesland
                     cumulatingLandkreis = currentLandkreis

             counter = counter+1
             if(counter % 100000 == 0):
                 print(counter)

             #if(counter > 1000):
             #    break