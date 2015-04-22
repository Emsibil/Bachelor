import os
import time
import numpy as np
from types import * 
import cardLibReader as cReader
import Card
import MouseControl as mc
from random import random

path = 'C:/Program Files (x86)'  #Uni
#path = 'D:/Programme' #Home

#returns the full path of a special file
def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

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
    global ENEMY_MULLIGAN_DONE
    return ENEMY_MULLIGAN_DONE
def setEnemyMulliganStateDone(State):
    global ENEMY_MULLIGAN_DONE
    ENEMY_MULLIGAN_DONE = State
  
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

def createCard(card):
    cardtype = cReader.cardType(card)
    _card = Card.Card(cReader.id(card), cReader.name(card), cardtype, cReader.manaCost(card))
    if cardtype == 'Minion':
        _card._attack = cReader.attackValue(card)
        _card._health = cReader.healthValue(card)
    if cardtype == 'Hero':
        _card._health = cReader.healthValue(card)
    return _card 

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



MinionsOnEnemySide = np.array([[0, None],[1, None], [2, None], [3, None], [4, None], [5, None], [6, None], [7, None]])
def getEnemyMinions():
    global MinionsOnEnemySide
    return MinionsOnEnemySide    
def getEnemyMinion(pos):
    global MinionsOnEnemySide
    return MinionsOnEnemySide[pos][1]
def addEnemyMinonToField(card, pos):
    global MinionsOnEnemySide
    card.set_pos(pos)
    MinionsOnEnemySide[pos] = card
def removeEnemyMinonFromField(pos):
    global MinionsOnEnemySide
    MinionsOnEnemySide[pos] = None
    reorderMinionsAfterRemoving(MinionsOnEnemySide, pos)
def getEnemyMinionCount():
    global MinionsOnEnemySide
    count = 0
    for minion in MinionsOnEnemySide:
        if minion[1] is not None:
            count += 1
        else:
            return count - 1
    return count - 1
def getEnemyMinionByIngameID(idx):
    global MinionsOnEnemySide
    try:
        for minion in MinionsOnEnemySide:
            if minion[1] is not None:
                if minion[1]._ingameID == idx:
                    return minion[1]
    except:
        print 'No Minion with that Id on Board'

CARDS = {}

def getCards():
    global CARDS
    return CARDS

def addHandcardAtPosition(cardId, pos, ingameID):
    cards = getCards()
    card = createCard(cReader.CardById(cardId))
    card._ingameID = ingameID
    if card._cardtype == 'Hero':
        card._zone = 'PLAY'
    else:
        card._zone = 'HAND'
    card.set_pos(pos)
    #card.zone = 'HAND'
    #card.zonePos = pos
    cards[ingameID] = card
     
    print 'got new Card:'
    output = ''
    for card in cards.values():
        if card._cardtype == 'Hero Power':
            continue
        output += card._name + ' '
    print output

def getHandcardCount():
    count = len([c for c in getCards().values() if c._zone=="HAND"])
    return (count - 1)

def getCardByIngameId(idx):
    return getCards()[idx]
    
def removeCardByIngameId(idx):
    del getCards()[idx]
    
def reorderHandCards(pos):
    cards = getCards()
    for c in cards:
        if cards[c]._zone == 'HAND' and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1

def addMyMinonToField(card, pos):
    cards = getCards()
    card.set_pos(pos)
    cards[card._ingameID] = card
    
def getMyMinionCount():
    count = len([c for c in getCards().values() if c._zone=="PLAY"])
    return (count - 1)

def reorderMinionsOnBoard(pos):
    cards = getCards()
    for c in cards:
        if cards[c]._zone == 'PLAY' and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1
            
MY_HERO = None
MY_HERO_POWER = None
ENEMY_HERO = None
ENEMY_HERO_POWER = None

def setMyHero(heroId, ingameID):
    global MY_HERO
    MY_HERO = heroId
    hero = createCard(cReader.CardById(heroId))
    hero._ingameID = ingameID
    addMyMinonToField(hero, 0)
    print 'Set Hero'
def setMyHeroPower(powerId, ingameID):
    global MY_HERO_POWER
    addHandcardAtPosition(powerId, 0, ingameID)
    MY_HERO_POWER = powerId
    print 'Set Hero Power'
def setEnemyHero(heroId, ingameID):
    global ENEMY_HERO
    ENEMY_HERO = heroId
    hero = createCard(cReader.CardById(heroId))
    hero._ingameID = ingameID
    addEnemyMinonToField(hero, 0)
    print 'Set Enemy Hero'
