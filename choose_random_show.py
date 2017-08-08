#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
from string import strip
import random
import re


SHOW_NAMES_LIST = ["Seinfeld", "Eastbound & Down", "Parks and Recreation",
"BoJack Horseman", "My Name Is Earl", "Reno 911!", "Friends", "American Dad!", 
"The Ren & Stimpy Show", "Squidbillies", "Futurama", "Beavis and Butt-Head",
"The Office (U.S. TV series)", "Check It Out! with Dr. Steve Brule","Family Guy",
"30 Rock", "The Simpsons", "Workaholics", "Bob's Burgers", "Curb Your Enthusiasm", 
"Brooklyn Nine-Nine", "Robot Chicken", "Trailer Park Boys", "Archer", "Aqua Teen Hunger Force", "South Park", "The League", "Modern Family", "Superjail!", "Arrested Development",
"It's Always Sunny in Philadelphia", "King of the Hill"]

SHOW_URLS_LIST = ["https://en.wikipedia.org/wiki/List_of_Seinfeld_episodes",
"https://en.wikipedia.org/wiki/List_of_Eastbound_%26_Down_episodes",
"https://en.wikipedia.org/wiki/List_of_Parks_and_Recreation_episodes",
"https://en.wikipedia.org/wiki/List_of_BoJack_Horseman_episodes",
"https://en.wikipedia.org/wiki/List_of_My_Name_Is_Earl_episodes",
"https://en.wikipedia.org/wiki/List_of_Reno_911!_episodes",
"https://en.wikipedia.org/wiki/List_of_Friends_episodes",
"https://en.wikipedia.org/wiki/List_of_American_Dad!_episodes",
"https://en.wikipedia.org/wiki/List_of_The_Ren_%26_Stimpy_Show_episodes",
"https://en.wikipedia.org/wiki/List_of_Squidbillies_episodes",
"https://en.wikipedia.org/wiki/List_of_Futurama_episodes",
"https://en.wikipedia.org/wiki/List_of_Beavis_and_Butt-Head_episodes",
"https://en.wikipedia.org/wiki/List_of_The_Office_(U.S._TV_series)_episodes",
"https://en.wikipedia.org/wiki/List_of_Check_It_Out!_with_Dr._Steve_Brule_episodes",
"https://en.wikipedia.org/wiki/List_of_Family_Guy_episodes",
"https://en.wikipedia.org/wiki/List_of_30_Rock_episodes",
"https://en.wikipedia.org/wiki/List_of_The_Simpsons_episodes",
"https://en.wikipedia.org/wiki/List_of_Workaholics_episodes",
"https://en.wikipedia.org/wiki/List_of_Bob%27s_Burgers_episodes",
"https://en.wikipedia.org/wiki/List_of_Curb_Your_Enthusiasm_episodes",
"https://en.wikipedia.org/wiki/List_of_Brooklyn_Nine-Nine_episodes",
"https://en.wikipedia.org/wiki/List_of_Robot_Chicken_episodes",
"https://en.wikipedia.org/wiki/List_of_Trailer_Park_Boys_episodes", 
"https://en.wikipedia.org/wiki/List_of_Archer_episodes", 
"https://en.wikipedia.org/wiki/List_of_Aqua_Teen_Hunger_Force_episodes",
"https://en.wikipedia.org/wiki/List_of_South_Park_episodes",
"https://en.wikipedia.org/wiki/List_of_The_League_episodes",
"https://en.wikipedia.org/wiki/List_of_Modern_Family_episodes",
"https://en.wikipedia.org/wiki/List_of_Superjail!_episodes",
"https://en.wikipedia.org/wiki/List_of_Arrested_Development_episodes",
"https://en.wikipedia.org/wiki/List_of_It%27s_Always_Sunny_in_Philadelphia_episodes",
"https://en.wikipedia.org/wiki/List_of_King_of_the_Hill_episodes"]

#Global variables
selected_episode = -1
page_content = ""
SPECIAL_EPISODES = ["Beavis and Butt-Head","Eastbound & Down"]



# Tinkering
random.seed()
#print "SHOWN_NAMES_LIST has " + str(len(SHOW_NAMES_LIST)) + " items."
#print "SHOW_URLS_LIST has " + str(len(SHOW_URLS_LIST)) + " items."
assert len(SHOW_NAMES_LIST) == len(SHOW_URLS_LIST)


#Ask user which show he or she wants to watch
print "Enter the number of the show you would like to watch below:"
for i in range(len(SHOW_NAMES_LIST)):
    print str(i) + " - " + SHOW_NAMES_LIST[i] 
    
    #Get number from user
try:
    selected_episode = int(raw_input('Episode Number:'))
except ValueError:
    print "Not a number"
    
