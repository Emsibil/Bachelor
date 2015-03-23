import os
import time
import numpy as np
import cardLibReader as cReader
from Card import *

path = 'C:/Program Files (x86)'  #Uni
#path = 'D:/Programme' #Home

#returns the full path of a special file
def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

#_BUGLOGGER = open(path('doc')+'/bug_log.txt', 'w')
def buglogger(line, *args):
    global _BUGLOGGER
    text = str(line)
    for a in args:
        text += '\n' + str(a)
    _BUGLOGGER.write(text+'\n')
    
def getPath():
    global path
    return path

def openLogFile():
    return open('C:/Program Files (x86)/Hearthstone/Hearthstone_Data/output_log.txt' , 'r')

def readLog():
    return openLogFile().readlines()

def split(*args):
    if len(args) == 2:
        return args[0].split(args[1])[1]
    elif len(args) == 3:
        return args[0].split(args[1])[1].split(args[2])[0]

#def interpretZone(line):
PLAYER_NAMES = np.array([None,None])
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

CUR_STATE = None
def getCurState():
    global CUR_STATE
    return CUR_STATE

def setCurState(new_state):
    global CUR_STATE
    CUR_STATE = new_state
   
MY_HERO = None
MY_HERO_POWER = None
ENEMY_HERO = None
ENEMY_HERO_POWER = None

def setMyHero(heroId):
    global MY_HERO
    MY_HERO = heroId
    addMyMinonToField(createCard(cReader.CardById(heroId)), 0)
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

MY_HANDCARDS = np.array([None,None,None,None,None,None,None,None,None,None])
def getHandcards():
    global MY_HANDCARDS
    return MY_HANDCARDS
def getHandcard(ZonePosition, WithRemoving):
    global MY_HANDCARDS
    if WithRemoving:
        card = MY_HANDCARDS[ZonePosition - 1]
        removeHandcardFromPosition(ZonePosition)
        MY_HANDCARDS = reOrderHandcards(MY_HANDCARDS, ZonePosition - 1)
        return card
    return MY_HANDCARDS[ZonePosition - 1]
def addHandcardAtPosition(cardId, pos):
    global MY_HANDCARDS
    card = createCard(cReader.CardById(cardId))
    #card.zone = 'HAND'
    #card.zonePos = pos
    if MY_HANDCARDS[pos - 1] is None:
        MY_HANDCARDS[pos - 1] = card 
    print 'got new Card:'
    for card in MY_HANDCARDS:
        if card is not None:
            print card
            try: 
                print card.name
            except Exception, e:
                print e
            try: 
                print card.getName()
            except Exception, e:
                print e
            try: 
                print card.name()
            except Exception, e:
                print e
            try: 
                print card._name
            except Exception, e:
                print e
            time.sleep(1000)
           # print card.name
def removeHandcardFromPosition(pos):
    global MY_HANDCARDS
    MY_HANDCARDS[pos - 1] = None
def setHandcards(handcardArray):
    global MY_HANDCARDS
    MY_HANDCARDS = handcardArray
def getHandcardCount():
    Handcards = getHandcards()
    count = 0
    for card in Handcards:
        if card is None:
            return count
        else:
            count += 1
    return count

def reOrderHandcards(handcards, pos):
    length = len(handcards - 1)
    if pos == length:
        return handcards
    while pos < length:
        if handcards[pos + 1] is None:
            return handcards
        else:
            handcards[pos] = handcards[pos + 1]
            handcards[pos].zonePos -= 1
            handcards[pos + 1] = None
            pos += 1
    return handcards

MY_MANA = 0
def setMyMana(value):
    global MY_MANA
    MY_MANA = value
def getMyMana():
    global MY_MANA
    return MY_MANA

ENEMY_MANA = 0
def setEnemyMana(value):
    global ENEMY_MANA
    ENEMY_MANA = value
def getEnemyMana():
    global ENEMY_MANA
    return ENEMY_MANA  

MinionsOnMySide = np.array([[0, None],[1, None], [2, None], [3, None], [4, None], [5, None], [6, None], [7, None]])
def getMyMinions():
    global MinionsOnMySide
    return MinionsOnMySide
def getMyMinion(pos):
    global MinionsOnMySide
    return MinionsOnMySide[pos]
def addMyMinonToField(card, pos):
    global MinionsOnMySide
    card.zone = 'PLAY'
    card.zonePos = pos
    MinionsOnMySide[pos] = card
def removeMyMinonFromField(pos):
    global MinionsOnMySide
    MinionsOnMySide[pos] = None
    reorderMinionsAfterRemoving(MinionsOnMySide, pos)

MinionsOnEnemySide = np.array([[0, None],[1, None], [2, None], [3, None], [4, None], [5, None], [6, None], [7, None]])
def getEnemyMinions():
    global MinionsOnEnemySide
    return MinionsOnEnemySide    
def getEnemyMinion(pos):
    global MinionsOnEnemySide
    return MinionsOnEnemySide[pos]
