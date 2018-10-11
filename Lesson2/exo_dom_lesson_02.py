#!/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# Je vous demande donc de récupérer les infos suivantes :
# * les ventes au quartier à fin décembre 2018
# * le prix de l'action et son % de changement au moment du crawling
# * le % Shares Owned des investisseurs institutionels
# * le dividend yield de la company, le secteur et de l'industrie

# pour les sociétés suivantes : Airbus, LVMH et Danone.
inputlist = ["Airbus", "LVMH", "Danone"]

# Un exemple de page https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA.
basesite='https://www.reuters.com'
rootSearchUrl = '/search/news?sortBy=&dateRange=&blob='
rootFinanceUrl= '/finance/stocks/financial-highlights/'

def recherche_stock_url(query):
    #TODO ajouter un htmlencode sur query
    soup = BeautifulSoup(requests.get(basesite+rootSearchUrl+query).content, "html.parser")

#page de retour de la recherche en :
#<div id="quoteKeymatch">
#[<div class=" :  module module-content search-stock
#<div class="search-stock-ticker">
#<a href="/finance/stocks/overview/AIR.PA">
# lien resolu https://www.reuters.com/finance/stocks/overview/AIR.PA
# onglet utile ensuite https://www.reuters.com/finance/stocks/financial-highlights/AIR.PA

    urlrelative = soup.find("div",class_="search-stock-ticker").findNext()["href"]
    # V1 regexp remplace, V2 todo extraire le code url et generer l'url
    urlongletfinance = re.sub(r'overview','financial-highlights',urlrelative)

    return basesite+urlongletfinance

# TODO FOR sur array de compagnies
compname = 'airbus'

#print("DEBUG URL",recherche_stock_url(compname))

def parsealldataurl(query):
    urlcontent = recherche_stock_url(query)
    soup = BeautifulSoup(requests.get(urlcontent).content, "html.parser")

# * les ventes au quartier à fin décembre 2018

#<tbody>
#		<tr>
#			<th>&nbsp;</th>
#			<th class="data"># of Estimates</th>
#			<th class="data">Mean</th>
#			<th class="data">High</th>
#			<th class="data">Low</th>
#			<th class="data">1 Year&nbsp;Ago</th>
#		</tr>
#<tr>
#			<td colspan="6" class="dataTitle">SALES (in millions)</td>
#		</tr>
#	<tr class="stripe">
#	  	<td>Quarter Ending&nbsp;Dec-18</td>
#			<td class="data">5</td>
#			<td class="data">23,493.00</td>
#			<td class="data">26,073.40</td>
#			<td class="data">21,431.00</td>
#			<td class="data">--</td>
#		</tr>

#sales = soup.find("td",string="SALES (in millions)")
#print(sales.parent.findNext('tr').select('td.data'))

    # TODO gestion unicode/hmtl voir comment rechercher dans le texte qu'il a lui où il a remplacé le html par de l'unicode
    quarterfirstelemP = soup.find("td", string="Quarter Ending"+u'\xa0'+"Dec-18")
    #quarterfirstelem = soup.find("td", text="Quarter Ending&nbsp;Dec-18")

    # pourquoi next_sibling(s) marche pas ???
    # On part de quarter ending text et on remonte au parent (tr?) pour aller chercher le 3e TD
    #   quarterdec18 = quarterfirstelemP.parent.find_all('td')[2].string.strip()
    #ah si mais c'est via un find pas via l'attribut pfffffff
    # du coup on est bon on recupere le second voisin vu que la colonne intermediaire est inutile
    quarterdec18 = quarterfirstelemP.find_next_siblings()[1].string.strip()

    # TODO voir si ya moyen de recuperer la position de la colonne d apres le header... trop long
    # TODO : filtres et accesseurs quelle difference entre .string ou .text ou .get_text() ?

