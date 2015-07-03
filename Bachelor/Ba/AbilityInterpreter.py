from Xml import readCard, existCardinfo
from Util_new import Effect, Ability, Stats
from Bachelor.Ba.Util_new import EffectTime, TargetSide
from Bachelor.Ba.Board import isMyCard, getCardByIngameId, getMyCardByIngameId

def isCardListed(card):
    return existCardinfo(card._id)

def getXmlInfo(card):
    return readCard(card._id)

def needsTargets(options, card):
    for o in options:
        if o[0] == card._ingameID:
            if len(o) == 3:
                return (True, o[3])
            else:
                return (False, None)
    return (False, None)

def possibleTargetSide(targets):
    my = 0
    enemy = 0
    for t in targets:
        if isMyCard(t):
            my = my + 1
        else:
            enemy = enemy + 1
    if my > 0 and enemy > 0:
        return TargetSide.BOTH
    elif my > 0:
        return TargetSide.MY
    else:
        return TargetSide.ENEMY
            
def isBuff(card):
    info = getXmlInfo(card)
    for i in info:
        if i[0] == Effect.BUFF and i[3] == EffectTime.ON_PLAY:
            return True
    return False  

def getBuffEffects(card):
    info = getXmlInfo(card)
    effects = []
    for i in info:
        if i[0] == Effect.BUFF:
            effects.append(i.text)
    return effects

def mostEffectiveTarget(targets, card):
    effects = getBuffEffects(card)
    for t in targets:
        tg = getMyCardByIngameId(t)
        for eff in effects:
            if eff
        

def targetFromMySide(targets):
    myTargets = []
    for t in targets:
        if isMyCard(t):
            myTargets.append(t)
    mostEffectiveTarget(myTargets)
         
def mostEffectiveEnemyTarget(targets, card):
    pass
   
def targetFromEnemySide(targets):
    eTargets = []
    for t in targets:
        if isMyCard(t):
            eTargets.append(t)
    mostEffectiveEnemyTarget(eTargets)
    