from urllib.request import urlopen
from urllib.error import *
import json
import xml.etree.ElementTree as ET
import datetime
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from operator import itemgetter, attrgetter

def get_recent_season_date(d):
    """Returns a date corresponding to the most recent season. If the date argument is within the current season, does nothing.
"""
    if type(d) != datetime.date:
        raise TypeError("get_recent_season_date expects a date object.")
    #end if
    
    season_start = datetime.date(d.year, 4, 5)
    season_end = datetime.date(d.year, 10, 4)

    if d >= season_start and d <= season_end:
        return d
    #end if

    new_date = None
    if d < season_start:
        new_date = d + relativedelta(datetime.date(d.year - 1, 10, 4), d)
    elif d > season_end:
        new_date = season_end
    #end if
    return new_date
#end get_recent_season_date

def date_to_mlb_url(d):

    year = d.year
    month = d.month
    day = d.day

    #Convert to d to MLB GameDay2-acceptable URL
    str_year = 'year_' + str(year) + '/'
    str_month = 'month_' + ('0' + str(month) if month < 10 else str(month)) + '/'
    str_day = 'day_' + ('0' + str(day) if day < 10 else str(day)) + '/'
    str_date = str_year + str_month + str_day
    base_url = "http://gd2.mlb.com/components/game/mlb/"
    return base_url + str_date + "scoreboard_windows.xml"
#end date_to_mlb_url

def get_index_from_name(name):
    return 0 if name == "White Sox" else (1 if name == "Indians" else (2 if name == "Tigers" else (3 if name == "Royals" else (4 if name == "Twins" else -1))))
#end get_index_from_name

class Team:
    def __init__(self, city, name, wins, losses):
        self.city = city
        self.name = name
        self.wins = int(wins)
        self.losses = int(losses)
    #end __init__
    
    def __repr__(self):
        return str(self.city) + ' ' + str(self.name) + ": (" + str(self.wins) + ", " + str(self.losses) + ")"
    #end __reper__

    #Sort by descending wins, then ascending losses, then city    
    def __lt__(self, other):
        if self.wins == other.wins:
            if self.losses == other.losses:
                if self.city == other.city:
                    return self.city < other.city
                #end if
            #end if
            return self.losses < other.losses
        #end if
        return self.wins > other.wins
    #end __lt__

#end Team


def parse_gameday_data(d, teams_cache, teams_played):

    cur_url = date_to_mlb_url(d)
    html = urlopen(url).read().decode()
    xml_tree = ET.fromstring(html)
    
    for child in xml_tree:
        if child.tag != "game":
            continue
        #end if
        
        league_value = child.attrib['league']
        #Team in the American League did not participate
        if league_value.find('A') < 0:
            continue
        #end if
            
        #Neither team is in AL-Central
        home_divison = child.attrib['home_division']
        away_divison = child.attrib['away_division']
        if home_divison != 'C' and away_divison != 'C':
            continue
        #end if

        #Get name/wins/losses for each AL-Central team
        if home_divison == 'C':
            name = child.attrib['home_team_name']
            wins = int(child.attrib['home_win'])
            losses = int(child.attrib['home_loss'])
            #Team played today
            teams_played = True
            teams_cache[name][0] = True
            teams_cache[name][1] = wins
            teams_cache[name][2] = losses
        #end if

        if away_divison == 'C':
            name = child.attrib['away_team_name']
            wins = int(child.attrib['away_win'])
            losses = int(child.attrib['away_loss'])
            #Team played today
            teams_played = True
            teams_cache[name][0] = True
            teams_cache[name][1] = wins
            teams_cache[name][2] = losses
        #end if
    #end for

#end parse_gameday_data


d = datetime.date.today()
url = date_to_mlb_url(get_recent_season_date(d))

cache_file = None
try:
cache_file = open("cache.dat", "r")

cache_file.write(d)
cache_file.close()

#Grab data from server.
cur_url = None
html = None
my_file = None
teams_cache = {"White Sox": [False, 0, 0], \
         "Indians": [False, 0, 0], \
         "Tigers": [False, 0, 0], \
         "Royals": [False, 0, 0], \
         "Twins": [False, 0, 0]}

teams_played = [False, False, False, False, False]


try:
    while all(teams_played) == False:
        parse_gameday_data(d, teams_cache, teams_played)
        d -= relativedelta(days=-1)
    #end while

    #sort teams by less than equivalence
    sorted_teams = sorted(teams)
    
    out_file = open("results.dat", "w")
    out_file.write(d)
    out_file.write(str(sorted_teams))
    out_file.close()
except URLError as e:
    print("No data available. Check back later.")
    url = None
#end try
