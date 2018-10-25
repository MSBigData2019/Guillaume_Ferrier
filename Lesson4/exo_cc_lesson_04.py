import requests
urlpara = "https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=paracetamol"
urlmed = "https://www.open-medicaments.fr/api/v1/medicaments/{}"
j = requests.get(urlpara).content
df = pandas.DataFrame.from_records(j)

# ne marche pas
#df['precomma'] = df['denomination'].str.split(pat=',',n=1,expand=False)
df['dosage'] = df['denomination'].str.extract(pat=' ([0-9]*) [mk]+g',expand=False)
df['unit'] = df['denomination'].str.extract(pat=' [0-9]* ([mk]+g)',expand=False)

df['previrg'] = df['denomination'].str.extract('^(.*),')
df['comprime'] = df['denomination'].str.extract(',(.*)$')

#https://www.open-medicaments.fr/views/display.html
#autre api details :

#https://www.open-medicaments.fr/api/v1/medicaments/67445776

