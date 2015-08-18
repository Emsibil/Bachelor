from tables import Enum
from Util_new import Cardtype, split, Zone, Option, ThreatClasses
from Board import getEnemyCards, getMyCards,getCardByIngameId, isMyCard,\
    getMyHandcardCount, getEnemyHandcardCount, getMyHero, getMyMana


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
    
def findTargetsInText(card, text):
    try:
        _race = None
        for race in getRaceDict().values():
            if race in text:
                _race = race
        if 'enemies' in text or 'enemy' in text:
            cards = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY)]
        elif 'friendly' in text or 'your' in text:
            if 'other' in text:
                cards = [c for c in getMyCards().values() if c.compareZone(Zone.PLAY) and not c._ingameID == card._ingameID]
            else:
                cards = [c for c in getMyCards().values() if c.compareZone(Zone.PLAY)]
        else:
            if 'other' in text:
                cards = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY)]
                + [c for c in getMyCards() if c.compareZone(Zone.PLAY) and not c._ingameID == card._ingameID]
            elif 'all' in text: 
                cards = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY)]
                + [c for c in getMyCards().values() if c.compareZone(Zone.PLAY)]
            else:
                cards = None
        if _race is not None and cards is not None:
            if _race == 'character':
                pass
            elif _race == 'hero':
                cards = [c for c in cards if card.compareCardtype(Cardtype.HERO)]
            else:
                if _race == 'minion':
                    cards = [c for c in cards if card.compareCardtype(Cardtype.MINION)]
                else:
                    cards = [c for c in cards if card.compareCardtype(Cardtype.MINION) and cards._race == _race]   
        return cards
    except Exception, e:
        print 'findTargetsInText()', e
        
def damageEffect(target, text, cost):
    try:
        if 'deal' in text:
            amount = split(text, 'deal', 'damage')
            if '-' in amount:
                a1, a2 = amount.split('-')
                amount = ((int(a1) + int(a2))/2.0)
            elif amount == '':
                pass
            else:
                amount = int(amount)
            if isMyCard(target._ingameID):
                value = amount
                if target.getHealth() <= amount and not target._divineShield:
                    value = value + (target._manacosts/2.0)
            else:
                value = (-1 * amount)
                if target.compareCardtype(Cardtype.MINION):
                    if not target._divineShield:
                        if target.getHealth() < amount:
                            value = value - (round(target._manacosts/2.0, 0))
                        elif target.getHealth() == amount:
                            value = (value - (round(target._manacosts/2.0, 0))) * 2
                if target.compareCardtype(Cardtype.HERO):
                    if target.getHealth() <= amount:
                        value = value - (round(target._manacosts/2.0, 0)) - 10
            return value
    except Exception, e:
        print 'damageEffect()', e    
        
def restoreEffect(target, text, cost):
    try:
        if 'restore' in text:
            if 'full health' in text:
                amount = target.getDamage()
            else:
                amount = split(text, 'restore', 'health')
            value = (-1*amount)
            if isMyCard(target._ingameID) and target.getDamage() <= amount:
                value = value - (target._manacosts/2.0)
            elif not isMyCard(target._ingameID) and target.getDamage() <= amount:
                value = value + (target._manacosts/2.0)
        return value
    except Exception, e:
        print 'restoreEffect()', e
        
def transformEffect(target, text, cost):
    try:
        if 'transform' in text:
            health, atk = text.split('/')
            health = int(health.split('into a ')[1])
            atk = int(atk.split(' ')[0])
            if isMyCard(target._ingameID) and target.getHealth() < health and target.getAttack() < atk:
                return (-1 * target._manacosts)
            elif not isMyCard(target._ingameID) and target.getHealth() > health and target.getAttack() > atk:
                return  (-1 * target._manacosts)
            else:
                return 0
    except Exception, e:
        print 'transformEffect()', e
        
def giveEffect(target, text, cost, threatClass):
    try:
        if 'give' in text or 'have +' in text:
            atk = 0
            hlt = 0
            if 'attack' in text and not 'health' in text:
                atk = int(split(text, '+', ' '))
            elif 'health' in text and not 'attack' in text:
                hlt = int(split(text, '+', ' '))
            else:
                atk = int(split(text, '+', '/'))
                hlt = int(split(text, '+', ' '))
            value = (-1 * (atk/2.0) + (hlt/2.0))
            if 'charge' in text:
                value = value - 1
            if 'taunt' in text:
                value = value - 1
                if threatClass == ThreatClasses.DEFENSE_THREAT or threatClass == ThreatClasses.THREAT:
                    value = value - (threatClass - 1)
            if 'windfury' in text:
                value = value - 2
            if 'divine shield' in text:
                value = value - 1
            if 'stealth' in text:
                value = value - 1
            if 'end of turn' in text:
                value = value + 1
            if isMyCard(target._ingameID):
                return value
            else:
                return (-1 * value)                
    except Exception, e:
        print 'giveEffect()', e

