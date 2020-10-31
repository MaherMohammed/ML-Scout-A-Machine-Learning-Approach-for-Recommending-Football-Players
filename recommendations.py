
########################## imports ############################################
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt
import pandas as pd
import math 
from sklearn.cluster import KMeans
from statistics import mode
import networkx as nx
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

##################################### Datasets ################################


#english_teams_from_fullData = ['Manchester Utd', 'Chelsea', 'Arsenal','Manchester City','Liverpool','Everton','Leicester City','Crystal Palace',
#                               'West Ham','Stoke City','Bournemouth','Watford','West Brom','Burnley','Newcastle Utd' , 'Huddersfield' , 'Brighton',
#                               'Southampton','Spurs']

#prem_teams = ['Arsenal' , 'Everton' , 'Huddersfield' , 'Liverpool' , 'Manchester+United'  , 'Bournemouth' , 'Leicester+City' ,
#     'Watford' , 'Southampton' , 'West+Ham' , 'Stoke+City' , 'Brighton+and+Hove' , 'Newcastle+United' , 'Crystal+Palace' , 'Tottenham'
#     , 'Manchester+City' , 'Chelsea' , 'West+Brom' , 'Burnley']
#players_teams = [1609 , 1623 , 1673 , 1612 , 1611 , 1659 , 1631 , 1644 , 1619 , 1633 , 1639 , 1651 , 1613 , 1628 , 1624 , 1625 , 1610
#                 ,1627 , 1646]
#full_data.info()


#premierLeague = pd.read_csv('premier league 201718.csv')
#data = pd.read_csv('data.csv')
#full_data = pd.read_csv('FullData.csv')
players_stats = pd.read_csv('players_stats.csv' , encoding = 'latin-1')
teams = pd.read_json('teams.json')
players = pd.read_json('players.json')
playerank = pd.read_json('playerank.json')
#players.to_json(r'players.json')

events_england = pd.read_json('events_England.json')
matches_england = pd.read_json('matches_England.json')

events_european_champ = pd.read_json('events_EuropeanChampionship.json')
matches_european_champ = pd.read_json('matches_European_Championship.json')


events_italy = pd.read_json('eventsItaly.json')
matches_italy = pd.read_json('matches_Italy.json')

events_france = pd.read_json('events_France.json')
matches_france = pd.read_json('matches_France.json')

events_spain = pd.read_json('events_Spain.json')
matches_spain = pd.read_json('matches_Spain.json')

events_germany = pd.read_json('events_Germany.json')
matches_germany = pd.read_json('matches_Germany.json')

events_world_cup = pd.read_json('events_World_Cup.json')
matches_world_cup = pd.read_json('matches_World_Cup.json')



passesEngland = events_england[events_england['eventName'] == 'Pass']
passesFrance = events_france[events_france['eventName'] == 'Pass']
passesGermany = events_germany[events_germany['eventName'] == 'Pass']
passesItaly = events_italy[events_italy['eventName'] == 'Pass']
passesSpain = events_spain[events_spain['eventName'] == 'Pass']


events_passes = passesEngland.append(passesFrance,ignore_index = True)
events_passes = events_passes.append(passesGermany,ignore_index = True)
events_passes = events_passes.append(passesItaly,ignore_index = True)
events_passes = events_passes.append(passesSpain,ignore_index = True)





duelsEngland = events_england[events_england['eventName'] == 'Duel']
duelsFrance = events_france[events_france['eventName'] == 'Duel']
duelsGermany = events_germany[events_germany['eventName'] == 'Duel']
duelsItaly = events_italy[events_italy['eventName'] == 'Duel']
duelsSpain = events_spain[events_spain['eventName'] == 'Duel']

events_duels = duelsEngland.append(duelsFrance,ignore_index = True)
events_duels = events_duels.append(duelsGermany,ignore_index = True)
events_duels = events_duels.append(duelsItaly,ignore_index = True)
events_duels = events_duels.append(duelsSpain,ignore_index = True)





shotsEngland = events_england[events_england['eventName'] == 'Shot']
shotsFrance = events_france[events_france['eventName'] == 'Shot']
shotsGermany = events_germany[events_germany['eventName'] == 'Shot']
shotsItaly = events_italy[events_italy['eventName'] == 'Shot']
shotsSpain = events_spain[events_spain['eventName'] == 'Shot']

events_shots = duelsEngland.append(shotsFrance,ignore_index = True)
events_shots = events_duels.append(shotsGermany,ignore_index = True)
events_shots = events_duels.append(shotsItaly,ignore_index = True)
events_shots = events_duels.append(shotsSpain,ignore_index = True)






matchesIDs_England = matches_england['wyId']
matchesIDs_France = matches_france['wyId']
matchesIDs_Germany = matches_germany['wyId']
matchesIDs_Italy = matches_italy['wyId']
matchesIDs_Spain = matches_spain['wyId']


matchesIds = matchesIDs_England.append(matchesIDs_France,ignore_index = True)
matchesIds = matchesIds.append(matchesIDs_Germany,ignore_index = True)
matchesIds = matchesIds.append(matchesIDs_Spain,ignore_index = True)
matchesIds = matchesIds.append(matchesIDs_Italy,ignore_index = True)

matchesIds = matchesIds.tolist()





#.encode('latin-1').decode('unicode-escape','ignore')

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



def name_from_full_data_in_lists(name):
    name = name.encode('utf-32').decode('utf-32','ignore')    
    playerNameList = name.split()
    return playerNameList
    



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
    
    #    index = 0
#    counter = 0
#    while index < len(lst_from_fullData_dataset):
#        if lst_from_fullData_dataset[index] in lst_from_players_dataset:
#            counter += 1
#        index += 1
#    if counter == len(lst_from_fullData_dataset):
#        return True
#    else:
#        return False
    
    
    
def is_unique(index):
    count = full_data.pivot_table(index=['Name'], aggfunc='size')[index]
    if count == 1:
        return True
    elif count > 1:
        return False
    


def search_in_data_dataSet(playerNameList):
    dataNames = players_stats['name'].tolist()
    dataPos = players_stats['position'].tolist()
    found = False
    index = 0
    while index < len(dataNames):
        if is_matching_name(playerNameList , dataNames[index].split()):
            found = True
            break
        index += 1
    if found:
        return dataPos[index]
    else:
        return 'not found'
 
    
def search_in_fullData_dataSet(playerNameList):
    dataNames = full_data['Name'].tolist()
    dataPos = full_data['Club_Position'].tolist()
    found = False
    index = 0
    while index < len(dataNames):
        if is_matching_name(playerNameList , dataNames[index].split()):
            found = True
            break
        index += 1
    if found:
        return dataPos[index]
    else:
        return 'not found'

def change_position_in_players_dataset():
    ids_from_players = players['wyId'].tolist()
    index = 0
    while index < len(ids_from_players):
        fn = players[players['wyId'] == ids_from_players[index]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == ids_from_players[index]]['lastName'].tolist()[0]
        lst = first_last_names_in_list(fn , ln)
        pos = search_in_data_dataSet(lst)
        players.loc[(players.wyId == ids_from_players[index]),'position']=pos
        index += 1
    


def minutes_played_by_one_player(matchesIds,playerId):
    matches = playerank[playerank['playerId'] == playerId]['matchId'].tolist()
    minutes_played_by_the_player = playerank[playerank['playerId'] == playerId]['minutesPlayed'].tolist()
    minutes = 0
    index = 0
    while index < len(matches):
        if matches[index] in matchesIds:
            minutes = minutes + minutes_played_by_the_player[index]
        index += 1
    return minutes


def minutes_for_list_of_players(matchesIds,list_of_players):
    returned_list = []
    index = 0
    while index < len(list_of_players):
        returned_list.append(minutes_played_by_one_player(matchesIds,list_of_players[index]))
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
            print(fn[0] ,ln[0] , identify_position_of_the_player(playersLocal[index]) , role)
            index += 1
        return playersLocal
    
 
def get_league_of_certain_team(teamId):
    try:
        league = teams[teams['wyId'] == teamId]['area'].tolist()[0]['name']
    except IndexError:
        league = 'null'
    
    return league



def matches_played_by_certain_team(teamId , league):
    matches = []
    all_matches = []
    if league == 'England':
        all_matches = events_england[events_england['teamId'] == teamId]['matchId'].tolist()
    elif league == 'France':
        all_matches = events_france[events_france['teamId'] == teamId]['matchId'].tolist()
    elif league == 'Germany':
        all_matches = events_germany[events_germany['teamId'] == teamId]['matchId'].tolist()
    elif league == 'Italy':
        all_matches = events_italy[events_italy['teamId'] == teamId]['matchId'].tolist()
    elif league == 'Spain':
        all_matches = events_spain[events_spain['teamId'] == teamId]['matchId'].tolist()
        
    ########### now get the set of these matches ###############
    index = 0
    while index < len(all_matches):
        if all_matches[index] not in matches:
            matches.append(all_matches[index])
        index += 1
    
    return matches
            



################# make sure that the matches are true ############

 
#####################################################################


def is_goal(event_tags):
    goal = False
    index = 0
    while index < len(event_tags):
        if event_tags[index]['id'] == 101 or event_tags[index]['id'] == 102:
            goal = True
            break
        index += 1
    return goal


def is_accurate(event_tags):
    accurate = False
    index = 0
    while index < len(event_tags):
        if event_tags[index]['id'] == 1801:
            accurate = True
            break
        index += 1
    return accurate

def is_own_goal(event_tags):
    own = False
    index = 0
    while index < len(event_tags):
        if event_tags[index]['id'] == 102:
            own = True
            break
        index += 1
    return own

