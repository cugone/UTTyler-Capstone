from urllib.request import urlopen
from urllib.error import *
import json
import xml
import datetime

def dict2xml(d, root_node=None):
    wrap          =     False if None == root_node or isinstance(d, list) else True
    root          = 'objects' if None == root_node else root_node
    root_singular = root[:-1] if 's' == root[-1] and None == root_node else root
    xml           = ''
    children      = []
    
    if isinstance(d, dict):
        for key, value in dict.items(d):
            if isinstance(value, dict):
                children.append(dict2xml(value, key))
            elif isinstance(value, list):
                children.append(dict2xml(value, key))
            else:
                xml = xml + ' ' + key + '="' + str(value) + '"'
            #end if
        #end for
    else:
        for value in d:
            children.append(dict2xml(value, root_singular))
        #end for
    #end if
    end_tag = '>' if 0 < len(children) else '/>'
    
    if wrap or isinstance(d, dict):
        xml = '<' + root + xml + end_tag
    #end if
    if 0 < len(children):
        for child in children:
            xml = xml + child
        #end for
        if wrap or isinstance(d, dict):
            xml = xml + '</' + root + '>'
        #end if
    #end if
    return xml
#end dict2xml

#Get current date.
now = datetime.datetime.now()
#year = now.year
#month = now.month
#day = now.day

year = 2015
month = 10
day = 4

#Convert to MLB GameDay2-acceptable URL
str_year = 'year_' + str(year) + '/'
str_month = 'month_' + ('0' + str(month) if month < 10 else str(month)) + '/'
str_day = 'day_' + ('0' + str(day) if day < 10 else str(day)) + '/'
base_url = "http://gd2.mlb.com/components/game/mlb/"
midseason_url = base_url + str_year + str_month + str_day + "scoreboard_windows.xml"
postseason_url = base_url + str_year + "postseason_scoreboard.json"

#Grab data from server.
url = None
html = None
my_file = None
json_dict = None
try:
    url = postseason_url
    html = urlopen(url).read().decode()
    json_dict = json.loads(html)
    html = dict2xml(json_dict)
except URLError as e:
    url = None
#end try

if url == None:
    try:
        url = midseason_url
        html = urlopen(url).read().decode()
    except URLError as e:
        print("No data available. Check back later.")
        url = None
    #end try
#end if

if url != None:
    my_file = open("daily_mlb_standings.dat", "w")
    print(html, file = my_file)
    my_file.close()
#end if

if my_file == None:
    #No data available for day.
    pass
#end if
