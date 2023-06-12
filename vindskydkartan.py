from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
link = 'https://vindskyddskartan.se/en/places'
req = Request(link)
req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0')
html = urlopen(req)
soup = BeautifulSoup(html)


tr = [tr for tr in soup.findAll('tr',{"name":True}) ]



layer = QgsVectorLayer('Point?crs=EPSG:4619', 'vindskyd', 'memory') #object fra qgis egen class, QgsVectorLayer, angivet med datum data fra dataforsyningen anvender
provider = layer.dataProvider()
provider.addAttributes([QgsField('Navn', QVariant.String),QgsField('Type', QVariant.String)])
layer.updateFields()

feature = QgsFeature()





for row in soup.find_all('tr'):
    vindskyd = ','.join(row.stripped_strings).split(',')
    try:
        vindskyd[2:1] = float(vindskyd[2]), float(vindskyd[3])
        pn = QgsGeometry.fromPointXY(QgsPointXY(vindskyd[3],vindskyd[2])) 
        feature.setGeometry(pn)
        feature.setAttributes([ vindskyd[0], vindskyd[1] ])
        provider.addFeature(feature)
        layer.updateExtents()
    except:
        print(vindskyd)
    #ØN = [ tal for tal in vindskyd if isinstance(tal,float) ]



QgsProject.instance().addMapLayer(layer) ## sender til qgis apien
    
