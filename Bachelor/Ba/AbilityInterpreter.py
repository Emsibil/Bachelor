from tables import Enum
from types import IntType
from Board import isMyCard, Zone, getMyCards,\
    getEnemyCards, getMyHero, getMyMinionCount, getEnemyMinionCount, getMyHandcardCount,\
    E_HERO, getCardByIngameId
from Util_new import split, Cardtype, Effectivness, ThreatLvl

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
    
def EnemyAttackPower():
    dmg = 0
    for c in getEnemyCards().values():
        if c.compareZone(Zone.PLAY):
            if c.compareCardtype(Cardtype.MINION) or c.compareCardtype(Cardtype.WEAPON):
                dmg = dmg + c.getAttack()
    return dmg
   
def MinionDmg():
    dmg = 0 
    for c in getMyCards().values():
        if c._zone == Zone.PLAY:
            if c.mayAttack():
                if c._cardtype == Cardtype.MINION or (c._cardtype == Cardtype.HERO and c._attack > 0) or (c._cardtype == Cardtype.WEAPON): 
                    dmg = dmg + c.getAttack()
    return dmg

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
                if target.getDamage()+value >= target._health:
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
        #vielleicht zusaetzlich ob die karte effective is

def effectivnessDsty(target):
    if isMyCard(target._ingameId):
        return Effectivness.WORSE
    else:
        return Effectivness.GREAT
    
def toHero(value, effect):
    hero = [c for c in getMyCards().values() if c._cardtype == Cardtype.HERO]
    if effect == Effect.DMG:
        return (effectivnessDmg(hero, value), 1)
    if effect == Effect.RES:
        return (effectivnessRes(hero, value), 1)
    #zurueckschreiben
    
def toEnemyHero(value, effect):
    hero = [c for c in getEnemyCards().values() if c._cardtype == Cardtype.HERO]
    if effect == Effect.DMG:
        return (effectivnessDmg(hero, value), 1)
    if effect == Effect.RES:
        return (effectivnessRes(hero, value), 1)
    #zurueckschreiben 

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
            mini, maxi = amount.split('-')
            amount = (int(mini)+int(maxi) / 2) 
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
        return effness
    

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
        return (Effectivness.WORSE, 1)
    elif h_count + amount == 10:
        return (Effectivness.LOW, 1)
    elif h_count <= 5:
        if amount > 1:
            return (Effectivness.GREAT, 1)
        else:
            return (Effectivness.GOOD, 1)
        
def summon(card):
    txt = card._text
    atk = 0
    m_count = getMyMinionCount()
    if 'summon' in txt:
        atk = split(txt, 'summon ', '/')     
    elif 'Summon' in txt:
        atk = split(txt, 'Summon ', '/')
    amount, atk = atk.split(' ')
    #hlt = split(txt, '/', ' ')
    if amount == 'a':
        amount = 1
    elif amount == 'two':
        amount = 2
    elif amount == 'three':
        amount = 3
    if 'opponent' in txt:
        return (Effectivness.BAD, 1)
    elif amount + m_count > 7:
        return (Effectivness.WORSE, 1)
    elif amount + m_count == 7:
        return (Effectivness.BAD, 1)
    elif amount + m_count < 7 and not m_count == 0:
        return (Effectivness.GOOD, 1)
    elif m_count == 0:
        return (Effectivness.GREAT, 1)
    
def discard():
    return (Effectivness.BAD, 1)

def add():
    return (Effectivness.GOOD, 1)

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
        return (Effectivness.LOW, 1)
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
            return (Effectivness.BAD, 1)
    return (Effectivness.GOOD, 1)

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
        return (Effectivness.GOOD, 1)
    elif '/' in txt:
        return effectivnessGain(txt) 
    elif 'Stealth' in txt or 'Divine Shield' in txt:
        return (Effectivness.GOOD, 1)  

def returnToHand(card, target):
    txt = card._text
    if Target.MINIONS in txt:
        if getEnemyMinionCount() - getMyMinionCount() > 0 and MinionDmg() - EnemyAttackPower() > 0:
            return (Effectivness.GREAT, 1)
        elif MinionDmg() - EnemyAttackPower() > 0:
            return (Effectivness.GOOD, 1)
    elif 'to life' in txt:
        if 'with 1 Health' in txt:
            return (Effectivness.GOOD, 1)
        elif 'with full Health' in txt and target.getDamage()/target.getHealth() < 0.5:
            return (Effectivness.GREAT, 1)
        else:
            return (Effectivness.LOW, 1)
    else:
        return effectivnessRet(target)
    
def enrage(card):
    if card.getHealth() > 1:
        return (Effectivness.GOOD, 1)
    else:
        return (Effectivness.BAD, 1)

def cost(card):    
    txt = card._text
    if 'cost' in txt:
        try:
            red = int(split(txt,'(', ')'))
            if 'less' in txt:
                if 'Your' in txt:
                    if red == 0:
                        return (Effectivness.GREAT, 1)
                    else:
                        return (Effectivness.GOOD, 1)
                elif 'Enemy' in txt:
                    return (Effectivness.BAD, 1)
            elif 'more' in txt:
                if 'Your' in txt:
                    return (Effectivness.BAD, 1)
                elif 'Enemy' in txt:
                    return (Effectivness.GOOD, 1)
        except:
            return Effectivness.LOW
                
