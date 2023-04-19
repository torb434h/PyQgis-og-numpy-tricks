#et script til at geokode csv filer i qgis, lavet i forbindelse med udarabejdelsen af et temakort over daginstitutioner i værlæser


# exec(open('sti til der hvor du har lagt den her python fil').read()) # en endog meget handy måde at loade et script på med adgang til alle funktioner i dine REPL'en

import json
import os
from urllib.request import urlopen
import urllib.parse

os.chdir(QgsProject.instance().readPath("./"))

link = 'https://api.dataforsyningen.dk/rest/gsearch/v1.0/adresse?q={}&token={}'

token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # token man får hos dataforsyningen hvis man laver en bruger, står i linket til fx deres wfs links

token = 'a34f178f6a8135036f17623c1c34b496'
filSti = 'furesoe_kommune_dag30-03-23.csv'
# [i if i.find('.csv') > -1 else None for i in os.listdir()][0] # fin oneliner der tjekker om der er en csv fil i mappen sciptet bliver kørt og sætter det til filSti


def enkod(sti):
    return sti.replace(' ', '%20').replace('æ','%c3%a6').replace('ø','%c3%b8').replace('å','%c3%a5') # skrald metode, kigger på det senere. Evt noget med urllib parse

csv = open(filSti).read()

csvM = [[y for y in x.split(',') if y != '' ] for x in csv.split('\n') ] # laver regneark filen om til et 2d matriks array, hvilket en csv fil egentlige allerede er, nu er den det bare i den her buffer

reqs = [] 


layer = QgsVectorLayer('Point?crs=EPSG:25832', '{} importeret med torb343MEGAGIXXX'.format(filSti), 'memory') #object fra qgis egen class, QgsVectorLayer, angivet med datum data fra dataforsyningen anvender
provider = layer.dataProvider()

for i in range(len(csvM[0])): # sætter fields i vektorlaget, gemt i buffer laget memory, til a svare til første række i regnearket 
    if csvM[1][i].isdigit():
        provider.addAttributes([QgsField(csvM[0][i], QVariant.Int)])
    else:
        provider.addAttributes([QgsField(csvM[0][i], QVariant.String)])
    
layer.updateFields()


for i in range(len(csv.split('\n'))-1):
    print(csv.split('\n')[i].split(',')[2])
    adresse = csv.split('\n')[i].split(',')[2]
    reqs.append(enkod(link.format(adresse,token))) # http request til dataforsyningen med adresse fra csv filen. I filen jeg her arbejder med står adresse som tredje kollone fra 

jsons = []

for i in range(len(reqs)):
    res = urlopen(reqs[i]).read()
    jsons.append(json.loads(res))

feature = QgsFeature()

for i in range(len(jsons)):
    for j in range(len(jsons[i])):
        koord = []
        if jsons[i][j]['kommunekode'] == '0190': # filtrerer svaret der har komunekode som værløse. Scriptet virker kun i værløse, men kan selvfølig ændres til relevant kommunekode
            EN = jsons[i][j]['geometri']['coordinates'][0] #øst nord
            pn = QgsGeometry.fromPointXY(QgsPointXY(EN[0],EN[1])) 
            feature.setGeometry(pn)
            feature.setAttributes([ csvM[i][j].replace(' ','-') for j in range(len(csvM[i])) ])
            #feature.setAttributes(['navn','type','adresse','by', '123','ejerforhold','hjemmeside'])
            provider.addFeature(feature)
            layer.updateExtents()
        


        
   
QgsProject.instance().addMapLayer(layer) ## sender til qgis apien