def setEnemyHeroPower(powerId, ingameID):
    global ENEMY_HERO_POWER
    ENEMY_HERO_POWER = powerId
    heroPower = createCard(cReader.CardById(powerId))
    heroPower._ingameID = ingameID
    print 'Set Enemy Hero Power'
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

COMBO = False
def setCombo(binary):
    global COMBO
    COMBO = binary
def isComboActive():
    global COMBO
    return COMBO

OPTIONS = []
def addOption(option):
    global OPTIONS
    OPTIONS.append(option)
def getOption(nr):
    global OPTIONS
    return OPTIONS[nr]
def getOptions():
    global OPTIONS
    return OPTIONS
def clearOptions():
    global OPTIONS
    OPTIONS = []

Mulligan = False
def isMulligan():
    global Mulligan
    return Mulligan
def setMulligan(binary):
    global Mulligan
    Mulligan = binary

CALC_OPTIONS = False
def setOptionsCalc(binary):
    global CALC_OPTIONS
    CALC_OPTIONS = binary
def isOptionCalc():
    global CALC_OPTIONS
    return CALC_OPTIONS

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

def setVariablesDefault():
    setTmp(None)
    setWaiting(False)
    setMyMana(0)
    setEnemyMana(0)
    setFound(False)
    setCombo(False)  
                  
def attack(line):
    try:
        attackerInfo, targetInfo= line.split('ATTACK')
        attackZone = int(split(attackerInfo, 'zonePos=', ' cardId='))
        idx = split(targetInfo, 'id=', ' ')
        a_minion = getEnemyMinion(attackZone) 
        t_minion = getCardByIngameId(idx)
        t_minion._health = t_minion._health - a_minion._attack
        a_minion._health = a_minion._health - t_minion._attack
        if a_minion._health <= 0:
            removeEnemyMinonFromField(attackZone)
        if t_minion._health <= 0:
            reorderMinionsOnBoard(t_minion._zonePos)
            t_minion._zone ='GRAVEYARD'  
    except Exception, e:
        print 'attack', e 
     
def cardPlayed(playingLines):
    card = None
    for line in playingLines:
        if 'SubType=PLAY' in line:
            idx = int(split(line, 'id=', ' '))
            card = getCardByIngameId(idx)
            print card._manacosts
            setMyMana(getMyMana() - card._manacosts)
        elif card is not None:
            if card._cardtype == 'Minion':
                if 'tag=ZONE value=PLAY' in line:
                    setWaiting(True)
                elif isWaiting() and 'ZONE_POSITION' in line:
                    addMyMinonToField(card, int(split(line, 'value=', '\n')))
                    setWaiting(False)
                    print 'Played', card._name
                    break
            elif card._cardtype == 'Spell':
                print 'Played', card._name
                break
            elif card._cardtype == 'Weapon':
                print 'Played', card._name
                break                       
            elif card._cardtype == 'Secret':
                print 'Played', card._name
                break
            elif card._cardtype == 'Hero Power':
                print 'Played', 'Hero Power' 
                break           

