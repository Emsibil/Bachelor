from tables import Enum
from Util_new import path, split
from Board import *
from Bachelor.Ba.Util_new import Cardtype
from Bachelor.Ba.Effective import Effectivness, EnemyAttackPower, MinionDmg
from types import IntType

class Target(Enum):
    MINION = 'a minion'
    HERO = 'your hero'
    RANDOM = 'random'            
    E_HERO = 'enemy hero'
    E_MINIONS = 'all enemy minions'
    ALL = 'all characters'
    CHARACTER = 'character'
    ENEMIES = 'all enemies'
    OTHER = 'all other characters'
    MINIONS = 'all minions'
    HEROS = 'each hero'
    E_CHARACTER = 'enemy character'
    UNDAMAGED_MINION = 'undamaged minion'
    ADJACENT = 'adjacent'
    FRIEND_CHAR = 'friendly characters'
    FRIEND_MIN = 'friendly minions'

class Effect(Enum):
    DMG = 0
    RES = 1
    
def effectivnessDmg(target, value):
    if isMyCard(target._ingameID):
        if target._cardtype == Cardtype.MINION:
            if target._divineShield:
                return Effectivness.LOW
            if target.getDamage() + value >= target._health:
                return Effectivness.BAD
        if target._cardtype == Cardtype.HERO:
            if target._armor > value:
                Effectivness.LOW
            if target._armor < value:
                if target._getDamage()+value >= target._health:
                    Effectivness.WORSE
                else:
                    Effectivness.BAD
    else:
        if target._cardtype == Cardtype.MINION:
            if target._divineShield:
                return Effectivness.LOW
            if target.getDamage() + value >= target._health:
                return Effectivness.GOOD
        if target._cardtype == Cardtype.HERO:
            if target._armor > value:
                Effectivness.LOW
            if target._armor < value:
                if target._getDamage()+value >= target._health:
                    Effectivness.GREAT
                else:
                    Effectivness.GOOD
        
def effectivnessRes(target, value):
    dmg = target.getDamage()
    hlt = target.getHealth()
    resPercental = (dmg - value)/hlt 
    if isMyCard(target._id):
        if resPercental >= 1:
            return Effectivness.GREAT
        else:
            return Effectivness.GOOD
    else:
        if resPercental >= 1:
            return Effectivness.WORSE
        elif resPercental > 0.5:
            return Effectivness.BAD
        else:
            return Effectivness.LOW
        
def effectivenessTrans(target, atk, health):
    if isMyCard(target._ingameID):
        if target.getHealth() > health or target.getAttack() > atk:
            return Effectivness.GOOD
        else:
            return Effectivness.WORSE
    else:
        if target.getHealth() < health or target.getAttack() < atk:
            return Effectivness.GOOD
        else:
            return Effectivness.WORSE
        
def effectivnessGain(txt):
    if 'this turn':
        return Effectivness.GOOD
    else:
        return Effectivness.GREAT
    
def effectivnessRet(target):
    if isMyCard(target._ingameID):
        if target.getDamage()/target.getHealth() <= 0.5 and target._charge == True:
            return Effectivness.GREAT
        elif target.getDamage()/target.getHealth() <= 0.5:
            return Effectivness.GOOD
        elif target._charge == True:
            return Effectivness.GOOD
    else:
        if target._getAttack >= 4:
            return Effectivness.GOOD
        else:
           return Effectivness.LOW
        #vielleicht zusätzlich ob die karte effective is

def toHero(value, effect):
    hero = [c for c in getMyCards().values() if c._cardtype == Cardtype.HERO]
    if effect == Effect.DMG:
        return (effectivnessDmg(hero, value), 1)
    if effect == Effect.RES:
        return (effectivnessRes(hero, value), 1)
    #zurückschreiben
    
def toEnemyHero(value, effect):
    hero = [c for c in getEnemyCards().values() if c._cardtype == Cardtype.HERO]
    if effect == Effect.DMG:
        return (effectivnessDmg(hero, value), 1)
    if effect == Effect.RES:
        return (effectivnessRes(hero, value), 1)
    #zurückschreiben 

def toAllEnemyMinions(value, effect):
    e = 0
    targets = [c for c in getEnemyCards().values() if (c._zone == Zone.PLAY and c._cardtype == Cardtype.MINION)]
    if Effect.DMG == effect:
        for t in targets:
            e = e + effectivnessDmg(t, value)
        return (e, len(targets))
    if Effect.RES == effect:
        for t in targets:
            e = e + effectivnessRes(t, value)
        return (e, len(targets))

