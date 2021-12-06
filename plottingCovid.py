import csv
import pandas as pd
import datetime
import matplotlib.pyplot as plt

csvName = 'csv_Data/aggregatedCovid_new.csv'
allFields = ['IdBundesland','IdLandkreis','AnzahlFall','AnzahlTodesfall','Refdatum']
fields = ['IdLandkreis','AnzahlFall','Refdatum']

df = pd.read_csv(csvName)

#Convert String to Refdatum
df['Refdatum']= pd.to_datetime(df['Refdatum'])

#Only SK Köln
#SK Köln IdLandkreis is: 5315
dfKoeln = df[df["IdLandkreis"] == 5315 ]
dfKoeln = dfKoeln.sort_values(by=['Refdatum'], ascending=False)

dfKoeln.to_csv('csv_Data/koelnCovid.csv', encoding='utf-8')

#Football Game - case reportings 2021/11/27
dfKoeln = dfKoeln[['Refdatum', 'AnzahlFall']]
dfKoeln = dfKoeln[dfKoeln['Refdatum'] >  datetime.datetime(2021,11,10)]

dfKoeln = dfKoeln.set_index('Refdatum')

dfKoeln.plot()
markers = [datetime.datetime(2021,11,27), dfKoeln.loc[datetime.datetime(2021,11,27)]]
plt.text(markers[0], markers[1],
'Fussballspiel',horizontalalignment='right')
plt.plot(markers[0], markers[1], 'o-')

plt.show()

