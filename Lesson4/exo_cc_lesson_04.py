import requests
urlpara = "https://www.open-medicaments.fr/api/v1/medicaments?limit=100&query=paracetamol"

j = requests.get(urlpara).content
df = pandas.DataFrame.from_records(j)
# ne marche pas
df['precomma'] = df['denomination'].str.split(pat=',',n=1,expand=False)


#https://www.open-medicaments.fr/views/display.html
#autre api details :/api/v1/medicaments/{id}

