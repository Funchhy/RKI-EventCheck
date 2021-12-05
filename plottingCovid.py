import csv
import pandas as pd
import datetime
import matplotlib.pyplot as plt

csvName = 'aggregatedCovid.csv'
allFields = ['IdBundesland','IdLandkreis','AnzahlFall','AnzahlTodesfall','Refdatum']
fields = ['IdLandkreis','AnzahlFall','Refdatum']

#df = pd.read_csv(csvName, usecols=fields)
df = pd.read_csv(csvName)
print(df.iloc[5:10])

#Convert String to Refdatum
df['Refdatum']= pd.to_datetime(df['Refdatum'])

#Only SK Köln
#SK Köln IdLandkreis is: 5315
dfKoeln = df[df["IdLandkreis"] == 5315 ]
dfKoeln.sort_values(by=['Refdatum'], inplace=True, ascending=False)

#dfKoeln = dfKoeln.set_index('Refdatum')
dfKoeln.to_csv('koelnCovid.csv', encoding='utf-8')
dfKoeln = dfKoeln[['Refdatum', 'AnzahlFall']]

dfKoeln = dfKoeln[dfKoeln['Refdatum'] >  datetime.datetime(2021,11,10)]

#Setting Index on Datetime somehow automatically sorts the Data
# Prior to this we get "Refdatum" starting from may going to november etc.
# ... basically all over the place
dfKoeln = dfKoeln.set_index('Refdatum')
print(dfKoeln)

#dfKoeln.to_csv('koelnCovid.csv', encoding='utf-8')

dfKoeln.plot()
plt.show()

