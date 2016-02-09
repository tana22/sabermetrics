##The following are the dictionaries and inverse dictionaries used in the
##NHL soup functions

##DICTIONARIES
##Teams
teams = {'ANAHEIM DUCKS' : 'ANA',
'ATLANTA THRASHERS' : 'ATL',
'ARIZONA COYOTES' : 'ARZ',
'BOSTON BRUINS' : 'BOS',
'BUFFALO SABRES' : 'BUF',
'CALGARY FLAMES' : 'CGY',
'CANADIENS MONTREAL' : 'MTL',
'CAROLINA HURRICANES' : 'CAR',
'CHICAGO BLACKHAWKS' : 'CHI',
'COLORADO AVALANCHE' : 'COL',
'COLUMBUS BLUE JACKETS' : 'COL',
'DALLAS STARS' : 'DAL',
'DETROIT RED WINGS' : 'DET',
'EDMONTON OILERS' : 'EDM',
'FLORIDA PANTHERS' : 'FLA',
'LOS ANGELES KINGS' : 'L.A',
'MINNESOTA WILD' : 'MIN',
'MONTREAL CANADIENS' : 'MTL',
'NASHVILLE PREDATORS' : 'NSH',
'NEW JERSEY DEVILS' : 'NJD',
'NEW YORK ISLANDERS' : 'NYI',
'NEW YORK RANGERS' : 'NYR',
'OTTAWA SENATORS' : 'OTT',
'PHOENIX COYOTES' : 'PHX',
'PHILADELPHIA FLYERS' : 'PHI',
'PITTSBURGH PENGUINS' : 'PIT',
'SAN JOSE SHARKS' : 'SJS',
'ST. LOUIS BLUES' : 'STL',
'TAMPA BAY LIGHTNING' : 'TBL',
'TORONTO MAPLE LEAFS' : 'TOR',
'VANCOUVER CANUCKS' : 'VAN',
'WASHINGTON CAPITALS' : 'WSH',
'WINNIPEG JETS' : 'WPG'
}

events = {
'Unknown' : '0',
'SHOT' : '1',
'GOAL' : '2',
'STOP' : '3',
'FAC' : '4',
'HIT' : '5',
'PENL' : '6',
'MISS' : '7',
'TAKE' : '8',
'GIVE' : '9',
'PSTR' : '10',
'PEND' : '11',
'GEND' : '12',
'BLOCK' : '13',
'SOC' : '14',
'GOFF' : '15'
}

shotTypes = {
'Unknown' : '0',
'Wrist' : '1',
'Slap' : '2',
'Snap' : '3',
'Wrap-around' : '4',
'Tip-In' : '5',
'Backhand' : '6'
}

strength = {
'SH' : '-1',
'EV' : '0',
'PP' : '1'
}

zone = {
'Neu. Zone' : '1',
'Def. Zone' : '2',
'Off. Zone' : '3'
}

stoppage = {
'Unknown' : '0',
'GOALIE STOPPED' : '1',
'OFFSIDE' : '2',
'PUCK IN CROWD' : '3',
'PUCK IN NETTING' : '4',
'HIGH STICK' : '5',
'ICING' : '6',
'RINK REPAIR' : '7',
'PUCK FROZEN' : '8',
'TV TIMEOUT' : '9',
'PUCK IN BENCHES':'10',
'HAND PASS' : '11'
}


###INVERSE DICTIONARIES

inv_teams = {v: k for k, v in teams.items()}
inv_events = {v: k for k, v in events.items()}
inv_shotTypes = {v: k for k, v in shotTypes.items()}
inv_strength = {v: k for k, v in strength.items()}
inv_zone = {v: k for k, v in zone.items()}
inv_stoppage = {v: k for k, v in stoppage.items()}



###Helper dicts
##Months
month = {'January' : '01', 'February' : '02', 'March' : '03', 'April' : '04', 'May' : '05', 'June' : '06',
'July' : '07', 'August': '08', 'September':'09','October':'10','November':'11','December':'12' }