# * le prix de l'action et son % de changement au moment du crawling
#<div class="sectionQuote nasdaqChange">
#<div class="sectionQuoteDetail">
#				<span class="nasdaqChangeHeader">
#				AIR.PA on Paris Stock Exchange</span>
#				<br class="clear"><br class="clear">
#				<span style="font-size: 23px;">
#				98.99</span><span>EUR</span><br>
#				<span class="nasdaqChangeTime">10 Oct 2018</span>
#			</div>
#on part du quotedetail et on cherche le 2e span en dessous
    prixaction = soup.find("div", class_="sectionQuote nasdaqChange").find_all("span")[1].text.strip()
#<div class="sectionQuote priceChange">
#<div class="sectionQuoteDetail">
#				<span class="priceDetail">
#				    Change	(% chg)</span>
#				<br class="clear"><br class="clear">
#				<span class="valueContent">
#				    <span class="neg">
#						    --</span>
#					<span class="valueContentPercent">
#					        <span class="neg">
#					            (--)
#					        </span>
#					</span>
#				</span>
#				</div>

#on part du priceChange et on cherche le 5e span...
    pourcentchg = soup.find("div", class_="sectionQuote priceChange").find_all("span")[4].text.strip()

# * le % Shares Owned des investisseurs institutionels
#<div class="module">
#
#		<div class="moduleHeader">
#				<h3>
#					Institutional Holders</h3>
#			</div>
#		<div class="moduleBody">
#		<table class="dataTable" width="100%" cellspacing="1" cellpadding="0">
#<tbody class="dataSmall">
#	<tr class="stripe">
#		<td><strong>% Shares Owned:</strong></td>
#		<td class="data">20.57%</td>
#	</tr>

# on a ptet plus de pollution dans la page et ces mots qui reviennent alors on va donner un niveau de plus de recherche : les h3
# et j'ai pas le texte exact vu qu'il y a pleins d'espaces et de retours à la ligne donc regexp
    ih = soup.find("h3", text=re.compile('Institutional Holders'))
    # sharesowned = ih.parent.parent.find("td",text=re.compile('% Shares Owned:')).parent.find("td",class_='data').string.strip()
    # pareil plus la peine de remonter on peut aller chopper les voisins
    sharesowned = ih.parent.parent.find("td",text=re.compile('% Shares Owned:')).find_next_sibling().string.strip()


## * le dividend yield de la company, le secteur et de l'industrie

#		<div class="moduleHeader">
#				<h3>
#					Dividends</h3>
#			</div>
#		<div class="moduleBody">
#		<table class="dataTable" width="100%" cellspacing="0" cellpadding="1">
#	<tbody>
#		<tr>
#			<th width="40%">&nbsp;</th>
#			<th class="data" width="15%"><strong>Company</strong></th>
#			<th class="data" width="15%"><strong>industry</strong></th>
#			<th class="data" width="15%"><strong>sector</strong></th>
#		</tr>
#		<tr class="stripe">
#			<td>Dividend Yield</td>
#			<td class="data">2.90</td>
#			<td class="data">2.78</td>
#			<td class="data">2.48</td>
#		</tr>
    # dytab = soup.find("h3", text=re.compile('Dividends')).parent.parent.find("td",string='Dividend Yield').parent.find_all("td")
    # companyyield = dytab[1].text.strip()
    # industryyield = dytab[2].text.strip()
    # sectoryield = dytab[3].text.strip()
    dytab = soup.find("h3", text=re.compile('Dividends')).parent.parent.find("td",string='Dividend Yield').find_next_siblings()
    companyyield = dytab[0].text.strip()
    industryyield = dytab[1].text.strip()
    sectoryield = dytab[2].text.strip()

    # c'est bon on renvoit toutes infos
    return ( query, quarterdec18, prixaction, pourcentchg, sharesowned, companyyield, sectoryield, industryyield )



# Ya plus qu'a lancer les appels
alldataarray = []
for company in inputlist:
    alldataarray.append(parsealldataurl(company))

# et aussi afficher quand meme ...
df = pd.DataFrame(alldataarray, columns=['Company', 'QuarterDec18', 'Price', '%chang', 'SharesOwned',
                                         'Company Yield', 'Sector Yield', 'Industry Yield'])
pd.option_context("display.max_rows",None,"display.max_columns", None)

print(df.to_string(index=False))

