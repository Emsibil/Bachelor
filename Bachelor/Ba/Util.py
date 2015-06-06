import os
import numpy as np
from tables import Enum
from cardLibReader import *
from Card import *

class Player(Enum):
    ME = 1
    ENEMY = 2

class Effect(Enum):
    DEBUFF = 0
    BUFF = 1
    
class Buff(Enum):
    ATTACK = 'Attack'
    HEALTH = 'Health'
    TAUNT = 'Taunt'
    DIVINE_SHIELD = 'Divine Shield'
    STEALTH = 'Stealth'
    CHARGE = 'Charge'
    DRAW = 'Draw'
    COPY = 'Copy'
    SPELLDAMAGE = 'Spelldamage'
    
class Debuff(Enum):
    ATTACK = 'Attack'
    HEALTH = 'Health'
    SILENCE = 'Silence'
    DESTROY = 'Destroy'
    TRANSFORM = 'Transform'
    
class EffectTime(Enum):
    ON_PLAY = 'Play'
    ON_DEATH = 'Death'
    ON_BOARD = 'Board'
    ON_DRAW = 'Draw'
    
class GameState(Enum):
    SEARCHING = 0
    GAME_START = 1
    MULLIGAN = 2
    MY_TURN = 3
    ENEMY_TURN = 4
    GAME_END = 5
    
class Zone(Enum):
    DECK = 'DECK'
    HAND = 'HAND'
    PLAY = 'PLAY'
    GRAVEYARD = 'GRAVEYARD'
    SETASIDE = 'SETASIDE'
    
class Cardtype(Enum):
    HERO = 'Hero'
    MINION = 'Minion'
    SPELL = 'Spell'
    WEAPON = 'Weapon'
    SECRET = 'Secret'
    HERO_POWER = 'Hero Power'
    ENCHANTMENT = 'Enchantment'
    
class Option(Enum):
    END = 'END'
    PLAY = 'PLAY'
    ATTACK = 'ATTACK'

class Ability(Enum):
    BATTLECRY = 'Battlecry'
    ENRAGE = 'Enrage'
    DEATHRATTLE = 'Deathrattle'
    CHARGE = 'Charge'
    TAUNT = 'Taunt'
    STEALTH = 'Stealth'
    DIVINESHIELD = 'Divine Shield'
    WINDFURY = 'Windfury'

def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path
    
def createCard(cardId):
    card = CardById(cardId)
    cardtype = cardType(card)
    _card = Card(id(card), name(card), cardtype, manaCost(card))
    if cardtype == Cardtype.MINION:
        _card._attack = attackValue(card)
        _card._health = healthValue(card)
    if cardtype == Cardtype.HERO:
        _card._health = healthValue(card)
    return _card

def split(*args):
    try:
        if len(args) == 2:
            return args[0].split(args[1])[1]
        elif len(args) == 3:
            return args[0].split(args[1])[1].split(args[2])[0]
    except Exception, e:
        print args[0], e

def gameId(line):
    return int(split(line, 'id=', ' '))

def controllerID(line): 
    return int(split(line, 'player=', ']'))

def editAbility(target, ability, value):
    if value == 1:
        if ability not in target._ability:
            target._ability.append(ability)
    else:
        if ability in target._ability:
            target._ability.remove(ability)
    
PLAYER_NAMES = {}
def getPlayerName(PlayerID):
    global PLAYER_NAMES
    return PLAYER_NAMES[PlayerID]
def setPlayerName(PlayerID, Name):
    global PLAYER_NAMES
    PLAYER_NAMES[PlayerID] = Name

ME = 'Emsibil'
def get_Me():
    global Me
    return ME

def is_Me(Id):
    return getPlayerName(Id) == get_Me()
    
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
    ENEMY_MULLIGAN_DONE = State0
  
def getGameState(i):
    global GAME_STATES
    return GAME_STATES[i]

CUR_STATE = GameState.SEARCHING
def getCurState():
    global CUR_STATE
    return CUR_STATE
def setCurState(new_state):
    global CUR_STATE
    CUR_STATE = new_state 

ENEMY_CARDS = {}
def getEnemyCards():
    global ENEMY_CARDS
    return ENEMY_CARDS