while selected_episode > len(SHOW_NAMES_LIST) or selected_episode < 0:
    print "Episode " + str(selected_episode) + " is not valid. Please select again."
    try:
        selected_episode = int(raw_input('Episode Number:'))
    except ValueError:
        print "Not a number"

selected_episode_name = SHOW_NAMES_LIST[selected_episode]
print "You chose " + selected_episode_name


#Get from wikipedia, page with list of shows
url = SHOW_URLS_LIST[selected_episode]
print "Getting " + url + " ... "
response = requests.get(url)
assert response.status_code == 200
#print "response code was " + str(response.status_code)
page_content = response.content


#Parse the wikipedia page for all show items (with title, season, episode number)
soup = BeautifulSoup(page_content, 'html.parser')
#print soup.prettify()

#Find all <table class="wikitable plainrowheaders" .... tags, and store them in a tables variable
table_candidates = soup.findAll("table", { "class":"wikitable plainrowheaders"})
table_candidates = soup.findAll("table", { "class":"wikiepisodetable"}) + table_candidates

if selected_episode_name == "The Simpsons":
    response = requests.get("https://en.wikipedia.org/wiki/List_of_The_Simpsons_episodes*#Episodes")
    page2_content = response.content
    soup2 = BeautifulSoup(page2_content, 'html.parser')
    table_candidates = soup2.findAll("table", { "class":"wikitable plainrowheaders"}) + table_candidates
    table_candidates = soup2.findAll("table", { "class":"wikiepisodetable"}) + table_candidates

    

tables = []
for table in table_candidates:
    header_record = table.find("tr") #get first table record which has headers
    #print header_record.prettify()
    th_elements = header_record.findAll("th")
    if len(th_elements) > 2 and strip(th_elements[2].text) == "Title":
        #print th_elements[2].text
        tables.append(table)
    elif selected_episode_name in SPECIAL_EPISODES and len(th_elements) > 1 and strip(th_elements[1].text) == "Title":
        tables.append(table)

# For each table, find all tr items
table_lengths = {}
i = 0
table_records = []
for table in tables:
    table_record_candidates = table.findAll("tr", {"class":"vevent"})
    #print table_record_candidates
    table_records += table_record_candidates
    table_lengths[i] = len(table_record_candidates)
    i += 1

print selected_episode_name + " has " + str(len(tables)) + " seasons and " + str(len(table_records)) + " total episodes "


def find_season(ep_title):
    season_name = ""
#    print "looking for " + ep_title[:-5] + " in soup ..." 
    title_td = soup.find('td', text = re.compile(re.escape(ep_title[:-4])))
    if not title_td:
        season_name = "UNK"
    try:
        table = title_td.findParent("table") # Should be table tag
        if not table or table.name != "table":
            season_name = "UNK"
        h3 = table.findPrevious("h3")
        if h3.name != "h3":
            season_name = "UNK"
        try:
            season_name = h3.span.text
        except:
            season_name = "UNK" 
    except:
        season_name = "UNK"
    #print "returning " + season_name
    return season_name

#Build episode list
episodes = []
for record in table_records:
    episode = {}
    column_th = record.find("th")
    if not column_th:
        continue
    column_th = strip(column_th.text)
    # while not isinstance( column_th, ( int, long ) ):
#         try:
#             column_th = int(column_th)
#         except:
#             column_th = column_th[0:len(column_th)-1]
    
    record_tds = record.findAll("td")

    episode["num_in_series"] = strip(column_th) if selected_episode_name not in SPECIAL_EPISODES else record_tds[0].text

    episode["num_in_season"] = record_tds[0].text if selected_episode_name not in SPECIAL_EPISODES else strip(column_th)
    
    episode["title"] = record_tds[1].text if selected_episode_name not in SPECIAL_EPISODES else record_tds[0].text
    
    
    
    #print "season is " + str(find_season(episode["column_th"]))
    episode["season"] = find_season(episode["title"]).encode('ascii','ignore')
#    print "Season is " + episode["season"]
    episodes.append(episode)
#     episode["num_in_series"].encode('ascii','ignore')
#     episode["num_in_season"].encode('ascii','ignore')
#     episode["title"].encode('ascii','ignore')
    i += 1
    #print episode["num_in_season"] + " " + episode["title"]

#Determine number of episodes
N_episodes = len(table_records)

#Generate random number between 1 and number of episodes
random_show_number = int(round(random.uniform(0, N_episodes)))

#Give user the nth episode title, season and episode number 
chosen_episode = episodes[random_show_number]
print "The episode of '" + selected_episode_name + "' you will watch is \n\t" \
+ chosen_episode["title"] + "\n which is Episode " + chosen_episode["num_in_season"] +   " of Season " + chosen_episode["season"]