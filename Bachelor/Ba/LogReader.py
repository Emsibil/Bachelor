import time
import treelib as t
from types import IntType 
from random import random
from cardLibReader import CardById, Abilities
from MouseControl import * 
from Util import *


#path = 'C:/Program Files (x86)'  #Uni
#path = 'D:/Programme' #Home

def openLogFile():
    #return open('C:/Program Files (x86)/Hearthstone/Hearthstone_Data/output_log.txt' , 'r')
    return open('D:/Programme/Hearthstone/Hearthstone_Data/output_log.txt' , 'r')

def readLog():
    return openLogFile().readlines()

def attack(line):
    try:
        attackerInfo, targetInfo= line.split('ATTACK')
        a_idx = gameId(attackerInfo)
        t_idx = gameId(targetInfo)
        a_minion = getEnemyCardByIngameID(a_idx) 
        t_minion = getCardByIngameId(t_idx)
        t_minion.takes_Damage(a_minion._attack)
        a_minion.takes_Damage(t_minion._attack)
    except Exception, e:
        print 'attack', e 

def simulateCards():
    cards = getCards().copy()
    e_cards = getEnemyCards().copy()
    
def followingOptions(optionTree, mana, parentID):
    cards = getCards()
    thisID = parentID + 1
    for c in cards:
        if cards[c]._zone == Zone.HAND and cards[c]._manacosts <= mana:
            #analyze Card
            optionTree.create_node((c, Option.PLAY), thisID, parent=parentID)
            optionTree, thisID = followingOptions(optionTree, mana - cards[c]._manacosts, thisID)
        elif cards[c]._zone == Zone.PLAY:
            optionTree.create_node((c, Option.ATTACK), parent=parentID)
            optionTree, thisID = followingOptions(optionTree, mana, thisID)
    return (optionTree, thisID)                    

def optionTree(options):
    oTree = t.Tree()
    nodeID = 1
    parentNodeID = 0
    oTree.create_node(None, nodeID)
    for opt in options:
        oTree.create_node(opt, nodeID, parent=parentNodeID)
        if opt[1] == Option.PLAY:
            oTree, nodeID = followingOptions(oTree, getMyMana() - getCardByIngameId(opt[0])._manacosts, nodeID)
        else:
            oTree, nodeID = followingOptions(oTree, getMyMana())
    #finished Tree

def cardPlayed(playingLines):
    card = None
    for line in playingLines:
        if 'SubType=PLAY' in line:
            idx = gameId(line)
            card = getCardByIngameId(idx)
            print card._manacosts
            setMyMana(getMyMana() - card._manacosts)
        elif card is not None:
            if card._cardtype == Cardtype.MINION:
                if 'tag=ZONE value=PLAY' in line:
                    setWaiting(True)
                elif isWaiting() and 'ZONE_POSITION' in line:
                    addMyMinonToField(card, int(split(line, 'value=', '\n')))
                    setWaiting(False)
                    print 'Played', card._name
                    break
            elif card._cardtype == Cardtype.SPELL:
                print 'Played', card._name
                break
            elif card._cardtype == Cardtype.WEAPON:
                print 'Played', card._name
                break                       
            elif card._cardtype == Cardtype.SECRET:
                print 'Played', card._name
                break
            elif card._cardtype == Cardtype.HERO_POWER:
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
                    addOption((Option.END, None))
                elif 'POWER' in optionLines[i] and 'zone=HAND' in optionLines[i]:
                    output += 'Play ' +str(split(optionLines[i], 'name=', ' id'))
                    parameter1 = gameId(optionLines[i])
                    parameter2 = Option.PLAY
                elif 'POWER' in optionLines[i] and 'zone=DECK' in optionLines[i]:
                    output += 'Play ' + getCardByIngameId(gameId(optionLines[i]))._name
                elif 'POWER' in optionLines[i] and 'zone=PLAY' in optionLines[i] and 'zonePos=0' in optionLines[i]:
                    parameter1 = gameId(optionLines[i])
                    if 'cardId=HERO' in optionLines[i]:
                        output += 'Hero Attack'
                        parameter2 = Option.ATTACK
                    else:
                        output += 'Play Hero Power'
                        parameter2 = Option.PLAY
                elif 'POWER' in optionLines[i] and 'zone=PLAY' in optionLines[i] and 'zonePos=0' not in optionLines[i]:
                    output += 'Attack with ' +str(split(optionLines[i], 'name=', ' id'))
                    parameter1 = gameId(optionLines[i])
                    parameter2 = Option.ATTACK
                if i+4 < len(optionLines):
                    if 'target' in optionLines[i+4]:
                        output += '\n \t Possible Targets: '
                print output
            if 'target' in optionLines[i]:
                name = ''
                idx = gameId(optionLines[i])
                if 'name' in optionLines[i]:
                    name = str(split(optionLines[i], 'name=', 'id'))
                else:
                    name = getEnemyCardByIngameID(idx)._name
                print '\t \t' + name
                if type(id) is IntType:
                    targets.append(idx)
                else:
                    targets.append(gameId(optionLines[i]))
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
            card = createCard(split(line, 'CardID=', '\n'))
            card._ingameID = gameId(line)
        if card is not None and 'ZONE_POSITION' in line:
            if card._cardtype == Cardtype.MINION:
                print 'Played', card._name
                addEnemyMinonToField(card, int(split(line, 'value=', '\n')))
                card = None
                break
            elif card._cardtype == Cardtype.SPELL:
                print 'Played', card._name
                card = None
                break
            elif card._cardtype == Cardtype.WEAPON:
                print 'Played', card._name
                card = None
                break                       
            elif card._cardtype == Cardtype.SECRET:
                print 'Played', card._name
                card = None
                break
        elif card is not None and '- ACTION_END' in line:
            if card._cardtype == Cardtype.MINION:
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
            mouseMove(getMouseMoveCoords(area(getMulliganCardArea(pos, (count)))))
        else:
            mouseMove(getMouseMoveCoords(area(getMulliganCardArea(pos, (count - 1)))))
        time.sleep(random()*1+0.5)
        mouseClick()
        time.sleep(random()*1+0.5)

