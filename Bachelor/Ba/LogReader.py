import os
import time
import numpy as np
import cardLibReader as cReader
import Card


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
    try:
        if len(args) == 2:
            return args[0].split(args[1])[1]
        elif len(args) == 3:
            return args[0].split(args[1])[1].split(args[2])[0]
    except Exception, e:
        print args[0], e

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
  
GAME_STATES = np.array(['GAME_START', 'MULLIGAN', 'MY_TURN', 'ENEMY_TURN', 'GAME_END'])
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
    addHandcardAtPosition(powerId, 0)
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

MY_HANDCARDS = np.array([None,None,None,None,None,None,None,None,None,None,None])
def getHandcards():
    global MY_HANDCARDS
    return MY_HANDCARDS
def getHandcard(ZonePosition, WithRemoving):
    global MY_HANDCARDS
    if WithRemoving:
        card = MY_HANDCARDS[ZonePosition]
        removeHandcardFromPosition(ZonePosition)
        MY_HANDCARDS = reOrderHandcards(MY_HANDCARDS, ZonePosition)
        return card
    return MY_HANDCARDS[ZonePosition]
def addHandcardAtPosition(cardId, pos):
    global MY_HANDCARDS
    card = createCard(cReader.CardById(cardId))
    card._zone = 'HAND'
    card._zonePos = pos
    #card.zone = 'HAND'
    #card.zonePos = pos
    if MY_HANDCARDS[pos] is None:
        MY_HANDCARDS[pos] = card 
    print 'got new Card:'
    output = ''
    for card in MY_HANDCARDS:
        if card is not None:
            if card._cardtype == 'Hero Power':
                continue
            output += card._name + ' '
    print output
           # print card._name
def removeHandcardFromPosition(pos):
    global MY_HANDCARDS
    MY_HANDCARDS[pos] = None
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
    length = len(handcards) - 1
    if pos == length:
        return handcards
    while pos < length:
        if handcards[pos + 1] is None:
            return handcards
        else:
            handcards[pos] = handcards[pos + 1]
            handcards[pos]._zonePos -= 1
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
    card._zone = 'PLAY'
    card._zonePos = pos
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
        elif getCurState() == getGameState(4):
            setCurState(None)
            return
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
        if '[Power]' in line:
            try:
                if 'GameEntity tag=NEXT_STEP value=BEGIN_MULLIGAN' in line:
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
                    elif int(split(line, 'value=', '\n')) == 2 and getPlayerName(2) is None:
                        setPlayerName(2, split(line, 'Entity=', ' tag'))
                        print getPlayerName(2)
                    continue
            except Exception, e:
                print 'GAME START', line, e
                
def readingMulligan(input):
    for idx, line in enumerate(input):
        if '[Power]' in line:
            try:
                if 'MULLIGAN_STATE' in line and 'DONE' in line:
                    print line
                    setWaiting(False)
                    time.sleep(0.5)
                    if split(line, 'Entity=', ' tag') == getPlayerName(1):
                        setMyMulliganStateDone(True)
                    elif split(line, 'Entity=', ' tag') == getPlayerName(2):
                        setEnemyMulliganStateDone(True)
                    if isMyMulliganStateDone() and isEnemyMulliganStateDone():
                        if getHandcardCount() == 4:
                            setCurState('MY_TURN')
                            print 'now reading My Turn'
                            completeReading(input[idx:], getCurState())
                            return
                        else:
                            setCurState('ENEMY_TURN')
                            print 'now reading Enemy Turn'
                            completeReading(input[idx:], getCurState())
                            return         
                elif getPlayerName(1) is not None and 'MULLIGAN_STATE' in line and 'DEALING' in line:
                    setWaiting(True)
                    continue
                elif isWaiting() and 'SHOW_ENTITY' in line:
                    setTmp(split(line, 'CardID=', '\n'))
                    continue
                elif isWaiting() and 'HIDE_ENTITY' in line:
                    pos = int(split(line, 'zonePos=', ' '))
                    removeHandcardFromPosition(pos)
                    # put removed Card back to DECK
                    addHandcardAtPosition(getTmp(), pos)
                    continue
                elif 'TAG_CHANGE' in line and 'CONTROLLER' in line:
                    if int(split(line, 'value=', '\n')) == 1 and getPlayerName(1) is None:
                        setPlayerName(1, split(line, 'Entity=', ' tag'))
                        print getPlayerName(1)
                    elif int(split(line, 'value=', '\n')) == 2 and getPlayerName(2) is None:
                        setPlayerName(2, split(line, 'Entity=', ' tag'))
                        print getPlayerName(2)
                    continue
            except Exception, e:
                print 'MULLIGAN:', line, e    
                        
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
    t_minion._health = t_minion._health - a_minion._attack
    a_minion._health = a_minion._health - t_minion._attack
    if attacker == 'ME':
        if a_minion._health <= 0:
            removeMyMinonFromField(attackZone)
        if t_minion._health <= 0:
            removeEnemyMinonFromField(targetZone)
    else:
        if a_minion._health <= 0:
            removeEnemyMinonFromField(attackZone)
        if t_minion._health <= 0:
            removeMyMinonFromField(targetZone)

