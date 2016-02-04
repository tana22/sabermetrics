import nhl_soup
import pandas as pd
###Function to iterate over URLS
gameDB = {'Date' : [],'Season':[], 'Away': [], 'Home' : [],'Away Score': [], 'Home Score': [],
'Corsi': [], 'Away Shots': [],'Home Shots':[], 'Away On Net': [], 'Home On Net': [],'ID': []}
playerDB = {}
def CollectGames(urlbase,season,start,end, buildDB = False):
    workingDir = "Games/" + "SE" + season + "/"
    for games in xrange(start,end+1):
        gameid = str(games).zfill(4)
        u = urlbase+gameid+".HTM"
        try:
            gameinfo = nhl_soup.ScrapePlayByPlay(u,workingDir,True,buildDB)
            #print gameinfo
            if(buildDB):
                gameDB['Date'].append(gameinfo[0])
                gameDB['Season'].append('/'.join([season[2:4],season[6:8]]))
                gameDB['Away'].append(gameinfo[1])
                gameDB['Home'].append(gameinfo[2])
                gameDB['Corsi'].append(gameinfo[3])
                gameDB['Away Shots'].append(gameinfo[4])
                gameDB['Home Shots'].append(gameinfo[5])
                gameDB['Away On Net'].append(gameinfo[6])
                gameDB['Home On Net'].append(gameinfo[7])
                gameDB['Away Score'].append(gameinfo[8])
                gameDB['Home Score'].append(gameinfo[9])
                gameID = ''.join([gameinfo[0].replace('/',''),gameinfo[1],gameinfo[2]])
                gameDB['ID'].append(gameID)
                playersInGame = gameinfo[10]+gameinfo[11]
                for player in playersInGame:
                    if player in playerDB.keys():
                        playerDB[player].append(gameID)
                    else:
                        playerDB[player] = [gameID]
        except:
            pass



def WriteDataBase():
    df_game = pd.DataFrame(gameDB)
    #df_players = pd.DataFrame(playerDB)
    print df_game
    #print df_player

    return 1



## 07/08 season collection
##Preseason -> PL01, Regular season -> PL02, Playoffs -> PL03. Try running
#this portion first (PL01)

season = "20072008"
'''
url = "http://www.nhl.com/scores/htmlreports/" + season + "/PL01"
end = 105
CollectGames(url,season,1,10)
'''

### PL02 seems to be the entire regular season, it takes roughly 1.5 hrs to scrape

url = "http://www.nhl.com/scores/htmlreports/" + season + "/PL02"
#end = 1230
end = 5
CollectGames(url,season,1,end,True)
WriteDataBase()