def destroyEffect(target, text, cost):
    try:
        if isMyCard(target._ingameID):
            return target._manacosts
        else:
            return (-1 * target._manacosts)
    except Exception, e:
        print 'destroyEffect()', e
        
def returnEffect(target, text, cost):
    try:
        if isMyCard(target._ingameID):
            pass
        else:
            pass
    except Exception, e:
        print 'returnEffect()', e

def drawEffect(text, cost):
    try:
        amount = split(text, 'draw ', ' card')
        try:
            amount = int(amount)
        except:
            if amount == 'a':
                amount = 1
            elif amount == 'two':
                amount = 2
        value = (-2 * amount)
        if 'each player draw' in text:
            if getEnemyHandcardCount() + amount > 10:
                value = value - 1
            else:
                value = value + 1
            if getMyHandcardCount() + amount > 10:
                value = value + 1
        elif 'your opponent draw' in text:
            if getEnemyHandcardCount() + amount > 10:
                value = value - 1
            else:
                value = value + 1
        else:
            if getMyHandcardCount() + amount > 10:
                value = value + 1
        return value
    except Exception, e:
        print 'drawEffect()', e    
        
def gainEffect(text, cost):
    try:
        if 'mana crystal' in text:
            try: 
                mana = int(split(text, 'gain ', ' mana'))
            except:
                if 'an' in text:
                    mana = 1
            if 'this turn only' in text:
                hand = [c for c in getMyCards().values() if c.compareZone(Zone.HAND) and c.compareCardtype(Cardtype.MINION)]
                resources = getMyMana()
                cardWithHigherCosts = False
                for c in hand:
                    if c._manacosts == resources + mana:
                        cardWithHigherCosts = True
                        print c._name
                        break
                if cardWithHigherCosts:
                    mana = (mana/2.0)
                else:
                    mana = -1
            return (-1 * mana) 
        elif 'armor' in text:
            armor = split(text, 'gain ', ' armor')
            return (-1 * armor)
        elif 'health' in text:
            hlt = int(split(text, '+', 'attack'))
            return (-1 * (hlt/2))
        elif 'attack' in text:
            atk = int(split(text, '+', 'attack'))
            return (-1 * (atk/2))
        elif '+' in text and '/' in text:
            atk = int(split(text, '+', '/'))
            hlt = int(text.split('/+')[1][:1])
            return (-1 * ((atk + hlt)/2.0))
    except Exception, e:
        print 'gainEffect()', e
        
def discardEffect(text, cost):
    try:
        pass
    except Exception, e:
        print 'discardEffect()', e
        
def addEffect(text, cost):
    try:
        if 'spare part' in text:
            return -1
    except Exception, e:
        print 'addEffect()', e
        
def equipEffect(text, cost):
    try:
        if 'equip' in text:
            atk = int(split(text, 'equip a ' '/'))
            hlt = int(split(text, '/', ''))
            return (-1 * ((atk + hlt)/2.0))
    except Exception, e:
        print 'equipEffect()', e
        
def summonEffect(text, cost):
    try:
        if 'summon' in text:
            amount = split(text, 'summon', '/')
            amount, atk = amount.split(' ')
            hlt = int(split('/', ' '))
            atk = int(atk)
            if amount == 'a':
                amount = 1
            elif amount == 'two':
                amount = 2
            elif amount == 'three':
                amount = 3
            elif amount == 'five':
                amount = 5
            return (-1 * (amount * ((atk + hlt)/2.0)))
    except Exception, e:
        print 'summonEffect()', e

def costEffect(text, cost):
    try:
        if 'cost' in text:
            amount = int(split(text, '(', ')'))
            if 'less' in text:
                return amount
            elif 'more' in text:
                return (amount * -1)
    except Exception, e:
        print 'costEffect()', e 