def showOptions(optionLines):
    i = 0
    parameter1 = None
    parameter2 = None
    targets = []
    try:
        while i < len(optionLines):
            if 'option' in optionLines[i]:
                output = str(split(optionLines[i], '() -   ', ' type')) + ': '
                if parameter1 is not None:
                    if len(targets) != 0:
                        addOption((parameter1, parameter2, targets))
                    else:
                        addOption((parameter1, parameter2))
                    parameter1 = None
                    parameter2 = None
                    targets = []
                if 'END_TURN' in optionLines[i]:
                    output += 'End Turn'
                    addOption(('END', None))
                elif 'POWER' in optionLines[i] and 'zone=HAND' in optionLines[i]:
                    output += 'Play ' +str(split(optionLines[i], 'name=', ' id'))
                    parameter1 = int(split(optionLines[i], 'id=', ' zone'))
                    parameter2 = 'PLAY'
                elif 'POWER' in optionLines[i] and 'zone=DECK' in optionLines[i]:
                    output += 'Play ' + getCardByIngameId(int(split(optionLines[i], 'id=', ' ')))._name
                elif 'POWER' in optionLines[i] and 'zone=PLAY' in optionLines[i] and 'zonePos=0' in optionLines[i]:
                    parameter1 = int(split(optionLines[i], 'id=', ' zone'))
                    if 'cardId=HERO' in optionLines[i]:
                        output += 'Hero Attack'
                        parameter2 = 'ATTACK'
                    else:
                        output += 'Play Hero Power'
                        parameter2 = 'PLAY'
                elif 'POWER' in optionLines[i] and 'zone=PLAY' in optionLines[i] and 'zonePos=0' not in optionLines[i]:
                    output += 'Attack with ' +str(split(optionLines[i], 'name=', ' id'))
                    parameter1 = int(split(optionLines[i], 'id=', ' zone'))
                    parameter2 = 'ATTACK'
                if i+4 < len(optionLines):
                    if 'target' in optionLines[i+4]:
                        output += '\n \t Possible Targets: '
                print output
            if 'target' in optionLines[i]:
                name = ''
                idx = int(split(optionLines[i], 'id=', ' '))
                if 'name' in optionLines[i]:
                    name = str(split(optionLines[i], 'name=', 'id'))
                else:
                    name = getEnemyMinionByIngameID(idx)._name
                print '\t \t' + name
                if type(id) is IntType:
                    targets.append(idx)
                else:
                    targets.append(int(split(optionLines[i], 'id=', ' ')))
            i += 1
        if parameter1 is not None:
            if len(targets) != 0:
                addOption((parameter1, parameter2, targets))
            else:
                addOption((parameter1, parameter2))
    except Exception, e:
        print 'showOptions', optionLines[i], e
                                  
def EnemyCardPlayed(playingLines):
    card = None
    for line in playingLines:
        if 'SubType=PLAY' in line and 'name' in line.split('SubType=PLAY')[0]:
            print 'Played Hero Power'
            break
        elif 'SHOW_ENTITY' in line:
            card = createCard(cReader.CardById(split(line, 'CardID=', '\n')))
            card._ingameID = int(split(line, 'id=', ' cardId'))
        if card is not None and 'ZONE_POSITION' in line:
            if card._cardtype == 'Minion':
                print 'Played', card._name
                addEnemyMinonToField(card, int(split(line, 'value=', '\n')))
                card = None
                break
            elif card._cardtype == 'Spell':
                print 'Played', card._name
                card = None
                break
            elif card._cardtype == 'Weapon':
                print 'Played', card._name
                card = None
                break                       
            elif card._cardtype == 'Secret':
                print 'Played', card._name
                card = None
                break
        elif card is not None and '- ACTION_END' in line:
            if card._cardtype == 'Minion':
                addEnemyMinonToField(card, 1)
                print 'Played', card._name
            else:
                print 'Player', card._name
                
               
def MulliganChoosing():
    cards = getCards()
    count = getHandcardCount()
    change = []
    for card in cards.values():
        if card._manacosts >= 4:
            change.append(card)
            
    for card in change:
        pos = card._zonePos
        if count == 3: 
            mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getMulliganCardArea(pos, (count)))))
        else:
            mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getMulliganCardArea(pos, (count - 1)))))
        time.sleep(random()*1+0.5)
        mc.mouseClick()
        time.sleep(random()*1+0.5)

def MulliganConfirm():
    mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getMulliganConfirm())))
    time.sleep(2)
    mc.mouseClick()

def findTarget(idx):
    try:
        cards = getCards()
        for c in cards:
            if cards[c]._zone == 'PLAY' and cards[c]._ingameID == idx: 
                return (0, cards[c])      
        enemy_minions = getEnemyMinions()
        for minion in enemy_minions:
            if minion[1] is None: 
                break
            else:
                if minion[1]._ingameID == idx:
                    return (1, minion[1])
    except:
        print 'No Target Found'
    
    
def playHandcard(card, targetArea):
    try:
        count = getHandcardCount()
        mc.mouseMove(mc.getMouseMoveCoords(mc.getHandcardArea(count, card.get_pos())))
        time.sleep(1)
        mc.mouseDown()   
        time.sleep(0.5)
        mc.mouseMove(targetArea)
        if card._cardtype == 'Minion':
            addMyMinonToField(card, (int(getMyMinionCount()/2) + 1))
        if not card._cardtype == 'Hero Power':
            card._zone = 'PLAY'
            reorderHandCards(card._zonePos)
        time.sleep(2)
        mc.mouseUp()
    except Exception, e:
        print 'playHandcards()', e
    
