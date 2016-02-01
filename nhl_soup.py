import requests
import os
import codecs
import unicodedata
import nhl_dictionaries as dicts
import nhl_soup_condensed as cd
from bs4 import BeautifulSoup
error = ''


##Gets the general game info using BeautifulSoup.
##Will have to add more to scrape the final score.
def GetGameInfo(soup):
    ### for the current tested season 07/08 the first try
    ## works for all cases EXCEPT those that have french accents
    ## as they are formatted differently and certain characters are
    ## unconvertable to ascii
    ## Notice any home games in Ottawa or Montreal are funky

    ##Get game date
    try:
        line = soup.find_all("table",{"id":"GameInfo"})[0]
        gameDate = str(line.contents[1].text.splitlines()[10].encode('utf-8'))
    except:
        try:
            line = soup.find_all("table",{"id":"GameInfo"})[0]
            gameDate = str(''.join(line.contents[1].text.encode('utf-8').splitlines()))
        except:
            print "Can't get game date"

    gameDate = (gameDate.replace(',','')).split(' ')
    fmtDate = '-'.join([gameDate[2].zfill(2), dicts.month[gameDate[1]], gameDate[3]])

    ##Get Away and Home teams:
    line_v = soup.find_all("table",{"id":"Visitor"})[0]
    line_v = line_v.contents[1].text.splitlines()
    line_h = soup.find_all("table",{"id":"Home"})[0]
    line_h = line_h.contents[1].text.splitlines()
    try:
        vis = str(line_v[15].encode('utf-8'))
        indv = vis.index("Game")
        sc_v = line_v[8].encode('utf-8')
        home = str(line_h[15].encode('utf-8'))
        indh = home.index("Game")
        sc_h = line_h[8].encode('utf-8')
    except:
        vis = str(line_v[19].encode('utf-8'))
        indv = vis.index("Match")
        sc_v = line_v[10].encode('utf-8')
        home = str(line_h[19].encode('utf-8'))
        indh = home.index("Match")
        sc_h = line_h[10].encode('utf-8')

    vis = vis[:indv]
    home = home[:indh]

    gametitle = ' '.join([sc_v, vis, '--', sc_h, home])
    return [fmtDate,gametitle,vis,home,sc_v,sc_h]


###Get players on ice using a content line from BeautifulSoup.
def GetPlayersOnIce(line,teamDict=False):
    onIce = ""
    for i in range(6):
        try:
            pl = line[i]
            pl = str(pl.encode('utf-8'))
            in0 = pl.index('-')+2
            in1 = pl.index("i")+6
            in2 = pl.index(">")+1
            in3 = pl.index("/")-1
            playerName = pl[in0:in2-2]
            playerNum = pl[in2:in3]

            if(teamDict != False):
                teamDict[playerName] = playerNum
                player = ' '.join([',',playerNum])
            else:
                player = ' '.join([ ',', playerName , playerNum])
            onIce = onIce+player
        except:
            onIce = onIce + '0,'

    return onIce


###Writes the play by play data to a file in CSV format.
def WriteCSV(directory,filename,soup):
    with open(directory+filename+'.csv','w') as f:
        f.write("#,Per,STR,Game Time,Elapsed Time,Event,Description,Away on Ice 1,")
        f.write("Away on Ice 2,Away on Ice 3,Away on Ice 4,Away on Ice 5,Away on Ice 6,")
        f.write("Home on Ice 1,Home on Ice 2,Home on Ice 3,Home on Ice 4,Home on Ice 5,")
        f.write("Home on Ice 6\n")

        for line in soup.find_all("tr", {"class" : "evenColor"}):
            #Event number
            f.write(str(line.contents[1].text.encode('utf-8'))+ ',')
            #Period
            f.write(str(line.contents[3].text.encode('utf-8'))+ ',')
            #STR
            f.write(str((line.contents[5].text).encode('utf-8'))+ ',')

            #Game time and Elapsed Time
            time = (line.contents[7].text).encode('utf-8')
            splt = (line.contents[7].text).index(":")
            f.write(str(time[:splt+3])+ ',')
            f.write(str(time[splt+3:])+ ',')
            #Event
            f.write(str((line.contents[9].text).encode('utf-8')).translate(None,',').translate(None,';') + ',')
            #Event Description
            f.write(str((line.contents[11].text).encode('utf-8')).translate(None,',').translate(None,';'))
            #Players on Ice Away
            f.write(GetPlayersOnIce(line.contents[13].find_all({"font"})))
            #Players on Ice Home
            f.write(GetPlayersOnIce(line.contents[15].find_all({"font"}))+ '\n')
    return 1

## Writes the play by play in the condensed format as outlined in the T&P sabermetrics manual
#def WriteFormatted(directory,filename,soup):


## Writes any errors to a file.
def ErrorReport(error,errfile):
    with open(errfile, 'a') as f:
        f.write(str(error))
        f.write('\n')
    return 1

### Main scraping function.
def ScrapePlayByPlay(url,mainDir='', condensed = True):
    err = mainDir + 'error.txt'
    r = requests.get(url)
    if(r.status_code>400):
        error = str(url) + " has error status: " + str(r.status_code)
        ErrorReport(error,err)
        print error
        return 1

    soup = BeautifulSoup(r.content,'html5lib')
##Get General info
    try:
        info = GetGameInfo(soup)
    except:
        error = str(url) + " cannot scrape game info"
        ErrorReport(error,err)
        print error
        return 0
    filename = info[1]
    dir_ = mainDir + info[0] + '/'
    ###Create csv and get info
    if(mainDir != ''):
        if not os.path.exists(mainDir):
            os.mkdir(mainDir)

    if not os.path.exists(dir_):
        os.mkdir(dir_)
    try:
        if(condensed):
            cd.WriteCondensedFmt(dir_,filename,soup,info)
        else:
            WriteCSV(dir_,filename,soup)
        print dir_, filename, " -- collected."
    except:
        error = str(url) + " couldn't write to file"
        ErrorReport(error,err)
        print error
        pass

    return 1



def main():
    ### TEST URLS
    #url = "http://www.nhl.com/scores/htmlreports/20072008/PL010002.HTM"
    #url = "http://www.nhl.com/scores/htmlreports/20152016/PL020355.HTM"
    #url = "http://www.nhl.com/scores/htmlreports/20072008/PL010034.HTM"
    url = 'http://www.nhl.com/scores/htmlreports/20072008/PL010001.HTM'
    ScrapePlayByPlay(url,"testing/")
    return True


if __name__ == "__main__":
  main()
