from tables import Enum
from Bachelor.Ba.LogInterpreter import getOptions
from Bachelor.Ba.Board import getMyCards, getEnemyCards, getMyCardByIngameId,\
    getEnemyCardByIngameId, getCardByIngameId, getMyMinionCount, isMyCard, getEnemyMinionCount
from Bachelor.Ba.Util_new import Zone, Cardtype, Option
from Bachelor.Ba.AbilityInterpreter import singleThread, attackEffectivness,\
    effectivness, eff_weapon, generell, isDefensiveCard

OPTIONS = getOptions()

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
    
def MinionDmg():
    dmg = 0 
    for c in getMyCards.values():
        if c._zone == Zone.PLAY:
            if c.mayAttack():
                if c._cardtype == Cardtype.MINION or (c._cardtype == Cardtype.HERO and c._attack > 0) or (c._cardtype == Cardtype.WEAPON): 
                    dmg = dmg + c.getAttack()
    return dmg

def EnemyMinionLife():
    life = 0
    for c in getEnemyCards.values():
        if c.compareZone(Zone.PLAY) and c.compareCardtype(Cardtype.MINION):
            life = life + c.getHealth() - c.getDamage()
    return life

def EnemyAttackPower():
    dmg = 0
    for c in getEnemyCards.values():
        if c.compareZone(Zone.PLAY):
            if c.compareCardtype(Cardtype.MINION) or c.compareCardtype(Cardtype.WEAPON):
                dmg = dmg + c.getAttack()
    return dmg

def ThreatLvlForMyHero():
    health = [(c.getHealth() + c._armor) for c in getMyCards().values() if c.compareCardtype(Cardtype.HERO)]
    return round((-4*(EnemyAttackPower()/health) + 2), 0)
   
def hasEnemyDefense():
    defense = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY) and c._taunt]
    if len(defense) > 0:
        return (True, defense)
    return (False, None)

def highestThreat(enemyMinions):
    maxThreat = []
    for m in enemyMinions:
        if maxThreat == []:
            maxThreat.append(m)
        else:
            for idx, t in enumerate(maxThreat):
                m_threat = singleThread(m)
                t_threat = singleThread(t)
                if m_threat > t_threat:
                    maxThreat.insert(idx, m)
                    break
                elif m_threat == t_threat:
                    if m.getAttack() >= t.getAttack():
                        maxThreat.insert(idx, m)
                        break
            if not m in maxThreat:
                maxThreat.append(m)   
    return maxThreat
    
def haveEffectiveCard(target, options):
    e = None
    for o in options:
        if o[2] == target._ingameID:
            e_tmp = (effectivness(getMyCardByIngameId(o[1]), target), getMyCardByIngameId(o[0]))
            if e is None or e_tmp[0] > e[0]:
                e = e_tmp
    if e >= Effectivness.LOW:
        return (True, e[1])
    else:
        return (False, None)
                 
def optionAgainstThreat(targets, options):
    threat = highestThreat(targets)
    for t in threat:
        eff = haveEffectiveCard(t, options)
        if eff[0]:
            return (t, eff[1])
                  
def buildDefense(options):
    for o in options:
        if o[1] == Option.PLAY:
            card = getMyCardByIngameId(o[0])
            defense = isDefensiveCard(card, o[2])
            if defense[0]:
                return (card, defense[1]) 
            
def buildOffense(options):
    eff = None
    toPlay = None
    for o in options:
        if o[1] == Option.PLAY:
            card = getMyCardByIngameId(o[0])
            if card.compareCardtype(Cardtype.MINION):
                e = generell(card)
            elif card.compareCardtype(Cardtype.WEAPON):
                e = eff_weapon()
            elif card.compareCardtype(Cardtype.SPELL):
                if o[2] == None:
                    e = effectivness(card, None)
                else:
                    e = (0, 0)
            if o[2] is not None:
                e3 = None
                target = None
                for t in o[2]:
                    t = getCardByIngameId(t)
                    tmp = effectivness(card, t)
                    e2 = (e[0] + tmp[0])/(e[1] + tmp[1])
                    if e3 is None or e2 > e3:
                        e3 = e2
                        target = t
                e = e3
            if eff is None or e > eff:
                eff = e
                toPlay = card
            
    return (toPlay, target)