def drawAttack(ownMinion ,target):
    mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getMinionBoard(getMyMinionCount([ownMinion.get_pos()])))))
    time.sleep(1)
    mc.mouseDown()
    time.sleep(0.5)
    mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getEnemyMinionBoard(getEnemyMinionCount()[target.get_pos()]))))
    time.sleep(1)
    mc.mouseUp()
    ownMinion._health = ownMinion._health - target._attack
    target._health = target._health - target._attack
    if ownMinion._health <= 0:
            reorderMinionsOnBoard(ownMinion._zonePos)
            ownMinion._zone ='GRAVEYARD' 
    if target._health <= 0:
        removeEnemyMinonFromField(target.get_pos())

def playMinionWithTarget(card, playZone, targetArea):
    count = getHandcardCount()
    mc.mouseMove(mc.getMouseMoveCoords(mc.getHandcardArea(count, card.get_pos())))
    time.sleep(1)
    mc.mouseDown()   
    time.sleep(0.5)
    mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getUneven1())))
    addMyMinonToField(card, playZone)
    time.sleep(1)
    mc.mouseUp()
    time.sleep(0.5)
    mc.mouseMove(targetArea)
    time.sleep(1)
    mc.mouseDown()
    time.sleep(0.5)
    mc.mouseUp()
        
def EndTurn():
    mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getTurn())))    
    time.sleep(1)
    mc.mouseDown()
    print "down"
    time.sleep(0.5)
    mc.mouseUp()
    print "up"
                  
def choosePlayingCard():
    try:
        options = getOptions()
        toDo = 0
        print 'allOptions', options
        if len(options) > 1:
            toDo = int(random()*len(options) - 1) + 1
        else:
            EndTurn()       
        choosenOption = options[toDo]
        print 'choosenOption', choosenOption
        
        if choosenOption[0] == 'END':
            EndTurn()
        else:
            if choosenOption[1] == 'PLAY':
                if len(choosenOption) == 3:
                    targetIndex = np.random.random_integers(1, len(choosenOption[2])) - 1
                    target = findTarget(choosenOption[2][targetIndex])
                    if target[0] == 0:
                        MinionBoard = mc.getMinionBoard(getMyMinionCount())
                    else:
                        MinionBoard = mc.getEnemyMinionBoard(getEnemyMinionCount())
                    card = getCardByIngameId(choosenOption[0])
                    try:
                        if card._cardtype == 'Minion':
                            playMinionWithTarget(card, 1, mc.getMouseMoveCoords(mc.area(MinionBoard[target[1].get_pos()])))
                        else:
                            playHandcard(card, mc.getMouseMoveCoords(mc.area(MinionBoard[target[1].get_pos()])))
                    except Exception, e:
                        print 'choosingOption with 3 args' ,e   
                else:       
                    #randomPos = np.random.random_integers(0,1)
                    playHandcard(getCardByIngameId(choosenOption[0]), mc.getMouseMoveCoords(mc.area(mc.getMinionBoard(1)[1])))
            else:
                targetIndex = np.random.random_integers(1, len(choosenOption[2])) - 1
                target = findTarget(choosenOption[2][targetIndex])
                while target[0] == 0:
                    targetIndex = np.random.random_integers(1, len(choosenOption[2])) - 1
                    target = findTarget(choosenOption[2][targetIndex])
                drawAttack(getCardByIngameId(choosenOption[0]), target[1])      
    except Exception, e:
        print 'choosePlayingCard:', e
        
def readingMyTurn(cont):
    nxt = 0
    Power = '[Power]'
    #Zone = '[Zone]'
    for idx, line in enumerate(cont):
        if nxt != 0:
            nxt -= 1
            continue
        if '[Power]' in line or '[Zone]' in line:
            try:
                if Power in line and 'm_currentTaskList' in line:
                    continue
                elif Power in line and'FINAL_GAMEOVER' in line:
                    print 'Game End'
                    setCurState('GAME_OVER')
                    return
                elif Power in line and'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState('ENEMY_TURN')
                    setVariablesDefault()
                    print 'Turn Change'
                    completeReading(cont[(idx+1):], getCurState())
                    return
                elif Power in line and 'TAG_CHANGE' in line and 'RESOURCES' in line:
                    setMyMana(int(split(line, 'value=', '\n')))
                elif Power in line and 'SHOW_ENTITY' in line:
                    addHandcardAtPosition(split(line, 'CardID=', '\n'), (getHandcardCount() + 1), int(split(line, 'id=', ' ')))
                elif Power in line and 'option' in line:
                    i = idx
                    jump = 0
                    while i <len(cont):
                        if 'm_currentTaskList' in cont[i]:
                            showOptions(cont[idx:(i-1)])
                            jump = i - idx
                            break
                        i += 1
                        if i == len(cont):
                            showOptions(cont[idx:])
                            jump = (i - 1) - idx
                            break
                    print 'Waiting for PlayingOptions'
                    nxt = jump
                    setOptionsCalc(True)
                elif isOptionCalc() and 'ZoneChangeList.FireCompleteCallback' in line:
                    time.sleep(10)
                    choosePlayingCard()
                    clearOptions()
                    setOptionsCalc(False)
                elif Power in line and '- ACTION_START' in line and 'SubType=PLAY' in line:
                    i = idx
                    jump = 0
                    while i < (len(cont) - 1):
                        i += 1
                        if '- ACTION_END' in cont[i]:
                            setFound(True)
