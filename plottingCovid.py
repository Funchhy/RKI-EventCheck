import csv
import pandas as pd
import datetime
import matplotlib.pyplot as plt

csvName = 'RKI_COVID19_history_2021_cut.csv'
allFields = ['IdBundesland','IdLandkreis','AnzahlFall','AnzahlTodesfall','Meldedatum']
fields = ['IdLandkreis','AnzahlFall','Meldedatum']

#df = pd.read_csv(csvName, usecols=fields)
df = pd.read_csv(csvName)
print(df.iloc[5:10])

#Convert String to Meldedatum
df['Meldedatum']= pd.to_datetime(df['Meldedatum'])

#Only SK Köln
#SK Köln IdLandkreis is: 5315
dfKoeln = df[df["IdLandkreis"] == 5315 ]
dfKoeln.sort_values(by=['Meldedatum'], inplace=True, ascending=False)

#dfKoeln = dfKoeln.set_index('Meldedatum')
dfKoeln.to_csv('koelnCovid.csv', encoding='utf-8')
dfKoeln = dfKoeln[['Meldedatum', 'AnzahlFall']]

dfKoeln = dfKoeln[dfKoeln['Meldedatum'] >  datetime.datetime(2021,11,20)]

#Setting Index on Datetime somehow automatically sorts the Data
# Prior to this we get "Meldedatum" starting from may going to november etc.
# ... basically all over the place
dfKoeln = dfKoeln.set_index('Meldedatum')
print(dfKoeln)

#dfKoeln.to_csv('koelnCovid.csv', encoding='utf-8')

dfKoeln.plot()
plt.show()

