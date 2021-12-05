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

fields = ["IdLandkreis", "IdBundesland", "Altersgruppe", "Geschlecht", "AnzahlFall",
          "AnzahlTodesfall", "Refdatum"]

# read Csv in Chunks
def chunkedCSVReaderWithFields(fields, csvName):
    tp = pd.read_csv(csvName, iterator=True, chunksize=1000,
                     usecols=fields)
    return pd.concat(tp)

df = chunkedCSVReaderWithFields(fields, 'RKI_COVID19_history.csv')

#Only keep 2021 Data / Omit everything that is earlier than 2021
df['Refdatum']= pd.to_datetime(df['Refdatum'])
df.drop(df[df['Refdatum'] < datetime.datetime(2021,1,1)].index, inplace=True)

#df = df.set_index('Refdatum')
print(df.iloc[500000:500005])

#Initialize with first Landkreis and first date of year
cumulatingLandkreis = '1001'
cumulatingTimestamp = datetime.datetime(2021,11,30)
cumulatingBundesland = '1'
cases = 0
deaths = 0

# - Doesnt do what it should do. Just Kicks some columns i guess...
# need to delete / refactor.
# Cumulate cases per day, ignoring sex and age groups
with open('RKI_COVID19_history_2021_cut.csv', mode='w', newline='') as ags_file:
        ags_writer = csv.writer(ags_file, delimiter=',')
        ags_writer.writerow(['IdBundesland','IdLandkreis'
                                        ,'AnzahlFall'
                                        ,'AnzahlTodesfall',
                                        'Refdatum'])

        for i, row in df.iterrows():
            #Save current AGS to check
            currentLandkreis = row['IdLandkreis']
            currentTimestamp = row['Refdatum']
            currentBundesland = row['IdBundesland']
            if(currentLandkreis == cumulatingLandkreis):
                if(currentTimestamp == cumulatingTimestamp):
                    #cumulate Values
                    cases = cases+ int(row['AnzahlFall'])
                    deaths = deaths+ int(row['AnzahlTodesfall'])
                else:
                    #Add Row to new CSV File
                    ags_writer.writerow([str(cumulatingBundesland),
                                        str(cumulatingLandkreis),str(cases)
                                        ,str(deaths),(str(cumulatingTimestamp))[0:10]])
                    cumulatingTimestamp = currentTimestamp
                    cases= int(row['AnzahlFall'])
                    deaths = int(row['AnzahlTodesfall'])
            else:
                cumulatingBundesland = currentBundesland
                cumulatingLandkreis = currentLandkreis
#df.to_csv('pandasCovid.csv', encoding='utf-8')