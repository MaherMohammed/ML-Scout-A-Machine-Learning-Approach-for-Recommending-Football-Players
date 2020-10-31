import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import Request, urlopen ## to open the url
from bs4 import BeautifulSoup as soup
import requests
from selenium import webdriver

germanyyy = pd.read_csv('german.csv',encoding = 'latin-1')
transfermarkt = pd.read_csv('transfermarkt.csv' , encoding = 'latin-1')
teams = pd.read_json('teams.json')
players = pd.read_json('players.json')
list_of_positions = ['Goalkeeper' , 'Centre-Back' , 'Left-Back' , 'Right-Back' , 'Defensive Midfield' , 'Central Midfield' , 'Attacking Midfield',
                      'Left Winger' , 'Right Winger' , 'Centre-Forward' , 'Left Midfield']
def get_teams_in_certain_area(league):
    returned_list = []
    index = 0
    while index < len(teams):
        if teams['area'][index]['name'] == league and teams['type'][index] != 'national':
            returned_list.append([teams['name'][index] , teams['wyId'][index]])
        index += 1
    return returned_list
def get_players_of_team(teamName):
    string_teamId = str(teams[teams['name'] == teamName]['wyId']).split()[1]
    playersLocal = players[players['currentTeamId'] == int(string_teamId)]['wyId'].tolist()
    #playersInternational = players[players['currentNationalTeamId'] == int(string_teamId)]['wyId']
    if len(playersLocal) == 0:
        return 'Team is not Local'
    else:
        index = 0
        while index < len(playersLocal):
            fn = players[players['wyId'] == playersLocal[index]]['firstName'].tolist()
            ln = players[players['wyId'] == playersLocal[index]]['lastName'].tolist()
            role = players[players['wyId'] == playersLocal[index]]['role'].tolist()[0]['name']
            #print(fn[0] ,ln[0] , identify_position_of_the_player(playersLocal[index]) , role)
            index += 1
        return playersLocal
  
    

def get_clubs():
    returned_list = []
    names = teams[teams['type'] == 'club']['name'].tolist()
    ids = teams[teams['type'] == 'club']['wyId'].tolist()
    
    index = 0
    while index < len(names):
        lst = [names[index] , ids[index]]
        returned_list.append(lst)
        index += 1
    return returned_list




my_url = 'https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query=Moustapha+Elhadji+Diallo&x=0&y=0'


browser = webdriver.Edge(executable_path = 'E:\guc\Semster 8\edge driver\driver\msedgedriver.exe')
browser.get(my_url)


html = browser.page_source
page_soup = soup(html, 'html.parser')
containers = page_soup.findAll("input" , {"class":"header-suche"})
containers.string = 'sdaads'
containers[0]['value'] = 'dsda'
containers
ff = page_soup.findAll("input" , {"class":"header-suche-abschicken"})
ff[0].click()

html = browser.page_source
page_soup = soup(html, 'html.parser')
containers = page_soup.findAll("table" , {"class":"inline-table"})
container = containers[0]
container.tr.img['title']
values = page_soup.findAll("td" , {"class":"rechts hauptlink"})
values[0].getText().replace('\xa0\xa0' , '')

file_name = 'transfermarkt.csv'
f= open(file_name , 'w')
headers = "name,position,value,teamName,teamId\n"
f.write(headers)
f.close()

ger = 'german.csv'
f= open(ger , 'w')
headers = "name,position,value,teamName,teamId\n"
f.write(headers)
f.close()


ita = 'italy.csv'
f = open(ita , 'w')
headers = "name,position,value,teamName,teamId\n"
f.write(headers)
f.close()



f= open(ger , 'a')
index = 0
while index < len(containers):
    container = containers[index]
    name = container.tbody.tr.img['title']
    body = container.tbody
    pos = ''
    for tr in body:
        if tr.getText() in list_of_positions:
            pos = tr.getText()
    value = values[index].getText()
    #print(name)
    f.write(str(name) + ',' + str(pos) + ',' + str(value) + ',' + 'RB Leipzig' + ',' + '2975' + '\n')
    index += 1
f.close()



germanyyy = pd.read_csv('german.csv',encoding = 'latin-1')

get_teams_in_certain_area('Italy')

teams[teams['wyId'] == 3789]['officialName']


germanyyy['name']

type(containers[0].tbody.tr.img['title'])


f= open(ger , 'a')
container = containers[0]
name = container.tbody.tr.img['title']
body = container.tbody
pos = ''
for tr in body:
    if tr.getText() in list_of_positions:
        pos = tr.getText()
value = values[0].getText()
print(name)
f.write(str(name) + ',' + str(pos) + ',' + str(value) + ',' + 'Borussia Mönchengladbach' + ',' + '2454' + '\n')