def get_tags_and_teamIds_and_positions_and_times_and_periods_of_events_of_certain_match(matchId , league):
    if league == 'England':
        tags = events_england[events_england['matchId'] == matchId]['tags'].tolist()
        teamIds = events_england[events_england['matchId'] == matchId]['teamId'].tolist()
        positions = events_england[events_england['matchId'] == matchId]['positions'].tolist()
        times = events_england[events_england['matchId'] == matchId]['eventSec'].tolist()
        periods = events_england[events_england['matchId'] == matchId]['matchPeriod'].tolist()
    elif league == 'France':
        tags = events_france[events_france['matchId'] == matchId]['tags'].tolist()
        teamIds = events_france[events_france['matchId'] == matchId]['teamId'].tolist()
        positions = events_france[events_france['matchId'] == matchId]['positions'].tolist()
        times = events_france[events_france['matchId'] == matchId]['eventSec'].tolist()
        periods = events_france[events_france['matchId'] == matchId]['matchPeriod'].tolist()
    elif league == 'Germany':
        tags = events_germany[events_germany['matchId'] == matchId]['tags'].tolist()
        teamIds = events_germany[events_germany['matchId'] == matchId]['teamId'].tolist()
        positions = events_germany[events_germany['matchId'] == matchId]['positions'].tolist()
        times = events_germany[events_germany['matchId'] == matchId]['eventSec'].tolist()
        periods = events_germany[events_germany['matchId'] == matchId]['matchPeriod'].tolist()
    elif league == 'Italy':
        tags = events_italy[events_italy['matchId'] == matchId]['tags'].tolist()
        teamIds = events_italy[events_italy['matchId'] == matchId]['teamId'].tolist()
        positions = events_italy[events_italy['matchId'] == matchId]['positions'].tolist()
        times = events_italy[events_italy['matchId'] == matchId]['eventSec'].tolist()
        periods = events_italy[events_italy['matchId'] == matchId]['matchPeriod'].tolist()
    elif league == 'Spain':
        tags = events_spain[events_spain['matchId'] == matchId]['tags'].tolist()
        teamIds = events_spain[events_spain['matchId'] == matchId]['teamId'].tolist()
        positions = events_spain[events_spain['matchId'] == matchId]['positions'].tolist()
        times = events_spain[events_spain['matchId'] == matchId]['eventSec'].tolist()
        periods = events_spain[events_spain['matchId'] == matchId]['matchPeriod'].tolist()
    return tags , teamIds , positions , times , periods
        

def get_goals_scored_aganist_certain_team(teamId , league , matches):
    positions = []
    times = []
    matches_of_goals = []
    tags = []
    periods = []
    index = 0
    while index < len(matches):
        ########### getting tags and teamIds of events
        t_and_i = get_tags_and_teamIds_and_positions_and_times_and_periods_of_events_of_certain_match(matches[index] , league)
        tags_of_events_of_current_match = t_and_i[0]
        teamsIds_of_events = t_and_i[1]
        positions_of_events = t_and_i[2]
        times_of_events = t_and_i[3]
        periods_of_events = t_and_i[4]
#        #print(tags_of_events_of_current_match)
#        print(teamsIds_of_events)
        ############ specify the goals
        index_inside_tags = 0
        while index_inside_tags < len(tags_of_events_of_current_match):
            if is_goal(tags_of_events_of_current_match[index_inside_tags]) == True:
                if (teamsIds_of_events[index_inside_tags] != teamId):
                    if is_accurate(tags_of_events_of_current_match[index_inside_tags]) and not is_own_goal(tags_of_events_of_current_match[index_inside_tags]):
                        positions.append(positions_of_events[index_inside_tags])
                        times.append(times_of_events[index_inside_tags])
                        matches_of_goals.append(matches[index])
                        periods.append(periods_of_events[index_inside_tags])
                        
                elif (teamsIds_of_events[index_inside_tags] == teamId): 
                    if is_own_goal(tags_of_events_of_current_match[index_inside_tags]):
                        positions.append(positions_of_events[index_inside_tags])
                        times.append(times_of_events[index_inside_tags])
                        matches_of_goals.append(matches[index])
                        periods.append(periods_of_events[index_inside_tags])
                    
            index_inside_tags += 1
        index += 1
    return positions , times,matches_of_goals, periods
                    
                    

#####################3 print teams in england and their ids####################
def is_nationalTeam(teamId):
    return teams[teams['wyId'] == teamId]['type'].tolist()[0] == 'national'
    


def get_teams_in_certain_area(league):
    returned_list = []
    index = 0
    while index < len(teams):
        if teams['area'][index]['name'] == league and teams['type'][index] != 'national':
            returned_list.append([teams['officialName'][index] , teams['wyId'][index]])
        index += 1
    return returned_list





def split_times_for_two_periods(events ,list_of_times):
    list_of_first_half_times = []
    list_of_second_half_times = []
    list_of_first_half_events = []
    list_of_second_half_events = []

    index = 0
    while index < len(list_of_times) - 1:
        if list_of_times[index] > list_of_times[index + 1]:
            list_of_first_half_times = list_of_times[0:index + 1]
            list_of_second_half_times = list_of_times[index + 1:]
            list_of_first_half_events = events[0:index + 1]
            list_of_second_half_events = events[index + 1:]

        index += 1
    
    return list_of_first_half_times , list_of_second_half_times , list_of_first_half_events , list_of_second_half_events
    
    

def condition(item , time_of_the_goal):
    if item < time_of_the_goal:
        return item
    

def identify_part_of_position_on_the_field(x , y):
    if x >= 0 and x < 16.67 and y >= 0 and y < 33.33:
        return 1
    elif x >= 16.67 and x < 33.34 and y >= 0 and y < 33.33:
        return 4
    elif x >= 33.34 and x < 50.01 and y >= 0 and y < 33.33:
        return 7
    elif x >= 50.01 and x < 66.68 and y >= 0 and y < 33.33:
        return 10
    elif x >= 66.68 and x < 83.35 and y >= 0 and y < 33.33:
        return 13
    elif x >= 83.35 and x < 100 and y >= 0 and y < 33.33:
        return 16
    
    if x >= 0 and x < 16.67 and y >= 33.33 and y < 66.66:
        return 2
    elif x >= 16.67 and x < 33.34 and y >= 33.33 and y < 66.66:
        return 5
    elif x >= 33.34 and x < 50.01 and y >= 33.33 and y < 66.66:
        return 8
    elif x >= 50.01 and x < 66.68 and y >= 33.33 and y < 66.66:
        return 11
    elif x >= 66.68 and x < 83.35 and y >= 33.33 and y < 66.66:
        return 14
    elif x >= 83.35 and x < 100 and y >= 33.33 and y < 66.66:
        return 17
    
    
    if x >= 0 and x < 16.67 and y >= 66.66 and y < 100:
        return 3
    elif x >= 16.67 and x < 33.34 and y >= 66.66 and y < 100:
        return 6
    elif x >= 33.34 and x < 50.01 and y >= 66.66 and y < 100:
        return 9
    elif x >= 50.01 and x < 66.68 and y >= 66.66 and y < 100:
        return 12
    elif x >= 66.68 and x < 83.35 and y >= 66.66 and y < 100:
        return 15
    elif x >= 83.35 and x < 100 and y >= 66.66 and y < 100:
        return 18
    else:
        return 0
    


def have_destination(position):
    return len(position) == 2

def is_gone_to_another_part_in_the_field(position):
    #print(position)
    origin = position[0]
    destination = position[1]
    if identify_part_of_position_on_the_field(origin['x'] , origin['y']) != identify_part_of_position_on_the_field(destination['x'] , destination['y']):
        return True
    else:
        return False


def most_frequent(List): 
    counter = 0
    if len(List) == 0:
        return 'non exist'
    num = List[0] 
      
    for i in List: 
        curr_frequency = List.count(i) 
        if(curr_frequency > counter): 
            counter = curr_frequency 
            num = i 
  
    return num 

def identify_position_of_the_player(playerId):
    return most_frequent(playerank[playerank['playerId'] == playerId]['roleCluster'].tolist())
    



###################################################################################################################################  

def get_the_accurate_events_before_a_goal(times_of_all_events , tags_of_all_events , positions_of_all_events):
    max_num_of_events = 4
    positions = []
    index = len(times_of_all_events) - 1
    #print('index',index)
    #print('positions' , len(positions_of_all_passes))
    while index > 0 and max_num_of_events > 0 and have_destination(positions_of_all_events[index]) and is_gone_to_another_part_in_the_field(positions_of_all_events[index]):
        if is_accurate(tags_of_all_events[index]):
            positions.append(positions_of_all_events[index])
            max_num_of_events -= 1
        index -= 1
    
    return positions



    
    
def positions_of_events_precced_a_certain_goal(match_of_the_team , times_of_goal , league , period_of_the_match):
    events = get_tags_and_teamIds_and_positions_and_times_and_periods_of_events_of_certain_match(match_of_the_team , league)
    tags = events[0]
    positions = events[2]
    seconds = events[3]

    splitting_tags = split_times_for_two_periods(tags,seconds)
    splitting_positions = split_times_for_two_periods(positions,seconds)    
    
    first_half_times = splitting_tags[0]
    second_half_times = splitting_tags[1]
    
    first_half_tags = splitting_tags[2]
    second_half_tags = splitting_tags[3]
    
    first_half_pos = splitting_positions[2]
    second_half_pos = splitting_positions[3]

    timesOf_all_events_precced_the_goal = []
    tagsOf_all_events_precced_the_goal = []
    positionsOf_all_events_precced_the_goal = []
        
    if period_of_the_match == '1H':
        helper = np.zeros(len(first_half_times)) + times_of_goal
        timesOf_all_events_precced_the_goal = list(filter(None ,map(condition, first_half_times, helper)))
        tagsOf_all_events_precced_the_goal = first_half_tags[0:len(timesOf_all_events_precced_the_goal)]
        positionsOf_all_events_precced_the_goal = first_half_pos[0:len(timesOf_all_events_precced_the_goal)]
    elif period_of_the_match == '2H':
        helper = np.zeros(len(second_half_times)) + times_of_goal
        timesOf_all_events_precced_the_goal = list(filter(None ,map(condition, second_half_times, helper)))
        tagsOf_all_events_precced_the_goal = second_half_tags[:len(timesOf_all_events_precced_the_goal)]
        positionsOf_all_events_precced_the_goal = second_half_pos[:len(timesOf_all_events_precced_the_goal)]
        
            
    return get_the_accurate_events_before_a_goal(timesOf_all_events_precced_the_goal , tagsOf_all_events_precced_the_goal , positionsOf_all_events_precced_the_goal)
        


def positions_of_events_precced_list_of_goals(matches_of_goals , list_of_times_of_goals , league , list_of_periods_of_goals):
    list_of_events = []
#    print(len(matches))
#    print(len(list_of_times_of_goals))
#    print(len(list_of_periods_of_goals))
    index = 0
    while index < len(matches_of_goals):
        list_of_events.append(positions_of_events_precced_a_certain_goal(matches_of_goals[index], list_of_times_of_goals[index], league , list_of_periods_of_goals[index]))
        index += 1
    return list_of_events
        



        



def create_matrix_to_draw(positions):
    returned_list = [[] for i in range(18)]
    rows = 0
    
    ######### initializing the matrix
    while rows < len(returned_list):
        col = 0
        while col < 18:
            returned_list[rows].append(0)
            col += 1
        rows += 1 
        
    #################### fill it with weigths #########
    index = 0
    while index < len(positions):
        index_inside = 0
        while index_inside < len(positions[index]):
            origin = positions[index][index_inside][0]
            des = positions[index][index_inside][1]
            
            part_of_origin = identify_part_of_position_on_the_field(origin['x'] , origin['y'])
            part_of_des = identify_part_of_position_on_the_field(des['x'] , des['y'])
            
            if part_of_origin != part_of_des:
                orgind = int(part_of_origin) - 1
                desind = int(part_of_des) - 1
                returned_list[orgind][desind] = returned_list[orgind][desind] + 1
            index_inside += 1
        index += 1
    return returned_list
        
        

