import os
from tables import Enum

class Player(Enum):
    ME = 1
    ENEMY = 2

class TargetSide(Enum):
    MY = 'My'
    ENEMY = 'Enemy'
    BOTH = 'Both'
    
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
    SEARCHING = 'Searching'
    GAME_START = 'GameStart'
    MULLIGAN = 'Mulligan'
    MY_TURN = 'MyTurn'
    ENEMY_TURN = 'EnemyTurn'
    GAME_END = 'GameEnd'
    
class Effectivness(Enum):
    WORSE = -2
    BAD = -1
    LOW = 0
    GOOD = 1
    GREAT = 2
    
class ThreatLvl(Enum):
    HIGH = -2
    INCREASED = -1
    NORMAL = 0
    LOW = 1
    NONE = 2
    
class Zone(Enum):
    DECK = 'DECK'
    HAND = 'HAND'
    PLAY = 'PLAY'
    GRAVEYARD = 'GRAVEYARD'
    SETASIDE = 'SETASIDE'
    WEAPON = 'WEAPON'
    
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
    
class ThreatClasses(Enum):
    NONE = 0
    DEFENSE = 1
    DEFENSE_THREAT = 2
    THREAT = 3
    STRONG_DEFENSE = 4
    
raceDict = {1: 'minion', 2: 'beast', 3: 'mech', 4: 'dragon', 5: 'pirate', 6: 'demon', 7: 'murloc', 8: 'character', 9: 'hero', 10: 'weapon'}
def getRaceDict():
    global raceDict
    return raceDict

class Side(Enum):
    MY = 0
    ENEMY = 1
    BOTH = 2
    
class Effect(Enum):
    DAMAGE = 'damage'
    RESTORE = 'restore'
    RETURN = 'return'
    DESTROY = 'destroy'
    GAIN = 'gain'
    TRANSFORM = 'transform'
    ADD = 'add'
    EQUIP = 'equip'
    DRAW = 'draw'
    DISCARD = 'discard'
    AURA = 'aura'
    GIVE = 'give'
    OVERLOAD = 'overload'
    HAVE = 'have +'
    SUMMON = 'summon'
    
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
def value(line):
    return split(line, 'value=', '\n')