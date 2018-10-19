#!/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
#On a un transporteur on veut une matrice des distances entre 50 plus grandes villes de france

# etape 1 collecte des 50 villes
soup = BeautifulSoup(requests.get('https://fr.wikipedia.org/wiki/Liste_des_unit%C3%A9s_urbaines_de_France').content, "html.parser")
matable = soup.find("table", class_="wikitable sortable alternance").findAll("tr")

df = pd.DataFrame()
villes = []
i = 1
while i <= 50:
    villes.append(matable[i].findAll("td")[1].text.replace('-',' ').replace('[',' ').split(" ")[0])
    i +=1

#etape 2 api

for indexi in range(len(villes)):
#for city1 in villes:
    for indexj in range(indexi+1,len(villes)):
        r = requests.get('https://fr.distance24.org/route.json?stops='+villes[indexi]+'|'+villes[indexj]).json()
        #print('debug ',r.headers)
        #repos = json.loads(r.content.decode())['distance']
        print(r['distance'])
        df[villes[indexi]][villes[indexj]]=r

print(df)