######################### row is origin and col is destination ################3

def draw_graph_for_events_before_goals(matrix):
    G= nx.DiGraph()
    ####################### adding the edges from matrix ############
    rows = 0
    while rows < len(matrix):
        col = 0
        while col < len(matrix[rows]):
            if matrix[rows][col] != 0:
                G.add_edge(str(rows + 1) , str(col + 1) , weight = matrix[rows][col])
            col += 1
        rows += 1

  
    pos=nx.circular_layout(G)

    nx.draw(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    nx.draw_networkx_labels(G,pos,font_size=20 ,font_family='sans-serif',edge_labels=labels)
    plt.axis('off')
    plt.savefig("Barcelona.png")
    plt.show() # display



def get_ratio_of_positions(number_of_goals_because_of_this_player , number_of_all_goals):
    return number_of_goals_because_of_this_player / number_of_all_goals




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
    

def get_clubs_in_fullData():
    list_of_teams = full_data['Club'].tolist()
    returned_list = []
    index = 0
    while index < len(list_of_teams):
        if list_of_teams[index] in returned_list:
            index += 1
        else:
            returned_list.append(list_of_teams[index])
            index += 1
    return returned_list
    


def apply_algo_to_all_teams_in_our_dataset():
    clubs = get_clubs()
    matrices = []
    goalss = []
    index = 0
    while index < len(clubs):
        league = get_league_of_certain_team(clubs[index][-1])
        matches = matches_played_by_certain_team(clubs[index][-1] , league)
        goals = get_goals_scored_aganist_certain_team(clubs[index][-1] , league , matches)
        p = positions_of_events_precced_list_of_goals(goals[2] , goals[1] , league , goals[-1])  
        mat = create_matrix_to_draw(p)
        matrices.append(mat)
        goalss.append(len(goals[0]))
        #draw_graph_for_events_before_goals(mat)
        index += 1
    return matrices , goalss

    




         
def max_of_matrix(matrix):
    row = 0
    max_number = matrix[0][0]

    
    while row < len(matrix):
        col = 0
        while col < len(matrix[row]):
            if matrix[row][col] > max_number:
                max_number = matrix[row][col]
            col += 1
        row += 1
    
    return max_number

#######################################################################


def get_maxes_of_matrix(matrix , max_of_matrix):
    list_of_maxes = []
    row = 0
    max_row = 0
    max_col = 0
    
    while row < len(matrix):
        col = 0
        while col < len(matrix[row]):
            if matrix[row][col] == max_of_matrix:
                max_number = matrix[row][col]
                max_row = row
                max_col = col
                list_of_maxes.append([max_number , max_row +1 , max_col +1])
            col += 1
        row += 1
    
    return list_of_maxes




def get_the_least_ratio(list_of_ratios):
    least_ratio = list_of_ratios[0]
    index = 1
    index_of_least = 0
    while index < len(list_of_ratios):
        if list_of_ratios[index] < least_ratio:
            least_ratio = list_of_ratios[index]
            index_of_least = index
        index += 1
    return least_ratio , index_of_least


############# row is origin and col is destination of worst def player in our team ########################
def get_least_ratio_from_all_teams(list_of_matrices , list_of_goals , row , col):
    list_of_ratios = []
    index = 0
    while index < len(list_of_matrices):
        number_of_goals_in_certain_pos = list_of_matrices[index][row - 1][col - 1]
        if list_of_goals[index] != 0:
            ratio_of_matrix = get_ratio_of_positions(number_of_goals_in_certain_pos , list_of_goals[index])
            list_of_ratios.append(ratio_of_matrix)
        else:
            #print('ooooooooooooooooooooooo')
            list_of_ratios.append(10000000000)
        index += 1
    print(list_of_ratios)
    return get_the_least_ratio(list_of_ratios)



def get_count_in_certain_position_from_matrix(matrix , row , col):
    return matrix[row-1][col-1]


##################### ranking Defenders #################################################
#a = apply_algo_to_all_teams_in_our_dataset()    
#get_least_ratio_from_all_teams(a[0] , a[1] , 18 , 17)
#
#get_clubs()
############################ extracting features #######################################

def which_passes_for_the_league(league):
    if league == 'England':
        return events_england[events_england['eventName'] == 'Pass']
    elif league == 'France':
        return events_france[events_france['eventName'] == 'Pass']
    elif league == 'Germany':
        return events_germany[events_germany['eventName'] == 'Pass']
    elif league == 'Italy':
        return events_italy[events_italy['eventName'] == 'Pass']
    else:
        return events_spain[events_spain['eventName'] == 'Pass']
    
def which_duels_for_the_league(league):
    if league == 'England':
        return events_england[events_england['eventName'] == 'Duel']
    elif league == 'France':
        return events_france[events_france['eventName'] == 'Duel']
    elif league == 'Germany':
        return events_germany[events_germany['eventName'] == 'Duel']
    elif league == 'Italy':
        return events_italy[events_italy['eventName'] == 'Duel']
    else:
        return events_spain[events_spain['eventName'] == 'Duel']        





def number_of_subEvents_for_one_player(playerId , events, subEventId):
    counter = 0
    e = events[events['playerId'] == playerId]
    tags = e[e['subEventId'] == subEventId]['tags'].tolist()
    
    index = 0
    while index < len(tags):
        if is_accurate(tags[index]):
            counter += 1
        index += 1
    return counter
    
    
    

def number_of_subEvents_for_list_of_players(list_of_players , events , subEventId):
    returned_list = []
    index = 0
    while index < len(list_of_players):
        returned_list.append(number_of_subEvents_for_one_player(list_of_players[index] , events , subEventId))
        index += 1
    return returned_list




def extract_players_in_general_position(position):
    players_in_certain_pos = []
    index = 0
    while index < len(players):
        if players['role'][index]['name'] == position:
            players_in_certain_pos.append(players['wyId'][index])
        index += 1
    
    return players_in_certain_pos
    


def extract_players_in_center_back(list_of_players):
    center_backs = []
    index = 0
    positions = ['right CB' , 'left CB' , 'central MF' , 'right CB-central MF-left CB' , 'central MF-right CB' , 'right MF-right CB' , 'right CB-left CB']
    while index < len(list_of_players):
        pos = identify_position_of_the_player(list_of_players[index])
        if pos in positions:
            center_backs.append(list_of_players[index])
        index += 1
    
    return center_backs


def extract_players_in_left_back(list_of_players):
    positions = ['left MF','left FW']
    left_backs = []
    index = 0
    while index < len(list_of_players):
        pos = identify_position_of_the_player(list_of_players[index])
        if pos in positions:
            left_backs.append(list_of_players[index])
        index += 1
    return left_backs



def extract_players_in_right_back(list_of_players):
    positions = ['right MF','right FW']
    right_backs = []
    index = 0
    while index < len(list_of_players):
        pos = identify_position_of_the_player(list_of_players[index])
        if pos in positions:
            right_backs.append(list_of_players[index])
        index += 1
    return right_backs


def extract_league_for_one_player(playerId):
    teamId = players[players['wyId'] == playerId]['currentTeamId'].tolist()[0]
    return get_league_of_certain_team(teamId)


def extract_number_of_accurate_events(list_of_tags):
    counter = 0
    index = 0
    while index < len(list_of_tags):
        if is_accurate(list_of_tags[index]):
            counter += 1
        index += 1
    return counter



def number_of_matches_for_one_player(playerId):
    matches_of_the_player = playerank[playerank['playerId'] == playerId]['matchId'].tolist()    
    counter = 0
    index = 0
    while index < len(matches_of_the_player):
        if matches_of_the_player[index] in matchesIds:
            counter += 1
        index += 1
    return counter
    

def number_of_matches_for_list_of_players(list_of_players):
    returned_list = []
    index = 0 
    while index < len(list_of_players):
        returned_list.append(number_of_matches_for_one_player(list_of_players[index]))
        index += 1
    return returned_list
        
        
        
        
        

list_of_leagues = ['England' , 'France' , 'Germany' , 'Spain' , 'Italy']

def extract_features_for_center_backs(list_of_players):
    air_duels = []
    ground_attacking_duels = []
    ground_defending_duels = []
    ground_loose_ball_duel = []
    accurate_passes = []
    playerss = []
    minutes = minutes_for_list_of_players(matchesIds , list_of_players)
    num_of_matches = number_of_matches_for_list_of_players(list_of_players)
    ########collecting the features for each player#######
    index = 0
    while index < len(list_of_players):

        if minutes[index] != 0:

            league_of_player = extract_league_for_one_player(list_of_players[index])

            if league_of_player in list_of_leagues:

                mean_of_minutes = minutes[index] / num_of_matches[index]

                passesTags_of_player = events_passes[events_passes['playerId'] == list_of_players[index]]['tags'].tolist()
                number_of_passes_for_player = extract_number_of_accurate_events(passesTags_of_player)
                
                duels_of_player = events_duels[events_duels['playerId'] == list_of_players[index]]
                number_of_airDuels_of_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 10)
                
                number_of_groundAttacking_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 11)
                number_of_groundDefending_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 12)
                number_of_groundLooseBall_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 13)
                ########### adding to lists ######
                accurate_passes.append(number_of_passes_for_player /mean_of_minutes)
                ground_attacking_duels.append(number_of_groundAttacking_duels_for_player /mean_of_minutes)
                ground_defending_duels.append(number_of_groundDefending_duels_for_player /mean_of_minutes)
                air_duels.append(number_of_airDuels_of_player /mean_of_minutes)
                ground_loose_ball_duel.append(number_of_groundLooseBall_duels_for_player/mean_of_minutes)
                playerss.append(list_of_players[index])
        
        index += 1
    
    return accurate_passes , air_duels , ground_attacking_duels , ground_defending_duels, ground_loose_ball_duel, playerss
     




