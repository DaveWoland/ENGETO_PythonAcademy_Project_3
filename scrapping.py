
import requests
from bs4 import BeautifulSoup as BS
from pprint import pprint as pp


#kod, obec, registrovani volici, odevzdane obalky, platne hlasy, politicka strana...

url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2108'

r = requests.get(url)
html = r.text
soup = BS(html, "html.parser")

#výběr dat(kod, obec, odkaz na konkrétní výsledky) pro všechny obce v okr. Nymburk. List o 3 položkách
#data = soup.find_all("div", {"class":'t3'})

#List kódů všech obcí
#lst_kodu_obci = [kod.text for kod in soup.find_all("td", {"class":"cislo"})]

#List názvů všech obcí - postupně projde všechny tři bloky obcí a sloučí je do jedhono listu
# lst_nazvy_obci = []
# for i in range(1, 4):
#     lst_box = [elem.text for elem in soup.find_all("td", {"headers":f"t{i}sa1 t{i}sb2"})]
#     lst_nazvy_obci.extend(lst_box)



#list všech obcí - URL odkazů na výsledky voleb v dané obci
#lst_obce_odkaz = [elem.a["href"] for elem in soup.find_all("td", {"class":"cislo"})]

# lst_obce = []
# for item in lst_obce_temp:
#     if item not in lst_obce:
#         lst_obce.append(item)
#     else:
#         continue
#
#
# url_obec = 'https://volby.cz/pls/ps2017nss/' + lst_obce[0]
# r_o = requests.get(url_obec)
# html_o = r_o.text
# soup_o = BS(html_o, "html.parser")

