#!/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd

# sur rue du commerce quelle marque a la plus grosse remise

baseurl = 'https://www.rueducommerce.fr/rayon/ordinateurs-64/ordinateur-portable-657/'
baseurl = 'https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/marque__'

# pour les sociétés suivantes : Airbus, LVMH et Danone.
inputlist = ["dell", "hp"]

#<div class="sale_price">
#<span class="darty_prix darty_normal">399,<span class="darty_cents">90€</span></span>
#</div>
#<div class="prix_barre">
#<div class="prix_barre_liste">
#<p class="darty_prix_barre_remise darty_small separator_top">- 31%</p>

company = 'dell'
def remavg(company):
    soup = BeautifulSoup(requests.get(baseurl+company+'__'+company.upper()+'.html').content, "html.parser")
    brand = []
    for elem in soup.findAll("span",class_="darty_prix darty_normal"):
        remise = elem.parent.find_next_sibling().find("p",class_="darty_prix_barre_remise darty_small separator_top")
        if remise == None:
            pourcent = 0.
        else:
            pourcent = float(re.sub(r'[ %]','',remise.string))
        brand.append(pourcent)
    return np.mean(brand)

for brand in inputlist:
    print(brand,remavg(brand))
    #TODO ajouter a une liste et la trier