def extract_features_for_left_or_right_backs(list_of_players):
    ground_defending_duels = []
    ground_attacking_duels = []
    ground_loose_ball_duel = []
    accurate_passes = []
    key_passes = []
    goals = []
    assists = []
    playerss = []
    
    minutes = minutes_for_list_of_players(matchesIds , list_of_players)
    num_of_matches = number_of_matches_for_list_of_players(list_of_players)    
    
    index = 0
    while index < len(list_of_players):
        if minutes[index] != 0:
            league_of_the_player = extract_league_for_one_player(list_of_players[index])
            
            if league_of_the_player in list_of_leagues:
                #mean_of_minutes = minutes[index] / num_of_matches[index]
                passesTags_of_player = events_passes[events_passes['playerId'] == list_of_players[index]]['tags'].tolist()
                number_of_passes_for_player = extract_number_of_accurate_events(passesTags_of_player)
                
                duels_of_player = events_duels[events_duels['playerId'] == list_of_players[index]]
                num_of_assists = number_of_events_for_one_player(events_passes , list_of_players[index] , 301)
                number_of_groundAttacking_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 11)
                number_of_groundDefending_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 12)
                number_of_groundLooseBall_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 13)
                num_of_keyPasses = number_of_events_for_one_player(events_passes , list_of_players[index] , 302)
                num_of_goals = get_number_of_goals_for_one_player(list_of_players[index])
                
                accurate_passes.append(number_of_passes_for_player / minutes[index])
                ground_attacking_duels.append(number_of_groundAttacking_duels_for_player / minutes[index])
                ground_defending_duels.append(number_of_groundDefending_duels_for_player / minutes[index])
                ground_loose_ball_duel.append(number_of_groundLooseBall_duels_for_player/ minutes[index])
                assists.append(num_of_assists)
                key_passes.append(num_of_keyPasses)
                goals.append(num_of_goals)
                playerss.append(list_of_players[index])
        index += 1
        
    return accurate_passes , ground_attacking_duels, ground_defending_duels, ground_loose_ball_duel ,assists , key_passes, playerss

## accurate_passes , ground_attacking_duels, ground_defending_duels, ground_loose_ball_duel ,assists , key_passes, goals, for left back
## accurate_passes , ground_attacking_duels, ground_defending_duels, ground_loose_ball_duel ,assists , key_passes for right back



def get_number_of_goals_for_one_player(playerId):
    l = playerank[playerank['playerId'] == playerId]['goalScored'].tolist()
    return sum(l)



def number_of_goals_for_one_player(matchIDs, playerId):
    matches = playerank[playerank['playerId'] == playerId]['matchId'].tolist()
    goals = playerank[playerank['playerId'] == playerId]['goalScored'].tolist()
    num_of_goals = 0
    index = 0
    while index < len(matches):
        if matches[index] in matchIDs:
            num_of_goals = num_of_goals + goals[index]
        index += 1
    return num_of_goals



    
def number_of_opportunity_shots_for_one_player(events ,playerId):
    tags = events[events['playerId'] == playerId]['tags'].tolist()
    
    opportunities = 0
    index = 0
    while index < len(tags):
        index_inside_tag = 0
        while index_inside_tag < len(tags[index]):
            if tags[index][index_inside_tag]['id'] == 201:
                opportunities += 1
            index_inside_tag += 1
        index += 1
    
    return opportunities
    

def number_of_goals_for_list_of_players(matchesIds,list_of_players):
    index = 0
    list_of_goals = []
    while index < len(list_of_players):
        list_of_goals.append(number_of_goals_for_one_player(matchesIds,list_of_players[index]))
        index += 1
    return list_of_goals


def extract_features_for_strikers(list_of_players):
    accurate_shots = []
    x_vars = []
    y_vars = []
    goals = []
    accurate_passes = []
    assists = []
    playerss = []
    mini = []
    minutes = minutes_for_list_of_players(matchesIds , list_of_players)
    #num_of_matches = number_of_matches_for_list_of_players(list_of_players)  
    
    index = 0
    while index < len(list_of_players):
        if minutes[index] != 0:
            league_of_the_player = extract_league_for_one_player(list_of_players[index])
            
            if league_of_the_player in list_of_leagues:
                #mean_of_minutes = minutes[index] / num_of_matches[index]
                passesTags_of_player = events_passes[events_passes['playerId'] == list_of_players[index]]['tags'].tolist()
                number_of_passes_for_player = extract_number_of_accurate_events(passesTags_of_player)

                shotsTags_of_player = events_shots[events_shots['playerId'] == list_of_players[index]]['tags'].tolist()
                xy = collect_Xes_and_Yes_for_one_player(events_passes , list_of_players[index])
                var_of_x = variance_of_axis(xy[0])
                var_of_y = variance_of_axis(xy[1])
                
                number_of_goals = get_number_of_goals_for_one_player(list_of_players[index])
                
                number_of_accurate_shots =  extract_number_of_accurate_events(shotsTags_of_player)
                num_of_assists = number_of_events_for_one_player(events_passes , list_of_players[index] , 301)
                
                accurate_shots.append(number_of_accurate_shots / minutes[index])
                goals.append(number_of_goals)
                x_vars.append(var_of_x  )
                y_vars.append(var_of_y )
                accurate_passes.append(number_of_passes_for_player / minutes[index])
                assists.append(num_of_assists)
                mini.append(minutes[index])
                playerss.append(list_of_players[index])
        index += 1

    return accurate_shots , goals,  accurate_passes,assists ,  playerss   



def extract_two_features_for_strikers(list_of_players):
    goals = []
    assists = []
    playerss = []
    minutes = minutes_for_list_of_players(matchesIds , list_of_players)
    #num_of_matches = number_of_matches_for_list_of_players(list_of_players)  
    
    index = 0
    while index < len(list_of_players):
        if minutes[index] != 0:
            league_of_the_player = extract_league_for_one_player(list_of_players[index])
            
            if league_of_the_player in list_of_leagues:
                #mean_of_minutes = minutes[index] / num_of_matches[index]
              
                
                number_of_goals = get_number_of_goals_for_one_player(list_of_players[index])
                
               
                num_of_assists = number_of_events_for_one_player(events_passes , list_of_players[index] , 301)
                
              
                goals.append(number_of_goals)
             
                assists.append(num_of_assists)
             
                playerss.append(list_of_players[index])
        index += 1

    return   goals,assists ,  playerss   
                
    


def extract_features_for_left_right_forward(list_of_players):
    accurate_shots = []
    x_vars = []
    y_vars = []
    goals = []
    accurate_passes = []
    assists = []
    playerss = []
    mini = []
    minutes = minutes_for_list_of_players(matchesIds , list_of_players)
    #num_of_matches = number_of_matches_for_list_of_players(list_of_players)  
    
    index = 0
    while index < len(list_of_players):
        if minutes[index] != 0:
            league_of_the_player = extract_league_for_one_player(list_of_players[index])
            
            if league_of_the_player in list_of_leagues:
                #mean_of_minutes = minutes[index] / num_of_matches[index]
                passesTags_of_player = events_passes[events_passes['playerId'] == list_of_players[index]]['tags'].tolist()
                number_of_passes_for_player = extract_number_of_accurate_events(passesTags_of_player)

                shotsTags_of_player = events_shots[events_shots['playerId'] == list_of_players[index]]['tags'].tolist()
                xy = collect_Xes_and_Yes_for_one_player(events_passes , list_of_players[index])
                var_of_x = variance_of_axis(xy[0])
                var_of_y = variance_of_axis(xy[1])
                
                number_of_goals = get_number_of_goals_for_one_player(list_of_players[index])
                
                number_of_accurate_shots =  extract_number_of_accurate_events(shotsTags_of_player)
                
                num_of_assists = number_of_events_for_one_player(events_passes , list_of_players[index] , 301)
                
                accurate_shots.append(number_of_accurate_shots / minutes[index])
                goals.append(number_of_goals )
                x_vars.append(var_of_x)
                y_vars.append(var_of_y / minutes[index] )
                accurate_passes.append(number_of_passes_for_player / minutes[index])
                assists.append(num_of_assists)
                mini.append(minutes[index])
                playerss.append(list_of_players[index])
        index += 1

    return accurate_shots , goals,accurate_passes, assists,playerss    
    


def extract_features_for_cmf_amf(list_of_players):
    accurate_shots = []
    x_vars = []
    y_vars = []
    goals = []
    accurate_passes = []
    assists = []
    keyPasses = []
    throughs = []
    playerss = []
    mini = []
    minutes = minutes_for_list_of_players(matchesIds , list_of_players)
    #num_of_matches = number_of_matches_for_list_of_players(list_of_players)  
    
    index = 0
    while index < len(list_of_players):
        if minutes[index] != 0:
            league_of_the_player = extract_league_for_one_player(list_of_players[index])
            
            if league_of_the_player in list_of_leagues:
                #mean_of_minutes = minutes[index] / num_of_matches[index]
                passesTags_of_player = events_passes[events_passes['playerId'] == list_of_players[index]]['tags'].tolist()
                number_of_passes_for_player = extract_number_of_accurate_events(passesTags_of_player)

                shotsTags_of_player = events_shots[events_shots['playerId'] == list_of_players[index]]['tags'].tolist()

                
                number_of_goals = get_number_of_goals_for_one_player(list_of_players[index])
                
                number_of_accurate_shots =  extract_number_of_accurate_events(shotsTags_of_player)
                
                num_of_assists = number_of_events_for_one_player(events_passes , list_of_players[index] , 301)
                num_of_keyPasses = number_of_events_for_one_player(events_passes , list_of_players[index] , 302)
                num_of_throughs = number_of_events_for_one_player(events_passes , list_of_players[index] , 901)
                
                accurate_shots.append(number_of_accurate_shots / minutes[index])
                goals.append(number_of_goals )
                accurate_passes.append(number_of_passes_for_player )
                assists.append(num_of_assists)
                keyPasses.append(num_of_keyPasses)
                throughs.append(num_of_throughs)
                mini.append(minutes[index])
                playerss.append(list_of_players[index])
        index += 1

    return accurate_passes, assists , keyPasses ,playerss    



