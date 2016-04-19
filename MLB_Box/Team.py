
##
# <summary>A team.</summary>
# <remarks>Casey Ugone, 2/24/2016.</remarks>
# <seealso cref="T:def"/>
# <seealso cref="T:__init__"/>
# <seealso cref="T:(self, played_today, city, name, wins, losses): self.played_today = played_today self.city = city self.name = name self.wins = int(wins) self.losses = int(losses) def __repr__(self): return str(self.city) + ' ' + str(self.name) + ": (" + str(self.wins) + ", " + str(self.losses) + ")" def __lt__(self, other): if self.wins == other.wins: if self.losses == other.losses: return self.city {other.city return self.losses {other.losses return self.wins} other.wins def parse_gameday_data(d, teams_cache): cur_url = date_to_mlb_url(d) html = urlopen(cur_url).read().decode() xml_tree = ET.fromstring(html) for child in xml_tree: if child.tag != "game": continue league_value = child.attrib['league'] if league_value.find('A') {0: continue home_divison = child.attrib['home_division'] away_divison = child.attrib['away_division'] if home_divison != 'C' and away_divison != 'C': continue if home_divison == 'C': name = child.attrib['home_team_name'] wins = int(child.attrib['home_win']) losses = int(child.attrib['home_loss']) teams_cache[name].played_today = True teams_cache[name].wins = wins teams_cache[name].losses = losses if away_divison == 'C': name = child.attrib['away_team_name'] wins = int(child.attrib['away_win']) losses = int(child.attrib['away_loss']) teams_cache[name].played_today = True teams_cache[name].wins = wins teams_cache[name].losses = losses teams_cache ="/>
class Team:
    def __init__(self, played_today, city, name, wins, losses):
        self._played_today = played_today
        self._city = city
        self._name = name
        self._wins = int(wins)
        self._losses = int(losses)
    #end __init__

    ##
    # <summary>Converts this object to a machine-readable string representation.</summary>
    # <remarks>Casey Ugone, 2/24/2016.</remarks>
    # <param name="self">The class instance that this method operates on.</param>
    # <returns>A value.</returns>
    def __repr__(self):
        return str(self._city) + ' ' + str(self._name) + ": (" + str(self._wins) + ", " + str(self._losses) + ")"
    #end __reper__

    ##
    # <summary>Less-than operator.</summary>
    # <remarks>Casey Ugone, 2/24/2016.</remarks>
    # <param name="self"> The class instance that this method operates on.</param>
    # <param name="other">Another instance to compare.</param>
    # <returns>A value.</returns>
    def __lt__(self, other):
        my_games_total = self.wins + self.losses
        your_games_total = other.wins + other.losses
        my_avg = self.wins / my_games_total
        your_avg = other.wins / your_games_total
        return my_avg < your_avg
#        if self._wins == other._wins:
#            if self._losses == other._losses:
#                return self._city < other._city
#            #end if
#            return self._losses < other._losses
        #end if
        return self._wins > other._wins
    #end __lt__
    
    def city(self, city = None):
        if city == None:
            return self._city
        else:
            self._city = city
        #end if
    #end city

    def name(self, name = None):
        if name == None:
            return self._name
        else:
            self._name = name
        #end if
    #end name
    
    def wins(self, wins = None):
        if wins == None:
            return self._wins
        else:
            self._wins = wins
        #end if
    #end wins
        
    def losses(self, losses = None):
        if losses == None:
            return self._losses
        else:
            self._losses = losses
        #end if
    #end wins

    def played_today(self, played = None):
        if played == None:
            return self._played_today
        else:
            self._played_today = played
        #end if
    #end played_today
    
    def set_played_today(self):
        self.played_today(True)
    #end set_played_today

    def clear_played_today(self):
        self.played_today(False)
    #end clear_played_today

#end Team