#                            cardPlayed(cont[idx:(i+1)])
                            jump = i - idx
                            break
                    if isFound():
                        setFound(False)
                        nxt=jump
                    else:
                        setTmp(cont[idx:])
                        setWaiting(True)
                        nxt = i - idx
                        print 'Action end Not found'
                    if not isComboActive():
                        setCombo(True)
                elif isWaiting():
                    i = 0
                    while i < len(cont):
                        if '- ACTION_END' in cont[i]:
                            setFound(True)
                            setWaiting(False)
#                            cardPlayed(getTmp()+cont[:(i+1)])
                            nxt = i
                            break
                        i += 1
                    if isFound():
                        setFound(False) 
                    else:
                        nxt = len(cont) - 1
                        setTmp(getTmp() + cont)     
                elif Power in line and '- ACTION_START' in line and 'SubType=ATTACK' in line:
                    attack(line)
                    i = idx
                    jump = 0
                    while i < len(cont):
                        i += 1
                        if '- ACTION_END' in cont[i]:
                            jump = i - idx
                            break
                    nxt = jump  
            except Exception, e:
                print 'MY TURN:', line, e
            
def readingEnemyTurn(cont):
    nxt = 0
    for idx, line in enumerate(cont):
        if nxt != 0:
            nxt -= 1
            continue
        if '[Power]' in line:
            try:
                if 'm_currentTaskList' in line:
                    continue
                elif 'FINAL_GAMEOVER' in line:
                    print 'Game End'
                    setCurState('GAME_OVER')
                    return
                elif 'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState('MY_TURN')
                    setVariablesDefault()
                    print 'Turn Change'
                    completeReading(cont[(idx+1):], getCurState())
                    return
                elif '- ACTION_START' in line and 'SubType=PLAY' in line:
                    i = idx
                    #jump = 0
                    while i < (len(cont) - 1):
                        i += 1
                        if '- ACTION_END' in cont[i]:
                            setFound(True)
                            EnemyCardPlayed(cont[idx:(i+1)])
                            #jump = i - idx
                            break
                    if isFound():
                        setFound(False)
                    else:
                        setTmp(cont[idx:])
                        setWaiting(True)
                        nxt = i - idx
                        print 'Action end Not found'
                    if not isComboActive():
                        setCombo(True)
                elif isWaiting():
                    i = 0
                    while i < len(cont):
                        if '- ACTION_END' in cont[i]:
                            setFound(True)
                            setWaiting(False)
                            EnemyCardPlayed(getTmp()+cont[:(i + 1)])
                            nxt = i
                            break
                        i += 1
                    if isFound():
                        setFound(False)
                    else:
                        nxt = len(cont) - 1
                        setTmp(getTmp() + cont)
                elif 'Entity='+getPlayerName(2) in line and 'RESOURCES' in line:
                    setEnemyMana(int(split(line, 'value=', '\n')))
            except Exception, e:
                print 'ENEMY TURN:', line, e
                