def extract_features_for_dmf(list_of_players):
    ground_defending_duels = []
    ground_attacking_duels = []
    ground_loose_ball_duel = []
    accurate_passes = []
    goals = []
    keyPasses = []
    slide_tacklings = []
    assists = []
    accurate_shots = []
    playerss = []
    minutes = minutes_for_list_of_players(matchesIds , list_of_players)
    #num_of_matches = number_of_matches_for_list_of_players(list_of_players)  
    
    index = 0
    while index < len(list_of_players):
        if minutes[index] != 0:
            league_of_the_player = extract_league_for_one_player(list_of_players[index])
            
            if league_of_the_player in list_of_leagues:
                #mean_of_minutes = minutes[index] / num_of_matches[index]
                passesTags_of_player = events_passes[events_passes['playerId'] == list_of_players[index]]['tags'].tolist()
                number_of_passes_for_player = extract_number_of_accurate_events(passesTags_of_player)

                shotsTags_of_player = events_shots[events_shots['playerId'] == list_of_players[index]]['tags'].tolist()
                #xy = collect_Xes_and_Yes_for_one_player(events_passes , list_of_players[index])
                #var_of_x = variance_of_axis(xy[0])
                #var_of_y = variance_of_axis(xy[1])
                number_of_goals = get_number_of_goals_for_one_player(list_of_players[index])
                duels_of_player = events_duels[events_duels['playerId'] == list_of_players[index]]
                
                
                num_of_assists = number_of_events_for_one_player(events_passes , list_of_players[index] , 301)
                number_of_groundAttacking_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 11)
                number_of_groundDefending_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 12)
                number_of_groundLooseBall_duels_for_player = number_of_subEvents_for_one_player(list_of_players[index] , duels_of_player , 13)
                num_of_slide_tacklings = number_of_events_for_one_player(events_duels , list_of_players[index] , 1601)
                num_of_keyPasses = number_of_events_for_one_player(events_passes , list_of_players[index] , 302)
                number_of_accurate_shots =  extract_number_of_accurate_events(shotsTags_of_player)
                
                accurate_passes.append(number_of_passes_for_player / minutes[index])
                ground_attacking_duels.append(number_of_groundAttacking_duels_for_player / minutes[index])
                ground_defending_duels.append(number_of_groundDefending_duels_for_player / minutes[index])
                ground_loose_ball_duel.append(number_of_groundLooseBall_duels_for_player / minutes[index])
                goals.append(number_of_goals)
                assists.append(num_of_assists / minutes[index])
                keyPasses.append(num_of_keyPasses)
                accurate_shots.append(number_of_accurate_shots / minutes[index])
                slide_tacklings.append(num_of_slide_tacklings)
                playerss.append(list_of_players[index])
        index += 1

    return accurate_shots,accurate_passes,ground_defending_duels , ground_attacking_duels , ground_loose_ball_duel , assists , keyPasses , goals,playerss    





def collect_Xes_and_Yes_for_one_player(events,playerId):
    list_of_Xes = []
    list_of_Yes = []
    positions = events[events['playerId'] == playerId]['positions'].tolist()
    index = 0
    while index < len(positions):
        x = positions[index][0]['x']
        y = positions[index][0]['y']
        list_of_Xes.append(x)
        list_of_Yes.append(y)
        index += 1
    return list_of_Xes , list_of_Yes
    

def variance_of_axis(lst):
    return np.var(lst)
#
#xy = collect_Xes_and_Yes_for_one_player(events_passes , 8422)
#variance_of_axis(xy[1])
def number_of_events_for_one_player(events , playerId , code_of_the_event):
    tags = events[events['playerId'] == playerId]['tags'].tolist()  
    num_of_events = 0
    index = 0
    found = False
    while index < len(tags):
        index_inside_tag = 0
        while index_inside_tag < len(tags[index]) and found == False:
            if tags[index][index_inside_tag]['id'] == code_of_the_event:
                if is_accurate(tags[index]):
                    num_of_events += 1
                    found = True
            index_inside_tag += 1
        index += 1
        found = False
    return num_of_events
        

def number_of_events_for_list_of_players(events , list_of_players , code_of_the_event):
    returned_list = []
    index = 0
    while index < len(list_of_players):
        returned_list.append(number_of_events_for_one_player(events , list_of_players[index] , code_of_the_event))
        index += 1
    return returned_list


#def extract_features_for_left_right_forwards(list_of_players):
    



############### applying clustering algo #####
  
    
def to_list_to_kmeans4(lst1,lst2,lst3,lst4):
    returned_list = []
    index = 0
    while index < len(lst1):
        returned_list.append([lst1[index] , lst2[index] , lst3[index] ,lst4[index]])
        index += 1
    return returned_list


    
def to_list_to_kmeans3(lst1,lst2,lst3):
    returned_list = []
    index = 0
    while index < len(lst1):
        returned_list.append([lst1[index] , lst2[index] , lst3[index]])
        index += 1
    return returned_list


def to_list_to_kmeans2(lst1,lst2):
    returned_list = []
    index = 0
    while index < len(lst1):
        returned_list.append([lst1[index] , lst2[index]])
        index += 1
    return returned_list


    
def to_list_to_kmeans5(lst1,lst2,lst3,lst4,lst5):
    returned_list = []
    index = 0
    while index < len(lst1):
        returned_list.append([lst1[index] , lst2[index] , lst3[index] , lst4[index] , lst5[index]])
        index += 1
    return returned_list





    
def to_list_to_kmeans6(lst1,lst2,lst3,lst4,lst5,lst6):
    returned_list = []
    index = 0
    while index < len(lst1):
        returned_list.append([lst1[index] , lst2[index] , lst3[index] , lst4[index] , lst5[index] , lst6[index]])
        index += 1
    return returned_list




def to_list_to_kmeans7(lst1,lst2,lst3,lst4,lst5,lst6,lst7):
    returned_list = []
    index = 0
    while index < len(lst1):
        returned_list.append([lst1[index] , lst2[index] , lst3[index] , lst4[index] , lst5[index] , lst6[index],lst7[index]])
        index += 1
    return returned_list


def to_list_to_kmeans8(lst1,lst2,lst3,lst4,lst5,lst6,lst7,lst8):
    returned_list = []
    index = 0
    while index < len(lst1):
        returned_list.append([lst1[index] , lst2[index] , lst3[index] , lst4[index] , lst5[index] , lst6[index],lst7[index],lst8[index]])
        index += 1
    return returned_list


def show_the_clusters(dataset , num_of_clusters):
    dataset1 = np.asarray(dataset)    
    kmeans = KMeans(n_clusters = num_of_clusters,init = 'k-means++',  max_iter = 300, n_init = 10, random_state = 0)
    y_kmeans = kmeans.fit_predict(dataset1)
    #print(y_kmeans)
    
#    plt.scatter(dataset1[y_kmeans == 0,0],dataset1[y_kmeans == 0,1], s = 100, c = 'red' , label = 'Cluster 0')
#    plt.scatter(dataset1[y_kmeans == 1,0],dataset1[y_kmeans == 1,1], s = 100, c = 'blue' , label = 'Cluster 1')
#    plt.scatter(dataset1[y_kmeans == 2,0],dataset1[y_kmeans == 2,1], s = 100, c = 'green' , label = 'Cluster 2')
#    #plt.scatter(dataset1[y_kmeans == 3,0],dataset1[y_kmeans == 3,1], s = 100, c = 'cyan' , label = 'Cluster 3')
#    plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1] , s = 300 , c = 'yellow' , label = 'Centroids')
#    #print(kmeans.labels_)
#    #print(kmeans.cluster_centers_)
#    plt.xlabel('duels per minutes')
#    plt.ylabel('passes per minutes')
#    plt.legend()
#    plt.show()
    return kmeans.labels_ , kmeans.cluster_centers_


