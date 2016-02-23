from urllib.request import urlopen
from urllib.error import *
import json
import xml.etree.ElementTree as ET
import datetime
import dateutil

def getdatestring(year, month, day):
    y = ''
    for i in range(4 - len(y)):
        y += '0'
    #end if
    y = y + str(year)
    m = ('0' + str(month) if month < 10 else str(month))
    d = ('0' + str(day) if day < 10 else str(day))
    return str(year) + str(m) + str(d)
#end getdatestring

def decrementday(d):
    if type(d) != datetime.date:
        raise TypeError("decrementday expects a date object.")
    #end if
    #d = d - datetime.timedelta(days=1)
    d = d - dateutil.relativedelta(days=-1)
#end decrementday

def end_of_last_season_date(d):
    if type(d) != datetime.date:
        raise TypeError("end_of_last_season_date expects a date object.")
    #end if
    
    today = datetime.date.today()
    new_date = d
    season_start = datetime.date(d.year, 4, 4)
    season_end = datetime.date(d.year, 10, 4)
    if d < season_start:
        new_date = dateutil.relativedelta(season_end, datetime(today.year, 10, 4))
    elif d > season_end:
        new_date = season_end
    #end if
    return new_date
#end end_of_last_season_date

#Get current date.
now = datetime.date.today()
year = now.year
month = now.month
day = now.day

print("Now: " + str(now) + " Last Season: " + str(end_of_last_season_date(now)))

#Convert to MLB GameDay2-acceptable URL
str_year = 'year_' + str(year) + '/'
str_month = 'month_' + ('0' + str(month) if month < 10 else str(month)) + '/'
str_day = 'day_' + ('0' + str(day) if day < 10 else str(day)) + '/'
str_date = str_year + str_month + str_day
base_url = "http://gd2.mlb.com/components/game/mlb/"
midseason_url = base_url + str_date + "scoreboard_windows.xml"

#Grab data from server.
url = None
html = None
my_file = None
json_dict = None

try:
    url = midseason_url
    html = urlopen(url).read().decode()
    xml_tree = ET.fromstring(html)
    root = xml_tree.getroot()
    has_children = False
    for child in root:
        if has_children == False:
            break
        #end if
    #end for
except URLError as e:
    print("No data available. Check back later.")
    url = None
#end try

if url != None:
    my_file = open(str(year) + str(month) + str(day) + "_mlb_standings.dat", "w")
    print(html, file = my_file)
    my_file.close()
#end if

if my_file == None:
    #No data available for day.
    pass
#end if
