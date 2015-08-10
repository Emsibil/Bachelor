import time
from Util_new import Tag, Option, SubType, setTmp, getTmp, setFound, isFound, isComboActive, setCombo, split, getPlayerID, gameId, setCurState, GameState, setWaiting, setMulligan
from Board import *
from Cards_new import *
from Bachelor.Ba.Util_new import getCurState, Player, EffectTime, Cardtype
from types import IntType
from Play import *



def setMyHero(Id, CardId):
    global MY_HERO
    MY_HERO = createCard(Id, CardId)
    addMinionToMyCards(MY_HERO, 0)
def setMyHeroPower(Id, CardId):
    global MY_HERO_POWER
    MY_HERO_POWER = createCard(Id, CardId)
    addHandcardToMyCards(MY_HERO_POWER, 0)
def setEnemyHero(Id, CardId):
    global E_HERO
    E_HERO = createCard(Id, CardId)
    addMinionToEnemyCards(E_HERO, 0)
def setEnemyHeroPower(Id, CardId):
    global E_HERO_POWER
    E_HERO_POWER = createCard(Id, CardId)
    addHandcardToEnemyCards(E_HERO_POWER, 0)
def setHeroPower(playerId, Id, CardId):
    if isMe(getPlayerID()):
        setMyHeroPower(Id, CardId)
    else:
        setEnemyHeroPower(Id, CardId)
def setHero(playerId, Id, CardId):
    if isMe(getPlayerID()):     
        setMyHero(Id, CardId)
    else:
        setEnemyHero(Id, CardId)
def setPlayerName(line):
    players = getPlayers()
    Entity = split(line, 'Entity=', ' tag=')
    if Entity == getMe():
        players[int(split(line, 'value=', '\n'))] = getMe()
    else:
        players[int(split(line, 'value=', '\n'))] = Entity
def setMyMana(count):
    global MY_MANA
    MY_MANA = count
def setEnemyMana(count):
    global E_MANA
    E_MANA = count
def getEnemyPlayerName():
    if isMe(1):
        return getPlayers()[2]
    else:
        return getPlayers()[1]
    
def addMulliganCards(cardInfo, pos):
    addHandcardToMyCards(createCard(cardInfo[1], cardInfo[0]), pos)
def changingMulliganCard(cardInfo, line):
    Id = gameId(line)
    removeMyCardByIngameId(Id)
    addHandcardToMyCards(createCard(cardInfo[1], cardInfo[0]), int(split(line, 'zonePos=', ' ')))

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
def changingToTurns(line):
    time.sleep(0.5)
    if split(line, 'Entity=', ' tag') == getMe():
        setMyMulliganStateDone(True)
    else:
        setEnemyMulliganStateDone(True)
    if isMyMulliganStateDone() and isEnemyMulliganStateDone():
        if getMyHandcardCount() == 3:
            setCurState(GameState.MY_TURN)
            print 'now reading My Turn'
    else:
        setCurState(GameState.ENEMY_TURN)
        print 'now reading Enemy Turn'

def MulliganStates(line, state):
    if not len(getPlayers()) == 2 and split(line, 'Entity=', ' tag') == getMe():
        if state == 'INPUT':
            setMulligan(True)
            print 'setMul'
        elif state == 'DEALING':
            setWaiting(True)

def MulliganCardsChanging(): 
    time.sleep(17)
    MulliganChoosing()
    setMulligan(False)
    time.sleep(2)
    MulliganConfirm()  
            
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
                addMinionToEnemyCards(card, int(split(line, 'value=', '\n')))
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
                addMinionToEnemyCards(card, 1)
                print 'Played', card._name
            else:
                print 'Player', card._name

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
                isMyCard = isMe(int(split(l, 'value=', '\n')))
        elif 'tage=ZONE_POSITION' in l:
            card.set_pos(int(split(l, 'value=', '\n')))
        elif 'SHOW_ENTITY' in l:
            ingameID = int(split(l, 'ID=', ' '))
            cardID = split(l, 'CardID=', '\n')
            card = createCard(cardID)
            card._ingameID = ingameID
            card._zone = Zone.SETASIDE
    if isMyCard and card._zone == Zone.PLAY:
        addMinionToMyCards(card, card.get_pos())
    elif not isMyCard and card._zone == Zone.PLAY:
        addMinionToEnemyCards(card, card.get_pos())
    elif isMyCard and card._zone == Zone.HAND:
        addHandcardToMyCards(card._id, card.get_pos, card._ingameID)
    elif not isMyCard and card._zone == Zone.HAND:
        pass
    
def tagging(card, tag, value):
    if tag == 'HEALTH':
        card._health = value
    elif tag == 'ATK':
        card._attack = value
    elif tag == 'TAUNT':
        card.editAbility(Ability.TAUNT, value)
    elif tag == 'DIVINE_SHIELD':
        card.editAbility(Ability.DIVINESHIELD, value)    
    elif tag == 'WINDFURY':
        card.editAbility(Ability.WINDFURY, value)
    elif tag == 'STEALTH':
        card.editAbility(Ability.STEALTH, value)
    elif tag == 'CHARGE':
        card.editAbility(Ability.CHARGE, value)    

