import pandas as pd

class Game():
    def __init__(self,path):
        with open(path,'r') as f_in:
            lines = [l.strip().split(',') for l in f_in.readlines()]
            self.date = lines[0][0].replace('#','')
            self.away = lines[1][0].replace('#','')
            self.home = lines[1][1]
            self.awayscore = lines[2][0].replace('#','')
            self.homescore = lines[2][1]
            self.awayteam = dict()
            self.hometeam = dict()
            events = []
            awaytm,hometm = False,False
            for i,line in enumerate(lines):
                if(len(line) == 25):
                    events.append(line)
                elif(line[0] == '# Away Players'):
                    awaytm = True
                elif(line[0] == '# Home Players'):
                    hometm = True
                elif(hometm):
                        try:
                            self.hometeam[line[0]] = line[1]
                        except:
                            pass
                elif(awaytm):
                        try:
                            self.awayteam[line[0]] = line[1]
                        except:
                            pass

            df = pd.DataFrame(events[1:])
            df.transpose
            df.columns = events[0]
            self.playbyplay = df.set_index('Event Number')


class NHLSearch():

    ##Constructor, initializes the search databases
    def __init__(self,
        pathToGameDB = 'gameDataBase.csv', pathToPlayerDB = 'playerDataBase.csv', games = True, players = True):

        ##Create Player Dictionary
        if(players):
            self.playerDB = dict()
            with open(pathToPlayerDB,'r') as f:
                for i,lines in enumerate(f.readlines()):
                    if i != 0:
                        line = [i for i in lines.replace('\n','').split(',') if i!='']
                        if len(line) !=0:
                            self.playerDB[line[0]] = line[1:]

        ##Create Game Database
        if(games):
            self.gameDB = pd.DataFrame.from_csv(pathToGameDB)
            self.gameDB = self.gameDB.set_index('ID')


def IDtoPath(ID):
    year = ID[:4]
    month = ID[4:6]
    day = ID[6:8]
    away = ID[8:11]
    home = ID[11:14]
    if(int(month.strip())<9):
        season = ''.join(['SE',str(int(year)-1),year])
    else:
        season = ''.join(['SE',year,str(int(year)+1)])

    game = '-'.join([away,home])+'.csv'

    return '/'.join(['Games',season,year,month,day,game])

def GetGames(listofGames):
    games = []
    for ID in listofGames:
        path = IDtoPath(ID)
        games.append(Game(path))

    return games


def main():
    #d = '20071003OTTTOR'
    #y = GetGames([d])
    #print y[0].playbyplay

if __name__ == "__main__":
  main()