def the_optimal_num_of_k_clusters(dataset):
    dataset1 = np.asarray(dataset)
    print(type(dataset1))
    wcss = []
    for i in range(1,11):
        kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
        kmeans.fit(dataset1.reshape(-1,1))
        wcss.append(kmeans.inertia_)
    plt.plot(range(1,11),wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('wcss')
    plt.show()
    return wcss
    

 
def optimal_number_of_clusters(wcss):
    x1, y1 = 2, wcss[0]
    x2, y2 = 10, wcss[len(wcss)-1]

    distances = []
    for i in range(len(wcss)):
        x0 = i+2
        y0 = wcss[i]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distances.append(numerator/denominator)
    
    return distances.index(max(distances)) + 2

   
    

import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors.nearest_centroid import NearestCentroid


def use_dendroGram_to_find_optimal_num_of_clusters(dataset):
    dataset1 = np.asarray(dataset)
    dendrogram = sch.dendrogram(sch.linkage(dataset1 , method = 'ward'))
    plt.title('Dendrogram')
    plt.xlabel('Players')
    plt.ylabel('Euclidean Distance')
    plt.show()


def build_clusters_with_HC(dataset , num_of_clusters):
    dataset1 = np.asarray(dataset)
    hc = AgglomerativeClustering(n_clusters = num_of_clusters , affinity = 'euclidean' , linkage = 'ward')
    y_hc = hc.fit_predict(dataset1)
    clf = NearestCentroid()
    clf.fit(dataset1, y_hc) 
    return hc.labels_ , clf.centroids_





    
def applyingPca(number_of_components , dataset):
    pca = PCA( n_components = number_of_components)
    pca.fit(dataset)
    #print((pd.DataFrame(pca.components_,  index = ['PC-1' , 'PC-2' , 'PC-3' , 'PC-4' , 'PC-5']).abs()))
    #print(pca.components_[0])
    res =  [abs(ele) for ele in pca.components_[0]] 
    return res

from sklearn.cluster import MeanShift
    
def applyingMeanShiftAlgorithm(dataset):
    dataset1 = np.asarray(dataset)
    ms = MeanShift()
    ms.fit(dataset1)
    return ms.labels_ , ms.cluster_centers_ 



def arrange_the_clusters(list_of_centroids ,list_of_percents):
    index = 0
    list_arranged = []
    while index < len(list_of_centroids):
        index_inside_centroid = 0
        summation = 0
        while index_inside_centroid < len(list_of_centroids[index]):
            summation = summation + list_of_percents[index_inside_centroid] * list_of_centroids[index][index_inside_centroid]
            index_inside_centroid += 1
        list_arranged.append([index,summation / len(list_of_percents)])
        index += 1
        
    return sorted(list_arranged ,  key=lambda x: x[1] , reverse=True)
    
    




def arrange_the_clusters_LFW(list_of_centroids ,list_of_percents):
    index = 0
    list_arranged = []
    while index < len(list_of_centroids):
        index_inside_centroid = 0
        summation = 0
        while index_inside_centroid < len(list_of_centroids[index]):
            summation = summation + list_of_percents[index_inside_centroid] * list_of_centroids[index][index_inside_centroid]
            index_inside_centroid += 1
        list_arranged.append([index,summation / len(list_of_percents)])
        index += 1
        
    return sorted(list_arranged ,  key=lambda x: x[1] , reverse=True)    
            
      


def extract_players_from_certain_cluster(cluster_number , list_of_players , list_of_labels):
    list_of_extracted_players = []
    indexes = []
    index = 0
    while index < len(list_of_labels):
        if list_of_labels[index] == cluster_number:
            list_of_extracted_players.append(list_of_players[index])
            indexes.append(index)
        index += 1
    return list_of_extracted_players , indexes




def rank_players_inside_cluster(cluster_number , list_of_players , list_of_labels , vector , features_for_players):
    players_and_indexes = extract_players_from_certain_cluster(cluster_number , list_of_players , list_of_labels)
    players_in_cluster = players_and_indexes[0]
    indexes = players_and_indexes[1]
    list_of_values = []
    ######### ranking process #################
    ################# getting values ###########
    index = 0
    while index < len(indexes):
        features_of_the_player = features_for_players[indexes[index]]
        value_of_the_player = 0
        index_inside_features = 0
        while index_inside_features < len(features_of_the_player):
            value_of_the_player = value_of_the_player + vector[index_inside_features] * features_of_the_player[index_inside_features]
            index_inside_features += 1
        list_of_values.append([players_in_cluster[index] , value_of_the_player])
        index += 1
        
    result = sorted(list_of_values ,  key=lambda x: x[1] , reverse=True)
    return result

    
    

def get_cluster_of_certain_player(playerId , list_of_players , list_of_labels):
    index_of_the_player = list_of_players.index(playerId)
    return list_of_labels[index_of_the_player]    



def get_players_in_certain_cluster(list_of_players, list_of_labels, list_of_features , num_of_cluster):
    players_of_cluster = []
    features_of_players = []
    index = 0
    while index < len(list_of_players):
        if list_of_labels[index] == num_of_cluster:
            players_of_cluster.append(list_of_players[index])
            features_of_players.append(list_of_features[index])
        index += 1
    return players_of_cluster , features_of_players


def get_most_valuable_player(list_of_players , list_of_features , index_of_required_feature):
    print(list_of_features[0])
    lst = []
    index = 0
    while index < len(list_of_players):
        lst.append(list_of_features[index][index_of_required_feature])
        index += 1
    m = max(lst)
    maxes = [i for i, j in enumerate(lst) if j == m]
    print(maxes)
    returned_list = []
    index = 0
    while index < len(maxes):
        returned_list.append(list_of_players[maxes[index]])
        index += 1
    return returned_list
    

#x = [5, 6,9,7,10,4,30,8,9,1,1,0]
#m = max(x)
#maxes = [i for i, j in enumerate(x) if j == m]
#print(maxes)

def recommend_player_in_certain_position(player_toBe_changed , list_of_players , list_of_labels , vector , features_of_players , clusters_ranked):
    cluster_of_player = get_cluster_of_certain_player(player_toBe_changed , list_of_players , list_of_labels)
    print('cluster number: ' , cluster_of_player)
    players_ranked = rank_players_inside_cluster(cluster_of_player , list_of_players , list_of_labels , vector , features_of_players)
    return players_ranked[0]
    
#    index = 0
#    while index < len(players_ranked):
#        if player_toBe_changed == players_ranked[index][0]:
#            break
#        index += 1
#    
#    if index != 0:
#        return players_ranked[index - 1][0]
#    else:
#        return -1

def print_name_for_one_player(fn , ln):
    print(first_last_names_in_list(fn , ln))
    


def print_names_for_list_of_players(list_of_players):
    index = 0
    while index < len(list_of_players):
        fn = players[players['wyId'] == list_of_players[index]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == list_of_players[index]]['lastName'].tolist()[0]
        lst = first_last_names_in_list(fn , ln)
        print( lst, list_of_players[index])
        index += 1
    
        
        
        
        
def get_players_in_team_by_teamId(teamId):
    players_IDs = players[players['currentTeamId'] == teamId]['wyId'].tolist()
    return players_IDs





def get_players_in_general_position_in_team(teamId , position):
    players_in_team = get_players_in_team_by_teamId(teamId)
    players_in_certain_pos = []
    index = 0
    while index < len(players_in_team):
        if players[players['wyId'] == players_in_team[index]]['role'].tolist()[0]['name'] == position:
            players_in_certain_pos.append(players_in_team[index])
        index += 1
    
    return players_in_certain_pos
    

list_of_positions = ['Goalkeeper' , 'Centre-Back' , 'Left-Back' , 'Right-Back' , 'Defensive Midfield' , 'Central Midfield' , 'Attacking Midfield',
                      'Left Winger' , 'Right Winger' , 'Centre-Forward' , 'Left Midfield' , 'Right Midfield']
def get_players_in_certain_position_from_position_section(name_of_pos):
    return players[players['position'] == name_of_pos]['wyId'].tolist()




def get_num_of_goals_scored_by_certain_team(teamId):
    players_of_team = get_players_in_team_by_teamId(teamId)
    return sum(number_of_goals_for_list_of_players(matchesIds,players_of_team))
    




def get_players_in_certain_position_of_team(teamId , pos):
    players_of_team = get_players_in_team_by_teamId(teamId)
    returned_list = []
    index = 0
    while index < len(players_of_team):
        if len(players[players['wyId'] == players_of_team[index]]['position'].tolist()) > 0:
            if players[players['wyId'] == players_of_team[index]]['position'].tolist()[0] == pos:
                returned_list.append(players_of_team[index])
        index += 1
    return returned_list
    
    
    

def get_players_in_forward_positions_for_list(list_of_players):
    returned_list = []
    index = 0
    while index < len(list_of_players):
        position = players[players['wyId'] == list_of_players[index]]['position'].tolist()[0]
        if position == 'Centre-Forward' or position == 'Right Winger' or position == 'Left Winger':
            returned_list.append(list_of_players[index])
        index += 1
    return returned_list



    
    



def get_players_in_mf_positions_for_list(list_of_players):
    returned_list = []
    index = 0
    while index < len(list_of_players):
        position = players[players['wyId'] == list_of_players[index]]['position'].tolist()[0]
        if position == 'Attacking Midfield' or position == 'Central Midfield':
            returned_list.append(list_of_players[index])
        index += 1
    return returned_list
        



def get_index_of_smallest_of_list(lst):
    mini = lst[0]
    index = 1
    returned_index = 0
    while index < len(lst):
        if lst[index] < mini:
            mini = lst[index]
            returned_index = index
        index += 1
    return returned_index


def who_played(list_of_players):
    returned_list = []
    index = 0
    while index < len(list_of_players):
        if minutes_played_by_one_player(matchesIds , list_of_players[index]) != 0:
           returned_list.append(list_of_players[index])
        index += 1
    return returned_list


def get_least_scoring_forward_for_certain_team(teamId):
    players_of_team = get_players_in_team_by_teamId(teamId)
    forwards = get_players_in_forward_positions_for_list(players_of_team)
    forwards_who_played = who_played(forwards)
    goals = number_of_goals_for_list_of_players(matchesIds , forwards_who_played)
    index = get_index_of_smallest_of_list(goals)
    return forwards_who_played[index]




def get_least_assisting_mf_for_certain_team(teamId):
    players_of_team = get_players_in_team_by_teamId(teamId)
    mf = get_players_in_mf_positions_for_list(players_of_team)
    mfs_who_played = who_played(mf)
    assists = number_of_events_for_list_of_players(events_passes ,mfs_who_played , mfs_who_played)
    index = get_index_of_smallest_of_list(assists)
    return mfs_who_played[index]


colors = ['red' , 'blue' , 'green' , 'cyan' , 'brown']

def show_the_two_clusters(dataset , num_of_clusters):
    dataset1 = np.asarray(dataset)
    #print(dataset1)    
    kmeans = KMeans(n_clusters = num_of_clusters,init = 'k-means++',  max_iter = 300, n_init = 10, random_state = 0)
    y_kmeans = kmeans.fit_predict(dataset1)
#    x = [x for x,y in dataset1]
#    y = [y for x,y in dataset1]
#    plt.scatter(x, y , s = 100 , c = 'red')
    index = 0
    while index < num_of_clusters:
        plt.scatter(dataset1[y_kmeans == index,0],dataset1[y_kmeans == index,1], s = 100, c = colors[index] , label = 'Cluster '+ str(index))
        plt.legend()
        index += 1
    plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1] , s = 300 , c = 'yellow' , label = 'Centroids')
    plt.title('Kmeans Feature Space for Strikers')
    plt.xlabel('Number of goals')
    plt.ylabel('Number of assists')
    plt.savefig("E:\guc\Semster 8\Project\FS\K-means Feature Space for ST")
    
    
def show_feature_space(dataset ):
    dataset1 = np.asarray(dataset)
    #print(dataset1)    

    x = [x for x,y in dataset1]
    y = [y for x,y in dataset1]
    plt.scatter(x, y , s = 100 , c = 'red')
  
    plt.title('Kmeans Feature Space for Strikers')
    plt.xlabel('Number of goals')
    plt.ylabel('Number of assists')
    plt.savefig("E:\guc\Semster 8\Project\FS\K-means Feature Space for ST")


    

def applyingMeanShiftAlgorithm_for_two_features(dataset):
    dataset1 = np.asarray(dataset)
    ms = MeanShift()
    x = ms.fit_predict(dataset1)
    
    #print(s)
    
    index = 0
    while index < len(ms.cluster_centers_):
        plt.scatter(dataset1[x == index,0],dataset1[x == index,1], s = 100, c = colors[index] , label = 'Cluster '+ str(index))
        plt.legend()
        index += 1
    plt.scatter(ms.cluster_centers_[:,0],ms.cluster_centers_[:,1] , s = 300 , c = 'yellow' , label = 'Centroids')
    plt.title('Mean Shift Feature Space for Strikers')
    plt.xlabel('Number of goals')
    plt.ylabel('Number of assists')
    plt.savefig("E:\guc\Semster 8\Project\FS\Mean Shift Feature Space for ST.png")
    
    #return ms.labels_ , ms.cluster_centers_  



def build_clusters_with_HC_for_two_features(dataset , number_of_clusters):
    dataset1 = np.asarray(dataset)
    hc = AgglomerativeClustering(n_clusters = number_of_clusters , affinity = 'euclidean' , linkage = 'ward')
    y_hc = hc.fit_predict(dataset1)
    clf = NearestCentroid()
    clf.fit(dataset1, y_hc)
    
    index = 0
    while index < number_of_clusters:
        plt.scatter(dataset1[y_hc == index,0],dataset1[y_hc == index,1], s = 100, c = colors[index] , label = 'Cluster '+ str(index))
        plt.legend()
        index += 1
    plt.scatter( clf.centroids_[:,0], clf.centroids_[:,1] , s = 300 , c = 'yellow' , label = 'Centroids')
    plt.title('HC Feature Space for Strikers')
    plt.xlabel('Number of goals')
    plt.ylabel('Number of assists')
    plt.savefig("E:\guc\Semster 8\Project\FS\HC Feature Space for ST.png")
    
    

def scatter_two_features_st():
    strikers = get_players_in_certain_position_from_position_section('Centre-Forward')
    center_Forwards_features = extract_two_features_for_strikers(strikers)
    tolist_to_kmeans = to_list_to_kmeans2(center_Forwards_features[0] , center_Forwards_features[1]) 
    show_feature_space(tolist_to_kmeans)
    plt.title('Feature Space for Strikers')
    plt.xlabel('Number of goals')
    plt.ylabel('Number of assists')
    plt.savefig("E:\guc\Semster 8\Project\FS\Feature Space.png")
        

