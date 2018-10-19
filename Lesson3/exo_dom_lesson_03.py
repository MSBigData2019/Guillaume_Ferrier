#!/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

#L'exercice pour le cours prochain est le suivant:
#- Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075
#- En utilisant l'API github https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens de stars des repositories qui leur appartiennent.
# Pour finir classer ces 256 contributors par leur note moyenne.﻿

mytoken = 'f09c19c5e3e4a3255483b00ad63199aabba46152'
#Etape 1 Crawler la page suivante pour recuperer les 256 utilisateurs
#https://gist.github.com/paulmillr/2657075
#la page est assez clean et on n'a que ce tableau qui utilse le scope row, cool
##<tr>
##   <th scope="row">#256</th>
##  <td><a href="https://github.com/unicodeveloper">unicodeveloper</a> (Prosper Otemuyiwa)</td>
##  <td>1322</td>    <td>Lagos, Nigeria</td>
##  <td><a target="_blank" rel="noopener noreferrer" href="https://avatars0.githubusercontent.com/u/2946769?s=30&amp;v=4"><img width="30" height="30" src="https://avatars0.githubusercontent.com/u/2946769?s=30&amp;v=4" style="max-width:100%;"></a></td></tr>
def genereurl(user,pagenb):
    return 'https://api.github.com/users/'+user+'/repos?per_page=100&page='+str(pagenb)

soup = BeautifulSoup(requests.get('https://gist.github.com/paulmillr/2657075').content, "html.parser")
thscoperow = soup.findAll("th", {"scope" : "row"})
df = pd.DataFrame(columns=['user','nbrepos','nbstars','avgstars'])

for th in thscoperow:
    nbrepos = 0
    nbstars = 0
    nbpageslues = 1
    nbpagesalire = 1
    # find href = https://github.com/andrew or fabpot
    # username will be transformed into https://api.github.com/users/fabpot/repos
    userquery = th.parent.find('a')['href'].rsplit('/', 1)[1]

    #curl -u username:token https://api.github.com/user
    #GET /users/:username/repos
    # params entree inutiles ... type, sort, direction
    additheaders = {'Authorization': 'token %s' % mytoken}

    r = requests.get(genereurl(userquery,1), headers=additheaders)
    print('debug ',userquery,nbpageslues,r.headers['Status'])
    #Question de la pagination : les headers de la reponse nous donnent s'il y a des elements malgre notre per_page
    # on ne le lit qu'une fois pour eviter de gerer tous les affichages first last prev ...
    # si Link est dans les headers de reponse alors on regarde le dernier chiffre qui est le "last"
    if 'Link' in r.headers:
        # on suppose qu'on n'aura pas plus de 900 repos à parser pour une personne sinon au lieu 1er caractere "[0]"
        #  il faudrait lire jusqu'au ">" en sortie du rsplit
        nbpagesalire = int(r.headers['Link'].rsplit('page=', 1)[1][0])

    # on recup deja le contenu de cette page avant de voir si de la pagination intervient
    repos = json.loads(r.content.decode())
    for repo in repos:
        nbrepos += 1
        nbstars += repo['stargazers_count']

    # si pagination il y a on refait le meme travail
    while nbpageslues < nbpagesalire:
        nbpageslues +=1
        r = requests.get(genereurl(userquery,nbpageslues), headers=additheaders)
        print('debug ',userquery,nbpageslues,r.headers['Status'])
        repos = json.loads(r.content.decode())
        for repo in repos:
            nbrepos += 1
            nbstars += repo['stargazers_count']

#    stargazers_count
#    Link → < https: // api.github.com / user / 1060 / repos?page = 2 >;
#    rel = "next", < https: // api.github.com / user / 1060 / repos?page = 11 >;
#    rel = "last"
    df = df.append({'user': userquery, 'nbrepos': nbrepos, 'nbstars': nbstars, 'avgstars': nbstars/nbrepos if nbrepos else 0 }, ignore_index=True)

# on a tout collecté il n'y a plus qu'à trier
df.sort_values(by='avgstars', ascending=False, inplace=True)

df.to_pickle('sauvegarde.pkl')

#for i in range(len(df)):
#    print(i+1, ' ', df[i]['user'],' (', df[i]['avgstars'], ' avg stars)')

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199

print(df)