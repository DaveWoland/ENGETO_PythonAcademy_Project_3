
import requests
from bs4 import BeautifulSoup as BS
import sys
import os
import csv
from pprint import pprint as pp

#csv file will include following columns from election scraper:
    #Township code, Township, Registered voters, Envelopes received, Valid votes sum, Parties Votes...

url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2108'


def main():
    #URL = sys.argv[1]
    #results_file = town_results.csv
    URL = url
    results_file = "town_results.csv"


    r = requests.get(url)
    html = r.text
    soup = BS(html, "html.parser")

    lst_township_codes = township_codes(soup)

    lst_township_names = township_names(soup)

    lst_township_links_urls = township_link_url(soup)





#List of all Townships codes
def township_codes(html_soup) -> list:
    return [code.text for code in html_soup.find_all("td", {"class":"cislo"})]


#List of all Townships names. Function goes through all blocks of Townships and concatenate them into one
def township_names(html_soup) -> list:
    lst_township_names = []
    for i in range(1, 5): #To generalize the number of lists of Township names (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
        try:
            lst_temp = [elem.text for elem in html_soup.find_all("td", {"headers":f"t{i}sa1 t{i}sb2"})]
        except IndexError:
            pass
        else:
            lst_township_names.extend(lst_temp)

    return lst_township_names


#List of all Townships URL links to election results in concrete Township
def township_link_url(html_soup) -> list:
    return [elem.a["href"] for elem in html_soup.find_all("td", {"class":"cislo"})]






#Concatenation of basic election URL with Township URL, where the results are available
url_township_0 = 'https://volby.cz/pls/ps2017nss/' + lst_township_link_url[0]
r_0 = requests.get(url_township_0)
html_0 = r_0.text
soup_0 = BS(html_0, "html.parser")

#Registered voters of concrete Township - 0
registered_voters_0 = soup_0.find("td", {"headers":"sa2"}).text

#Envelopes received of concrete Township - 0
envelopes_received_0 = soup_0.find("td", {"headers":"sa5"}).text

#Valid votes sum of concrete Township - 0
valid_votes_sum_0 = soup_0.find("td", {"headers":"sa6"}).text

#List of Parties
lst_parties_names = []
for i in range(1,5): #To generalize the number of lists of Parties (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
    try:
        lst_temp = [elem.text for elem in soup_0.find_all("td", {"headers":f"t{i}sa1 t{i}sb2"})]
    except IndexError:
        pass
    else:
        lst_parties_names.extend(lst_temp)

#List of valid votes of Parties
lst_party_valid_votes = []
for i in range(1,5): #To generalize the number of lists of valid Parties votes (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
    try:
        lst_temp = [elem.text for elem in soup_0.find_all("td", {"headers":f"t{i}sa2 t{i}sb3"})]
    except IndexError:
        pass
    else:
        lst_party_valid_votes.extend(lst_temp)

#Creation of list, which will be header in csv file. It consists of concrete required (scrapped) data and all Parties
lst_header_data_required = ['Township code', 'Township', 'Registered voters', 'Envelopes received', 'Valid votes sum']
lst_header = lst_header_data_required + lst_parties_names

#Creation of ordered list, where every item is sorted based on its order in list header
lst_values = [lst_township_codes[0], lst_township_names[0], registered_voters_0, envelopes_received_0, valid_votes_sum_0, *lst_party_valid_votes]

#Creation of csv file for inserting scrapped data
path = "C:\\Users\\david\\Desktop\\TestFolder\\test.csv"
if os.path.exists(path):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(lst_values)
else:
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(lst_header)
