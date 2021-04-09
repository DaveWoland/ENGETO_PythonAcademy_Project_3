# ENGETO_PythonAcademy_Project_3
Final project of Engeto Python Academy

**PROJECT DESCRIPTION**

Purpose of this project is to extract the results of the parliamentrary elections in year 2017. Elections link: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ


LIBRARIES INSTALLATION

Libraries, which are used in this project to extrat the data from web are saved in the file requirements.txt. It is convenient to use new virtual environment for Libraries installation. With installed manager you should run it as follows:
WIN:
    pip install requests
    pip install beautifulsoup4

Mac OS:
    python3 -m pip install requests
    python3 -m pip install beautifulsoup4
    
    
HOW TO RUN THE PROJECT

To run the program election_scrapping.py via command line, you need to input two mandatory arguments.
Win Example:
   election_scrapping.py <link_of_township> <name_of_output_file.csv>
        
The results will be extracted and saved as .csv file.


EXAMPLE OF THE PROJECT

Election results of Nymburk Township:
  1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2108
  2. argument: nymburk_results.csv

Running the program:
  election_scrapping.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2108" "nymburk_results.csv"

Process:
  DOWNLOADING... DATA FROM CHOSEN URL:  https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2108
  SAVING DATA TO FILE:  nymburk_results.csv
  ENDING election_scrapping

Partial results:
Township code,Township,Registered voters,Envelopes received,Valid votes sum, Parties names (outputs are their results)...
537021,Běrunice,690,382,382,27,3,0,40,1,28,30,7,4,7,0,0,25,0,6,8,136,1,0,14,0,1,0,1,42,1
537039,Bobnice,666,389,387,37,0,0,33,0,42,31,5,2,3,0,0,27,0,0,23,124,0,1,7,0,0,1,1,50,0
537047,Bříství,268,193,190,26,1,0,18,0,13,12,2,2,1,0,0,16,1,0,3,66,0,0,4,0,3,0,0,22,0
...
