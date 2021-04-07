
import requests
from bs4 import BeautifulSoup as BS
import os
import csv
from pprint import pprint as pp

#csv files will include following columns from election scraper
#Township code, Township, Registered voters, Envelopes received, Valid votes sum, Parties Votes...

url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2108'

r = requests.get(url)
html = r.text
soup = BS(html, "html.parser")

#List kódů všech obcí
lst_kodu_obci = [kod.text for kod in soup.find_all("td", {"class":"cislo"})]

#List názvů všech obcí - postupně projde všechny tři bloky obcí a sloučí je do jedhono listu
lst_nazvy_obci = []
for i in range(1, 5): #Pro zevšeobecnění počtu bloků názvů obcí, užití try: except IndexError:, které odchytí případné neexistující listy
    try:
        lst_temp = [elem.text for elem in soup.find_all("td", {"headers":f"t{i}sa1 t{i}sb2"})]
    except IndexError:
        pass
    else:
        lst_nazvy_obci.extend(lst_temp)

#list všech obcí - URL odkazů na výsledky voleb v dané obci
lst_obce_odkaz = [elem.a["href"] for elem in soup.find_all("td", {"class":"cislo"})]

#Propojení základního URL s URL obce, na které jsou výsledky
url_obec_0 = 'https://volby.cz/pls/ps2017nss/' + lst_obce_odkaz[0]
r_0 = requests.get(url_obec_0)
html_0 = r_0.text
soup_0 = BS(html_0, "html.parser")

#Registrovaní voliči konkrétní obce - 0
registrovani_volici_0 = soup_0.find("td", {"headers":"sa2"}).text

#Odevzdané obálky konkrétní obce - 0
odevzdane_obalky_0 = soup_0.find("td", {"headers":"sa5"}).text

#Platné hlasy celkem konkrétní obce - 0
platne_obalky_0 = soup_0.find("td", {"headers":"sa6"}).text

#List politických stran konkrétní obce - 0
lst_nazvy_stran = []
for i in range(1,5): #Pro zevšeobecnění počtu bloků názvů stran, užití try: except IndexError:, které odchytí případné neexistující listy
    try:
        lst_temp = [elem.text for elem in soup_0.find_all("td", {"headers":f"t{i}sa1 t{i}sb2"})]
    except IndexError:
        pass
    else:
        lst_nazvy_stran.extend(lst_temp)

#List platných hlasů politických stran
lst_platne_hlasy = []
for i in range(1,5): #Pro zevšeobecnění počtu bloků hlasů, užití try: except IndexError:, které odchytí případné neexistující listy
    try:
        lst_temp = [elem.text for elem in soup_0.find_all("td", {"headers":f"t{i}sa2 t{i}sb3"})]
    except IndexError:
        pass
    else:
        lst_platne_hlasy.extend(lst_temp)

#Vytvoření listu, který bude sloužit jako hlavička - složen z konkrétních oblastí a všech polit. stran
lst_header_first = ['Township code', 'Township', 'Registered voters', 'Envelopes received', 'Valid votes sum']
lst_header = lst_header_first + lst_nazvy_stran

#Vytvoření listu, kde pořadí prvků bude odpovídat pořadí listu hlavičky
lst_values = [lst_kodu_obci[0], lst_nazvy_obci[0], registrovani_volici_0, odevzdane_obalky_0, platne_obalky_0, *lst_platne_hlasy]

#Vytvoření csv souboru pro zápis
path = "C:\\Users\\david\\Desktop\\TestFolder\\test.csv"
if os.path.exists(path):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(lst_values)
else:
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(lst_header)