f.close()


#b = containers[-1].tbody
#containers[-1].tbody.tr.img['title']
#for tr in b:
#    if tr.getText() in list_of_positions:
#        print(tr.getText())
#
##browser.get(my_url)
#index = 10
#while index < 21:
#    page = str(index)
#    element = browser.find_elements_by_link_text(page)
#    element[0].click()
#    time.sleep(4)
#    html = browser.page_source # now this has new reviews on it
#    page_soup = soup(html, 'html.parser')
#    containers = page_soup.findAll("table" , {"class":"inline-table"})
#    
#    
#    file_name = 'players_stats.csv'
#    f= open(file_name , 'a')
#    
#    for container in containers:
#        name = container.tr.img['title']
#        position = 'Goalkeeper'
#        f.write(name + ',' + position + '\n')
#        
#    f.close()
#    index += 1
#
#req = Request(my_url)
#page_html = urlopen(req).read()
#req.close()
#
#element = browser.find_elements_by_link_text("2")
#element[0].click()
#html = browser.page_source # now this has new reviews on it
#page_soup = soup(html, 'html.parser')
#containers = page_soup.findAll("table" , {"class":"inline-table"})
#containers[0]
#    
#file_name = 'players_stats.csv'
#f= open(file_name , 'a')
#    
#for container in containers:
#    name = container.tr.img['title']
#    position = 'Center Forward'
#    f.write(name + ',' + position + '\n')
#        
#f.close()
#
#
#
#

def first_last_names_in_list(fn , ln):
    fn = fn.encode('latin-1').decode('unicode-escape','ignore')
    ln = ln.encode('latin-1').decode('unicode-escape','ignore')
    
    returned_list = []
    
    fnList = fn.split()
    lnList = ln.split()
    
    index = 0
    while index < len(fnList):
        returned_list.append(fnList[index])
        index += 1
    
    index = 0
    while index < len(lnList):
        returned_list.append(lnList[index])
        index += 1
    
    return returned_list


def is_matching_name(lst_from_players_dataset , lst_from_data_dataset):
    string_from_players = lst_from_players_dataset[0]
    
    
    index = 1
    while index < len(lst_from_players_dataset):
        string_from_players = string_from_players + ' ' + lst_from_players_dataset[index]
        index += 1
    
    if lst_from_data_dataset[0][-1] == '.':
        lst_from_data_dataset[0] = lst_from_data_dataset[0][0:-1]
        
    
    counter = 0
    index = 0
    while index < len(lst_from_data_dataset):
        if lst_from_data_dataset[index] in string_from_players:
            counter += 1
        index += 1
    return counter == len(lst_from_data_dataset)


def search_in_transfermarkt_dataSet(playerNameList):
    dataNames = transfermarkt['name'].tolist()
    dataPos = transfermarkt['position'].tolist()
    found = False
    index = 0
#    print(dataNames[0])
    while index < len(dataNames):
        print(dataNames[index])
        if is_matching_name(playerNameList , dataNames[index].split()):
            found = True
            break
        index += 1
    if found:
        return dataPos[index]
    else:
        return 'not found'

def get_players_in_team_by_teamId(teamId):
    players_IDs = players[players['currentTeamId'] == teamId]['wyId'].tolist()
    return players_IDs

def get_players_of_team_in_transferMarkt(teamId):
    return transfermarkt[transfermarkt['teamId'] == teamId]['name']

def get_positions_of_players_in_team_transfermarkt(teamId):
    return transfermarkt[transfermarkt['teamId'] == teamId]['position']



def get_players_of_team_in_germany(teamId):
    return germanyyy[germanyyy['teamId'] == teamId]['name']

def get_positions_of_players_in_team_germany(teamId):
    return germanyyy[germanyyy['teamId'] == teamId]['position']




def search_in_certain_team(teamId , list_of_name):
    players_of_team = get_players_of_team_in_transferMarkt(teamId).tolist()
    positions_of_team = get_positions_of_players_in_team_transfermarkt(teamId).tolist()
    index = 0
    found = 0
    while index < len(players_of_team):
        print(type(players_of_team[index]))
        if is_matching_name(list_of_name , players_of_team[index].split()):
            found = True
            break
        index += 1
    if found == True:
        return positions_of_team[index]
    else:
        return 'not found'
    
    
#transfermarkt['position'].tolist()
#transfermarkt['name'].tolist()
#get_players_of_team_in_transferMarkt(1625).tolist()
#get_positions_of_players_in_team_transfermarkt(1625).tolist()
#def search_by_team(list_of_players , list_of_positions)


