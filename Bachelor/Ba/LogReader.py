import os
import time
import numpy as np
import cardLibReader as cReader
import Card
import MouseControl as mc

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

def createCard(card):
    cardtype = cReader.cardType(card)
    _card = Card.Card(cReader.id(card), cReader.name(card), cardtype, cReader.manaCost(card))
    if cardtype == 'Minion':
        _card._attack = cReader.attackValue(card)
        _card._health = cReader.healthValue(card)
    if cardtype == 'Hero':
        _card._health = cReader.healthValue(card)
    return _card 
   
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
def addHandcardAtPosition(cardId, pos, ingameID):
    global MY_HANDCARDS
    card = createCard(cReader.CardById(cardId))
    card._ingameID = ingameID
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
            return (count - 1)
        else:
            count += 1
    return (count - 1)

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

def createOption(*args):
    if len(args) == 0: #if no argument: EndTurn
        return 0
    elif len(args) == 2: #if 1 Argument: PLAY (with no Effects) -> (1, zonePos)
        return (1, args[0]) 
    else: #if more Arguments: PLAY with Effects -> (2, zonePos, targets[]) or ATTACK -> (3, zonePos, targets[])
        option = []
        if args[1] == 'PLAY':
            option.append(2)
        elif args[1] == 'ATTACK':
            option.append(3)
        for idx, arg in enumerate(args):
            if idx == 1:
                continue
            option.append(arg)
        return np.ndarray(option)    
    
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
            
def cardPlayed(playingLines):
    card = None
    for line in playingLines:
        if 'SubType=PLAY' in line:
            zone = int(split(line, 'zonePos=', ' cardId'))
            if zone == 0:
                card = getHandcard(zone, 0)
            else:
                card = getHandcard(zone, 1)
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
    paramter1 = None
    paramter2 = None
    targets = []
    try:
        while i < len(optionLines):
            if 'option' in optionLines[i]:
                output = str(split(optionLines[i], '() -   ', ' type')) + ': '
                createOption(paramter1, paramter2, targets)
                paramter1 = None
                paramter2 = None
                if 'END_TURN' in optionLines[i]:
                    output += 'End Turn'
                    createOption()
                elif 'POWER' in optionLines[i] and 'zone=HAND' in optionLines[i]:
                    output += 'Play ' +str(split(optionLines[i], 'name=', ' id'))
                    paramters1 = int(split(optionLines[i], 'id=', ' zone'))
                    paramters2 = 'PLAY'
    #            elif 'POWER' in optionLines[i] and 'zone=DECK' in optionLines[i]:
     #               output += 'Play' + str(getHandcard(,0))
                elif 'POWER' in optionLines[i] and 'zone=PLAY' in optionLines[i] and 'zonePos=0' in optionLines[i]:
                    output += 'Play Hero Power'
                elif 'POWER' in optionLines[i] and 'zone=PLAY' in optionLines[i] and 'zonePos=0' not in optionLines[i]:
                    output += 'Attack with ' +str(split(optionLines[i], 'name=', ' id'))
                    paramter1 = int(split(optionLines[i], 'id=', ' zone'))
                    paramter2 = 'ATTACK'
                if i+4 < len(optionLines):
                    if 'target' in optionLines[i+4]:
                        output += '\n \t Possible Targets: '
                print output
            if 'target' in optionLines[i]:
                print '\t \t' + str(split(optionLines[i], 'name=', 'id'))
                targets.append(int(split(optionLines[i], 'id=', ' zone')))
            i += 1
    except Exception, e:
        print optionLines[i], e
                                  
def EnemyCardPlayed(playingLines):
    card = None
    for line in playingLines:
        if 'SubType=PLAY' in line and 'name' in line:
            print 'Played Hero Power'
            break
        elif 'SHOW_ENTITY' in line:
            card = createCard(cReader.CardById(split(line, 'CardID=', '\n')))
        if card is not None and 'ZONE_POSITION' in line:
            if card._cardtype == 'Minion':
                print 'Played', card._name
                addEnemyMinonToField(card, int(split(line, 'value=', '\n')))
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
               
def MulliganChoosing():
    handcards = getHandcards()
    count = getHandcardCount()
    change = []
    for idx, card in enumerate(handcards):
        if idx == 0:
            continue
        elif idx > (count - 1):
            break
        else:
            if card._manacosts >= 4:
                change.append(idx)
    for pos in change:  
        if count == 3: 
            mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getMulliganCardArea(pos, (count)))))
        else:
            mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getMulliganCardArea(pos, (count - 1)))))
        time.sleep(2)
        mc.mouseClick()
        time.sleep(3)

def MulliganConfirm():
    mc.mouseMove(mc.getMouseMoveCoords(mc.area(mc.getMulliganConfirm())))
    time.sleep(2)
    mc.mouseClick()
    
def playHandcard(pos):
    count = getHandcardCount()
    mc.mouseMove(mc.getMouseMoveCoords(mc.getHandcardArea(count, pos)))
    time.sleep(1)
    mc.mouseDown()   
    time.sleep(0.5)
    mc.mouseMove((100,100))
    time.sleep(30)
    
def choosePlayingCard():
    handcards = getHandcards()
    mana = getMyMana()
    opportunities = []
    for idx, card in enumerate(handcards):
        if idx == 0:
            continue
        elif card is None:
            break
        else:
            if card._manacosts <= mana:
                opportunities.append(card)
    playHandcard(opportunities[np.random.random_integers(0, len(opportunities) - 1)]._zonePos)
            
        