def addEnemyMinonToField(card, pos):
    global MinionsOnEnemySide
    card.zone = 'PLAY'
    card.zonePos = pos
    MinionsOnEnemySide[pos] = card
def removeEnemyMinonFromField(pos):
    global MinionsOnEnemySide
    MinionsOnEnemySide[pos] = None
    reorderMinionsAfterRemoving(MinionsOnEnemySide, pos)

def reorderMinionsAfterPlaying(array, pos):
    i = (len(array) - 1)
    while i >= pos:
        array[i, 1] = array[i - 1, 1] 
        i -= 1    
    array[pos, 1] = None    

def reorderMinionsAfterRemoving(array, pos):
    if pos == len(array) - 1:
        return array
    while pos < len(array) - 1:
        if array[pos + 1] == None:
            return array
        else:
            array[pos] = array[pos + 1]
            array[pos + 1] = None
        pos += 1
    return array
            
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
    return split(line, 'CardID=',' ')
def getPosition(line):
    return int(split(line, 'pos from 0 -> '))

def Statedecision():
    log = readLog()
    nol = len(log)
    while True:
        time.sleep(0.03)
        new_log = readLog()
        new_nol = len(new_log)
        new_lines = new_log[nol : new_nol]
        i = 0
        while i < len(new_lines):
            if 'CREATE_GAME' in new_lines[i]:
                print 'GameStart'
                setCurState('GAME_START')
                completeReading(new_lines[i:], 'GAME_START')
                break
            elif not getCurState() is None: 
                completeReading(new_lines[i:], getCurState())
                break
            i += 1   
        log = new_log
        nol = new_nol
                
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
        print 'no Correct State'

#variables for readGameStartPowerLines()
Found= False
def isFound():
    global Found
    return Found
def setFound(binary):
    global Found
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
    playerID = Id
def getPlayerID():
    global playerID
    return playerID
tmp = None
def getTmp():
    global tmp
    return tmp
def setTmp(temp):
    global tmp
    tmp = temp


def readGameStartPowerLines(input):
    for idx, line in enumerate(input):
        if '[Zone]' in line:
            setCurState('MULLIGAN')
            completeReading(input[idx:], getCurState())
            return
        elif 'CardID=HERO_' in line:
            setFound(True)
            setWaiting(True)
            setTmp(split(line, 'CardID=', '\n'))
        elif isFound() and 'tag=CONTROLLER' in line:
            setFound(False)
            setPlayerID(int(split(line, 'value=', '\n')))
            if getPlayerID() == 1:
                setMyHero(getTmp())
            else:
                setEnemyHero(getTmp())
        elif isWaiting() and not isFound() and 'CardID=' in line:
            setWaiting(False)
            if getPlayerID() == 1:
                setMyHeroPower(split(line, 'CardID=', '\n'))
            else:
                setEnemyHeroPower(split(line, 'CardID=', '\n'))
        elif not isWaiting() and 'CardID=' in line and not 'HERO' in line:
            cardId = split(line, 'CardID=')
            if '\n' == cardId:
                continue
            else:
                setWaiting(True)
                setTmp(cardId.split('\n')[0])
        elif isWaiting() and 'ZONE_POSITION' in line:
            setWaiting(False)
            # buglogger(line, getTmp())
            addHandcardAtPosition(getTmp(), int(split(line, 'value=', '\n')))
        elif 'TAG_CHANGE' in line and 'CONTROLLER' in line:
            if int(split(line, 'value=', '\n')) == 1 and getPlayerName(1) is None:
                setPlayerName(1, split(line, 'Entity=', ' tag'))
                print getPlayerName(1)
                time.sleep(0.5)
            elif int(split(line, 'value=', '\n')) == 2 and getPlayerName(2) is None:
                setPlayerName(2, split(line, 'Entity=', ' tag'))
                print getPlayerName(2)
                time.sleep(0.5)
            continue
                
def readingMulligan(input):
    for idx, line in enumerate(input):
        if 'MULLIGAN_STATE' in line and 'DONE' in line:
            print line
            time.sleep(0.5)
            if split(line, 'Entity=', ' tag') == getPlayerName(1):
                setMyMulliganStateDone(True)
            elif split(line, 'Entity=', ' tag') == getPlayerName(2):
                setEnemyMulliganStateDone(True)
            if isMyMulliganStateDone() and isEnemyMulliganStateDone():
                if getHandcardCount() == 3:
                    setCurState('MY_TURN')
                    print 'now reading My Turn'
                    time.sleep(1000)
                    # completeReading(input[idx:], getCurState())
                    return
                else:
                    setCurState('ENEMY_TURN')
                    print 'now reading Enemy Turn'
                    time.sleep(1000)
                    # completeReading(input[idx:], getCurState())
                    return         
        elif getPlayerName(1) is not None and 'MULLIGAN_STATE' in line and 'DEALING' in line:
            setWaiting(True)
            continue
        elif isWaiting() and 'SHOW_ENTITY' in line:
            setTmp(split(line, 'CardID=', '\n'))
            continue
        elif isWaiting() and 'HIDE_ENTITY' in line:
            setWaiting(False)
            pos = int(split(line, 'zonePos=', ' '))
            removeHandcardFromPosition(pos)
            # put removed Card back to DECK
            addHandcardAtPosition(getTmp(), pos)
            continue
        elif 'TAG_CHANGE' in line and 'CONTROLLER' in line:
            if int(split(line, 'value=', '\n')) == 1 and getPlayerName(1) is None:
                setPlayerName(1, split(line, 'Entity=', ' tag'))
                print getPlayerName(1)
                time.sleep(0.5)
            elif int(split(line, 'value=', '\n')) == 2 and getPlayerName(2) is None:
                setPlayerName(2, split(line, 'Entity=', ' tag'))
                print getPlayerName(2)
                time.sleep(0.5)
            continue
        
