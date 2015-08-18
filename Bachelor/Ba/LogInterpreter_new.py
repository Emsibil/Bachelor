from random import random
from time import sleep
from types import IntType
from Util_new import split, Cardtype, Zone, gameId,\
    value, Option
from Cards_new import createCard
from Board import setMyCards, setEnemyCards,\
    getCardByIngameId, addCardToMyCards, addCardToEnemyCards,\
    setMyMana, setEnemyMana, getMyMana, getEnemyMana
from Play import MulliganChoosing, MulliganConfirm, chooseOption,\
    addOption, getOptions
    
PLAYER_ONE_CARDS = {}
def setPlayerOneCard(card):
    global PLAYER_ONE_CARDS
    PLAYER_ONE_CARDS[card._ingameID] = card
def getPlayerOneCards():
    global PLAYER_ONE_CARDS
    return PLAYER_ONE_CARDS
PLAYER_TWO_CARDS = {}
def setPlayerTwoCard(card):
    global PLAYER_TWO_CARDS
    PLAYER_TWO_CARDS[card._ingameID] = card
def getPlayerTwoCards():
    global PLAYER_TWO_CARDS
    return PLAYER_TWO_CARDS

PLAYER_ONE_IN_MULLIGAN = False
def setPlayerOneInMulligan(value):
    global PLAYER_ONE_IN_MULLIGAN
    PLAYER_ONE_IN_MULLIGAN = value
def isPlayerOneInMulligan():
    global PLAYER_ONE_IN_MULLIGAN
    return PLAYER_ONE_IN_MULLIGAN

PLAYER_TWO_IN_MULLIGAN = False
def setPlayerTwoInMulligan(value):
    global PLAYER_TWO_IN_MULLIGAN
    PLAYER_TWO_IN_MULLIGAN = value
def isPlayerTwoInMulligan():
    global PLAYER_TWO_IN_MULLIGAN
    return PLAYER_TWO_IN_MULLIGAN

PLAYER_ONE_MULLIGAN_DONE = False
def isPlayerOneMulliganStateDone():
    global PLAYER_ONE_MULLIGAN_DONE
    return PLAYER_ONE_MULLIGAN_DONE
def setPlayerOneMulliganStateDone(State):
    global PLAYER_ONE_MULLIGAN_DONE
    PLAYER_ONE_MULLIGAN_DONE = State  
     
PLAYER_TWO_MULLIGAN_DONE = False
def isPlayerTwoMulliganStateDone():
    global PLAYER_TWO_MULLIGAN_DONE
    return PLAYER_TWO_MULLIGAN_DONE
def setPlayerTwoMulliganStateDone(State):
    global PLAYER_TWO_MULLIGAN_DONE
    PLAYER_TWO_MULLIGAN_DONE = State
def isMulliganOver():
    return (isPlayerOneMulliganStateDone() and isPlayerTwoMulliganStateDone())
        
def containsUNKOWNCards(cardDict):
    for Id in cardDict:
        if cardDict[Id]._id is not None:
            if not (cardDict[Id].compareCardtype(Cardtype.HERO) or cardDict[Id].compareCardtype(Cardtype.HERO_POWER)):
                return False
    return True
    
def allocateCardToPlayers():
    cardDict = getPlayerOneCards()
    if containsUNKOWNCards(cardDict):
        setEnemyCards(cardDict)
        setMyCards(getPlayerTwoCards())
    else:
        setEnemyCards(getPlayerTwoCards())
        setMyCards(cardDict)
        
PLAYERS = {}
def setPlayer(name, Id):
    global PLAYERS
    PLAYERS[Id] = name
    if len(PLAYERS) == 2:
        allocateCardToPlayers()
def getPlayerId(name):
    global PLAYERS
    if PLAYERS[1] == name:
        return 1
    else:
        return 2
def getPlayer(Id):
    global PLAYERS
    return PLAYERS[Id]
ME = None
def setMe(Id):
    global ME
    ME = Id
def isThatMe(name):
    global ME
    return getPlayerId(name) == ME
def isThatMyId(Id):
    global PLAYERS
    return isThatMe(PLAYERS[Id])
def isEnemyTurn(l):
    return isThatMe(split(l, 'Entity=', ' tag'))   
TEMP_CARD = None
def setTempCard(card):
    global TEMP_CARD
    TEMP_CARD = card
def getTempCard():
    global TEMP_CARD
    return TEMP_CARD

def EntityFinder(line):
    return 'TAG_CHANGE Entity=[' in line

