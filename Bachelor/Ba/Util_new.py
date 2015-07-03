import os
from tables import Enum

class Player(Enum):
    ME = 1
    ENEMY = 2

class TargetSide(Enum):
    MY = 'My'
    ENEMY = 'Enemy'
    BOTH = 'Both'
    
class Effect(Enum):
    DEBUFF = 'Debuff'
    BUFF = 'Buff'
    BOTH = 'BuffDebuff'
    
class Stats():
    ATTACK = 'Attack'
    HEALTH = 'Health'
    ARMOR = 'Armor'
    
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
    ON_ACTIVATE = 'aktivateSecret'
    
class GameState(Enum):
    SEARCHING = 0
    GAME_START = 1
    MULLIGAN = 2
    MY_TURN = 3
    ENEMY_TURN = 4
    GAME_END = 5
    
CUR_STATE = GameState.SEARCHING
def getCurState():
    global CUR_STATE
    return CUR_STATE
def setCurState(new_state):
    global CUR_STATE
    CUR_STATE = new_state 
    
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
    
class SubType(Enum):
    DEATH = 'DEATHS'
    TRIGGER = 'TRIGGER'
    PLAY = 'PLAY'
    ATTACK = 'ATTACK'
    
class Tag(Enum):
    ATTACK = 'ATK'
    HEALTH = 'HEALTH'
    TAUNT = 'TAUNT'
    STEALTH = 'STEALTH'
    DIVINESHIELD = 'DIVINE_SHIELD'
    CHARGE = 'CHARGE'
    WINDFURY = 'WINDFURY'
    
def TagEqualToAbility(tag):
    if Tag.TAUNT == tag:
        return Ability.TAUNT
    elif Tag.CHARGE == tag:
        return Ability.CHARGE
    elif Tag.DIVINESHIELD == tag:
        return Ability.DIVINESHIELD
    elif Tag.STEALTH == tag:
        return Ability.STEALTH
    elif Tag.WINDFURY == tag:
        return Ability.WINDFURY    
    
def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

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
waiting = False
def setWaiting(binary):
    global waiting
    waiting = binary
def isWaiting():
    global waiting
    return waiting
Found= False
def isFound():
    global Found
    return Found
def setFound(binary):
    global Found
    Found = binary
Mulligan = False
def isMulligan():
    global Mulligan
    return Mulligan
def setMulligan(binary):
    global Mulligan
    Mulligan = binary
COMBO = False
def setCombo(binary):
    global COMBO
    COMBO = binary
def isComboActive():
    global COMBO
    return COMBO
CALC_OPTIONS = False
def setOptionsCalc(binary):
    global CALC_OPTIONS
    CALC_OPTIONS = binary
def isOptionCalc():
    global CALC_OPTIONS
    return CALC_OPTIONS
    
def setVariablesDefault():
    setTmp(None)
    setWaiting(False)
    #setMyMana(0)
    #setEnemyMana(0)
    setFound(False)
    setCombo(False)  
    setOptionsCalc(False)
    #clearOptions()     