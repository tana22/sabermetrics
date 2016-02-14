import requests
import os
import codecs
import unicodedata
import nhl_dictionaries as dicts
import nhl_soup_condensed as cd
from bs4 import BeautifulSoup
error = ''



def getTextArray(url):
    """Take in a url as an argument and applies bs4 to it
    then it takes the soup and uses get_text. This is then
    parsed by '\n' into a list and then blank entries are 
    removed"""
    
    err ='errorRy.txt'
    r = requests.get(url)
    if(r.status_code>400):
        error = str(url) + " has error status: " + str(r.status_code)
        ErrorReport(error,err)
        print error
        return 1
    soup = BeautifulSoup(r.content,'html5lib')
    longString=soup.get_text().encode('utf8')
    oldArray=longString.split('\n')
    newArray=[]
    for item in oldArray:
        if item !='':
            newArray.append(item)
    
        
    return newArray


def findAwayPos(array):
    ''' Finds the position in an array of the string VISITOR
    prints a warning and returns -1 if no such string is found'''
    for i in range (0,len(array)):
        if array[i]=='VISITOR':
            return i
    print 'could not find VISITOR position'
    return -1

def findHomePos(array):
    ''' Finds the position in an array of the string HOME
    prints a warning and returns -1 if no such string is found'''
    for i in range (0,len(array)):
        if array[i]=='HOME':
            return i
    print 'could not find VISITOR position'
    return -1

def findHomeTeam(array):
    '''returns string of home team'''
    spot=findHomePos(array)
    if spot==-1:
        return ''
    else:
        raw=array[spot+2]
        return raw.split('Game ')[0]

def findAwayTeam(array):
    '''returns string of home team'''
    spot=findAwayPos(array)
    if spot==-1:
        return ''
    else:
        raw=array[spot+2]
        return raw.split('Game ')[0]

def findDateStr(array):
    spot=findAwayPos(array)
    if spot==-1:
        return ''
    else:
        raw=array[spot+5]
        return raw

def getPlayerPos(array):
    playerPositions=[]
    for n in range(0,len(array)):
        item=array[n]
        if item =='Shift #':
            playerPositions.append(n-1)
    return playerPositions

def getEventPos(array):
    eventPos=[]
    for n in range(0,len(array)):
        item=array[n]
        #This encode call takes care of the 
        #fact that bs4 ouputs unicode 
        #google Unicode-How To FMI
        if item =='\xc2\xa0' or item=='GP' or item=='EventG=GoalP=Penalty':
            if array[n+1]!='\xc2\xa0' and array[n+1]!='Per':
                if n+2==getPlayerPos(array)[0]:
                    eventPos.append(n+2)
                else:
                    eventPos.append(n+1)
            
    return eventPos

def buildPlayerList(array):
    players=[]
    playerPos=getPlayerPos(array)
    
    for position in playerPos:
        players.append(array[position])

    return players

def buildEvent(array,eventPos):
    period=array[eventPos+1]
    time1=array[eventPos+2]
    time2=array[eventPos+3]
    
    return [period,time1,time2]


def buildEventTable(array):
    table=[]
    playerPositions=getPlayerPos(array)
    eventPositions=getEventPos(array)

    for playerPos in playerPositions:
        setOfEvents=[]
        for eventPos in eventPositions:
            if eventPos==playerPos:
                nEvent=eventPositions.index(eventPos)
                nPlay=playerPositions.index(playerPos)
                if nPlay+1<len(playerPositions):
                    nextPlayPos=playerPositions[nPlay+1]
                for  eventPos2 in eventPositions[nEvent+1:]:
                    if eventPos2==nextPlayPos or len(array[eventPos2])>3:
                        break
                    else:
                        setOfEvents.append(buildEvent(array,eventPos2))
        table.append(setOfEvents)
    return table




def main():
    url = "http://www.nhl.com/scores/htmlreports/20152016/TV020809.HTM"
    array=getTextArray(url)

    players=buildPlayerList(array)
    events=getEventPos(array)
   
    table=buildEventTable(array)

    print players[1], table[1]

    #print array

if __name__ == "__main__":
    main()