def readingMyTurn(input):
    for idx, line in enumerate(input):
        if '[Power]' in line:
            try:
                if 'FINAL_GAMEOVER' in line:
                    print 'Game End'
                    setCurState('GAME_OVER')
                    return
                if 'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState('ENEMY_TURN')
                    print 'Turn Change'
                    completeReading(input[(idx+1):], getCurState())
                    return
                elif 'TAG_CHANGE' in line and 'RESOURCES' in line:
                    setMyMana(int(split(line, 'value=', '\n')))
                elif 'SHOW_ENTITY' in line:
                    addHandcardAtPosition(split(line, 'CardID=', '\n'), (getHandcardCount() + 1))
                elif 'option ' in line:
                    setWaiting(False)
                    if 'type=END_TURN' in line:
                        print 'option ', split(line, 'option ', ' type'), ': ' ,split(line, 'type=', 'main')
                    elif 'type=POWER' in line and 'zone=HAND' in line:
                        print 'option ', split(line, 'option ', ' type'), ': PLAY ' , split(line, 'name=', ' id') 
                    elif 'type=POWER' in line and 'zone=PLAY' in line and 'zonePos=0' not in line:
                        setWaiting(True)
                        print 'option ', split(line, 'option ', ' type'), ': ATTACK WITH ' , split(line, 'name=', ' id')
                elif isWaiting() and 'target' in line:
                    print 'target ', split(line, 'target ', ' entity'), ': ', split(line, 'name=', ' id')   
                elif isWaiting() and 'm_currentTaskList' in line:
                    setWaiting(False)   
                elif 'SubType=PLAY' in line:
                    pos = int(split(line, 'zonePos=', ' '))
                    if pos == 0:
                        card = getHandcard(pos, 0)
                    else:
                        card = getHandcard(pos, 1)
                    setMyMana(getMyMana() - card._manacosts)
                    if card._cardtype == 'Minion':
                        print 'Played', card._name
                        setWaiting(True)
                        setTmp(card)
                    elif card._cardtype == 'Spell':
                        print 'Played', card._name
                    elif card._cardtype == 'Weapon':
                        print 'Played', card._name
                    elif card._cardtype == 'Secret':
                        print 'Played', card._name
                    elif card._cardtype == 'Hero Power':
                        print 'Played', 'Hero Power'
                elif isWaiting() and 'CardID='+getTmp()._id in line and 'ZONE_POSITION' in line:
                    setWaiting(False)
                    addMyMinonToField(getTmp(), split(line, 'value=', '\n'))
                #if 'option 0' in Line and 'END_TURN' in Line:
                #    print 'no more option. Click End Turn'
                elif 'SubType=ATTACK' in line:
                    attack(line, 'ME')
            except Exception, e:
                print 'MY TURN:', line, e
def readingEnemyTurn(input):
    for idx, line in enumerate(input):
        if '[Power]' in line:
            try:
                if 'FINAL_GAMEOVER' in line:
                    print 'Game End'
                    setCurState('GAME_OVER')
                    return
                if 'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState('MY_TURN')
                    print 'Turn Change'
                    completeReading(input[(idx+1):], getCurState())
                    return
                elif 'TAG_CHANGE' in line and 'RESOURCES' in line:
                    setEnemyMana(int(split(line, 'value=', '\n')))
                elif 'SubType=PLAY' in line:
                    setWaiting(True)
                elif isWaiting() and 'SHOW_ENTITY' in line:
                    card = createCard(cReader.CardById(split(line, 'CardID=', '\n')))   
                    if card._cardtype == 'Minion':
                        setTmp(card)
                        print 'Played', card._name
                    elif card._cardtype == 'Spell':
                        print 'Played', card._name
                        setWaiting(False)
                    elif card._cardtype == 'Weapon':
                        print 'Played', card._name
                        setWaiting(False)                       
                    elif card._cardtype == 'Secret':
                        print 'Played', card._name
                        setWaiting(False)
                    elif card._cardtype == 'Hero Power':
                        print 'Played', 'Hero Power'
                        setWaiting(False)
                elif isWaiting() and 'ZONE_POSITION' in line:
                    addEnemyMinonToField(getTmp(), int(split(line, 'value=', '\n')))
                    setWaiting(False)
            except Exception, e:
                print 'ENEMY TURN:', line, e
def createCard(card):
    cardtype = cReader.cardType(card)
    _card = Card.Card(cReader.id(card), cReader.name(card), cardtype, cReader.manaCost(card))
    if cardtype == 'Minion':
        _card._attack = cReader.attackValue(card)
        _card._health = cReader.healthValue(card)
    if cardtype == 'Hero':
        _card._health = cReader.healthValue(card)
    return _card     
  
def Main():
    Statedecision()
    
Main()
   #-----TESTREADER-----#
def splitter():
    file = open(path('doc/output_log2.txt'), 'r')
    power = open(path('doc')+'/power2.txt', 'w')
    for l in file:
        if '[Power]' in l:
            power.write(l)

#splitter()
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