def toAllMyMinions(value, effect):
    e = -1
    targets = [c for c in getMyCards().values() if (c._zone == Zone.PLAY and c._cardtype == Cardtype.MINION)]
    if Effect.DMG == effect:
        for t in targets:
            e =  e + effectivnessDmg(t, value)
        return (e, len(targets))
    if Effect.RES == effect:
        for t in targets:
            e = e + effectivnessRes(t, value)
        return (e, len(targets))
        
def toAllEnemyChars(value, effect):
    e1 = toAllEnemyMinions(value, effect)
    e2 = toEnemyHero(value, effect)
    return (e1[0] + e2[0], e1[1] + e2[1])

def toEachHero(value, effect):
    e1 = toEnemyHero(value, effect)
    e2 = toHero(value, effect)
    return (e1[0] + e2[0], e1[1] + e2[1])
    
def toAllMinions(value, effect):
    e1 = toAllEnemyMinions(value, effect)
    e2 = toAllMyMinions(value, effect)
    return (e1[0] + e2[0], e1[1] + e2[1])

def toALL(value, effect):
    e1 = toEachHero(value, effect)
    e2 = toAllMinions(value, effect)
    return (e1[0] + e2[0], e1[1] + e2[1])
        
def toAllOthers(card, value, effect):
    e = 0
    e1 = toAllEnemyChars(value, effect)
    e2 = toHero(value, effect)        
    targets = [c for c in getMyCards().values() if (c._zone == Zone.PLAY and c._cardtype == Cardtype.MINION and not c._ingameID == card._ingameID)]
    if Effect.DMG == effect:
        for t in targets:
            e = e + effectivnessDmg(t, value)
    return (e + e1[0] + e2[0], len(targets) + e1[1] + e2[1])
        
def getAdjacent(target):
    targets = []
    if isMyCard(target._ingameID):
        for c in getMyCards().values():
            if not c._zonePos == 0:
                if (c._zonePos == target._zonePos - 1) or (c._zonePos == target._zonePos + 1):
                    targets.append(c)
    else:
        for c in getEnemyCards().values():
            if not c._zonePos == 0:
                if (c._zonePos == target._zonePos - 1) or (c._zonePos == target._zonePos + 1):
                    targets.append(c)
    return targets

def toAdjacent(value, effect, target):
    e = 0
    targets = getAdjacent(target)
    if Effect.DMG == effect:
        for t in targets:
            e = e + effectivnessDmg(t, value)
    return (e, len(targets))
      
        
def dmg(card, target):
    txt = card._text
    amount = 0
    effness = None
    sideEffnes = (0, 0)
    if 'Deal' in txt:
        amount = split(txt, 'Deal ', ' damage')
    elif 'deal' in txt:
        amount = split(txt, 'deal ', ' damage')
    try:
        if '-' in amount:
            min, max = amount.split('-')
            amount = (int(min)+int(max) / 2) 
        else:
            amount = int(amount)
            if 'and' in txt:
                second = txt.split('and')[1]
                if E_HERO in second:
                    sideEffnes = toEnemyHero(amount, Effect.DMG)
                elif 'damage' in second:
                    new_amount = int(second.split('damage'))
                if Target.ADJACENT in second:
                    sideEffnes = toAdjacent(new_amount, Effect.DMG, target)
                if 'all other enemies' in second:
                    amount = amount - new_amount
                    sideEffnes = toAllEnemyChars(new_amount, Effect.DMG)
            effness = (effectivnessDmg(target, amount) + sideEffnes, 1 + sideEffnes[1])
    except:
        amount = None
    if target == None and type(amount) is IntType :
        if Target.HERO in txt:
            effness = toHero(amount, Effect.DMG)
        elif Target.MINIONS in txt:
            effness = toAllMinions(amount, Effect.DMG)
        elif Target.E_MINIONS in txt:
            effness = toAllEnemyMinions(amount, Effect.DMG)
        elif Target.E_HERO in txt:
            effness = toEnemyHero(amount, Effect.DMG)
        elif Target.ALL in txt:
            effness = toALL(amount, Effect.DMG)
        elif Target.ENEMIES in txt:
            effness = toAllEnemyChars(amount, Effect.DMG)
        elif Target.OTHER in txt:
            effness = toAllOthers(card, amount, Effect.DMG)
        elif Target.HEROS in txt:
            pass
        elif Target.MINION in txt:
            pass
            effness = toEachHero(amount, Effect.DMG)
        elif Target.RANDOM in txt:
            pass
        return int(effness[0]/effness[1])
    

