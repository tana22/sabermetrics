from nhl_dictionaries import *
## Functions to break down play by play event descriptions
##Typically will follow:
##Home or Away,Acting Player,Recieving Player,Location,
#slot1,slot2,slot3,slot4
## 0's will represent NA data.

##SHOT
def ShotDes(des):
    team = des[0]
    l = len(des)
    playerNum = des[3]
    shotType = des[5]
    if shotType in shotTypes.keys():
        shotType = shotTypes[shotType]
    else:
        shotType = '0'
    location = ' '.join(des[l-4:l-2])
    distance = des[l-2]
    return [team,playerNum,'0',location,distance,shotType,'0','0']

##GOAL
def GoalDes(des):
    team = des[0]
    playerNums = [i.replace('#','') for i in des if i.find('#') == 0]
    shotType = des[3]
    if shotType in shotTypes.keys():
        shotType = shotTypes[shotType]
    else:
        shotType = '0'
    ind = des.index('Zone')
    location = ' '.join(des[ind-1:ind+1])
    distance = des[ind+1]
    if len(playerNums[1:])>1:
        assistlist = playerNums[1:3]
    else:
        assistlist = [playerNums[1],'0']
    return [team,playerNums[0],'0',location,distance,shotType] + assistlist

##HIT
def HitDes(des):
    team = des[0]
    playerNums = [i.replace('#','') for i in des if i.find('#') == 0]
    location = ' '.join(des[len(des)-2:])
    return [team, playerNums[0], playerNums[1], location,'0','0','0','0']

##FACEOFF
def FacDes(des):
    winningteam = des[0]
    playerNums = [i.replace('#','') for i in des if i.find('#') == 0]
    visPlayer = playerNums[0]
    homePlayer = playerNums[1]
    location = ' '.join(des[2:4])
    return [winningteam, visPlayer, homePlayer, location,'0','0','0','0']

##MISS
def MissDes(des):
    team = des[0]
    l = len(des)
    playerNum = des[1]
    #playerNum = des[1].replace('#','')
    #shotType = des[3]
    location = ' '.join(des[l-4:l-2])
    distance = des[l-2]
    return [team,playerNum,'0',location,distance,'0','0','0']

##GIVE/TAKE
def GiveTakeDes(des):
    team = des[0][:3]
    playerNum = des[2]
    #playerNum = des[2].remove('#','')
    location = ' '.join(des[4:])
    return [team,playerNum,'0',location,'0','0','0','0']

##PENALTY
def PenlDes(des):
    team = des[0]
    players = [i.replace('#','') for i in des if i.find('#') == 0]
    try:
        ind = des.index('Zone')
        location = ' '.join(des[ind-1:ind+1])
    except:
        location = '0'
        pass
    oppPlayer = '0'
    if(len(players)>1):
        oppPlayer = players[1]
    return [team, players[0], oppPlayer, location,'0','0','0','0']

##BLOCK
def BlockDes(des):
    team = des[0]
    l = len(des)
    players = [i.replace('#','') for i in des if i.find('#') == 0]
    location = ' '.join(des[l-2:])
    return [team, players[0], players[1], location,'0','0','0','0']

##Others -- Returns Description
def ReturnDes(des):
    return [str(des),'0','0','0','0','0','0','0']


##Event + Description Mung
def MungDes(event,des):
    fcnDict = {
    'SHOT' : ShotDes,
    'GOAL' : GoalDes,
    'FAC' : FacDes,
    'HIT' : HitDes,
    'MISS' : MissDes,
    'GIVE' : GiveTakeDes,
    'TAKE' : GiveTakeDes,
    'PENL' : PenlDes,
    'BLOCK' : BlockDes}
    if event in fcnDict.keys():
        des = des.split(' ')
        return fcnDict[event](des)
    else:
        return ReturnDes(des)