def overloadEffect(text, cost):
    try:
        amount = split(text, 'overload:', ')')
        amount = int(amount.split('(')[1])
        return cost + round(amount/2.0,0)
    except Exception, e:
        print 'overloadEffect()', e

def attackEffectivness(attacker, target, threatClass):
    try:
        value = 0
        atk = attacker.getHealth() - target.getAttack()
        tar = target.getHealth() - attacker.getAttack()
        if not isMyCard(target._ingameID):
            if not target.compareCardtype(Cardtype.HERO):
                if target._divineShield:
                    if attacker._divineShield:
                        value = -2
                    elif attacker.getAttack() == 1:
                        if atk > 0:
                            value = -2
                        else:
                            value = -1
                elif attacker.getAttack() > 1:
                    if atk > 0:
                        value = -1
                    else:
                        value = 0
            elif attacker._divineShield:
                if tar <= 0:
                    value = (target._manacosts *-1) - 1
                else:
                    value = 0
            elif target.getHealth() == attacker.getAttack():
                value = (target._manacosts *-1) - 0.5
            elif target.getHealth() < attacker.getAttack():
                value = target._manacosts * -1
            else: 
                value = 0
            if atk > 0:
                if atk == attacker.getHealth():
                    value = value - 1
            else:
                value = value + 1
            if tar > 0 and not target.compareCardtype(Cardtype.HERO):
                value = value + 1
            elif tar <= 0 and target.compareCardtype(Cardtype.HERO):
                value = value - 10
            if threatClass == ThreatClasses.DEFENSE or threatClass == ThreatClasses.DEFENSE_THREAT or threatClass == ThreatClasses.THREAT:
                value = value - threatClass
            return value
        else:
            return 3
    except Exception, e:
        print 'attackEffectiness()', e

def abilityWithoutTarget(text, cost):
    try:
        value = cost
        if Effect.GAIN in text:
            value = value + gainEffect(text, cost)
        if Effect.ADD in text:
            value = value + gainEffect(text, cost)
        if Effect.DRAW in text:
            value = value + drawEffect(text, cost)
        if Effect.EQUIP in text:
            value = value + equipEffect(text, cost)
        if Effect.DISCARD in text:
            value = value + discardEffect(text, cost)
        if Effect.OVERLOAD in text:
            value = value + overloadEffect(text, cost)
        return value
    except Exception, e:
        print 'abilityWithoutTarget()', e
                       
def abilityOnSingleTarget(target, text, cost, threatClass):
    try:
        value = cost
        if Effect.DAMAGE in text:
            value = value + damageEffect(target, text, cost)
        if Effect.RESTORE in text:
            value = value + restoreEffect(target, text, cost)
        if Effect.TRANSFORM in text:
            value = value + transformEffect(target, text, cost)
        if Effect.GIVE in text or Effect.HAVE in text:
            value = value + giveEffect(target, text, cost, threatClass)
        if Effect.DESTROY in text:
            value = value + destroyEffect(target, text, cost)
        if Effect.RETURN in text:
            value = value + returnEffect(target, text, cost)
        if Effect.GAIN in text:
            value = value + gainEffect(text, cost)
        if Effect.ADD in text:
            value = value + gainEffect(text, cost)
        if Effect.DRAW in text:
            value = value + drawEffect(text, cost)
        if Effect.EQUIP in text:
            value = value + equipEffect(text, cost)
        if Effect.DISCARD in text:
            value = value + discardEffect(text, cost)
        if Effect.OVERLOAD in text:
            value = value + overloadEffect(text, cost)
        return value
    except Exception, e:
        print 'abilityOnSingleTarget()', e    

def abilityOnGroupOfTargets(text, cost, targets):
    _sum = 0
    for t in targets:
        _sum = _sum + abilityOnSingleTarget(t, text, cost, ThreatClasses.NONE)
    return _sum

def abilityEffectivness(card, text, cost, targets, threatClass):
    try:
        if targets is None and card._text is not None:
            targets = findTargetsInText(card, text)
            if targets is None:
                effectivness = abilityWithoutTarget(text, cost)
            else:
                effectivness = abilityOnGroupOfTargets(text, cost, targets)
        else:
            effectivness = abilityOnSingleTarget(targets, text, cost, threatClass)
        if targets is None and 'random' in text:
            effectivness = (effectivness / len(targets))
        if card.compareCardtype(Cardtype.MINION):
            if card._taunt:
                effectivness = effectivness - 1
                if threatClass == ThreatClasses.DEFENSE_THREAT or threatClass == ThreatClasses.THREAT:
                    effectivness = effectivness - (threatClass - 1)
            if card._windfury:
                effectivness = effectivness - (card._attack/2.0)
            if card._charge:
                effectivness = effectivness - 1 
                if threatClass == ThreatClasses.DEFENSE_THREAT or threatClass == ThreatClasses.THREAT:
                    effectivness = effectivness - (threatClass / 2.0)
            if card._divineShield:
                effectivness = effectivness - 1                
        return effectivness
    except Exception, e:
        print 'abilityEffectivness()', e
        
