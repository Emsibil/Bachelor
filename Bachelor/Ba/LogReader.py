import os
import time
import numpy as np
import cardLibReader as cReader

path = 'C:/Program Files (x86)'  #Uni
#path = 'D:/Programme' #Home

#returns the full path of a special file
def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

def getPath():
    global path
    return path

def openLogFile():
    return open('C:/Program Files (x86)/Hearthstone/Hearthstone_Data/output_log.txt' , 'r')

def readLog():
    return openLogFile().readlines()

def split(*args):
    if len(args) == 2:
        return args[1].split(args[2])[1]
    elif len(args) == 3:
        return args[0].split(args[1])[1].split(args[2])[0]

#def interpretZone(line):
PLAYER_NAMES = np.array(['NONE','NONE'])
def getPlayerName(PlayerID):
    global PLAYER_NAMES
    return PLAYER_NAMES[PlayerID - 1]

def setPlayerName(PlayerID, Name):
    global PLAYER_NAMES
    PLAYER_NAMES[PlayerID - 1] = Name


MY_MULLIGAN_DONE = False
def isMyMulliganStateDone():
    global MY_MULLIGAN_DONE
    return MY_MULLIGAN_DONE

def setMyMulliganStateDone(State):
    global MY_MULLIGAN_DONE
    MY_MULLIGAN_DONE = State
    
ENEMY_MULLIGAN_DONE = False
def isEnemyMulliganStateDone():
    global MULLIGAN_STATE_OF_ENEMY
    return MULLIGAN_STATE_OF_ENEMY

def setEnemyMulliganStateDone(State):
    global MULLIGAN_STATE_OF_ENEMY
    MULLIGAN_STATE_OF_ENEMY = State
  
GAME_STATES = np.array(['GAME_START', 'MULLIGAN', 'MY_TURN', 'ENEMY_TURN'])
def getGameState(i):
    global GAME_STATES
    return GAME_STATES[i]

CUR_STATE = 'NONE'
def getCurState():
    global CUR_STATE
    return CUR_STATE

def setCurState(new_state):
    global CUR_STATE
    CUR_STATE = new_state
   
MY_HERO = 'NONE'
MY_HERO_POWER = 'NONE'
ENEMY_HERO = 'NONE'
ENEMY_HERO_POWER = 'NONE'

def setMyHero(heroId):
    global MY_HERO
    MY_HERO = heroId
    setMyMinios(cReader.CardById(heroId),0)
def setMyHeroPower(powerId):
    global MY_HERO_POWER
    MY_HERO_POWER = powerId
def setEnemyHero(heroId):
    global ENEMY_HERO
    ENEMY_HERO = heroId
def setEnemyHeroPower(powerId):
    global ENEMY_HERO_POWER
    ENEMY_HERO_POWER = powerId
def getMyHero():
    global MY_HERO
    return MY_HERO
def getMyHeroPower():
    global MY_HERO_POWER
    return MY_HERO_POWER
def getEnemyHero():
    global ENEMY_HERO
    return ENEMY_HERO
def getEnemyHeroPower():
    global ENEMY_HERO_POWER
    return ENEMY_HERO_POWER

MY_HANDCARDS = np.array(['None','None','None','None','None','None','None','None','None','None'])
def getHandcards():
    global MY_HANDCARDS
    return MY_HANDCARDS
def getHandcard(ZonePosition, WithRemoving):
    global MY_HANDCARDS
    if WithRemoving:
        card = MY_HANDCARDS[ZonePosition - 1]
        removeHandCardFromPosition(ZonePosition)
        MY_HANDCARDS = reOrderHandcards(MY_HANDCARDS, ZonePosition - 1)
        return card
    return MY_HANDCARDS[ZonePosition - 1]
def addHandcardAtPosition(cardId, pos):
    global MY_HANDCARDS
    card = cReader.CardById(cardId)
    if MY_HANDCARDS[pos - 1] == 'None':
        MY_HANDCARDS[pos - 1] = card 
def removeHandcardFromPosition(pos):
    global MY_HANDCARDS
    MY_HANDCARDS[pos - 1] = 'None'
def setHandcards(handcardArray):
    global MY_HANDCARDS
    MY_HANDCARDS = handcardArray
def getHandcardCount():
    Handcards = getHandcards()
    count = 0
    for card in Handcards:
        if card == 'None':
            return count
        else:
            count += 1
    return count

def reOrderHandcards(handcards, pos):
    length = len(handcards - 1)
    if pos == length:
        return handcards
    while pos < length:
        if handcards[pos + 1] == 'None':
            return handcards
        else:
            handcards[pos] = handcards[pos + 1]
            handcards[pos + 1] = 'None'
            pos += 1
    return handcards

MY_MANA = 0
def setMyMana(value):
    global MY_MANA
    MY_MANA = value
