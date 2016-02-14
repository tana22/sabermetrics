import requests
import os
import codecs
import unicodedata
import nhl_dictionaries as dicts
import nhl_soup_condensed as cd
from bs4 import BeautifulSoup
error = ''


def main():
    url = "http://www.nhl.com/scores/htmlreports/20152016/TV020809.HTM"
    array=getTextArray(url)

    players=buildPlayerList(array)
    events=getEventPos(array)
   
    table=buildShiftTable(array)

    for n in range(0,len(players)):
        print players[n], table[n]

    #print array



def getTextArray(url):
    '''
    Take in a url as an argument and applies bs4 to it
    then it takes the soup and uses get_text. The string 
    returned by get_text is in unicode, this is then encoded
    to ASCII with utf8. This ASCII string is then parsed 
    by newlines into a list and then blank entries are removed
    the function returns the resultant array of strings in 
    utf-8 encoded ASCII
    '''
    
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


def buildShiftTable(array):
    '''
    This function takes the ASCII-encoded array
    from getTextArray and returns a list of lists
    where the nested lists contain all of the events
    for a given player. They are organized in the
    same order as buildPlayerList and so to see a 
    players shifts on ice one could do
    print playerName[__X__],shiftTable[__X__]
    '''


    table=[]
    playerPositions=getPlayerPos(array)
    eventPositions=getEventPos(array)


    # This is probably the most inefficient way to 
    # do this. This might be a bottleneck

    # Cycle through each player
    for playerPos in playerPositions:
        setOfEvents=[]
        start=0

        #search through eventPos starting at 
        # start and check when the current 
        #player is found
       
        for eventPos in eventPositions[start:]:
            if eventPos==playerPos:

                #upon finding the player find what 
                # index we are at
                nEvent=eventPositions.index(eventPos)
                nPlay=playerPositions.index(playerPos)

                # if we are not at the end of the 
                # list of players find where the 
                # next player is 
                if nPlay+1<len(playerPositions):
                    nextPlayPos=playerPositions[nPlay+1]

                # append all events to this current player's
                # list of events until either a string with
                # more than 3 chars is encountered (end of list)
                # or the next player is encountered 
                for  eventPos2 in eventPositions[nEvent+1:]:
                    if eventPos2==nextPlayPos or len(array[eventPos2])>3:
                        # re-set start so that the program does not 
                        # loop through events it already recorded in
                        # the first nested loop
                        start=eventPositions.index(eventPos2)
                        break
                    else:
                        # use position to gather events and append
                        # them to the list of events for a player
                        setOfEvents.append(buildEvent(array,eventPos2))

        # add all the events for a player to their position in the table
        table.append(setOfEvents)

    return table



def findAwayPos(array):
    ''' 
    Finds the position in an array of the string VISITOR
    prints a warning and returns -1 if no such string is found
    '''
    
    for i in range (0,len(array)):
        if array[i]=='VISITOR':
            return i
    print 'could not find VISITOR position'
    return -1

def findHomePos(array):
    ''' 
    Finds the position in an array of the string HOME
    prints a warning and returns -1 if no such string is found
    '''
    
    for i in range (0,len(array)):
        if array[i]=='HOME':
            return i
    print 'could not find VISITOR position'
    return -1

def findHomeTeam(array):
    '''
    takes ASCII encoded text array
    returns ASCII encoded string of home team
    '''

    spot=findHomePos(array)
    if spot==-1:
        return ''
    else:
        raw=array[spot+2]
        return raw.split('Game ')[0]

def findAwayTeam(array):
    '''
    takes ASCII encoded text array
    returns ASCII encoded string of home team
    '''
    spot=findAwayPos(array)
    if spot==-1:
        return ''
    else:
        raw=array[spot+2]
        return raw.split('Game ')[0]

def findDateStr(array):
    '''
    takes ASCII encoded text array
    Function to find the date of the game
    '''

    spot=findAwayPos(array)
    if spot==-1:
        return ''
    else:
        raw=array[spot+5]
        return raw

def getPlayerPos(array):
    '''
    returns a list of integers that are the 
    index locatoions for players' names
    in the text array passed to the function
    '''
    playerPositions=[]
    for n in range(0,len(array)):
        item=array[n]
        if item =='Shift #':
            playerPositions.append(n-1)
    return playerPositions

def getEventPos(array):
    '''
    returns a list of integers with positions of any
    'Event' in practice this is the date, a players 
    name, an event ID, or the copyright at the bottom
    '''

    eventPos=[]
    for n in range(0,len(array)):
        item=array[n]
        
        # check for events that we like
        if array[n] =='\xc2\xa0' or array[n] =='GP' or \
           array[n] =='EventG=GoalP=Penalty':
            #filter out ones that we dont
            if array[n+1]!='\xc2\xa0' and array[n+1]!='Per':
                # check if we are at the start of 
                # this is just to deal with a weird 
                # formatting irregularity 

                if n+2==getPlayerPos(array)[0]:
                    eventPos.append(n+2)
                else:
                    eventPos.append(n+1)
            
    return eventPos

def buildPlayerList(array):
    '''
    returns a list of strings which are all of
    the players full names and numbers
    '''
    players=[]
    playerPos=getPlayerPos(array)
    
    for position in playerPos:
        players.append(array[position])

    return players

def buildEvent(array,eventPos):
    '''
    This funciton takes an array and the position
    of an event tag and returns a 3 entry list of 
    strings with the period time on and time off
    '''
    period=array[eventPos+1]
    time1=array[eventPos+2]
    time2=array[eventPos+3]
    
    return [period,time1,time2]





if __name__ == "__main__":
    main()