def attack(atkoptions):
    for o in atkoptions:
        attacker = getMyCardByIngameId(o[0])
        enemyHero = None
        for t in o[2]:
            if not isMyCard(t):
                target = getEnemyCardByIngameId(t)
                if attackEffectivness(attacker, target) >= Effectivness.GOOD and not target.compareCardtype(Cardtype.HERO) and getEnemyMinionCount() >= 3:
                    if attacker.getAttack() == target.getHealth() or (attacker.getAttack() + 1) == target.getHealth():
                        return (attacker, target)
                elif target.compareCardtype(Cardtype.HERO):
                    enemyHero = target
        return (attacker, enemyHero)
     

def options(options):
    if ThreatLvlForMyHero() >= ThreatLvl.INCREASED:
        defense = hasEnemyDefense()
        if defense[0]:
            target, card = optionAgainstThreat(defense[1], options)
        else:
            targets = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY)]
            target, card = optionAgainstThreat(targets, options)
        if target is None and card is None:
            card, target = buildDefense(options)
    else:
        if (MinionDmg()/getMyMinionCount()) <= 1 and getMyMinionCount() < 7:
            card, target = buildOffense(options)
        else: 
            card, target = attack([o for o in options if o[1] == Option.ATTACK])
    return (card, target)            
            
            

# [Power] GameState.DebugPrintOptions() -   option 0 type=END_TURN mainEntity=
# [Power] GameState.DebugPrintOptions() -   option 1 type=POWER mainEntity=[name=Acidic Swamp Ooze id=56 zone=HAND zonePos=1 cardId=EX1_066 player=2]
# [Power] GameState.DebugPrintOptions() -   option 2 type=POWER mainEntity=[name=Chillwind Yeti id=50 zone=HAND zonePos=2 cardId=CS2_182 player=2]
# [Power] GameState.DebugPrintOptions() -   option 3 type=POWER mainEntity=[name=Sludge Belcher id=47 zone=HAND zonePos=3 cardId=FP1_012 player=2]
# [Power] GameState.DebugPrintOptions() -   option 4 type=POWER mainEntity=[name=Chillwind Yeti id=62 zone=HAND zonePos=4 cardId=CS2_182 player=2]
# [Power] GameState.DebugPrintOptions() -   option 5 type=POWER mainEntity=[name=Gnomish Inventor id=45 zone=HAND zonePos=5 cardId=CS2_147 player=2]
# [Power] GameState.DebugPrintOptions() -   option 6 type=POWER mainEntity=[name=Stormpike Commando id=43 zone=HAND zonePos=6 cardId=CS2_150 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Uther Lightbringer id=4 zone=PLAY zonePos=0 cardId=HERO_04 player=1]
# [Power] GameState.DebugPrintOptions() -     target 1 entity=[name=Garrosh Hellscream id=36 zone=PLAY zonePos=0 cardId=HERO_01 player=2]
# [Power] GameState.DebugPrintOptions() -     target 2 entity=[name=Arathi Weaponsmith id=40 zone=PLAY zonePos=1 cardId=EX1_398 player=2]
# [Power] GameState.DebugPrintOptions() -   option 7 type=POWER mainEntity=[name=Shattered Sun Cleric id=64 zone=HAND zonePos=7 cardId=EX1_019 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Arathi Weaponsmith id=40 zone=PLAY zonePos=1 cardId=EX1_398 player=2]
# [Power] GameState.DebugPrintOptions() -   option 8 type=POWER mainEntity=[name=Garrosh Hellscream id=36 zone=PLAY zonePos=0 cardId=HERO_01 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Uther Lightbringer id=4 zone=PLAY zonePos=0 cardId=HERO_04 player=1]
# [Power] GameState.DebugPrintOptions() -   option 9 type=POWER mainEntity=[name=Armor Up! id=37 zone=PLAY zonePos=0 cardId=CS2_102 player=2]
# [Power] GameState.DebugPrintOptions() -   option 10 type=POWER mainEntity=[name=Arathi Weaponsmith id=40 zone=PLAY zonePos=1 cardId=EX1_398 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Uther Lightbringer id=4 zone=PLAY zonePos=0 cardId=HERO_04 player=1]