def scatter_two_features_kmeans_st():
    strikers = get_players_in_certain_position_from_position_section('Centre-Forward')
    center_Forwards_features = extract_two_features_for_strikers(strikers)
    tolist_to_kmeans = to_list_to_kmeans2(center_Forwards_features[0] , center_Forwards_features[1])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show_the_two_clusters(tolist_to_kmeans , num_of_clusters)
    
    
def scatter_two_features_meanShift_st():
    strikers = get_players_in_certain_position_from_position_section('Centre-Forward')
    center_Forwards_features = extract_two_features_for_strikers(strikers)
    tolist_to_kmeans = to_list_to_kmeans2(center_Forwards_features[0] , center_Forwards_features[1])
    applyingMeanShiftAlgorithm_for_two_features(tolist_to_kmeans)
    
    

def scatter_two_features_HC_st():
    strikers = get_players_in_certain_position_from_position_section('Centre-Forward')
    center_Forwards_features = extract_two_features_for_strikers(strikers)
    tolist_to_kmeans = to_list_to_kmeans2(center_Forwards_features[0] , center_Forwards_features[1])
    use_dendroGram_to_find_optimal_num_of_clusters(tolist_to_kmeans)
    number_of_clusters = eval(input('Please Enter The number of clusters: '))
    build_clusters_with_HC_for_two_features(tolist_to_kmeans , number_of_clusters)
    

scatter_two_features_st()
scatter_two_features_kmeans_st()
scatter_two_features_meanShift_st()
scatter_two_features_HC_st()
#players_of_team = get_players_in_team_by_teamId(1625)
#forwards = get_players_in_forward_positions_for_list(players_of_team)
#print_names_for_list_of_players(forwards)
#number_of_goals_for_list_of_players(matchesIds , forwards)
#
#get_least_scoring_forward_for_certain_team(1625)
#    
#players[players['wyId'] == 265673]['firstName']
#players[players['wyId'] == 265673]['lastName']
#
#
    
get_least_scoring_forward_for_certain_team(676)
get_least_assisting_mf_for_certain_team(676)
players[players['wyId'] == 28529]['firstName'].tolist()[0]
players[players['wyId'] == 28529]['lastName'].tolist()[0]
players[players['wyId'] == 211885]['position'].tolist()[0]
players
pl = get_players_in_team_by_teamId(1625)
print_names_for_list_of_players(pl)

get_teams_in_certain_area('Spain')



get_players_in_certain_position_of_team(676 , 'Right-Back')

teamId = 676
league = get_league_of_certain_team(teamId)
matches = matches_played_by_certain_team(teamId , league)
goals = get_goals_scored_aganist_certain_team(teamId , league , matches)



p = positions_of_events_precced_list_of_goals(goals[2] , goals[1] , league , goals[-1])  



mat = create_matrix_to_draw(p)

draw_graph_for_events_before_goals(mat)

m = max_of_matrix(mat)


get_maxes_of_matrix(mat , m)

################3 running the code ##################################################################

def run_kmeans_for_cb():
    center_backs = get_players_in_certain_position_from_position_section('Centre-Back')
    center_backs_features = extract_features_for_center_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans5(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3] , center_backs_features[4])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(5 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , center_backs_features[-1] , show[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0] , players_ranked[index][1])
        index += 1
        
    return center_backs_features[-1] , show[0] , vector , tolist_to_kmeans
        

km_cb = run_kmeans_for_cb()
extract_features_for_center_backs([138408])