def MulliganConfirm():
    mouseMove(getMouseMoveCoords(area(getMulliganConfirm())))
    time.sleep(2)
    mouseClick()

def findTarget(idx):
    try:
        cards = getCards()
        for c in cards:
            if cards[c]._zone == Zone.PLAY and cards[c]._ingameID == idx: 
                return (0, cards[c])      
        cards = getEnemyCards()
        for c in cards:
            if cards[c]._zone == Zone.PLAY and cards[c]._ingameID == idx: 
                return (1, cards[c])     
    except:
        print 'No Target Found'
    
def playHandcard(card, targetArea):
    try:
        count = getHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        time.sleep(1)
        mouseDown()   
        time.sleep(0.5)
        mouseMove(targetArea)
        if card._cardtype == Cardtype.MINION:
            addMyMinonToField(card, (int(getMyMinionCount()/2) + 1))
            if hasAbility(card, Ability.BATTLECRY):
                pass
        if not card._cardtype == Cardtype.HERO_POWER:
            card._zone = Zone.PLAY
            reorderHandCards(card._zonePos)
        time.sleep(2)
        mouseUp()
    except Exception, e:
        print 'playHandcards()', e
    
def drawAttack(ownMinion ,target):
    try:
        mouseMove(getMouseMoveCoords(getOnBoardArea(getMyMinionCount(), ownMinion)))
        time.sleep(1)
        mouseDown()
        time.sleep(0.5)
        mouseMove(getMouseMoveCoords(getOnBoardArea(getEnemyMinionCount(), target)))
        time.sleep(1)
        mouseUp()
        ownMinion.takes_Damage(target._attack)
        target.takes_Damage(ownMinion._attack)
        if ownMinion._zone == Zone.GRAVEYARD:
                reorderMinionsOnBoard(ownMinion._zonePos)
        if target._zone == Zone.GRAVEYARD:
            reorderEnemyMinionsOnBoard(target._zonePos)
    except Exception, e:
        print 'drawAttack()', e

def playMinionWithTarget(card, playZone, targetArea):
    count = getHandcardCount()
    mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
    time.sleep(1)
    mouseDown()   
    time.sleep(0.5)
    mouseMove(getMouseMoveCoords(area(getUneven1())))
    addMyMinonToField(card, playZone)
    time.sleep(1)
    mouseUp()
    time.sleep(0.5)
    mouseMove(targetArea)
    time.sleep(1)
    mouseDown()
    time.sleep(0.5)
    mouseUp()
        
