from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen
from colorthief import ColorThief
import csv

ufs = ["ac", "al",]

#ufs = ["ac", "al", "am", "ap", "ba", "ce", "df", "es", "go", "ma", "mg", "ms", "mt", "pa", "pb", "pe", "pi", "pr", "rj", "rn", "ro", "rr", "rs", "sc", "se", "sp", "to"]
data_arr = []
data_csv_arr = []
data_csv = ''

def data(uf):

    url = f"https://www.ibge.gov.br/cidades-e-estados/{uf}/"

    images = []

    try:
        html = urlopen(url)
    except:
        error = {'erro' : '404 - not found'}
        return error

    soup = BeautifulSoup(html, 'lxml')

    indicador_tag = soup.find_all('div', {"class" : "indicador"})

    labels_txt = []
    values_txt = []
    data = []

    for tag in indicador_tag:
        labels = tag.find_all('div', {"class": "ind-label"})
        values = tag.find_all('p', {"class": "ind-value"})

        label_txt = ''
        value_txt = ''

        for label in labels:
           label_txt = label.find('p').text.strip()
        
        for value in values:
            value_tag = value.get_text(strip=True, separator=' ')
            value_txt = value_tag.split()[0]

        data.append({label_txt: value_txt})
       
    data_arr.append(data)
    #print(data)

for uf in ufs:
    data(uf)

csv_file = 'output.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write headers
    headers = data_arr[0][0].keys()  # Assuming the first dictionary in the first array has all keys
    writer.writerow(headers)
    
    # Write data rows
    for sublist in data_arr:
        row = [item[next(iter(item))] for item in sublist]  # Extract values in the order of headers
        writer.writerow(row)

print(f"Data has been written to {csv_file}")

#print(data_arr)