def readingMulligan(cont):
    for idx, line in enumerate(cont):
        if '[Power]' in line:
            try:
                if 'MULLIGAN_STATE' in line and 'DONE' in line:
                    setWaiting(False)
                    time.sleep(0.5)
                    if split(line, 'Entity=', ' tag') == getPlayerName(1):
                        setMyMulliganStateDone(True)
                    elif split(line, 'Entity=', ' tag') == getPlayerName(2):
                        setEnemyMulliganStateDone(True)
                    if isMyMulliganStateDone() and isEnemyMulliganStateDone():
                        if getHandcardCount() == 3:
                            setCurState('MY_TURN')
                            print 'now reading My Turn'
                            completeReading(cont[idx:], getCurState())
                            return
                        else:
                            setCurState('ENEMY_TURN')
                            print 'now reading Enemy Turn'
                            completeReading(cont[idx:], getCurState())
                            return         
                elif getPlayerName(1) is not None and 'MULLIGAN_STATE' in line and 'INPUT' in line and split(line, 'Entity=', ' tag') == getPlayerName(1):
                    #print line, idx
                    print 'setMul'
                    setMulligan(True)
                    continue     
                elif getPlayerName(1) is not None and 'MULLIGAN_STATE' in line and 'DEALING' in line and split(line, 'Entity=', ' tag') == getPlayerName(1):
                    setWaiting(True)
                    continue
                elif isMulligan():
                    time.sleep(17)
                    MulliganChoosing()
                    setMulligan(False)
                    time.sleep(2)
                    MulliganConfirm()
                elif isWaiting() and 'SHOW_ENTITY' in line:
                    setTmp((split(line, 'CardID=', '\n'), int(split(line, 'id=', ' '))))
                    setFound(True)    
                elif isFound() and isWaiting() and 'HIDE_ENTITY' in line:
                    setFound(False)
                    idx = int(split(line, 'id=', ' '))
                    cardInfo = getTmp()
                    removeCardByIngameId(idx)
                    # put removed Card back to DECK
                    pos = int(split(line, 'zonePos=', ' '))
                    addHandcardAtPosition(cardInfo[0], pos, cardInfo[1])
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
                 
def readGameStartPowerLines(cont):
    for idx, line in enumerate(cont):
        if '[Power]' in line:
            try:
                if 'GameEntity tag=NEXT_STEP value=BEGIN_MULLIGAN' in line:
                    setCurState('MULLIGAN')
                    setVariablesDefault()
                    completeReading(cont[idx:], getCurState())
                    return
                elif 'CardID=HERO_' in line:
                    setFound(True)
                    setWaiting(True)
                    setTmp((split(line, 'CardID=', '\n'), int(split(line, 'ID=', ' '))))
                elif isFound() and 'tag=CONTROLLER' in line:
                    setFound(False)
                    setPlayerID(int(split(line, 'value=', '\n')))
                    heroInfo = getTmp()
                    if getPlayerID() == 1:     
                        setMyHero(heroInfo[0], heroInfo[1])
                    else:
                        setEnemyHero(heroInfo[0], heroInfo[1])
                elif isWaiting() and not isFound() and 'CardID=' in line:
                    setWaiting(False)
                    if getPlayerID() == 1:
                        setMyHeroPower(split(line, 'CardID=', '\n'), int(split(line, 'ID=', ' ')))
                    else:
                        setEnemyHeroPower(split(line, 'CardID=', '\n'), int(split(line, 'ID=', ' ')))
                elif not isWaiting() and 'CardID=' in line and not 'HERO' in line:
                    cardId = split(line, 'CardID=')  
                    if '\n' == cardId:
                        continue
                    else:
                        idx = int(split(line, 'ID=', ' '))
                        setWaiting(True)
                        setTmp((cardId.split('\n')[0], idx))
                elif isWaiting() and 'ZONE_POSITION' in line:
                    setWaiting(False)
                    cardInfo = getTmp()
                    # buglogger(line, getTmp())
                    addHandcardAtPosition(cardInfo[0], int(split(line, 'value=', '\n')), cardInfo[1])
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
                
def completeReading(cont, state):
    if state == getCurState():
        if getCurState() == getGameState(0):
            readGameStartPowerLines(cont)
        elif getCurState() == getGameState(1):
            readingMulligan(cont)
        elif getCurState() == getGameState(2):
            readingMyTurn(cont)
        elif getCurState() == getGameState(3):
            readingEnemyTurn(cont)
        elif getCurState() == getGameState(4):
            setCurState(None)
            return
    else:
        print 'no Correct State'


def Statedecision():
    log = readLog()
    nol = len(log)
    while True:
        time.sleep(0.04)
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
    
def Main():
    Statedecision()
    
Main()

#-----TESTREADER-----#
def splitter():
    fi = readLog()
    power = open(path('doc')+'/powerZone.txt', 'w')
    for l in fi:
        if '[Power]' in l or '[Zone]' in l:
            power.write(l)

#splitter()