def nonMinionEffectivness(card, target):
    return abilityEffectivness(card, card._text, card._manacosts, target, ThreatClasses.NONE)       

def minionEffectivness(card, targets, threatClass):
    mana = card._manacosts
    mana = mana - ((card._attack + card._health)/2.0)
    if card._text is not None:
        mana = abilityEffectivness(card, card._text, mana, targets, threatClass) #abilityEffectivness returns negative values for effective cards
    enemyDmg = [c.getAttack() for c in getEnemyCards().values() if c.compareZone(Zone.PLAY) and c.compareCardtype(Cardtype.MINION)]
    dmg = 0
    for d in enemyDmg:
        dmg = dmg + d
    if card._attack > dmg:
        mana = mana - (card._attack - dmg)
    return mana
def playEffectivness(card, target, threatClass):
    if card.compareCardtype(Cardtype.MINION):
        return minionEffectivness(card, target, threatClass)
    else:
        return nonMinionEffectivness(card, target)   
    
def effectivness(option, threatClass):
    try:
        bestAttack = None
        bestPlay = None
        card = getCardByIngameId(option[0])
        if option[2] is not None:
            targets = [getCardByIngameId(Id) for Id in option[2]]                
        else: 
            targets = None
        if option[1] == Option.ATTACK:
            for t in targets:
                eff = attackEffectivness(card, t, threatClass)
                if bestAttack is None or eff < bestAttack[0]:
                    bestAttack = (eff, card, t)
        elif option[1] == Option.PLAY:
            if targets is None:
                bestPlay = (playEffectivness(card, None, threatClass), card, None)
            else:                
                for t in targets:
                    eff = playEffectivness(card, t, threatClass)
                    if bestPlay is None or eff < bestPlay[0]:
                        bestPlay = (eff, card, t)
        if bestAttack is None:
            return (Option.PLAY, bestPlay)
        else:
            return (Option.ATTACK, bestAttack)
    except Exception, e:
        print 'effectivness()', e

def enemyHasDefense(targets):
    try:
        defense = [t for t in targets if (t.compareCardtype(Cardtype.MINION) and t._taunt) or t._id == 'GVG_021' or t.getAttack() >= 6]
        return (len(defense) > 0, defense)
    except Exception, e:
        print 'enemyHasDefense()', e
        
def enemyHasThreat(targets):
    try:
        threat = []
        potentialDmg = 0
        myDamage = [c.getAttack() for c in getMyCards().values() if c.compareZone(Zone.PLAY)]
        Damage = 0
        for d in myDamage:
            Damage = Damage + d
        for t in targets:
            potentialDmg = potentialDmg + t.getAttack()
        if potentialDmg >= getMyHero().getHealth() or Damage < potentialDmg:
            for t in targets:
                atk = t.getAttack()
                if t.compareCardtype(Cardtype.MINION):
                    if t._windfury:
                        atk = atk * 2
                if atk > 3:
                    threat.append(t)
            if len(threat) > 0:
                return (True, threat)
        return (False, threat)
    except Exception, e:
        print 'enemyHasThreat()', e

def sortAfterStrength(minions):
    try:
        retVal = []
        for m in minions:
            if retVal == []:
                retVal.append(m)
                continue
            i = 0
            while i < len(retVal):
                if m.getAttack() > retVal[i].getAttack():
                    retVal.insert(i, m)
                    break
                i = i + 1
            if m not in retVal:
                retVal.append(m)
        return retVal
    except Exception, e:
        print 'sortAfterStrength()', e
                