def change_pos_for_one_team(teamId):
    list_of_players_ids = get_players_in_team_by_teamId(teamId)
#    list_of_players_transfermarkt = get_players_of_team_in_transferMarkt(teamId)
#    list_of_positions_transfermarkt = get_positions_of_players_in_team_transfermarkt(teamId)
    index = 0
    while index < len(list_of_players_ids):
        fn = players[players['wyId'] == list_of_players_ids[index]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == list_of_players_ids[index]]['lastName'].tolist()[0]
        list_of_name = first_last_names_in_list(fn , ln)
        pos = search_in_certain_team(teamId ,list_of_name)
        #print(pos)
        players.loc[(players.wyId == list_of_players_ids[index]),'position']=pos
        index += 1
    

def change_pos_for_list_of_teams(list_of_teams):
    index = 0
    while index < len(list_of_teams):
        change_pos_for_one_team(list_of_teams[index])
        index += 1


def print_not_found(list_of_teams):
    index = 0
    counter = 0
    while index < len(list_of_teams):
        l = get_players_in_team_by_teamId(list_of_teams[index])
        index_inside_team = 0
        while index_inside_team < len(l):
            fn = players[players['wyId'] == l[index_inside_team]]['firstName'].tolist()[0]
            ln = players[players['wyId'] == l[index_inside_team]]['lastName'].tolist()[0]
            pos = players[players['wyId'] == l[index_inside_team]]['position'].tolist()[0]
            if pos == 'not found':
                print(fn , ln , pos , l[index_inside_team])
                counter += 1
            index_inside_team += 1
        index += 1
    print(counter)

list_of_teams = get_teams_in_certain_area('Spain')
print(list_of_teams)

li = []
index = 0
while index < len(list_of_teams):
    li.append(list_of_teams[index][1])
    index += 1
print(li)
print_not_found(li)



list_of_positions = ['Goalkeeper' , 'Centre-Back' , 'Left-Back' , 'Right-Back' , 'Defensive Midfield' , 'Central Midfield' , 'Attacking Midfield',
                      'Left Winger' , 'Right Winger' , 'Centre-Forward' , 'Left Midfield' , 'Right Midfield']
players.loc[(players.wyId == 3337),'position']='Centre-Back'
players.to_json(r'players.json')


change_pos_for_one_team(3159)

l = get_players_in_team_by_teamId(3799)
index = 0
while index < len(l):
    fn = players[players['wyId'] == l[index]]['firstName'].tolist()[0]
    ln = players[players['wyId'] == l[index]]['lastName'].tolist()[0]
    pos = players[players['wyId'] == l[index]]['position'].tolist()[0]
    print(fn , ln , pos , l[index])
    index += 1

s = "Andreu Font\u00e0s Prat"
s = s.encode('utf-8').decode('utf-8','ignore')
print(s)

f = players[players['position'] == 'Centre-Back']['wyId'].tolist()
index = 0
while index < len(f):
    fn = players[players['wyId'] == f[index]]['firstName'].tolist()[0]
    ln = players[players['wyId'] == f[index]]['lastName'].tolist()[0]
    print(fn , ln)
    index += 1

transfermarkt[transfermarkt['teamId'] == 1673]

teams[teams['wyId'] == 1659]['name']
transfermarkt['name'].tolist()
get_teams_in_certain_area('Spain')
change_pos_for_one_team(3767)

players['position'].value_counts()
l = players[players['position'] == 'not found']['wyId'].tolist()
index = 35
while index < 40:
    fn = players[players['wyId'] == l[index]]['firstName'].tolist()[0]
    ln = players[players['wyId'] == l[index]]['lastName'].tolist()[0]
    print(fn , ln , l[index])
    index +=1 


list_of_positions = ['Goalkeeper' , 'Centre-Back' , 'Left-Back' , 'Right-Back' , 'Defensive Midfield' , 'Central Midfield' , 'Attacking Midfield',
                      'Left Winger' , 'Right Winger' , 'Centre-Forward']
players.loc[(players.wyId == 263803),'position']='Right-Back'

players[players['wyId'] == 274345]['currentTeamId']
players[players['wyId'] == 10108]['lastName']

change_pos_for_list_of_teams(li)
players[players['currentTeamId'] == 3804]['shortName'].tolist()
players[players['wyId'] == 229198]['currentTeamId']
teams[teams['wyId'] == 3804]['name']
transfermarkt[transfermarkt['teamId'] == 3799]['name']

players['position'].value_counts()

l = players[players['position'] == 'LWB']['wyId'].tolist()

index = 0
while index < len(l):
    players.loc[(players.wyId == l[index]),'position']='Left-Back'
    index += 1


players.to_json(r'players.json')