def readingMyTurn(input):
    for idx, line in enumerate(input):
        if not '[ZONE]' in line and not '[POWER]' in line:
            continue
        else:
            if 'MAIN_END' in line:
                setCurState('ENEMY_TURN')
                completeReading(input[idx:], getCurState())
                return
            if 'TAG_CHANGE' in line and 'RESOURCES' in line:
                setMyMana(int(split(line, 'value= ', '\n')))
            if 'SHOW_ENTITY' in line:
                addHandcardAtPosition(split(line, 'CardID=', '\n'), (getHandcardCount() + 1))
            if 'SubType=PLAY' in line:
                card = getHandcard(int(split(line, 'ZonePos=', ' ')), 1)
                setMyMana(getMyMana() - card.manacosts)
                if card.cardtype == 'Minion':
                    print card.name
                    setWaiting(True)
                    setTmp(card)
                elif card.cardtype == 'Spell':
                    print card.name
                elif card.cardtype == 'Weapon':
                    print card.name
                elif card.cardtype == 'Secret':
                    print card.name
            if isWaiting() and 'CardID='+getTmp().id in line and 'ZONE_POSITION' in line:
                setWaiting(False)
                addMyMinonToField(getTmp(), split(line, 'value=', '\n'))
            #if 'option 0' in Line and 'END_TURN' in Line:
            #    print 'no more option. Click End Turn'
            if 'SubType=ATTACK' in line:
                attack(line, 'ME')

            
def attack(line, attacker):
    attackerInfo, targetInfo= line.split('ATTACK')
    attackZone = int(split(attackerInfo, 'zonePos=', ' cardId='))
    targetZone = split(targetInfo, 'zonePos=', ' cardId')
    a_minion = None
    t_minion = None
    if attacker == 'ME':
        a_minion = getMyMinion(attackZone) 
        t_minion = getEnemyMinion(targetZone)
    else:
        a_minion = getEnemyMinion(attackZone) 
        t_minion = getMyMinion(targetZone)
    t_minion.health = t_minion.health - a_minion.attack
    a_minion.health = a_minion.health - t_minion.attack
    if attacker == 'ME':
        if a_minion.health <= 0:
            removeMyMinonFromField(attackZone)
        if t_minion.health <= 0:
            removeEnemyMinonFromField(targetZone)
    else:
        if a_minion.health <= 0:
            removeEnemyMinonFromField(attackZone)
        if t_minion.health <= 0:
            removeMyMinonFromField(targetZone)
            
def readingEnemyTurn(input):
    for idx, line in enumerate(input):
        if not '[ZONE]' in line and not '[POWER]' in line:
            continue
        else:
            if 'MAIN_END' in line:
                setCurState('ENEMY_TURN')
                completeReading(input[idx:], getCurState())
                return
            if 'TAG_CHANGE' in line and 'RESOURCES' in line:
                setEnemyMana(int(split(line, 'value= ', '\n')))

def createCard(card):
    cardtype = cReader.cardType(card)
    _card = Card(cReader.id(card), cReader.name(card), cardtype, cReader.manaCost(card))
    if cardtype == 'Minion':
        _card.attack = cReader.attackValue(card)
        _card.health = cReader.healthValue(card)
    if cardtype == 'Hero':
        _card.health = cReader.healthValue(card)
    return _card     
  
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

def Statedecision_test():
    log = None
    nol = 0
    while True:
        time.sleep(0.03)
        new_log = open(path('doc/output_log_fullInfo.txt'), 'r').readlines()
        new_nol = len(new_log)
        new_lines = new_log[nol : new_nol]
        i = 0
        while i < len(new_lines):
            if 'CREATE_GAME' in new_lines[i]:
                print 'GameStart'
                setCurState('GAME_START')
                completeReading(new_lines[i:], 'GAME_START')
                break
            elif not getCurState() is None: 
                completeReading(new_lines[i:], getCurState())
                break
            i += 1   
        log = new_log
        nol = new_nol
#--------EVENTS-------#
#?????????????????????#
def MinionChanges():
    print 'Minion Changes'

def DocumentChanges():
    print 'There are new line of code'

def HandcardsChanges():
    print 'Something within your handcards changes'

def GameStatusChanges():
    print 'Gamestatus changes'

