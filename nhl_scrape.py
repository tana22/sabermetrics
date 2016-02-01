import nhl_soup
###Function to iterate over URLS
def CollectGames(urlbase,season,start=1,end=100):
    workingDir = "testing/" + "SE" + season + "/"
    for games in xrange(start,end+1):
        gameid = str(games).zfill(4)
        u = urlbase+gameid+".HTM"
        try:
            nhl_soup.ScrapePlayByPlay(u,workingDir,True)
        except:
            pass


## 07/08 season collection
##Preseason -> PL01, Regular season -> PL02, Playoffs -> PL03. Try running
#this portion first (PL01)
season = "20072008"
url = "http://www.nhl.com/scores/htmlreports/" + season + "/PL01"
end = 105
CollectGames(url,season,1,10)


### PL02 seems to be the entire regular season, it takes roughly 1.5 hrs to scrape
'''
url = "http://www.nhl.com/scores/htmlreports/" + season + "/PL02"
end =1230
CollectGames(url,1,end)
'''
