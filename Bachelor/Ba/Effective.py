from Board import getMyCards, getEnemyCards, getMyCardByIngameId,\
    getEnemyCardByIngameId, getCardByIngameId, getMyMinionCount, isMyCard,\
    getEnemyMinionCount
from Util_new import Zone, Cardtype, Option, Effectivness, ThreatLvl
from AbilityInterpreter import singleThread, attackEffectivness,\
    effectivness, eff_weapon, generell, isDefensiveCard, EnemyAttackPower,\
    MinionDmg
    
def EnemyMinionLife():
    life = 0
    for c in getEnemyCards.values():
        if c.compareZone(Zone.PLAY) and c.compareCardtype(Cardtype.MINION):
            life = life + c.getHealth() - c.getDamage()
    return life

def ThreatLvlForMyHero():
    health = [(c.getHealth() + c._armor) for c in getMyCards().values() if c.compareCardtype(Cardtype.HERO)]
    return round((-4*(EnemyAttackPower()/health[0]) + 2), 0)
   
def hasEnemyDefense():
    defense = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY) and c.compareCardtype(Cardtype.MINION) and c._taunt]
    if len(defense) > 0:
        return (True, defense)
    return (False, None)

def highestThreat(enemyMinions):
    try:
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
    except Exception, e:
        print 'highestThreat()', e
        
def haveEffectiveCard(target, options):
    try:
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
    except Exception, ex:
        print 'haveEffectiveCard()', ex
                 
def optionAgainstThreat(targets, options):
    try:
        threat = highestThreat(targets)
        for t in threat:
            eff = haveEffectiveCard(t, options)
            if eff[0]:
                return (t, eff[1])
        return (None, None)
    except Exception, e:
        print 'optionAgainstThreat()', e
                       
def buildDefense(options):
    try:
        for o in options:
            if o[1] == Option.PLAY:
                card = getMyCardByIngameId(o[0])
                defense = isDefensiveCard(card, o[2])
                if defense[0]:
                    return (card, defense[1])
    except Exception, e:
        print 'buildDefense()', e 
            
def buildOffense(options):
    try:
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
    except Exception, ex:
        print 'buildOffense()', ex

def attack(atkoptions):
    try:
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
    except Exception, e:
        print 'attack()', e 

def options(options):
    try:
        if ThreatLvlForMyHero() >= ThreatLvl.INCREASED:
            defense = hasEnemyDefense()
            if defense[0]:
                target, card = optionAgainstThreat(defense[1], options)
            else:
                targets = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY) and not c.compareCardtype(Cardtype.HERO)]
                target, card = optionAgainstThreat(targets, options)
            if target is None and card is None:
                card, target = buildDefense(options)
        else:
            if (MinionDmg()/getMyMinionCount()) <= 1 and getMyMinionCount() < 7:
                card, target = buildOffense(options)
            else: 
                card, target = attack([o for o in options if o[1] == Option.ATTACK])
        return (card, target)
    except Exception, e:
        print 'options()', e            
    