import requests
urlpara = "https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=paracetamol"
urlmed = "https://www.open-medicaments.fr/api/v1/medicaments/{}"
j = requests.get(urlpara).content
df = pandas.DataFrame.from_records(j)

# split ne marche pas ou mal et en plus c'est pas l'exo on voulait des regex
#df['precomma'] = df['denomination'].str.split(pat=',',n=1,expand=False)

# version 1 par 1 ... moche
df['dosage'] = df['denomination'].str.extract(pat=' (\d+) [m]?g',expand=False)
df['unit'] = df['denomination'].str.extract(pat=' \d+ ([m]?g)',expand=False)
df['previrg'] = df['denomination'].str.extract('^(.*),')
df['comprime'] = df['denomination'].str.extract(',(.*)$')

#https://www.open-medicaments.fr/api/v1/medicaments/67445776

# version 2 : recup tous les groupes
df2 = df['denomination'].str.extract('^(.*) (\d+) ([m]?g)[^,]*, (.*)$')
# mais on a pas mal de NaN sur certaines lignes ...
# eg NOVACETOL (ASPIRINE PARACETAMOL), comprimé
df2['mult'] = 1
df2['mult'] = df2['mult'].where(df2[2]=='mg',1000)
# le where conserve la valeur sauf ni test en echec et donc lui remplace l element
# ici tout ce qui n'est pas mg on met 1000 (parcque on sait que c'est g)
df2['dosagehomogene'] = df2[1].fillna(0).astype(int)*df2['mult']