def getMyMana():
    global MY_MANA
    return MY_MANA 

MinionsOnMySide = np.array([[0, 'None'][1, 'None'], [2, 'None'], [3, 'None'], [4, 'None'], [5, 'None'], [6, 'None'], [7, 'None']])
def getMyMinion(pos):
    global MinionsOnMySide
    return MinionsOnMySide[pos]
def setMyMinion(card, pos):
    global MinionsOnMySide
    MinionsOnMySide[pos] = card

MinionsOnEnemySide = np.array([[0, 'None'][1, 'None'], [2, 'None'], [3, 'None'], [4, 'None'], [5, 'None'], [6, 'None'], [7, 'None']])
def getEnemyMinion(pos):
    global MinionsOnEnemySide
    return MinionsOnEnemySide[pos]
def setEnemyMinion(card, pos):
    global MinionsOnEnemySide
    MinionsOnEnemySide[pos] = card
def reorderMyMinions(Array, pos):
    i = (len(Array) - 1)
    while i >= pos:
        Array[i, 1] = Array[i - 1, 1] 
        i -= 1    
    Array[pos, 1] = 'None'    
            
Mulligan = False
def isMulligan():
    global Mulligan
    return Mulligan
def setMulligan(binary):
    global Mulligan
    Mulligan = binary
    
TurnChanged = False
def setTurnChanged(binary):
    global TurnChanged
    TurnChanged = binary
def isTurnChanged():
    global TurnChanged
    return TurnChanged

myTurn = False
def setMyTurn(binary):
    global myTurn
    myTurn = binary
def isMyTurn():
    global myTurn
    return myTurn 
   
def cardName(line):
    return split(line, 'name=',' id')
def cardId(line):
    return split(line, 'cardId=',' ')
def getPosition(line):
    return int(split(line, 'pos from 0 -> '))

def Statedecision():
    log = readLog()
    nol = len(log)
    while True:
        time.sleep(0.03)
        new_log = readLog()
        new_nol = len(new_log)
        new_lines = new_nol[nol : new_nol]
        i = 0
        while i < len(new_lines):
            if 'CREATE_GAME' in new_lines[i]:
                completeReading(new_lines[i:], 'GAME_START')
            else:
                completeReading(new_lines[i:], getCurState())
                       
def completeReading(input, state):
    if state == getCurState():
        if getCurState() == getGameState(0):
            readGameStartPowerLines(input)
        elif getCurState() == getGameState(1):
            readingMulligan(input)
        elif getCurState() == getGameState(2):
            readingMyTurn(input)
        elif getCurState() == getGameState(3):
            readingEnemyTurn(input)
    else:
        setCurState(state)

#variables for readGameStartPowerLines()
Found= False
def isFound():
    global Found
    return Found
def setFound(binary):
    global HeroFoundFound
    Found = binary
waiting = False
def setWaiting(binary):
    global waiting
    waiting = binary
def isWaiting():
    global waiting
    return waiting
playerID = 0
def setPlayerID(Id):
    global playerID
    playerID = id
def getPlayerID():
    global playerID
    return playerID
tmp = 'NONE'
def getTmp():
    global tmp
    return tmp
def setTmp(temp):
    global tmp
    tmp = temp


def readGameStartPowerLines(input):
    for line in input:
        if '[ZONE]' in line:
            setCurState('MULLIGAN')
            return
        elif 'CardId=HERO_' in line:
            setFound(True)
            setWaiting(True)
            setTmp(split(line, 'CardId=','\n'))
        elif isFound() and 'tag=CONTROLLER' in line:
            setFound(False)
            setPlayerID(int(split(line, 'value=', '\n')))
            if getPlayerID() == 1:
                setMyHero(getTmp())
            else:
                setEnemyHero(getTmp())
        elif isWaiting() and not isFound() and 'CardId=' in line:
            setWaiting(False)
            if getPlayerID() == 1:
                setMyHeroPower(split(line, 'CardId=', '\n'))
            else:
                setEnemyHeroPower(split(line, 'CardId=','\n'))
        elif not isWaiting() and 'CardId=' in line and not 'HERO' in line:
            cardId = split(line, 'CardId=')
            if '\n' == cardId:
                continue
            else:
                setFound(True)
                setTmp(cardId.split('\n')[0])
        elif isFound() and 'ZONE_POSITION' in line:
            setFound(False)
            addHandcardAtPosition(getTmp(), int(split(line,'value=','\n')))
        elif 'TAG_CHANGE' in line and 'CONTROLLER' in line:
            if int(split(line,'value=','\n')) == 1:
                setPlayerName(1, split(line, 'Entity=',' tag'))
            else:
                setPlayerName(2, split(line, 'Entity=',' tag'))
                