def EntityChanger(line):
    try:
        card = None
        try:
            card = getCardByIngameId(gameId(line))
        except:
            print 'EntityChanger could not find Card and build it new'
            _card = createCard(gameId(line), split(line, 'cardId=', ' '))
            _card._zone = split(line, 'zone=', ' ')
            _card.set_pos(int(split(line, 'zonePos=', ' ')))
            if isThatMyId(int(split(line, 'player=', ']'))):
                addCardToMyCards(_card)
            else:
                addCardToEnemyCards(_card)
            card = getCardByIngameId(_card._ingameID)
        if 'ZONE_POSITION' in line:
            card.set_pos(int(value(line)))
        elif 'ZONE ' in line:
            card._zone = value(line)
        elif not 'PREDAMAGE' in line and 'DAMAGE' in line:
            card.takes_Damage(int(value(line)))
        elif 'ATK' in line:
            card._attack = int(value(line))
        elif 'HEALTH' in line:
            card._health = int(value(line))
        elif 'EXHAUSTED' in line:
            card.set_exhausted(int(value(line)))
        elif 'ARMOR' in line:
            card._armor = int(value(line))
        elif 'TAUNT' in line:
            card._taunt = True if int(value(line)) == 1 else False 
        elif 'CHARGE' in line:
            card._charge = True if int(value(line)) == 1 else False
        elif 'WINDFURY' in line:
            card._windfury = True if int(value(line)) == 1 else False
        elif 'DIVINE_SHIELD' in line:
            card._divineShield = True if int(value(line)) == 1 else False
        elif 'STEALTH' in line:
            card._stealth = True if int(value(line)) == 1 else False
    except Exception, e:
        print 'EntityChanger()', e
        
             
def GameStart_Full_Entity(lines):
    try:
        card = None
        playerId = None
        zone = None   
        for l in lines:
            if 'FULL_ENTITY' in l:
                card = createCard(int(split(l, 'ID=', ' ')), split(l, 'CardID=', '\n'))
            if 'ZONE ' in l:
                zone = value(l)
            elif 'CONTROLLER' in l:  
                playerId = int(value(l))
                if card._id is not None:
                    if not (card.compareCardtype(Cardtype.HERO) or card.compareCardtype(Cardtype.HERO_POWER)):  
                        card._zone = zone
                        setMe(playerId)
                    elif card.compareCardtype(Cardtype.HERO):
                        card._zone = Zone.PLAY
                        card.set_pos(0)
                    elif card.compareCardtype(Cardtype.HERO_POWER):
                        card._zone = Zone.HAND
                        card.set_pos(0)
            elif 'ZONE_POSITION' in l:
                card.set_pos(int(value(l)))
        if  playerId == 1:
            setPlayerOneCard(card)
        else:
            setPlayerTwoCard(card)
    except Exception, e:
        print 'GameStart_Full_Entity()', e

def Mulligan():
    sleep(random()*7+13)
    MulliganChoosing()
    sleep(2)
    MulliganConfirm() 
        
def Full_Entity(lines):
    try:
        card = None
        zone = Zone.DECK
        for l in lines:
            if 'FULL_ENTITY' in l:
                if not split(l, 'CardID=', '\n') == '': 
                    card = createCard(int(split(l, 'ID=', ' ')), split(l, 'CardID=', '\n'))
            elif 'ZONE_POSITION' in l and not zone == Zone.SETASIDE :
                _card = getCardByIngameId(card._ingameID)
                _card.set_pos(int(value(l)))
            elif 'ZONE' in l:
                zone = value(l)
            elif 'CONTROLLER' in l:
                playerId = int(value(l))
                if card is not None:
                    card._zone = zone
                    if isThatMyId(playerId):
                        addCardToMyCards(card)
                    else:
                        addCardToEnemyCards(card)
            elif 'SHOW_ENTITY' in l:
                card = createCard(int(split(l, 'Entity=', ' ')), split(l, 'CardID=', '\n'))
                card._zone = zone
                card.set_pos(0)
                if isThatMyId(playerId):
                    addCardToMyCards(card)
                else:
                    addCardToEnemyCards(card)
                break
    except Exception, e:
        print 'Full_Entity()', e        
        
def Show_Entity(lines):
    try:
        for l in lines:
            if 'SHOW_ENTITY' in l:
                card = createCard(gameId(l), split(l, 'CardID=', '\n'))
                playerId = int(split(l, 'player=', ']'))
            elif 'ZONE' in l:
                card._zone = value(l)
        if isThatMyId(playerId):
            addCardToMyCards(card)
        else:
            addCardToEnemyCards(card)
    except Exception, e:
        print 'Show_Entity()', e
    
def searching_Show_Entity(index, lines):
    try:
        i = index
        while not 'TAG_CHANGE' in lines[i]:
            i = i + 1
        Show_Entity(lines[index:(i-1)])
        return i - index - 2
    except Exception, e:
        print 'searching_Show_Entity()', e
        
def searching_Full_Entity(index, lines):
    try:
        i = index
        while not 'CREATOR' in lines[i]:
            i = i + 1
        Full_Entity(lines[index:i])
        return i - index
    except Exception, e:
        print 'searching_Full_Entity()', e 
             
