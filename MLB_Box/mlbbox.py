import datetime
import json
import os
import xml.etree.ElementTree as ET
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from operator import itemgetter, attrgetter
from urllib.request import urlopen
from urllib.error import *

##
# <summary>Date to mlb URL.</summary>
# <remarks>Casey Ugone, 2/24/2016.</remarks>
# <param name="date">The date.</param>
# <returns>A URL string pointing to the scoreboard_windows.xml file for the given date.</returns>
def date_to_mlb_url(date):

    year = date.year
    month = date.month
    day = date.day

    #Convert to date to MLB GameDay2-acceptable URL
    str_year = 'year_' + str(year) + '/'
    str_month = 'month_' + ('0' + str(month) if month < 10 else str(month)) + '/'
    str_day = 'day_' + ('0' + str(day) if day < 10 else str(day)) + '/'
    str_date = str_year + str_month + str_day
    base_url = "http://gd2.mlb.com/components/game/mlb/"
    return base_url + str_date + "scoreboard_windows.xml"
#end date_to_mlb_url

##
# <summary>A team.</summary>
# <remarks>Casey Ugone, 2/24/2016.</remarks>
# <seealso cref="T:def"/>
# <seealso cref="T:__init__"/>
# <seealso cref="T:(self, played_today, city, name, wins, losses): self.played_today = played_today self.city = city self.name = name self.wins = int(wins) self.losses = int(losses) def __repr__(self): return str(self.city) + ' ' + str(self.name) + ": (" + str(self.wins) + ", " + str(self.losses) + ")" def __lt__(self, other): if self.wins == other.wins: if self.losses == other.losses: return self.city {other.city return self.losses {other.losses return self.wins} other.wins def parse_gameday_data(d, teams_cache): cur_url = date_to_mlb_url(d) html = urlopen(cur_url).read().decode() xml_tree = ET.fromstring(html) for child in xml_tree: if child.tag != "game": continue league_value = child.attrib['league'] if league_value.find('A') {0: continue home_divison = child.attrib['home_division'] away_divison = child.attrib['away_division'] if home_divison != 'C' and away_divison != 'C': continue if home_divison == 'C': name = child.attrib['home_team_name'] wins = int(child.attrib['home_win']) losses = int(child.attrib['home_loss']) teams_cache[name].played_today = True teams_cache[name].wins = wins teams_cache[name].losses = losses if away_divison == 'C': name = child.attrib['away_team_name'] wins = int(child.attrib['away_win']) losses = int(child.attrib['away_loss']) teams_cache[name].played_today = True teams_cache[name].wins = wins teams_cache[name].losses = losses teams_cache ="/>
class Team:
    def __init__(self, played_today, city, name, wins, losses):
        self.played_today = played_today
        self.city = city
        self.name = name
        self.wins = int(wins)
        self.losses = int(losses)
    #end __init__

    ##
    # <summary>Converts this object to a machine-readable string representation.</summary>
    # <remarks>Casey Ugone, 2/24/2016.</remarks>
    # <param name="self">The class instance that this method operates on.</param>
    # <returns>A value.</returns>
    def __repr__(self):
        return str(self.city) + ' ' + str(self.name) + ": (" + str(self.wins) + ", " + str(self.losses) + ")"
    #end __reper__

    ##
    # <summary>Less-than operator.</summary>
    # <remarks>Casey Ugone, 2/24/2016.</remarks>
    # <param name="self"> The class instance that this method operates on.</param>
    # <param name="other">Another instance to compare.</param>
    # <returns>A value.</returns>
    def __lt__(self, other):
        if self.wins == other.wins:
            if self.losses == other.losses:
                return self.city < other.city
            #end if
            return self.losses < other.losses
        #end if
        return self.wins > other.wins
    #end __lt__

#end Team

##
# <summary>Parse gameday2 data.</summary>
# <remarks>Casey Ugone, 2/24/2016.</remarks>
# <param name="date">       The date.</param>
# <param name="teams_cache">The teams cache.</param>
def parse_gameday2_data(date, teams_cache):

    cur_url = date_to_mlb_url(date)
    html = urlopen(cur_url).read().decode()
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

            teams_cache[name].played_today = True
            teams_cache[name].wins = wins
            teams_cache[name].losses = losses
        #end if

        if away_divison == 'C':
            name = child.attrib['away_team_name']
            wins = int(child.attrib['away_win'])
            losses = int(child.attrib['away_loss'])

            teams_cache[name].played_today = True
            teams_cache[name].wins = wins
            teams_cache[name].losses = losses
        #end if
    #end for

#end parse_gameday2_data


#Grab data from server.
teams_cache = {"White Sox": Team(False, "Chicago", "White Sox", 0, 0), \
               "Indians": Team(False, "Cleveland", "Indians", 0, 0), \
               "Tigers": Team(False, "Detroit", "Tigers", 0, 0), \
               "Royals": Team(False, "Kansas City", "Royals", 0, 0), \
               "Twins": Team(False, "Minnesota", "Twins", 0, 0)}

try:
    d = datetime.date.today()
    parse_gameday2_data(d, teams_cache)
    while all([x.played_today for x in teams_cache.values()]) == False:
        d += relativedelta(days=-1)
        parse_gameday_data(d, teams_cache)
    #end while

    #sort teams by less than equivalence
    sorted_teams = sorted([_ for _ in teams_cache.values()])
    
    out_file = open("results.dat", "w")
    out_file.write(str(d) + '\n')
    out_file.write(str(sorted_teams))
    out_file.close()
except URLError as e:
    print("No data available. Check back later.")
    url = None
#end try