def destroy(card, target):
    txt = card._text
    if target is None:
        if Target.MINIONS in txt:
            if getMyMinionCount() - getEnemyMinionCount() < 0:
                return (Effectivness.GOOD, 1)
            else:
                return (Effectivness.BAD, 1)
        elif Target.OTHER in txt:
                return (Effectivness.GOOD, 1)
    else:
        if isMyCard(target._ingameID):
            return (Effectivness.WORSE, 1)
        else:
            return (Effectivness.GREAT, 1)     
                   
def generell(card):
    effnes = 0
    effnes = effnes + (card._attack - card._manacosts) + (card._health - card._manacosts)
    if effnes < 0:
        return (Effectivness.BAD, 1)
    elif effnes > 0:
        return (Effectivness.GOOD, 1)
    else:
        return (Effectivness.LOW, 1)
    
def isDefensiveCard(card, targets):    
    if card.compareCardtype(Cardtype.SPELL) or card.compareCardtype(Cardtype.MINION):
        target = None
        if 'Give' in card._text and ('Taunt' in card._text or 'Divine Shield' in card._text) and not getMyMinionCount() == 0:
            return True
        elif 'Restore' or 'restore' in card._text:
            if targets is not None:
                eff = None
                for t in targets:
                    t = getCardByIngameId(t)
                    e = restore(card, t) 
                    if e > eff or eff is None:
                        eff = e
                        target = t 
                
            else:
                eff = restore(card, None)
        elif 'Gain' in card._text and 'Armor' in card._text:
            eff = gain(card)
    elif card.compareCardtype(Cardtype.MINION):
        eff = generell(card)
        if targets is not None:
                high = None
                for t in targets:
                    t = getCardByIngameId(t)
                    e = effectivness(card, t) 
                    if e > high or high is None:
                        high = e
                        target = t 
        else:
            high = effectivness(card, None)
        eff = (eff[0] + high[0])/(eff[1] + high[1])
        if card._taunt:
            eff = eff + 0.5
        if card._divineShield:
            eff = eff + 0.5
        eff = round(eff, 0)
    if eff >= Effectivness.GOOD:
        return (True, target)
    return (False, None)
            
def attackEffectivness(attacker, target):
    a_l = attacker.getHealth() - target.getAttack()
    t_l = target.getHealth() - attacker.getAttack()
    if a_l > 0 and t_l <= 0:
        return Effectivness.GOOD
    elif a_l <= 0 and t_l <= 0:
        return Effectivness.LOW
    elif a_l <= 0 and t_l > 0:
        return Effectivness.BAD
    elif target.getHealth() == t_l and target._divineShield:
        Effectivness.LOW
    elif t_l == target.getHealth():
        return Effectivness.WORSE
    elif a_l == attacker.getHealth():
        return Effectivness.GREAT
        
def singleThread(card):
    hero = getMyHero()
    percent = card.getAttack()/(hero._health - hero._armor)
    if percent > 0.2:
        ThreatLvl.HIGH
    elif percent > 0.13:
        ThreatLvl.INCREASED
    elif percent > 0.05:
        ThreatLvl.NORMAL
    elif percent <= 0.05:
        ThreatLvl.LOW
    elif percent == 0:
        ThreatLvl.NONE

def eff_weapon():
    weapon = [c for c in getMyCards().value() if c.compareCardtype(Cardtype.WEAPON) and c.compareZone(Zone.PLAY)]
    if len(weapon) == 0:
        return Effectivness.GOOD
    else:
        return Effectivness.WORSE
    
        
def effectivness(card, target):
    txt = card._text
    e = (0, 0)
    if card.compareZone(Zone.HAND):
        if 'Damage' in txt or 'damage' in txt:
            v = dmg(card, target)
            e = (e[0] + v[0], e[1] + v[1]) 
        elif 'Destroy' in txt or 'destroy' in txt:
            v = destroy(card, target)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'cost' in txt:
            v = cost(card)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'Enrage' in txt:
            v = enrage(card)#
            e = (e[0] + v[0], e[1] + v[1])
        elif 'return' in txt or 'Return' in txt:
            v = returnToHand(card, target)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'gain' in txt or 'Gain' in txt:
            v = gain(card)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'Transform' in txt or 'transform' in txt:
            v = transform(card, target)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'Equip' in txt or 'equip' in txt:
            v = equip(card)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'Restore' in txt or 'restore' in txt:
            v = restore(card, target)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'Add' in txt or 'add' in txt:
            v = add()
            e = (e[0] + v[0], e[1] + v[1])
        elif 'Discard' in txt or 'discard' in txt:
            v = discard()
            e = (e[0] + v[0], e[1] + v[1])
        elif 'summon' in txt or 'Summon' in txt:
            v = summon(card)
            e = (e[0] + v[0], e[1] + v[1])
        elif 'Draw' in txt or 'draw' in txt:
            v =  draw(card)
            e = (e[0] + v[0], e[1] + v[1])
        return round(e[0]/e[1], 0)
    elif card.compareZone(Zone.PLAY):
        return attackEffectivness(card, target)