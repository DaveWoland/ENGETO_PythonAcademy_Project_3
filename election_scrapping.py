
import requests
import sys
from bs4 import BeautifulSoup as BS
import csv


#csv file will include following columns from election scraper:
#Township code, Township, Registered voters, Envelopes received, Valid votes sum, Parties - Votes...


def main():

    #Checking correct argv inputs
    try:
        URL = sys.argv[1]
        results_file = sys.argv[2]
    except:
        print("Missing argument!")
        exit()


    CORE_URL = 'https://volby.cz/pls/ps2017nss/'

    #Creating main data list, its purpose is to collect continuously all scrapped data (lists), and at the end insert it into csv as list of lists
    lst_all_collected_data = []


    #Checking correct link input
    try:
        r = requests.get(URL)
        html = r.text
        soup = BS(html, "html.parser")
    except requests.RequestException:
        print("Connection error!")
        exit()
    else:
        print("DOWNLOADING... DATA FROM CHOSEN URL: ", URL)


    #Townships codes creation, appending to main data list
    lst_townships_codes = township_codes(soup)
    lst_all_collected_data = [[elem] for elem in lst_townships_codes]


    #Townships names creation, appending to main data list (using defined function)
    lst_townships_names = township_names(soup)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_townships_names)


    #Extraction of links of Townships, creation of url links to go a level deeper to extract concrete election data
    lst_townships_links = townships_links(soup)
    lst_townships_urls = townships_urls(CORE_URL, lst_townships_links)


    #Extracting registered_voters, envelopes_received, valid_votes_sum and Parties votes for one Township for each loop iteration.

    #Creation of temporary lists as mid step: due to return of some non-digit values when numbers are greater than 999
    #Temporary lists will be itterated, in case of non-numeral value found, non-digit part will be replaced with ''(empty string), and then all values stored in new lists

    lst_registered_voters_temp = []
    lst_envelopes_received_temp = []
    lst_valid_votes_sum_temp = []

    lst_party_valid_votes = [] #All votes outputs are digits, so no need to do the mid step with checking-clearing non-digit values

    for link in lst_townships_urls:
        r_ = requests.get(link)
        html_ = r_.text
        soup_ = BS(html_, "html.parser")

        #Extracting temporary data
        lst_registered_voters_temp.append(soup_.find("td", {"headers": "sa2"}).text)
        lst_envelopes_received_temp.append(soup_.find("td", {"headers": "sa5"}).text)
        lst_valid_votes_sum_temp.append(soup_.find("td", {"headers": "sa6"}).text)

        lst_party_valid_votes.append(parties_votes(soup_))

    #Creating clean registered voters, appending to main data
    lst_registered_voters = clear_number(lst_registered_voters_temp)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_registered_voters)


    #Creating clean envelopes received, appending to main data
    lst_envelopes_received = clear_number(lst_envelopes_received_temp)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_envelopes_received)


    #Creating clean valid votes, appending to main data
    lst_valid_votes_sum = clear_number(lst_valid_votes_sum_temp)
    lst_all_collected_data = append_to_main_list(lst_all_collected_data, lst_valid_votes_sum)


    #Appending Parties votes to main data list => completing main list of lists for csv file
    for i in range(len(lst_all_collected_data)):
        lst_all_collected_data[i].extend(lst_party_valid_votes[i])


    #csv header - part of Parties names
    #List of Parties -> as every Township has the same Parties, it is enough to pull just one list from any Township
    lst_parties_names = []
    for i in range(1,8):  #To generalize the number of lists of Parties (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
        try:
            lst_temp = [elem.text for elem in soup_.find_all("td", {"headers": f"t{i}sa1 t{i}sb2"})]
        except IndexError:
            pass
        else:
            lst_parties_names.extend(lst_temp)


    #Creating list for csv header
    lst_election_header = ['Township code', 'Township', 'Registered voters', 'Envelopes received', 'Valid votes sum', *lst_parties_names]


    print("SAVING DATA TO FILE: ", results_file)


    #Saving all the data into csv file
    with open(results_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(lst_election_header)
        writer.writerows(lst_all_collected_data)


    print("ENDING election_scrapping")



#FUNCTIONS DEFITIONS

#List of all Townships codes
def township_codes(html_soup) -> list:
    return [code.text for code in html_soup.find_all("td", {"class":"cislo"})]


#Help function, which purpose is to append new scrapped data into main data list
def append_to_main_list(main_list: list, append_list: list) -> list:
    for i in range(len(main_list)):
        main_list[i].append(append_list[i])
    return main_list


#List of all Townships names. Function itterates through all blocks of Townships and concatenate them into one
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


#Concatenation of basic election URL with Townships links (where the results are available)
def townships_urls(main_page_url: str, links: list) -> list:
    return [main_page_url + item for item in links]


#Function for clearing non-numerical values in extracted numbers
def clear_number(lst: list) -> list:
    return [item.replace('\xa0', '') for item in lst]


#Function for valid votes of Parties
def parties_votes(html_soup) -> list:
    lst_party_valid_votes = []
    for i in range(1,8): #To generalize the number of lists of valid Parties votes (if there would be more than 3 lists) I use try: except IndexError:, which  should cover non-existed lists
        try:
            lst_temp = [elem.text for elem in html_soup.find_all("td", {"headers":f"t{i}sa2 t{i}sb3"})]
        except IndexError:
            pass
        else:
            lst_party_valid_votes.extend(lst_temp)

    return lst_party_valid_votes


#Running the script
if __name__ == "__main__":
    main()