def run_mean_shift_for_cb():
    center_backs = get_players_in_certain_position_from_position_section('Centre-Back')
    center_backs_features = extract_features_for_center_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans4(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3])
    mean_shift = applyingMeanShiftAlgorithm(tolist_to_kmeans)
    num_of_clusters = len(mean_shift[-1])
    vector = applyingPca(4 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(mean_shift[1] , vector))
    print(vector)
    print('number-of_clusters is: ' ,num_of_clusters )
    players_ranked = rank_players_inside_cluster(1 , center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(fn , ln, players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans

ms = run_mean_shift_for_cb()


def run_hc_for_cb():
    center_backs = get_players_in_certain_position_from_position_section('Centre-Back')
    center_backs_features = extract_features_for_center_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans4(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3])
    use_dendroGram_to_find_optimal_num_of_clusters(tolist_to_kmeans)
    num_of_clusters = eval(input('please enter the number of the clusters: '))
    hc_model = build_clusters_with_HC(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(4 , tolist_to_kmeans)
    print(arrange_the_clusters(hc_model[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(0 , center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(fn , ln, players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans


hc = run_hc_for_cb()
    
    

def run_kmeans_for_left_back():
    center_backs = get_players_in_certain_position_from_position_section('Left-Back')
    center_backs_features = extract_features_for_left_or_right_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans7(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3] , center_backs_features[4] , center_backs_features[5] , center_backs_features[6])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(7 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(2 , center_backs_features[-1] , show[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn,ln),players_ranked[index][1] ,players_ranked[index][0])
        index += 1
    return center_backs_features[-1] , show[0] , vector , tolist_to_kmeans
    
km = run_kmeans_for_left_back()
number_of_events_for_one_player(events_duels , 222220 , 1601)

extract_features_for_left_or_right_backs([3310])
number_of_events_for_one_player(events_passes , 3269 , 302)


def run_mean_shift_for_lb():
    center_backs = get_players_in_certain_position_from_position_section('Left-Back')
    center_backs_features = extract_features_for_center_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans5(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3],  center_backs_features[4])
    mean_shift = applyingMeanShiftAlgorithm(tolist_to_kmeans)
    num_of_clusters = len(mean_shift[-1])
    vector = applyingPca(5 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(mean_shift[1] , vector))
    print(vector)
    print('number-of_clusters is: ' ,num_of_clusters )
    
    players_ranked = rank_players_inside_cluster(1 ,center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(fn , ln, players_ranked[index][0])
        index += 1

    return center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans

ms = run_mean_shift_for_lb()



def run_hc_for_lb():
    center_backs = get_players_in_certain_position_from_position_section('Left-Back')
    center_backs_features = extract_features_for_center_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans5(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3],  center_backs_features[4])
    use_dendroGram_to_find_optimal_num_of_clusters(tolist_to_kmeans)
    num_of_clusters = eval(input('please enter the number of the clusters: '))
    hc_model = build_clusters_with_HC(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(5 , tolist_to_kmeans)
    print(arrange_the_clusters(hc_model[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(fn , ln, players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans


hc = run_hc_for_lb()
    





def run_kmeans_for_right_back():
    center_backs = get_players_in_certain_position_from_position_section('Right-Back')
    center_backs_features = extract_features_for_left_or_right_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans6(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3],  center_backs_features[4] , center_backs_features[5])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(6 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(2 , center_backs_features[-1] , show[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0] , players_ranked[index][1])
        index += 1   
    return center_backs_features[-1] , show[0] , vector , tolist_to_kmeans
    


km = run_kmeans_for_right_back()
get_cluster_of_certain_player(3347 , km[0] , km[1])

o = get_players_in_certain_cluster(km[0] , km[1] , km[-1] , 2)

get_most_valuable_player(o[0] ,o[1] , 4 )


extract_features_for_left_or_right_backs([167145])

f = get_players_in_team_by_teamId(1625)
print_names_for_list_of_players(f)

get_teams_in_certain_area('Germany')

def run_mean_shift_for_rb():
    center_backs = get_players_in_certain_position_from_position_section('Right-Back')
    center_backs_features = extract_features_for_left_or_right_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans6(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3] , center_backs_features[4] , center_backs_features[5])
    mean_shift = applyingMeanShiftAlgorithm(tolist_to_kmeans)
    num_of_clusters = len(mean_shift[-1])
    vector = applyingPca(6 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(mean_shift[1] , vector))
    print(vector)
    print('number-of_clusters is: ' ,num_of_clusters )
    players_ranked = rank_players_inside_cluster(2 , center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans

ms = run_mean_shift_for_rb()

get_cluster_of_certain_player(3347 , ms[0] , ms[1])

o = get_players_in_certain_cluster(ms[0] , ms[1] , ms[-1] , 2)

get_most_valuable_player(o[0] ,o[1] , 4 )

players[players['wyId'] == 3270]['firstName']

def run_hc_for_rb():
    center_backs = get_players_in_certain_position_from_position_section('Right-Back')
    center_backs_features = extract_features_for_left_or_right_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans6(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3] , center_backs_features[4], center_backs_features[5])
    use_dendroGram_to_find_optimal_num_of_clusters(tolist_to_kmeans)
    num_of_clusters = eval(input('please enter the number of the clusters: '))
    hc_model = build_clusters_with_HC(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(6 , tolist_to_kmeans)
    print(arrange_the_clusters(hc_model[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(fn , ln, players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans


hc = run_hc_for_rb()

get_cluster_of_certain_player(3347 , hc[0] , hc[1])

o = get_players_in_certain_cluster(hc[0] , hc[1] , hc[-1] , 1)

get_most_valuable_player(o[0] ,o[1] , 4 )

def run_kmeans_for_st():
    strikers = get_players_in_certain_position_from_position_section('Centre-Forward')
    center_Forwards_features = extract_features_for_strikers(strikers)
    tolist_to_kmeans = to_list_to_kmeans4(center_Forwards_features[0] , center_Forwards_features[1] , center_Forwards_features[2], center_Forwards_features[3])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(4 , tolist_to_kmeans)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , center_Forwards_features[-1] , show[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn ,ln) ,players_ranked[index][1])
        index += 1   
    return center_Forwards_features[-1] , show[0] , vector , tolist_to_kmeans


km = run_kmeans_for_st()
get_cluster_of_certain_player(8717 , km[0] , km[1])


extract_features_for_strikers([7972])

if 28.75167434184722 > 28.751299029900814:
    print(28.75167434184722 - 28.751299029900814)

def run_mean_shift_for_st():
    center_backs = get_players_in_certain_position_from_position_section('Centre-Forward')
    center_backs_features = extract_features_for_center_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans4(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3])
    mean_shift = applyingMeanShiftAlgorithm(tolist_to_kmeans)
    num_of_clusters = len(mean_shift[-1])
    vector = applyingPca(4 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(mean_shift[1] , vector))
    print(vector)
    print('number-of_clusters is: ' ,num_of_clusters )
    players_ranked = rank_players_inside_cluster(0 , center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(index , '--' ,fn , ln, players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans

ms = run_mean_shift_for_st()
get_cluster_of_certain_player(8717 , ms[0] , ms[1])


def run_hc_for_st():
    center_backs = get_players_in_certain_position_from_position_section('Centre-Forward')
    center_backs_features = extract_features_for_center_backs(center_backs)
    tolist_to_kmeans = to_list_to_kmeans4(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3])
    use_dendroGram_to_find_optimal_num_of_clusters(tolist_to_kmeans)
    num_of_clusters = eval(input('please enter the number of the clusters: '))
    hc_model = build_clusters_with_HC(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(4 , tolist_to_kmeans)
    print(arrange_the_clusters(hc_model[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(fn , ln, players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans


hc = run_hc_for_st()
get_cluster_of_certain_player(8717 , hc[0] , hc[1])



def run_kmeans_for_right_fw():
    strikers = get_players_in_certain_position_from_position_section('Right Winger')
    right_Forwards_features = extract_features_for_left_right_forward(strikers)
    tolist_to_kmeans = to_list_to_kmeans4(right_Forwards_features[0] , right_Forwards_features[1] , right_Forwards_features[2], right_Forwards_features[3])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(4 , tolist_to_kmeans)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , right_Forwards_features[-1] , show[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][1])
        index += 1  
    return right_Forwards_features[-1] , show[0] , vector , tolist_to_kmeans


rfw_kmeans = run_kmeans_for_right_fw()

get_cluster_of_certain_player(4256 , rfw_kmeans[0] , rfw_kmeans[1])

o = get_players_in_certain_cluster(rfw_kmeans[0] , rfw_kmeans[1] , rfw_kmeans[-1] , 3)

get_most_valuable_player(o[0] ,o[1] , 1 )


def run_mean_shift_for_rfw():
    center_backs = get_players_in_certain_position_from_position_section('Right Winger')
    center_backs_features = extract_features_for_left_right_forward(center_backs)
    tolist_to_kmeans = to_list_to_kmeans4(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3])
    mean_shift = applyingMeanShiftAlgorithm(tolist_to_kmeans)
    num_of_clusters = len(mean_shift[-1])
    vector = applyingPca(4 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(mean_shift[1] , vector))
    print(vector)
    print('number-of_clusters is: ' ,num_of_clusters )
    players_ranked = rank_players_inside_cluster(2 , center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans


rfw_meanshift = run_mean_shift_for_rfw()


get_cluster_of_certain_player(4256 , rfw_meanshift[0] , rfw_meanshift[1])

o = get_players_in_certain_cluster(rfw_meanshift[0] , rfw_meanshift[1] , rfw_meanshift[-1] , 1)

get_most_valuable_player(o[0] ,o[1] , 1 )

extract_features_for_left_right_forward([120353])

def run_hc_for_rfw():
    center_backs = get_players_in_certain_position_from_position_section('Right Winger')
    center_backs_features = extract_features_for_left_right_forward(center_backs)
    tolist_to_kmeans = to_list_to_kmeans4(center_backs_features[0] , center_backs_features[1] , center_backs_features[2] , center_backs_features[3])
    use_dendroGram_to_find_optimal_num_of_clusters(tolist_to_kmeans)
    num_of_clusters = eval(input('please enter the number of the clusters: '))
    hc_model = build_clusters_with_HC(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(4 , tolist_to_kmeans)
    print(arrange_the_clusters(hc_model[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(0 , center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans


hc_rfw = run_hc_for_rfw()
get_cluster_of_certain_player(4256 , hc_rfw[0] , hc_rfw[1])

o = get_players_in_certain_cluster(hc_rfw[0] , hc_rfw[1] , hc_rfw[-1] , 0)

get_most_valuable_player(o[0] ,o[1] , 1 )

extract_features_for_left_right_forward([120353])


def run_kmeans_for_left_fw():
    strikers = get_players_in_certain_position_from_position_section('Left Winger')
    left_Forwards_features = extract_features_for_left_right_forward(strikers)
    tolist_to_kmeans = to_list_to_kmeans4(left_Forwards_features[0] , left_Forwards_features[1] , left_Forwards_features[2] , left_Forwards_features[3])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(4 , tolist_to_kmeans)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , left_Forwards_features[-1] , show[0] ,vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][1])
        index += 1 
    return left_Forwards_features[-1] , show[0] , vector , tolist_to_kmeans
   ## shots/ minutes , passes/ minutes , goals , assists LFW   RFW   
   
lfw_kmeans = run_kmeans_for_left_fw()   

        
def run_kmeans_for_cmf():
    strikers = get_players_in_certain_position_from_position_section('Central Midfield')
    features_cmf = extract_features_for_cmf_amf(strikers)
    tolist_to_kmeans = to_list_to_kmeans3(features_cmf[0] , features_cmf[1] , features_cmf[2] )
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(3 , tolist_to_kmeans)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(0 , features_cmf[-1] , show[0] ,vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0] , players_ranked[index][1])
        index += 1
    return features_cmf[-1] , show[0] , vector , tolist_to_kmeans

p = run_kmeans_for_cmf()
get_cluster_of_certain_player(211885 , p[0] , p[1])

o = get_players_in_certain_cluster(p[0] , p[1] , p[-1] , 2)

get_most_valuable_player(o[0] ,o[1] , 1 )

recommend_player_in_certain_position(211885, p[0], p[1], p[2], p[3])
players[players['wyId'] == 142755]['firstName']
players[players['wyId'] == 142755]['lastName']


get_cluster_of_certain_player(8287 ,p[0] , p[1])
get_clubs()
f = get_players_in_team_by_teamId(676)
print_names_for_list_of_players(f)

number_of_events_for_one_player(events_passes , 7936 , 901)
extract_features_for_cmf_amf([3318])



def run_hc_for_cmf():
    center_backs = get_players_in_certain_position_from_position_section('Central Midfield')
    center_backs_features = extract_features_for_cmf_amf(center_backs)
    tolist_to_kmeans = to_list_to_kmeans3(center_backs_features[0] , center_backs_features[1] , center_backs_features[2])
    use_dendroGram_to_find_optimal_num_of_clusters(tolist_to_kmeans)
    num_of_clusters = eval(input('please enter the number of the clusters: '))
    hc_model = build_clusters_with_HC(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(3 , tolist_to_kmeans)
    print(arrange_the_clusters(hc_model[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(1 , center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , hc_model[0] , vector , tolist_to_kmeans

hc_cmf = run_hc_for_cmf()
get_cluster_of_certain_player(211885 , hc_cmf[0] , hc_cmf[1])

o = get_players_in_certain_cluster(hc_cmf[0] , hc_cmf[1] , hc_cmf[-1] , 1)

get_most_valuable_player(o[0] ,o[1] , 1 )


def run_mean_shift_for_cmf():
    center_backs = get_players_in_certain_position_from_position_section('Central Midfield')
    center_backs_features = extract_features_for_cmf_amf(center_backs)
    tolist_to_kmeans = to_list_to_kmeans3(center_backs_features[0] , center_backs_features[1] , center_backs_features[2])
    mean_shift = applyingMeanShiftAlgorithm(tolist_to_kmeans)
    num_of_clusters = len(mean_shift[-1])
    vector = applyingPca(3 , tolist_to_kmeans)
    #arrange_the_clusters(show[1] , vector)
    print(arrange_the_clusters(mean_shift[1] , vector))
    print(vector)
    print('number-of_clusters is: ' ,num_of_clusters )
    players_ranked = rank_players_inside_cluster(0 , center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0])
        index += 1
        
    return center_backs_features[-1] , mean_shift[0] , vector , tolist_to_kmeans

cmf_meanshift = run_mean_shift_for_cmf()
get_cluster_of_certain_player(211885 , cmf_meanshift[0] , cmf_meanshift[1])

o = get_players_in_certain_cluster(cmf_meanshift[0] , cmf_meanshift[1] , cmf_meanshift[-1] ,0)

get_most_valuable_player(o[0] ,o[1] , 1 )


def run_kmeans_for_amf():
    strikers = get_players_in_certain_position_from_position_section('Attacking Midfield')
    features_cmf = extract_features_for_cmf_amf(strikers)
    tolist_to_kmeans = to_list_to_kmeans5(features_cmf[0] , features_cmf[1] , features_cmf[2] , features_cmf[3] , features_cmf[4])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(4 , tolist_to_kmeans)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(0 , features_cmf[-1] , show[0] ,vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn ,ln), players_ranked[index][1] , players_ranked[index][0])
        index += 1 
    return features_cmf[-1] , show[0] , vector , tolist_to_kmeans

amf_kmeans = run_kmeans_for_amf()
number_of_events_for_one_player(events_passes , 8317 , 302)    
    
def run_kmeans_for_dmf():
    strikers = get_players_in_certain_position_from_position_section('Defensive Midfield')
    features_cmf = extract_features_for_dmf(strikers)
    tolist_to_kmeans = to_list_to_kmeans8(features_cmf[0] , features_cmf[1] , features_cmf[2] , features_cmf[3] , features_cmf[4],features_cmf[5] , features_cmf[6] , features_cmf[7])
    wcss = the_optimal_num_of_k_clusters(tolist_to_kmeans)
    num_of_clusters = optimal_number_of_clusters(wcss)
    show = show_the_clusters(tolist_to_kmeans , num_of_clusters)
    vector = applyingPca(8 , tolist_to_kmeans)
    print(arrange_the_clusters(show[1] , vector))
    print(vector)
    players_ranked = rank_players_inside_cluster(3 , features_cmf[-1] , show[0] ,vector , tolist_to_kmeans)
    index = 0
    while index < len(players_ranked):
        fn = players[players['wyId'] == players_ranked[index][0]]['firstName'].tolist()[0]
        ln = players[players['wyId'] == players_ranked[index][0]]['lastName'].tolist()[0]
        print(first_last_names_in_list(fn , ln), players_ranked[index][0] , players_ranked[index][1])
        index += 1
    return features_cmf[-1] , show[0] , vector , tolist_to_kmeans         
     

        
dmf_kmeans = run_kmeans_for_dmf()
extract_features_for_dmf([69968])


run_kmeans_for_amf()
number_of_events_for_one_player(events_duels , 21315 , 1601)
number_of_subEvents_for_one_player(21315 , events_duels , 13)   
cmf_kmeans = run_kmeans_for_cmf()
recommend_player_in_certain_position(8246 , cmf_kmeans[0] , cmf_kmeans[1] , cmf_kmeans[2] , cmf_kmeans[3])
    
run_kmeans_for_left_fw()   
    

run_kmeans_for_right_fw()

players['position'].value_counts()
run_kmeans_for_st()

extract_features_for_strikers([3359])
number_of_goals_for_one_player(matchesIds , 3359)
minutes_played_by_one_player(matchesIds , 21385)
s = "Antonio Barrag\u00e1n Fern\u00e1ndez"
s = s.encode('utf-32').decode('utf-32','ignore')
print(s)

number_of_events_for_one_player(events_passes,14723 , 301)
f = get_players_in_team_by_teamId(676)
extract_features_for_cmf_amf([25826])
print_names_for_list_of_players(f)
extract_features_for_dmf([40756])
#####################################################################################################
recommend_player_in_certain_position(211885, )
