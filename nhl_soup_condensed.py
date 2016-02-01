import nhl_dictionaries as dicts
import eventFunctions as ef
import nhl_soup as nhls

def WriteCondensedFmt(directory,filename,soup,gameinfo):
    ##Create away-home dict:
    away = dicts.teams[gameinfo[2]]
    home = dicts.teams[gameinfo[3]]
    team = {away : '0', home : '1'}
    ##Create away and home player sets
    awayPlayers = dict()
    homePlayers = dict()
    #print 'here'
    with open(directory+filename+'.csv','w') as f:
        ##Write opening lines.
        #print 'here'
        f.write(' '.join(["#",gameinfo[0],"\n"]))
        f.write(' '.join(["#",dicts.teams[gameinfo[2]],",",dicts.teams[gameinfo[3]], "\n"]))
        f.write(' '.join(["#",gameinfo[4],',',gameinfo[5],"\n"]))
        f.write("Event Number,Period,STR,Game-Time, Event,Acting Player,Recieving Player,Location,")
        f.write("slot1,slot2,slot3,slot4,Away on Ice 1,")
        f.write("Away on Ice 2,Away on Ice 3,Away on Ice 4,Away on Ice 5,Away on Ice 6,")
        f.write("Home on Ice 1,Home on Ice 2,Home on Ice 3,Home on Ice 4,Home on Ice 5,")
        f.write("Home on Ice 6\n")
        for line in soup.find_all("tr", {"class" : "evenColor"}):
            #Event number
            f.write(str(line.contents[1].text.encode('utf-8'))+ ',')
            #Period
            f.write(str(line.contents[3].text.encode('utf-8'))+ ',')
            #Strength
            strn = str((line.contents[5].text).encode('utf-8'))
            if strn in dicts.strength.keys():
                strn = dicts.strength[strn]
            f.write(strn + ',')
            #print 'here'
            #Game-time
            time = (line.contents[7].text).encode('utf-8')
            splt = (line.contents[7].text).index(":")
            f.write(str(time[splt+3:])+ ',')

            #Event ID
            evnt = str((line.contents[9].text).encode('utf-8')).translate(None,',').translate(None,';')
            f.write(str(dicts.events[evnt]) + ',')
            #print 'here'
            #Mung and write the Event Description
            des = str((line.contents[11].text).encode('utf-8')).translate(None,',').translate(None,';')
            des = ef.MungDes(evnt,des)
            if des[0] in team.keys():
                des[0] = team[des[0]]
            des = ','.join(des)
            f.write(str(des))
            ##Write the away and home players
            #Away players
            aPlayers = nhls.GetPlayersOnIce(line.contents[13].find_all({"font"}), awayPlayers)
            f.write(aPlayers)
            #Home players
            hPlayers = nhls.GetPlayersOnIce(line.contents[15].find_all({"font"}),homePlayers)
            f.write(hPlayers)
            f.write('\n')

        #write player dictionaries
        f.write("# Away Players\n")
        for key in awayPlayers.keys():
            f.write(''.join([awayPlayers[key], ',', key, '\n' ]))
        f.write("# Home Players\n")
        for key in homePlayers.keys():
            f.write(''.join([homePlayers[key],',',key,'\n']))

    return 1
