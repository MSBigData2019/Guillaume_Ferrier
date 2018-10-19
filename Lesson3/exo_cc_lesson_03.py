#!/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import scipy as s
#On a un transporteur on veut une matrice des distances entre 50 plus grandes villes de france

# etape 1 collecte des 50 villes
soup = BeautifulSoup(requests.get('https://fr.wikipedia.org/wiki/Liste_des_unit%C3%A9s_urbaines_de_France').content, "html.parser")
matable = soup.find("table", class_="wikitable sortable alternance").findAll("tr")

villes = []
i = 1
while i <= 5:
    villes.append(matable[i].findAll("td")[1].text.replace('-',' ').replace('[',' ').split(" ")[0])
    i +=1

#etape 2 api

#Mon dataframe de sortie initialisé à NaN
df = pd.DataFrame(index=villes,columns=villes)

# pas besoin du produit croisé juste de la moitié des élements vu que c'est symétrique
for indexi in range(len(villes)):
    # distance nulle de la ville a elle meme !
    df[villes[indexi]][villes[indexi]] = 0
    for indexj in range(indexi+1,len(villes)):
        # API gratuite sans token
        r = requests.get('https://fr.distance24.org/route.json?stops='+villes[indexi]+'|'+villes[indexj]).json()
        df[villes[indexi]][villes[indexj]] = r['distance']
        df[villes[indexj]][villes[indexi]] = r['distance']
# reste a faire un pretty print
print(df)

