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

from Team import Team

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
        home_league = league_value[1]
        if home_league == 'A' and home_divison == 'C':
            name = child.attrib['home_team_name']
            wins = int(child.attrib['home_win'])
            losses = int(child.attrib['home_loss'])
            if teams_cache[name].played_today() == False:
                #!!DEBUG CODE!!
                print("Home: " + "Div: " + home_divison + " " + name + " W: " + str(wins) + " L: " + str(losses))
                #!!DEBUG CODE!!
                #print(name + " W: " + str(wins) + " L: " + str(losses))
                teams_cache[name].set_played_today()
                teams_cache[name].wins(wins)
                teams_cache[name].losses(losses)
            #end if
        #end if
        
        away_league = league_value[0]
        if away_league == 'A' and away_divison == 'C':
            name = child.attrib['away_team_name']
            wins = int(child.attrib['away_win'])
            losses = int(child.attrib['away_loss'])
            if teams_cache[name].played_today() == False:
                print("Away: " + "Div: " + away_divison + " " + name + " W: " + str(wins) + " L: " + str(losses))
                teams_cache[name].set_played_today()
                teams_cache[name].wins(wins)
                teams_cache[name].losses(losses)
            #end if
        #end if
    #end for

#end parse_gameday2_data

##
# <summary>Raises the physical flags based on standings position.</summary>
# <remarks>Casey Ugone, 3/3/2016.</remarks>
# <param name="cache">The teams cache.</param>
def raiseflags(cache):
    pass
#end raiseflags

#Grab data from server.
teams_cache = {"White Sox": Team(False, "Chicago", "White Sox", 0, 0), \
               "Indians": Team(False, "Cleveland", "Indians", 0, 0), \
               "Tigers": Team(False, "Detroit", "Tigers", 0, 0), \
               "Royals": Team(False, "Kansas City", "Royals", 0, 0), \
               "Twins": Team(False, "Minnesota", "Twins", 0, 0)}

try:
    d = datetime.date.today()
    print(d)
    parse_gameday2_data(d, teams_cache)
    while all([x.played_today() for x in teams_cache.values()]) == False:
        d += relativedelta(days=-1)
        print(d)
        parse_gameday2_data(d, teams_cache)
    #end while

    #sort teams by less than equivalence
    sorted_teams = sorted([_ for _ in teams_cache.values()])
    
    #Flag/Servo Code Here from teams_cache
    #raise_flags(teams_cache)    
    
    out_file = open("results.dat", "w")
    out_file.write(str(d) + '\n')
    out_file.write(str(sorted_teams))
    out_file.close()
except URLError as e:
    print("No data available. Check back later.")
    url = None
#end try
