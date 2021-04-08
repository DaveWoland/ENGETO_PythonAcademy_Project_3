
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
    core_url = 'https://volby.cz/pls/ps2017nss/'

    #Purpose of this main data list is to collect continuously all scrapped data (lists),
    # and at the end insert it into csv as list of lists
    lst_all_collected_data = []


    r = requests.get(url)
    html = r.text
    soup = BS(html, "html.parser")


    #Townships codes creation, appending to main data list
    lst_townships_codes = township_codes(soup)
    lst_all_collected_data = [[elem] for elem in lst_townships_codes]


    #Townships names creation, appending to main data list
    lst_townships_names = township_names(soup)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_townships_names)


    #Extract of links of Townships, creation of url links to go level deeper to extract concrete election data
    lst_townships_links = townships_links(soup)
    lst_townships_urls = townships_urls(core_url, lst_townships_links)


    #Extracting registered_voters, envelopes_received, valid_votes_sum in at once during loop iteration through all Townships_urls

    #Creation of temporary lists as mid step: due to return of some non-numeral values when numbers are greater than 999
    #Temporary lists will be itterated, in case non-numeral value the part will be replaced with ''(empty) and alle stored in new lists

    lst_registered_voters_temp = []
    lst_envelopes_received_temp = []
    lst_valid_votes_sum_temp = []

    for link in lst_townships_urls:
        r_ = requests.get(link)
        html_ = r_.text
        soup_ = BS(html_, "html.parser")

        lst_registered_voters_temp.append(soup_.find("td", {"headers": "sa2"}).text)
        lst_envelopes_received_temp.append(soup_.find("td", {"headers": "sa5"}).text)
        lst_valid_votes_sum_temp.append(soup_.find("td", {"headers": "sa6"}).text)


    #List of registered voters, appending to main data
    lst_registered_voters = clear_number(lst_registered_voters_temp)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_registered_voters)

    #List of envelopes received, appending to main data
    lst_envelopes_received = clear_number(lst_envelopes_received_temp)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_envelopes_received)

    #List of valid votes, appending to main data
    lst_valid_votes_sum = clear_number(lst_valid_votes_sum_temp)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_valid_votes_sum)

    pp(lst_all_collected_data)





    # List of Parties, as every Township has same Parties, it is enough just to pull the list from the first Township
    # lst_parties_names = []
    # for i in range(1,
    #                5):  # To generalize the number of lists of Parties (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
    #     try:
    #         lst_temp = [elem.text for elem in soup_0.find_all("td", {"headers": f"t{i}sa1 t{i}sb2"})]
    #     except IndexError:
    #         pass
    #     else:
    #         lst_parties_names.extend(lst_temp)











#List of all Townships codes
def township_codes(html_soup) -> list:
    return [code.text for code in html_soup.find_all("td", {"class":"cislo"})]


#Help function, which purpose is to append new scrapped data into main data list
def append_to_main_list(main_list: list, append_list: list) -> list:
    for i in range(len(main_list)):
        main_list[i].append(append_list[i])
    return main_list


#List of all Townships names. Function goes through all blocks of Townships and concatenate them into one
def township_names(html_soup) -> list:
    lst_township_names = []
    for i in range(1, 8): #To generalize the number of lists of Township names (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
        try:
            lst_temp = [elem.text for elem in html_soup.find_all("td", {"headers":f"t{i}sa1 t{i}sb2"})]
        except IndexError:
            pass
        else:
            lst_township_names.extend(lst_temp)

    return lst_township_names


#List of all Townships URL links to election results in concrete Township
def townships_links(html_soup) -> list:
    return [elem.a["href"] for elem in html_soup.find_all("td", {"class":"cislo"})]


#Concatenation of basic election URL with Townships links, where the results are available
def townships_urls(main_page_url: str, links: list) -> list:
    return [main_page_url + item for item in links]


#Function for clearing non-numerical values in extracted numbers
def clear_number(lst: list) -> list:
    return [item.replace('\xa0', '') for item in lst]

main()













#
# #List of Parties
# lst_parties_names = []
# for i in range(1,5): #To generalize the number of lists of Parties (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
#     try:
#         lst_temp = [elem.text for elem in soup_0.find_all("td", {"headers":f"t{i}sa1 t{i}sb2"})]
#     except IndexError:
#         pass
#     else:
#         lst_parties_names.extend(lst_temp)
#
# #List of valid votes of Parties
# lst_party_valid_votes = []
# for i in range(1,8): #To generalize the number of lists of valid Parties votes (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
#     try:
#         lst_temp = [elem.text for elem in soup_0.find_all("td", {"headers":f"t{i}sa2 t{i}sb3"})]
#     except IndexError:
#         pass
#     else:
#         lst_party_valid_votes.extend(lst_temp)
#
# #Creation of list, which will be header in csv file. It consists of concrete required (scrapped) data and all Parties
# lst_header_data_required = ['Township code', 'Township', 'Registered voters', 'Envelopes received', 'Valid votes sum']
# lst_header = lst_header_data_required + lst_parties_names
#
# #Creation of ordered list, where every item is sorted based on its order in list header
# lst_values = [lst_township_codes[0], lst_township_names[0], registered_voters_0, envelopes_received_0, valid_votes_sum_0, *lst_party_valid_votes]
#
# #Creation of csv file for inserting scrapped data
# path = "C:\\Users\\david\\Desktop\\TestFolder\\test.csv"
# if os.path.exists(path):
#     with open(path, "a", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(lst_values)
# else:
#     with open(path, "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(lst_header)