def readingMulligan(input):
    for line in input:
        if 'MULLIGAN_STATE' in line and 'DONE' in line:
            if split(line, 'Entity=', ' tag') == getPlayerName(1):
                setMyMulliganStateDone(True)
            elif split(line, 'Entity=', ' tag') == getPlayerName(2):
                setEnemyMulliganStateDone(True)
            if isMyMulliganStateDone() and isEnemyMulliganStateDone():
                if getHandcardCount() == 3:
                    setCurState('MY_TURN')
                else:
                    setCurState('ENEMY_TURN')
                return
        if getPlayerName(1) in line and 'MULLIGAN_STATE' in line and 'DEALING' in line:
            setWaiting(True)
        if isWaiting() and 'SHOW_ENTITY':
            setTmp(split(line, 'CardID=', '\n'))
        if isWaiting() and 'HIDE_ENTITY':
            setWaiting(False)
            pos = int(split(line, 'zonePos=', ' '))
            removeHandcardFromPosition(pos)
            #put removed Card back to DECK
            addAtPosition(getTmp, pos)
            
def readingMyTurn(input):
    for line in input:
        if 'MAIN_END' in lsine:
            setCurState('ENEMY_TURN')
            return
        if 'TAG_CHANGE' in line and 'RESOURCES' in line:
            setMyMana(int(split(line, 'value= ', '\n')))
        if 'SHOW_ENTITY' in line:
            addHandcardAtPosition(split(line, 'CardID=', '\n'), (getHandcardCount() + 1))
        if 'SubType=PLAY' in line:
            card = getHandcard(int(split(line, 'ZonePos=', ' ')), 1)
            setMyMana(getMyMana() - cReader.manaCost(card))
            if cReader.cardType(card) == 'Minion':
                setWaiting(True)
                setTmp(card)
        if isWaiting() and 'cardId='+cReader.Id(getTmp()) in line and 'ZONE_POSITION' in line:
            setWaiting(False)
            setMyMinion(getTmp(), split(line, 'value=', '\n'))
        #if 'option 0' in Line and 'END_TURN' in Line:
        #    print 'no more option. Click End Turn'
        if 'SubType=ATTACK' in line:
            attack(line, 'ME')

            
def attack(line, attacker):
    attackerInfo, targetInfo= line.split('ATTACK')
    attackZone = int(split(attackerInfo, 'zonePos=', ' cardId='))
    #attack = split(attackerInfo, 'cardId', ' player')
    #target = split(targetInfo, 'cardId', ' player')
    targetZone = split(targetInfo, 'zonePos=', ' cardId')
    a_strength = 0
    a_health = 0
    t_strength = 0
    a_health = 0
    a_minion = 'None'
    t_minion = 'None'
    if attacker == 'ME':
        a_minion = getMyMinion(attackZone) 
        t_minion = getEnemyMinion(targetZone)
    else:
        a_minion = getEnemyMinion(attackZone) 
        t_minion = getMyMinion(targetZone)
    a_strength = cReader.attackValue(a_minion)
    a_health = cReader.healthValue(a_minion)
    t_strength = cReader.attackValue(t_minion)
    t_health = cReader.healthValue(t_minion)
    new_t_health = t_health - a_strength
    new_a_health = a_health - t_strength
    if attacker == 'ME':
        if new_a_health <= 0:
            setMyMinion('None', attackZone)
        else:
            a_minion = cReader.setHealth(a_minion, new_a_health)
            setMyMinion(a_minion, attackZone)
        if new_t_health <= 0:
            setEnemyMinion('None', targetZone)
            if targetZone == 0:
                print 'You Won'
        else:
            t_minion = cReader.setHealth(t_minion, new_t_health)
            setEnemyMinion(t_minion, attackZone)
    else:
         if new_a_health <= 0:
            setEnemyMinion('None', attackZone)
         else:
            a_minion = cReader.setHealth(a_minion, new_a_health)
            setEnemyMinion(a_minion, attackZone)
         if new_t_health <= 0:
            setMyMinion('None', targetZone)
         else:
            t_minion = cReader.setHealth(t_minion, new_t_health)
            setMyMinion(t_minion, attackZone)
            if targetZone == 0:
                print 'You Lost'         
   
def readingEnemyTurn(input):
    for line in input:
        if 'MAIN_END' in line:
            setCurState('ENEMY_TURN')
            return
        

   #-----TESTREADER-----#
def splitter():
    file = readLog()
    power = open(path('doc')+'/Mulliganpower.txt', 'w')
    zone = open(path('doc')+'/Mulliganzone.txt', 'w')
    for l in file:
        if '[Power]' in l:
            power.write(l)
        elif '[Zone]' in l:
            zone.write(l)

#--------EVENTS-------#

def MinionChanges():
    print 'Minion Changes'

def DocumentChanges():
    print 'There are new line of code'

def HandcardsChanges():
    print 'Something within your handcards changes'

def GameStatusChanges():
    print 'Gamestatus changes'