def draw(card):
    txt = card._text
    amount = 0
    if 'Draw' in txt:
        amount = split(txt, 'Draw ', ' card')
    elif 'draw' in txt:
        amount = split(txt, 'draw ', ' card')
    if amount == 'a':
        amount = 1
    else:
        try:
            amount = int(amount)
        except:
            amount = None
    h_count = getMyHandcardCount()
    if h_count + amount > 10:
        return Effectivness.WORSE
    elif h_count + amount == 10:
        return Effectivness.LOW
    elif h_count <= 5:
        if amount > 1:
            return Effectivness.GREAT
        else:
            return Effectivness.GOOD
        
def summon(card):
    txt = card._text
    atk = 0
    amount = 0
    m_count = getMyMinionCount()
    if 'summon' in txt:
        atk = split(txt, 'summon ', '/')     
    elif 'Summon' in txt:
        atk = split(txt, 'Summon ', '/')
    amount, atk = atk.split(' ')
    hlt = split(txt, '/', ' ')
    if amount == 'a':
        amount = 1
    elif amount == 'two':
        amount = 2
    elif amount == 'three':
        amount = 3
    if 'opponent' in txt:
        return Effectivness.BAD
    elif amount + m_count > 7:
        return Effectivness.WORSE
    elif amount + m_count == 7:
        return Effectivness.BAD
    elif amount + m_count < 7 and not m_count == 0:
        return Effect.GOOD
    elif m_count == 0:
        return Effect.GREAT
    
def discard():
    return Effectivness.BAD

def add():
    return Effectivness.GOOD

def restore(card, target):
    txt = card._text
    amount = 0
    effness = None
    if 'full Health' in txt:
        amount = 99
    elif 'Restore' in txt:
        amount = int(split(txt, 'Restore ', 'Health'))
    elif 'restore' in txt:
        amount = int(split(txt, 'restore ', 'Health'))
    else:
        return Effectivness.LOW
    if target is None:
        if Target.HERO in txt:
            effness = toHero(amount, Effect.RES)
        elif Target.MINIONS in txt:
            effness = toAllMinions(amount, Effect.RES)
        elif Target.ALL in txt:
            effness = toALL(amount, Effect.RES)
    else:
        if isMyCard(target._ingameID):
            effness = (effectivnessRes(target, amount), 1)
        else:
            effness = (effectivnessRes(target, amount), 1)
    return int(effness[0]/effness[1])
        
def equip(card):
    for c in getMyCards().value():
        if c.compareCardtype(Cardtype.WEAPON) and c.compareZone(Zone.PLAY):
            return Effectivness.BAD
    return Effectivness.GOOD

def transform(card, target):
    txt = card._text
    if 'Transform' in txt:
        if 'random' in txt:
            pass
        else:
            atk, hlt = txt.split('/')
            return effectivenessTrans(target, int(atk.split('a ')[1]), int(hlt.split(' ')[0]))   

def gain(card):
    txt = card._text
    if 'Mana Crystal' in txt:
        return effectivnessGain(txt)
    elif 'Attack' in txt:
        return effectivnessGain(txt)
    elif 'Health' in txt:
        return effectivnessGain(txt)
    elif 'Armor' in txt:
        return Effectivness.GOOD
    elif '/' in txt:
        return effectivnessGain(txt) 
    elif 'Stealth' in txt or 'Divine Shield' in txt:
        return Effectivness.GOOD  

def returnToHand(card, target):
    txt = card._text
    if Target.MINIONS in txt:
        if getEnemyMinionCount() - getMyMinionCount() > 0 and MinionDmg() - EnemyAttackPower() > 0:
            return Effectivness.GREAT
        elif MinionDmg() - EnemyAttackPower() > 0:
            return Effectivness.GOOD
    elif 'to life' in txt:
        if 'with 1 Health' in txt:
            return Effectivness.GOOD
        elif 'with full Health' in txt and target.getDamage()/target.getHealth() < 0.5:
            return Effectivness.GREAT
        else:
            return Effectivness.LOW
    else:
        return effectivnessRet(target)
    