def readingMyTurn(input):
    nxt = 0
    for idx, line in enumerate(input):
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
                    setCurState('ENEMY_TURN')
                    setVariablesDefault()
                    print 'Turn Change'
                    completeReading(input[(idx+1):], getCurState())
                    return
                elif 'TAG_CHANGE' in line and 'RESOURCES' in line:
                    setMyMana(int(split(line, 'value=', '\n')))
                elif 'SHOW_ENTITY' in line:
                    addHandcardAtPosition(split(line, 'CardID=', '\n'), (getHandcardCount() + 1), int(split(line, 'id=', ' cardId')))
                elif 'option' in line:
                    i = idx
                    jump = 0
                    print 'len input:',len(input)
                    while i <len(input):
                        if 'm_currentTaskList' in input[i]:
                            showOptions(input[idx:(i-1)])
                            jump = i - idx
                            break
                        i += 1
                        if i == len(input):
                            showOptions(input[idx:])
                            jump = (i - 1) - idx
                            break
                    print '30'
                    time.sleep(30)
                    choosePlayingCard()
                    time.sleep(5)
                    nxt = jump
                elif '- ACTION_START' in line and 'SubType=PLAY' in line:
                    i = idx
                    jump = 0
                    while i < (len(input) - 1):
                        i += 1
                        if '- ACTION_END' in input[i]:
                            setFound(True)
                            cardPlayed(input[idx:(i+1)])
                            jump = i - idx
                            break
                    if isFound():
                        setFound(False)
                        nxt=jump
                    else:
                        setTmp(input[idx:])
                        setWaiting(True)
                        nxt = i - idx
                        print 'Action end Not found'
                    if not isComboActive():
                        setCombo(True)
                elif isWaiting():
                    i = 0
                    while i < len(input):
                        if '- ACTION_END' in input[i]:
                            setFound(True)
                            setWaiting(False)
                            cardPlayed(getTmp()+input[:(i+1)])
                            nxt = i
                            break
                        i += 1
                    if isFound():
                        setFound(False) 
                    else:
                        nxt = len(input) - 1
                        setTmp(getTmp() + input)     
                elif '- ACTION_START' in line and 'SubType=ATTACK' in line:
                    attack(line, 'ME')
                    i = idx
                    jump = 0
                    while i < len(input):
                        i += 1
                        if '- ACTION_END' in input[i]:
                            jump = i - idx
                            break
                    nxt = jump  
            except Exception, e:
                print 'MY TURN:', line, e
            
def readingEnemyTurn(input):
    nxt = 0
    for idx, line in enumerate(input):
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
                    completeReading(input[(idx+1):], getCurState())
                    return
                elif '- ACTION_START' in line and 'SubType=PLAY' in line:
                    i = idx
                    jump = 0
                    while i < (len(input) - 1):
                        i += 1
                        if '- ACTION_END' in input[i]:
                            setFound(True)
                            EnemyCardPlayed(input[idx:(i+1)])
                            jump = i - idx
                            break
                    if isFound():
                        setFound(False)
                    else:
                        setTmp(input[idx:])
                        setWaiting(True)
                        nxt = i - idx
                        print 'Action end Not found'
                    if not isComboActive():
                        setCombo(True)
                elif isWaiting():
                    i = 0
                    while i < len(input):
                        if '- ACTION_END' in input[i]:
                            setFound(True)
                            setWaiting(False)
                            EnemyCardPlayed(getTmp()+input[:(i + 1)])
                            nxt = i
                            break
                        i += 1
                    if isFound():
                        setFound(False)
                    else:
                        nxt = len(input) - 1
                        setTmp(getTmp() + input)
                elif 'Entity='+getPlayerName(2) in line and 'RESOURCES' in line:
                    setEnemyMana(int(split(line, 'value=', '\n')))
            except Exception, e:
                print 'ENEMY TURN:', line, e
                
def readingMulligan(input):
    for idx, line in enumerate(input):
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
                            completeReading(input[idx:], getCurState())
                            return
                        else:
                            setCurState('ENEMY_TURN')
                            print 'now reading Enemy Turn'
                            completeReading(input[idx:], getCurState())
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
                    setTmp((split(line, 'CardID=', '\n'), int(split(line, 'id=', ' cardId'))))
                    setFound(True)    
                elif isFound() and isWaiting() and 'HIDE_ENTITY' in line:
                    setFound(False)
                    pos = int(split(line, 'zonePos=', ' '))
                    cardInfo = getTmp()
                    removeHandcardFromPosition(pos)
                    # put removed Card back to DECK
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
                 
def readGameStartPowerLines(input):
    for idx, line in enumerate(input):
        if '[Power]' in line:
            try:
                if 'GameEntity tag=NEXT_STEP value=BEGIN_MULLIGAN' in line:
                    setCurState('MULLIGAN')
                    setVariablesDefault()
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
                    id = int(split(line, 'ID=', ' CardID='))
                    if '\n' == cardId:
                        continue
                    else:
                        setWaiting(True)
                        setTmp((cardId.split('\n')[0], id))
                elif isWaiting() and 'ZONE_POSITION' in line:
                    setWaiting(False)
                    cardInfo = getTmp()
                    # buglogger(line, getTmp())
                    addHandcardAtPosition(cardInfo[0], int(split(line, 'value=', '\n'), cardInfo[1]))
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
    file = open(path('doc/output_log2.txt'), 'r')
    power = open(path('doc')+'/power2.txt', 'w')
    for l in file:
        if '[Power]' in l:
            power.write(l)

#splitter()