def addEnemyMinonToField(card, pos):
    cards = getEnemyCards()
    card.set_pos(pos)
    card._zone = Zone.PLAY
    cards[card._ingameID] = card
def removeEnemyCard(idx):
    card = getEnemyCards()[idx]
    card._zone = Zone.GRAVEYARD
def getEnemyMinionCount():
    count = len([c for c in getEnemyCards().values() if c._zone==Zone.PLAY])
    return (count - 1)
def getEnemyCardByIngameID(idx):
    return getEnemyCards()[idx]
def reorderEnemyMinionsOnBoard(pos):
    cards = getEnemyCards()
    for c in cards:
        if cards[c]._zone == Zone.PLAY and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1
            
E_HANCARDS = 0
def getEnemyHandcardCount():
    global E_HANCARDS
    return E_HANCARDS

def addEnemyHancard():
    count = getEnemyHandcardCount() + 1    
    
def removeEnemyHandcard():
    count = getEnemyHandcardCount() - 1

CARDS = {}

def getCards():
    global CARDS
    return CARDS

def addHandcardAtPosition(cardId, pos, ingameID):
    cards = getCards()
    stringCard = CardById(cardId)
    card = createCard(cardId)
    card._ability = Abilities(stringCard)
    card._ingameID = ingameID
    if card._cardtype == Cardtype.HERO:
        card._zone = Zone.PLAY
    else:
        card._zone = Zone.HAND
    card.set_pos(pos)
    #card.zone = Zone.HAND
    #card.zonePos = pos
    cards[ingameID] = card
     
    print 'got new Card:'
    output = ''
    for card in cards.values():
        if card._cardtype == Cardtype.HERO_POWER:
            continue
        output += card._name + ' '
    print output

def getHandcardCount():
    count = len([c for c in getCards().values() if c._zone== Zone.HAND])
    return (count - 1)

def getCardByIngameId(idx):
    return getCards()[idx]
    
def removeCardByIngameId(idx):
    del getCards()[idx]
    
def reorderHandCards(pos):
    cards = getCards()
    for c in cards:
        if cards[c]._zone == Zone.HAND and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1

def addMyMinonToField(card, pos):
    cards = getCards()
    card.set_pos(pos)
    cards[card._ingameID] = card
    
def getMyMinionCount():
    count = len([c for c in getCards().values() if c._zone==Zone.PLAY])
    return (count - 1)

def reorderMinionsOnBoard(pos):
    cards = getCards()
    for c in cards:
        if cards[c]._zone == Zone.PLAY and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1
    
def hasAbility(card, abilityName):
    if abilityName in card._ability:
        return True
    else:
        return False 

MY_HERO = None
MY_HERO_POWER = None
ENEMY_HERO = None
ENEMY_HERO_POWER = None

def setMyHero(heroId, ingameID):
    global MY_HERO
    MY_HERO = heroId
    hero = createCard(heroId)
    hero._ingameID = ingameID
    hero._zone = Zone.PLAY
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
    hero = createCard(heroId)
    hero._ingameID = ingameID
    addEnemyMinonToField(hero, 0)
    print 'Set Enemy Hero'
def setEnemyHeroPower(powerId, ingameID):
    global ENEMY_HERO_POWER
    ENEMY_HERO_POWER = powerId
    heroPower = createCard(powerId)
    heroPower._ingameID = ingameID
    heroPower._zone = Zone.HAND
    heroPower.set_pos(0)
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
    setOptionsCalc(False)
    clearOptions()          
           
def clearAll():
    setVariablesDefault()
    setMulligan(False)
    cards = getCards()
    cards = {}
    e_cards = getEnemyCards()
    e_cards = {}
    hero = getMyHero()
    hero = None
    hero_power = getMyHeroPower()
    hero_power = None
    e_hero = getEnemyHero()
    e_hero = None
    e_hero_power = getEnemyHeroPower()  
    e_hero_power = None  
    setPlayerID(0)
    setMyTurn(False)
    setTurnChanged(False)
    setEnemyMulliganStateDone(False)
    setMyMulliganStateDone(False)
    setPlayerName(1, None)
    setPlayerName(2, None)