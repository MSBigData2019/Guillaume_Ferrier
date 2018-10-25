#!/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
#import cookielib
"""
Par ailleurs voici l'exercice que je vous propose pour  la semaine prochaine.
L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine. 
Vous utiliserez leboncoin.fr comme source. Si leboncoin ne fonctionne plus vous pouvez vous rabattre sur d'autres sites d'annonces comme lacentrale, paruvendu, autoplus,... Le fichier doit être propre et contenir les infos suivantes : version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier.
Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.

Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.

"""
"""
 <div class="phoneNumber1">
                    <span class="bold">
                05&nbsp;79&nbsp;96&nbsp;18&nbsp;50                <span>  </span>
"""

basedomain = "https://www.lacentrale.fr"
url0 = basedomain
headers = json.loads(open("headersdict", "r").read())
url_template = basedomain+"/listing?energies=elec&makesModelsCommercialNames=RENAULT%3AZOE&sortBy=visitPlaceAsc&regions=FR-NAQ%2CFR-PAC%2CFR-IDF&page={}"

# Generer un cookie de session avec une premiere page ~credible~
jar = requests.cookies.RequestsCookieJar()
response0 = requests.get(url0, headers=headers, cookies=jar) # or post ...
jar.update(response0.cookies)
# ok j'ai mon cookie
# la page principale de recherche
r = requests.get(url_template.format(1), headers=headers, cookies=jar)
# deja recup du nb de pages a scrapper ...
"""
<h2 class="titleNbAds bold sizeC"><span class="numAnn">911</span>
"""
soup = BeautifulSoup(r.content, "html.parser")
nbpages = int(soup.find("h2", class_="titleNbAds").text.split()[0])//16

# debug limit
nbpages = 1

# TBD ajouter une boucle sur les pages


# Debug ... ecriture contenu
#file = open("withheaders.html","w")  
#file.write(r.content.decode("utf-8"))
#file.close

listeannoncespage = soup.findAll("div",class_="adLineContainer")
#for annonce in listeannoncespage:
for annonce in listeannoncespage[0:2]:
	# lien pour les details
	for e2 in elem.findAll("a"):
		if (not(e2.has_attr('href'))): continue
		liendetailvoiture = e2['href']
		break
	# annee
	annee = int(annonce.find("div",class_="fieldYear").text)
	# km
	km = int(annonce.find("div",class_="fieldMileage").text.encode('ascii', 'ignore').__str__()[2:-3])
	# prices
	price = int(annonce.find("div",class_="fieldPrice sizeC").text.encode('ascii', 'ignore').__str__().split('\'')[1])
	# classe pro/partic
	classe = annonce.find("p", class_="txtBlack typeSeller hiddenPhone").text
"""
<div class="adLineContainer">
	<div class="adContainer ">
		<p class="favContainer"><a title="Ajouter l’annonce à vos favoris" rel="nofollow" data-xtclick="{&quot;label&quot;:&quot;Ajout_favoris_ListingPA&quot;,&quot;typeClick&quot;:&quot;action&quot;}"><span class="pictoFavAdd"></span></a>
		</p>
		<a href="/auto-occasion-annonce-69103282517.html" id="E103282517" title="Voir cette annonce de RENAULT ZOE q90 life" class="linkAd ann">
		<div class="contour">
			<div class="imgContent"><img src="https://static.lacentrale.fr/images/lc_fr/listing_nophoto.png" alt="RENAULT ZOE q90 life"></div>
			<div class="subContRight">
				<h3 class="brandModelTitle">
					<span class="brandModel txtGrey3">RENAULT<!-- --> <!-- -->ZOE</span>
					<span class="version txtGrey7C noBold">Q90 LIFE</span>
				</h3>
				<div class="typeSellerGaranty">
					<p class="txtBlack typeSeller hiddenPhone">Professionnel</p>
					<div class="dptLocCont flexBox"><div class="dptCont"><span class="pictoMapPointer"></span> <!-- -->04<!-- -->,</div>
		<span class="localizeItemCont"><div title="Voir la distance de cette annonce" class="localizeItemLink underline floatL pL5" data-xtclick="{&quot;label&quot;:&quot;Partager_sa_location::voir&quot;,&quot;typeClick&quot;:&quot;action&quot;}"><span class="hiddenPhone">Voir la distance</span><span class="onlyPhone">Distance</span></div></span></div></div><div class="vehicleCont"><div class="warranty bold hiddenPhone"><span>Garantie&nbsp;<!-- -->12<!-- -->&nbsp;mois</span></div>

		<div class="kmYearPrice">
			<div class="fieldYear">2015</div>
			<div class="fieldMileage">58&nbsp;495&nbsp;km</div>
			<div class="fieldPrice sizeC"><nobr><span class=""></span><span class="">8&nbsp;290&nbsp;€</span></nobr></div>

</div></div></div></div></a></div></div>
"""