def isMyDefenseStrong(minions,targets):
    try:
        potentialDmg = 0
        for t in targets:
            potentialDmg = potentialDmg + t.getAttack()
        weaponAtk = [c for c in getEnemyCards().values() if c.compareZone(Zone.WEAPON)]
        if not weaponAtk == []:
            potentialDmg = potentialDmg + weaponAtk[0].getAttack()
            targets.append(weaponAtk[0])
        defense = 0
        taunts = [] 
        for m in minions:
            if m._taunt:
                defense = defense + m.getHealth()
                taunts.append(m)
        if defense >= potentialDmg:
            return True
        elif len(taunts) >= len(targets):
            return True
        else:
            targets = sortAfterStrength(targets)
            for t in targets:
                potentialDmgAfterReduction = potentialDmg - t.getAttack()
                if potentialDmgAfterReduction > defense:
                    return False           
    except Exception, e:
        print 'isMyDefenseStrong()', e
        
def options(options):
    try:
        if len(options) > 1:
            enemyTargets = [c for c in getEnemyCards().values() if c.compareZone(Zone.PLAY)]
            myBoard = [c for c in getMyCards().values() if c.compareZone(Zone.PLAY)]
            defense = enemyHasDefense(enemyTargets)
            threat = enemyHasThreat(enemyTargets)
            threatClass = ThreatClasses.NONE
            if defense[0]:
                if threat[0]:
                    threatClass = ThreatClasses.DEFENSE_THREAT
                else:
                    threatClass = ThreatClasses.DEFENSE
                for index,option in enumerate(options):
                    if option[2] is None:
                        continue
                    else:
                        new_opt_id = []
                        for Id in option[2]:
                            card = getCardByIngameId(Id)
                            if threat[0]:
                                if card in defense[1] or card in threat[1]:
                                    new_opt_id.append(Id)      
                            else:
                                if card in defense[1]:
                                    new_opt_id.append(Id)          
                        options[index] = (option[0], option[1], new_opt_id)  
            elif threat[0]:
                threatClass = ThreatClasses.THREAT
                for option in enumerate(options):
                    if option[2] is None:
                        continue
                    else:
                        new_opt_id = []
                        for Id in option[2]:
                            if getCardByIngameId(Id) in threat[1]:
                                new_opt_id.append(Id)
                        options[index] = (option[0], option[1], new_opt_id)   
                if isMyDefenseStrong(myBoard, enemyTargets):
                    threatClass = ThreatClasses.STRONG_DEFENSE
                    for index, option in enumerate(options):
                        if option[2] is None:
                            continue
                        elif option[1] == Option.ATTACK and getCardByIngameId(option[0])._taunt:
                            new_opt_id = []
                            for Id in option[2]:
                                if not isMyCard(Id) and not getCardByIngameId(Id).compareCardtype(Cardtype.HERO):
                                    new_opt_id.append(Id)
                            options[index] = (option[0], option[1], new_opt_id) 
                        else:
                            new_opt_id = []
                            for Id in option[2]:
                                if not isMyCard(Id) and getCardByIngameId(Id) not in threat[1]:
                                    new_opt_id.append(Id)             
                            options[index] = (option[0], option[1], new_opt_id)        
                            
            efficiency = None
            for option in options:
                if option == options[0]:
                    continue
                eff = effectivness(option, threatClass)
                if efficiency is None:
                    efficiency = eff
                elif eff[0] == Option.PLAY and efficiency[0] == eff[0] and efficiency[1][0] == eff[1][0]:
                    if eff[1][1].compareCardtype(Cardtype.MINION) and efficiency[1][1].compareCardtype(Cardtype.MINION):
                        if eff[1][1]._attack < efficiency[1][1]._attack:
                            eff = efficiency
                elif eff[0] == Option.PLAY and efficiency[0] == eff[0] and efficiency[1][0] > eff[1][0]:
                    efficiency = eff
                elif eff[0] == Option.ATTACK and efficiency[0] == eff[0]:
                    if efficiency[1][0] < eff[1][0]:
                        efficiency = eff
                    elif efficiency[1][0] == eff[1][0]:
                        if eff[1][1].getAttack() > efficiency[1][1].getAttack():
                            efficiency = eff
                elif eff[0] == Option.ATTACK and not efficiency[0] == eff[0]:
                    if efficiency[0] < -7 and eff[1][0] == -2:
                        efficiency = eff
                elif eff[0] == Option.PLAY and not efficiency[0] == eff[0]:
                    if eff[1][0] > -7:
                        efficiency = eff
            if efficiency[0] == Option.PLAY and efficiency[1][0] > 0:
                return options[0]
            else:
                return (efficiency[0], efficiency[1][1], efficiency[1][2])              
    except Exception, e:
        print 'options()', e            