def EndTurn():
    mouseMove(getMouseMoveCoords(area(getTurn())))    
    time.sleep(1)
    mouseDown()
    print "down"
    time.sleep(0.5)
    mouseUp()
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
        
        if choosenOption[0] == Option.End:
            EndTurn()
        else:
            if choosenOption[1] == Option.PLAY:
                if len(choosenOption) == 3:
                    targetIndex = np.random.random_integers(1, len(choosenOption[2])) - 1
                    target = findTarget(choosenOption[2][targetIndex])
                    if target[0] == 0:
                        MinionBoard = getMinionBoard(getMyMinionCount())
                    else:
                        MinionBoard = getEnemyMinionBoard(getEnemyMinionCount())
                    card = getCardByIngameId(choosenOption[0])
                    try:
                        if card._cardtype == Cardtype.MINION:
                            playMinionWithTarget(card, 1, getMouseMoveCoords(area(MinionBoard[target[1].get_pos()])))
                        else:
                            playHandcard(card, getMouseMoveCoords(area(MinionBoard[target[1].get_pos()])))
                    except Exception, e:
                        print 'choosingOption with 3 args' ,e   
                else:       
                    #randomPos = np.random.random_integers(0,1)
                    playHandcard(getCardByIngameId(choosenOption[0]), getMouseMoveCoords(area(getMinionBoard(1)[1])))
            else:
                targetIndex = np.random.random_integers(1, len(choosenOption[2])) - 1
                target = findTarget(choosenOption[2][targetIndex])
                while target[0] == 0:
                    targetIndex = np.random.random_integers(1, len(choosenOption[2])) - 1
                    target = findTarget(choosenOption[2][targetIndex])
                drawAttack(getCardByIngameId(choosenOption[0]), target[1])      
    except Exception, e:
        print 'choosePlayingCard:', e

def readTrigger(lines):
    for l in lines:
        if 'SubType=TRIGGER' in l:
            if getCardByIngameId(gameId(l))._zone == Zone.GRAVEYARD:
                Full_Entity(lines)

def readDeaths(lines):
    for l in lines:
        if 'GRAVEYARD' in l:
            if is_Me(controllerID(l)):
                card = getCardByIngameId(gameId(l))
                card._zoone = Zone.GRAVEYARD
                reorderMinionsOnBoard(card.get_pos())
            else:
                card = getEnemyCardByIngameID(gameId(l))
                card._zoone = Zone.GRAVEYARD
                reorderEnemyMinionsOnBoard(card.get_pos())
                
            
def readingFULL_ENTITY(lines):
    card = None
    isMyCard = False
    for l in lines:
        if 'CREATOR' in l: 
            if card._type == Cardtype.ENCHANTMENT:
                return Cardtype.ENCHANTMENT
        elif 'FULL_ENTITY' in l and not 'CardID=\n' in l:
            idx = split(l, 'ID=', ' ')
            cardID = split(l, 'CardID=', '\n')
            card = createCard(cardID)
            card._ingameID = idx
        elif 'tag=ZONE' in l:
            zone = split(l, 'value=', '\n')
            card._zone = zone
        elif 'tag=CONTROLLER' in l:
                isMyCard = is_Me(int(split(l, 'value=', '\n')))
        elif 'tage=ZONE_POSITION' in l:
            card.set_pos(int(split(l, 'value=', '\n')))
        elif 'SHOW_ENTITY' in l:
            ingameID = int(split(l, 'ID=', ' '))
            cardID = split(l, 'CardID=', '\n')
            card = createCard(cardID)
            card._ingameID = ingameID
            card._zone = Zone.SETASIDE
    if isMyCard and card._zone == Zone.PLAY:
        addMyMinonToField(card, card.get_pos())
    elif not isMyCard and card._zone == Zone.PLAY:
        addEnemyMinonToField(card, card.get_pos())
    elif isMyCard and card._zone == Zone.HAND:
        addHandcardAtPosition(card._id, card.get_pos, card._ingameID)
    elif not isMyCard and card._zone == Zone.HAND:
        pass

def tagging(Id, tag, value):
    card = getCardByIngameId(Id)
    if tag == 'HEALTH':
        card._health = value
    elif tag == 'ATK':
        card._attack = value
    elif tag == 'TAUNT':
        editAbility(card, Ability.TAUNT, value)
    elif tag == 'DIVINE_SHIELD':
        editAbility(card, Ability.DIVINESHIELD, value)    
    elif tag == 'WINDFURY':
        editAbility(card, Ability.WINDFURY, value)
    elif tag == 'STEALTH':
        editAbility(card, Ability.STEALTH, value)
    elif tag == 'CHARGE':
        editAbility(card, Ability.CHARGE, value)    