def toXml(target, Id, tag, value, time):
    caster = getCardByIngameId(Id)
    if Ability.BATTLECRY in caster._ability:
        continue
    else:
        if caster._cardtype == Cardtype.SECRET:
            time = EffectTime.ON_ACTIVATE
        elif caster._cardtype == Cardtype.MINION:
            time = EffectTime.ON_BOARD
    if tag == Tag.TAUNT or tag == Tag.DIVINESHIELD or tag == Tag.WINDFURY or tag == Tag.STEALTH or tag == Tag.CHARGE:
        if value == 0:
            XML_write(Id, (Effect.DEBUFF, value, tag, time))
        else:
            XML_write(Id, (Effect.BUFF, value, tag, time))
    elif tag == Tag.HEALTH or tag == Tag.ATTACK:
        diff = 0
        if tag == Tag.HEALTH:
            diff = value - target._health
        else:
            diff = value - target._attack
        if diff > 0:
            XML_write(Id, (Effect.BUFF, diff, tag, time))
        else:    
            XML_write(Id, (Effect.DEBUFF, diff,tag ,time))

def Full_Entity(lines, time):
    i = 0
    start = None
    end = None
    enchanted = []
    while i < len(lines):
        if 'FULL_ENTITY' in lines[i]:
            start = i
        elif 'CREATOR' in lines[i] and start is not None:
            Id = split(lines[i], 'value=', '\n')
            end = i
            typ = readingFULL_ENTITY(lines[start:end])
            start = None
            end = None
            if typ == Cardtype.ENCHANTMENT and 'ATTACHED' in lines[i+1]:
                enchanted.append(int(split(lines[i+1], 'value=', '\n')))
        if len(enchanted) > 0 and 'id=' in lines[i] and 'cardId=' in lines[i]:
            idx = gameId(lines[i])
            if id in enchanted:
                tag = split(lines[i], 'tag=', ' ')
                value = int(split(lines[i], 'value=', '\n'))  
                card = getCardByIngameId(idx)
                toXml(card, Id, tag, value, time)
                tagging(card, tag, value)

def readTrigger(lines):
    for l in lines:
        if 'SubType=TRIGGER' in l:
            if getMyCardByIngameId(gameId(l))._zone == Zone.GRAVEYARD:
                Full_Entity(lines, EffectTime.ON_DEATH)

def readDeaths(lines):
    for l in lines:
        if 'GRAVEYARD' in l:
            if isMe(controllerID(l)):
                card = getMyCardByIngameId(gameId(l))
                card._zoone = Zone.GRAVEYARD
                reorderMyMinionsOnBoard(card.get_pos())
            else:
                card = getEnemyCardByIngameId(gameId(l))
                card._zone = Zone.GRAVEYARD
                reorderEnemyMinionsOnBoard(card.get_pos())
                
def SubTypeAction(Subtype, lines):
    if Subtype == SubType.DEATH:
        readDeaths(lines)
    elif Subtype == SubType.PLAY:
        if getCurState() == GameState.ENEMY_TURN:
            EnemyCardPlayed(lines)
        elif getCurState() == GameState.MY_TURN:
            Full_Entity(lines, EffectTime.ON_PLAY)
        if not isComboActive():
            setCombo(True)
    elif Subtype == SubType.TRIGGER:
        readTrigger(lines)
                  
def interpretingSubType(idx, cont, Subtype):
    i = idx
    #jump = 0
    while i < (len(cont) - 1):
        i += 1
        if '- ACTION_END' in cont[i]:
            setFound(True)
            SubTypeAction(Subtype, cont[idx:(i+1)])
            break
    if Subtype == SubType.PLAY:
        if isFound():
            setFound(False)
        else:
            setTmp(cont[idx:])
            setWaiting(True)
            print 'Action end Not found'
    return i - idx
            
def interpretingSubType2(cont, Subtype):
    i = 0
    while i < len(cont):
        if '- ACTION_END' in cont[i]:
            setFound(True)
            setWaiting(False)
            SubTypeAction(Subtype, getTmp()+cont[:(i + 1)])
            break
        i += 1
    if isFound():
        setFound(False)
        return i
    else:
        setTmp(getTmp() + cont)
        return len(cont) - 1
    
def readingMana(line, player):
    if player == Player.ME:
        setMyMana(int(split(line, 'value=', '\n')))
    else:
        setEnemyMana(int(split(line, 'value=', '\n')))   
                        
def drawCard(line):
    addHandcardToMyCards(createCard(gameId(line), split(line, 'CardID=', '\n')), getMyHandcardCount() + 1)
 
def attack(lines):
    attacker = None
    target = None
    for l in lines:
        if 'SubType=ATTACK' in l:
            a, t = l.split('ATTACK')
            target = getCardByIngameId(gameId(t))
            attacker = getCardByIngameId(gameId(a))
            target.takes_Damage(attacker._attack)
            attacker.takes_Damage(target._attack)
            
 
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
                    output += 'Play ' + getMyCardByIngameId(gameId(optionLines[i]))._name
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
                    name = getEnemyCardByIngameId(idx)._name
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
        
def findTarget(idx):
    try:
        cards = getMyCards()
        for c in cards:
            if cards[c]._zone == Zone.PLAY and cards[c]._ingameID == idx: 
                return (0, cards[c])      
        cards = getEnemyCards()
        for c in cards:
            if cards[c]._zone == Zone.PLAY and cards[c]._ingameID == idx: 
                return (1, cards[c])     
    except:
        print 'No Target Found'        
         
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
                    card = getMyCardByIngameId(choosenOption[0])
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