def SubTypeMulliganTrigger(lines):
    try:
        jumpLines = 0
        for index, l in enumerate(lines):
            if jumpLines > 0:
                jumpLines = jumpLines - 1
            elif '[Power]' in l:
                if 'MULLIGAN_STATE' in l and 'INPUT' in l:
                    if getPlayer(1) in l:
                        setPlayerOneInMulligan(True)     
                    elif getPlayer(2) in l:
                        setPlayerTwoInMulligan(True)
                elif 'MULLIGAN_STATE' in l and 'DONE' in l:
                    if getPlayerId(split(l, 'Entity=', ' tag')) == 1:
                        setPlayerOneMulliganStateDone(True)
                    else:
                        setPlayerTwoMulliganStateDone(True)    
                elif 'SHOW_ENTITY' in l:    
                    jumpLines = searching_Show_Entity(index, lines)
                elif EntityFinder(l):
                    EntityChanger(l)
    except Exception, e:
        print 'SubTypeMulliganTrigger()', e
               
def SubType(lines):
    try:
        jumpLines = 0
        for index, l in enumerate(lines):
            if jumpLines > 0:
                jumpLines = jumpLines - 1
                continue
            if EntityFinder(l):
                EntityChanger(l)
            elif 'SHOW_ENTITY' in l:
                jumpLines = searching_Show_Entity(index, lines)
            elif 'FULL_ENTITY' in l:
                jumpLines = searching_Full_Entity(index, lines)
            elif 'TEMP_RESOURCES' in l:
                if isThatMe(split(l, 'Entity=', ' tag')):
                    setMyMana(getMyMana() + int(value(l)))
                else:
                    setEnemyMana(getEnemyMana() + int(value(l)))
            elif 'RESOURCES_USED' in l:
                if isThatMe(split(l, 'Entity=', ' tag')):
                    setMyMana(getMyMana() - int(value(l)))
                else:
                    setEnemyMana(getEnemyMana() - int(value(l)))
            elif 'RESOURCES' in l:
                if isThatMe(split(l, 'Entity=', ' tag')):
                    setMyMana(int(value(l)))
                else:
                    setEnemyMana(int(value(l)))
    except Exception, e:
        print 'SubType()', e
        
def readOptions(lines):
    i = 0
    parameter1 = None
    parameter2 = None
    targets = []
    try:
        while i < len(lines):
            if 'option' in lines[i]:
                output = str(split(lines[i], '() -   ', ' type')) + ': '
                if parameter2 is not None:
                    if not len(targets) == 0:
                        addOption((parameter1, parameter2, targets))
                    else:
                        addOption((parameter1, parameter2, None))
                    parameter1 = None
                    parameter2 = None
                    targets = []
                if 'END_TURN' in lines[i]:
                    output += 'End Turn'
                    parameter2 = Option.END
                elif 'POWER' in lines[i] and 'zone=HAND' in lines[i]:
                    Id = gameId(lines[i])
                    if getCardByIngameId(Id).compareZone(Zone.HAND):
                        output += 'Play ' +str(split(lines[i], 'name=', ' id'))
                        parameter1 = Id
                        parameter2 = Option.PLAY
                    elif getCardByIngameId(Id).compareZone(Zone.PLAY):
                        output += 'Attack with ' +str(split(lines[i], 'name=', ' id'))
                        parameter1 = Id
                        parameter2 = Option.ATTACK
                elif 'POWER' in lines[i] and 'zone=DECK' in lines[i]:
                    output += 'Play ' + getCardByIngameId(gameId(lines[i]))._name
                    parameter1 = gameId(lines[i])
                    parameter2 = Option.PLAY
                elif 'POWER' in lines[i] and 'zone=PLAY' in lines[i] and 'zonePos=0' in lines[i]:
                    parameter1 = gameId(lines[i])
                    if 'cardId=HERO' in lines[i]:
                        output += 'Hero Attack'
                        parameter2 = Option.ATTACK
                    else:
                        output += 'Play Hero Power'
                        parameter2 = Option.PLAY
                elif 'POWER' in lines[i] and 'zone=PLAY' in lines[i] and 'zonePos=0' not in lines[i]:
                    output += 'Attack with ' +str(split(lines[i], 'name=', ' id'))
                    parameter1 = gameId(lines[i])
                    parameter2 = Option.ATTACK
                if i+4 < len(lines):
                    if 'target' in lines[i+4]:
                        output += '\n \t Possible Targets: '
                print output
            if 'target' in lines[i]:
                Id = gameId(lines[i])
                name = getCardByIngameId(Id)._name
                print '\t \t' + name
                if type(id) is IntType:
                    targets.append(Id)
                else:
                    targets.append(gameId(lines[i]))
            i += 1
        if parameter2 is not None:
            if not len(targets) == 0:
                addOption((parameter1, parameter2, targets))
            else:
                addOption((parameter1, parameter2, None))
        chooseOption(getOptions())
    except Exception, e:
        print 'showOptions', lines[i], e