def Full_Entity(lines):
    i = 0
    start = None
    end = None
    enchanted = []
    while i < len(lines):
        if 'FULL_ENTITY' in lines[i]:
            start = i
        elif 'CREATOR' in lines[i] and start is not None:
            end = i
            type = readingFULL_ENTITY(lines[start:end])
            start = None
            end = None
            if type == Cardtype.ENCHANTMENT and 'ATTACHED' in lines[i+1]:
                enchanted.append(int(split(lines[i+1], 'value=', '\n')))
        if len(enchanted) > 0 and 'id=' in lines[i] and 'cardId=' in lines[i]:
            idx = gameId(lines[i])
            if id in enchanted:
                tag = split(lines[i], 'tag=', ' ')
                value = int(split(lines[i], 'value=', '\n'))  
                tagging(idx, tag, value)
                
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
                    setCurState(GameState.GAME_END)
                    return
                elif Power in line and'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState(GameState.ENEMY_TURN)
                    setVariablesDefault()
                    print 'Turn Change'
                    completeReading(cont[(idx+1):], getCurState())
                    return
                elif Power in line and 'TAG_CHANGE' in line and 'RESOURCES' in line:
                    setMyMana(int(split(line, 'value=', '\n')))
                elif Power in line and 'SHOW_ENTITY' in line:
                    addHandcardAtPosition(split(line, 'CardID=', '\n'), (getHandcardCount() + 1), gameId(line))
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
                            Full_Entity(cont[idx:(i+1)])
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
                            Full_Entity(getTmp()+cont[:(i+1)])
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
                    setCurState(GameState.GAME_END)
                    return
                elif 'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState(GameState.MY_TURN)
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
                elif '_ACTION_START' in line and 'SubType=TRIGGER' in line:
                    i = idx
                    while i < len(cont) - 1:
                        if '- ACTION_END' in cont[i]:
                            readTrigger(cont[idx:(i+1)])
                            break
                elif '_ACTION_START' in line and 'SubType=DEATHS' in line:
                    i = idx
                    while i < len(cont) - 1:
                        if '- ACTION_END' in cont[i]:
                            readDeaths(cont[idx:(i+1)])
                            break
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
                            setCurState(GameState.MY_TURN)
                            print 'now reading My Turn'
                            completeReading(cont[idx:], getCurState())
                            return
                        else:
                            setCurState(GameState.ENEMY_TURN)
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
                    setTmp((split(line, 'CardID=', '\n'), gameId(line)))
                    setFound(True)    
                elif isFound() and isWaiting() and 'HIDE_ENTITY' in line:
                    setFound(False)
                    idx = gameId(line)
                    cardInfo = getTmp()
                    removeCardByIngameId(idx)
                    # put removed Card back to DECK
                    pos = int(split(line, 'zonePos=', ' '))
                    addHandcardAtPosition(cardInfo[0], pos, cardInfo[1])
                elif 'TAG_CHANGE' in line and 'CONTROLLER' in line and 'Entity=' in line:
                    Entity = split(line, 'Entity=', ' tag=')
                    if Entity == get_Me():
                        setPlayerName(int(split(line, 'value=', '\n')), get_Me())
                    else:
                        setPlayerName(int(split(line, 'value=', '\n')), Entity)
                    continue
            except Exception, e:
                print 'MULLIGAN:', line, e 
                 
def readGameStartPowerLines(cont):
    for idx, line in enumerate(cont):
        if '[Power]' in line:
            try:
                if 'GameEntity tag=NEXT_STEP value=BEGIN_MULLIGAN' in line:
                    setCurState(GameState.MULLIGAN)
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
                    if is_Me(getPlayerID()):     
                        setMyHero(heroInfo[0], heroInfo[1])
                    else:
                        setEnemyHero(heroInfo[0], heroInfo[1])
                elif isWaiting() and not isFound() and 'CardID=' in line:
                    setWaiting(False)
                    if is_Me(getPlayerID()):
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
                elif 'TAG_CHANGE' in line and 'CONTROLLER' in line and 'Entity=' in line:
                    Entity = split(line, 'Entity=', ' tag=')
                    if Entity == get_Me():
                        setPlayerName(int(split(line, 'value=', '\n')), get_Me())
                    else:
                        setPlayerName(int(split(line, 'value=', '\n')), Entity)
                    continue
            except Exception, e:
                print 'GAME START', line, e   
                
def completeReading(cont, state):
    if state == getCurState():
        if getCurState() == GameState.GAME_START:
            readGameStartPowerLines(cont)
        elif getCurState() == GameState.MULLIGAN:
            readingMulligan(cont)
        elif getCurState() == GameState.MY_TURN:
            readingMyTurn(cont)
        elif getCurState() == GameState.ENEMY_TURN:
            readingEnemyTurn(cont)
        elif getCurState() == GameState.GAME_END:
            setCurState(GameState.SEARCHING)
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
            if 'CREATE_GAME' in new_lines[i] and getCurState() == GameState.SEARCHING:
                print 'GameStart'
                setCurState(GameState.GAME_START)
                completeReading(new_lines[i:], GameState.GAME_START)
                break
            elif not getCurState() == GameState.SEARCHING: 
                completeReading(new_lines[i:], getCurState())
                break
            i += 1   
        log = new_log
        nol = new_nol
    
def Main():
    Statedecision()
    
#Main()

#-----TESTREADER-----#
def splitter():
    fi = readLog()
    power = open(path('doc')+'/power4.txt', 'w')
    for l in fi:
        if '[Power]' in l or '[Zone]' in l:
            power.write(l)


splitter()



