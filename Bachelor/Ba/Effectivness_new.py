from Board import getCardByIngameId,getEnemyMinionsInPlay, getEnemyHandcardCount,\
    getMyMinionsInPlay, getEnemyHero, getEnemyWeapon, getMyWeapon, getMyHandcards,\
    getMyMana, getMyHero, isMyCard, getMyHandcardCount
from Util_new import Cardtype, Effect, getRaceDict, split, Option


def damageEffect(targets, text, specialTarget, targetsBesideMain):
    try:
        specTarIsDead = False
        extraKills = 0
        if 'deal' in text:
            amount = split(text, 'deal', 'damage')
            if '-' in amount:
                a1, a2 = amount.split('-')
                amount = ((int(a1) + int(a2))/2.0)
            elif amount == '':
                pass
            else:
                amount = int(amount)
        value = 0
        if type(targets) is list:
            for t in targets:
                if not isMyCard(t._ingameID):
                    if t.compareCardtype(Cardtype.HERO):
                        value = value - amount
                        if t.getHealth() <= 0:
                            value = value - 10
                    elif t.compareCardtype(Cardtype.MINION) and t._divineShield:
                        value = value - 1 
                    else:
                        if amount == t.getHealth():  
                            if t == specialTarget:
                                specTarIsDead = True
                            elif t in targetsBesideMain:
                                extraKills = extraKills + 1
                            value = value - amount - (t._manacosts/2.0)
                        elif amount > t.getHealth():
                            if t == specialTarget:
                                specTarIsDead = True
                            elif t in targetsBesideMain:
                                extraKills = extraKills + 1
                            value = value - t.getHealth() - (t._manacosts/2.0)
                        else:
                            value = value - amount 
                else:
                    if t.getHealth() >= amount:
                        value = value + t.getHealth() + t._manacosts
                    else:
                        value = value + amount  
        else:
            if not isMyCard(targets._ingameID):    
                if targets.compareCardtype(Cardtype.HERO):
                    value = value - amount
                    if targets.getHealth() <= 0:
                        value = value - 10
                elif targets.compareCardtype(Cardtype.MINION) and targets._divineShield:
                    value = value - 1 
                else:
                    if amount == targets.getHealth():
                        value = value - (targets.getHealth() - (targets._manacosts/2.0))
                        if targets == specialTarget:
                            specTarIsDead = True
                        elif t in targetsBesideMain:
                            extraKills = extraKills + 1
                        value = value - amount - (targets._manacosts/2.0)
                    elif amount > targets.getHealth():
                                if targets == specialTarget:
                                    specTarIsDead = True
                                elif targets in targetsBesideMain:
                                    extraKills = extraKills + 1
                                value = value - targets.getHealth() - (targets._manacosts/2.0)
                    else:
                        value = value - amount 
            else:
                if targets.getHealth() >= amount:
                    value = value + amount  
                else:
                    value = value + targets.getHealth() + targets._manacosts 
        if specTarIsDead:
            value = value - (10 + extraKills)
        if ('split' in text or 'random' in text) and type(targets) == list:
            value = value / (float(len(targets)))
    
        return value
    except Exception, e:
        print 'damageEffect()', e
        
def restoreEffect(targets, text):
    try:
        value = 0
        if 'full health' in text:
            if type(targets) == list:
                for t in targets:
                    if isMyCard(t._ingameID):
                        value = value - t.getDamage()
                    else:
                        value = value + t.getDamage()
            else:
                if isMyCard(targets._ingameID):
                    value = value - targets.getDamage()
                else:
                    value = value + targets.getDamage()
        else:
            amount = int(split(text, 'restore', 'health'))
            if type(targets) == list:
                for t in targets:
                    if isMyCard(t._ingameID):
                        if amount < t.getDamage():
                            value = value - amount
                        else:
                            amount = value - t.getDamage()
                    else:
                        if amount < t.getDamage():
                            value = value + amount
                        else:
                            value = value + t.getDamage()
            else:
                if isMyCard(targets._ingameID):
                    if amount < targets.getDamage():
                        value = value - amount
                    else:
                        value = value - targets.getDamage()
                else:
                    if amount < targets.getDamage():
                        value = value + amount
                    else:
                        value = value + targets.getDamage()
        return value
    except Exception, e:
        print 'restoreEffect()', e
        
def transformEffect(targets, text, specialTarget):
    try:
        if 'transform' in text:
            health, atk = text.split('/')
            health = int(health.split('into a ')[1])
            atk = int(atk.split(' ')[0])
        if not isMyCard(targets._ingameID):
            value = ((atk - targets.getAttack()) + (health - targets.getHealth()) / 2.0)
            if targets == specialTarget and value < 0:
                value = value - 10
        else:
            value = ((targets.getAttack() - atk) + (targets.getHealth() - health) / 2.0)
        return value
    except Exception, e:
        print 'transformEffect()', e
        
def giveEffect(targets, text):
    try:
        atk = 0
        hlt = 0
        if 'attack' in text and not 'health' in text:
            atk = int(split(text, '+', ' '))
        elif 'health' in text and not 'attack' in text:
            hlt = int(split(text, '+', ' '))
        else:
            atk = int(split(text, '+', '/'))
            hlt = int(split(text, '+', ' '))
        value = 0
        if targets is not None:
            if type(targets) == list:
                for t in targets:
                    if isMyCard(t._ingameID):
                        value = value - ((atk+hlt)/2.0)
                    if 'charge' in text:
                        value = value - 1
                    if 'taunt' in text:
                        value = value - 1
                    if 'windfury' in text:
                        value = value - 2
                    if 'divine shield' in text:
                        value = value - 1
                    if 'stealth' in text:
                        value = value - 1
                    if 'end of turn' in text:
                        value = value + 1
                    else:
                        value = value - ((atk+hlt)/2.0)    
            else:
                if isMyCard(targets._ingameID):
                    value = value - ((atk+hlt)/2.0)
                    if 'charge' in text:
                        value = value - 1
                    if 'taunt' in text:
                        value = value - 1
                    if 'windfury' in text:
                        value = value - 2
                    if 'divine shield' in text:
                        value = value - 1
                    if 'stealth' in text:
                        value = value - 1
                    if 'end of turn' in text:
                        value = value + 1
                else:
                    value = value - ((atk+hlt)/2.0)
        return value
    except Exception, e:
        print 'giveEffect()', e     
          
def destroyEffect(targets, text, specialTarget, targetsBesideMain):
    try:
        specTarIsDead = False
        extraKills = 0
        value = 0
        if type(targets) is list:
            for t in targets:
                if not isMyCard(t._ingameID):
                    value = value - t._manacosts
                    if t == specialTarget:
                        specTarIsDead = True
                    if t in targetsBesideMain:
                        extraKills = extraKills + 1
                else:
                    if amInStrongerPosition():
                        value = value + (2 * t._manacosts)
                    else:
                        value = value + t._manacosts
        else:
            if not isMyCard(t._ingameID):
                value = value - t._manacosts
                if t == specialTarget:
                    specTarIsDead = True
            else:
                value = value + t._manacosts
        if specTarIsDead:
            value = value - (10 + extraKills)
        return value
    except Exception, e:
        print 'destroyEffect()', e
        
def returnEffect(targets, text, specialTarget, targetsBesideMain):
    try:
        value = 0
        extraReturns = 0
        specTarIsRet = False
        if type(targets) == list:
            for t in targets:
                if not isMyCard(t._ingameID):
                    value = value - t._manacosts
                    if t == specialTarget:
                            specTarIsRet = True
                    if t in targetsBesideMain:
                        extraReturns = extraReturns + 1
                else:
                    if amInStrongerPosition():
                        value = value + (2 * t._manacosts)
                    else:
                        value = value + t._manacosts
        else:
            if not isMyCard(t._ingameID):
                value = value - t._manacosts
                if t == specialTarget:
                    specTarIsRet = True
        if specTarIsRet:
            value = value - (10 + extraReturns)
        return value
    except Exception, e:
        print 'returnEffect()', e    
            
def gainEffect(text):
    try:
        if 'mana crystal' in text:
            try: 
                mana = int(split(text, 'gain ', ' mana'))
            except:
                if 'an' in text:
                    mana = 1
            if 'this turn only' in text:
                hand = getMyHandcards()
                resources = getMyMana()
                cardWithHigherCosts = False
                for c in hand:
                    if c.compareCardtype(Cardtype.MINION) and c._manacosts == resources + mana:
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
            return (-1 * (hlt/2.0))
        elif 'attack' in text:
            atk = int(split(text, '+', 'attack'))
            return (-1 * (atk/2.0))
        elif '+' in text and '/' in text:
            atk = int(split(text, '+', '/'))
            hlt = int(text.split('/+')[1][:1])
            return (-1 * ((atk + hlt)/2.0))
    except Exception, e:
        print 'gainEffect()', e   
             
def addEffect(text):
    try:
        if 'spare part' in text:
            return -1
    except Exception, e:
        print 'addEffect()', e  
              
def drawEffect(text):
    try:
        amount = split(text, 'draw ', ' card')
        try:
            amount = int(amount)
        except:
            if amount == 'a':
                amount = 1
            elif amount == 'two':
                amount = 2
        value = -1.5 * amount
        if 'each player draw' in text:
            if getEnemyHandcardCount() + amount > 10:
                value = value - 1
            else:
                value = value + 1.5
            if getMyHandcardCount() + amount > 10:
                value = 0
        elif 'your opponent draw' in text:
            if getEnemyHandcardCount() + amount > 10:
                value = value - 1.5
            else:
                value = -1 * value
        else:
            if getMyHandcardCount() + amount > 10:
                value = 0
        return value 
    except Exception, e:
        print 'drawEffect()', e    
        
def equipEffect(text):
    try:
        atk = int(split(text, 'equip a ' '/'))
        hlt = int(split(text, '/', ''))
        return (-1 * ((atk + hlt)/2.0))
    except Exception, e:
        print 'equipEffect()', e  
          
def discardEffect(text):
    try:
        try:
            amount = split(text, 'discard ', ' random')
            if amount == 'a':
                return 1
            elif amount == 'two':
                return 2
        except:
            return 3                
    except Exception, e:
        print 'discardEffect()', e
            
def summonEffect(text):
    try:
        amount = split(text, 'summon', '/')
        amount, atk = amount.split(' ')
        hlt = int(split('/', ' '))
        atk = int(atk)
        extra = 0
        if amount == 'a':
            amount = 1
        elif amount == 'two':
            amount = 2
        elif amount == 'three':
            amount = 3
        elif amount == 'five':
            amount = 5
        mc = len(getMyMinionsInPlay())
        if mc == 7:
            return 0
        elif mc + amount > 7:
            amount = 7 - mc
        if 'with taunt' in text or 'with charge' in text:
            extra = amount * -1 
        return ((-1 * ((atk+hlt)/2.0) * amount) + extra)
    except Exception, e:
        print 'summonEffect()', e 
        
def costEffect(text):
    try:
        if 'cost' in text:
            amount = int(split(text, '(', ')'))
            if 'less' in text:
                return (-1 * amount)
            elif 'more' in text:
                return amount
    except Exception, e:
        print 'costEffect()', e 
        
def overloadEffect(text):
    try:
        amount = split(text, 'overload:', ')')
        amount = int(amount.split('(')[1])
        return round(amount/2.0,0)
    except Exception, e:
        print 'overloadEffect()', e

def findTargetsInText(card):
    try:
        if card._text == None:
            return None
        text = card._text
        _race = None
        for race in getRaceDict().values():
            if race in text:
                _race = race
                break
        if 'enemies' in text or 'enemy' in text:
            cards = getEnemyMinionsInPlay()
            cards.append(getEnemyHero())
        elif 'friendly' in text or 'your' in text:
            cards = getMyMinionsInPlay()
            cards.append(getMyHero())
        else:
            if 'all' in text or 'other' in text: 
                cards = (getEnemyMinionsInPlay() + getMyMinionsInPlay())
                cards.append(getEnemyHero())
                cards.append(getMyHero())
            else:
                cards = None
        if _race is not None and cards is not None:
            if _race == 'hero':
                _cards = [c for c in cards if c.compareCardtype(Cardtype.HERO)]
                cards = _cards
            elif _race == 'character':
                return cards
            else:
                if _race == 'minion':
                    _cards = [c for c in cards if c.compareCardtype(Cardtype.MINION)]
                else:
                    _cards = [c for c in cards if c.compareCardtype(Cardtype.MINION) and c._race == _race]   
                cards = _cards
        return cards
    except Exception, e:
        print 'findTargetsInText()', e

def cardTextValue(card, target, targetsBesideMain):
    try:
        text = card._text
        value = 0
        if target is None:
            targets = findTargetsInText(card)
        else:
            targets = target
        if Effect.DAMAGE in text:
            value = value + damageEffect(targets, text, target, targetsBesideMain)
        if Effect.RESTORE in text:
            value = value + restoreEffect(targets, text)
        if Effect.TRANSFORM in text:
            value = value + transformEffect(targets, text, target)
        if Effect.GIVE in text or Effect.HAVE in text:
            value = value + giveEffect(targets, text)
        if Effect.DESTROY in text:
            value = value + destroyEffect(targets, text, target, targetsBesideMain)
        if Effect.RETURN in text:
            value = value + returnEffect(targets, text, target, targetsBesideMain)
        if Effect.GAIN in text:
            value = value + gainEffect(text)
        if Effect.ADD in text:
            value = value + addEffect(text)
        if Effect.DRAW in text:
            value = value + drawEffect(text)
        if Effect.EQUIP in text:
            value = value + equipEffect(text)
        if Effect.DISCARD in text:
            value = value + discardEffect(text)
        if Effect.SUMMON in text:
            value = value + summonEffect(text)
        if Effect.OVERLOAD in text:
            value = value + overloadEffect(text)
        return value
    except Exception, e:
        print 'cardTextValue()', e
        
def minionEffectivness(card, target, targetsBesideMain):
    try:
        specialValue = 0
        if card._taunt:
            specialValue = specialValue - 1
        if card._windfury:
            specialValue = specialValue - (card._attack/2.0)
        if card._charge:
            specialValue = specialValue - 1 
        if card._divineShield:
            specialValue = specialValue - 1 
        if card._text is None:
            return (-1 * ((card.getAttack()+card.getHealth())/2.0)) + specialValue
        else:
            return (-1 * ((card.getAttack()+card.getHealth())/2.0)) + cardTextValue(card, target, targetsBesideMain) + specialValue
    except Exception, e:
        print 'minionEffectivness()', e
        
def nonMinionEffectivness(card, target, targetsBesideMain):
    try:
        return cardTextValue(card, target, targetsBesideMain)
    except Exception, e:
        print 'nonMinionEffectivness()', e
        
def attackEffectivness(attacker, target):
    try:
        value = 0
        atk = attacker.getHealth() - target.getAttack()
        tar = target.getHealth() - attacker.getAttack()
        if not isMyCard(target._ingameID) and not target.compareCardtype(Cardtype.HERO):
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
                        value = attacker._manacosts
            elif attacker._divineShield:
                if tar <= 0:
                    value = (target._manacosts * -1) - 1
                else:
                    value = 0
            elif target.getHealth() == attacker.getAttack():
                value = (target._manacosts * -1) - 0.5
            elif target.getHealth() < attacker.getAttack():
                value = target._manacosts * -1
            else: 
                value = 0
            if atk > 0:
                if atk == attacker.getHealth():
                    value = value - 1
            else:
                value = value + attacker._manacosts
        elif not isMyCard(target._ingameID) and target.compareCardtype(Cardtype.HERO):
            value = (-1 * attacker.getAttack())
        if tar > 0 and not target.compareCardtype(Cardtype.HERO):
            value = value + 1
        elif tar <= 0 and target.compareCardtype(Cardtype.HERO):
            value = value - 10
        return value
    except Exception, e:
        print 'attackEffectivness()', e
        
def effectivness(card, target, targetsBesideMain, option):
    try:
        if option == Option.ATTACK:
            return attackEffectivness(card, target)
        elif option == Option.PLAY:
            if card.compareCardtype(Cardtype.MINION):
                return card._manacosts + minionEffectivness(card, target, targetsBesideMain)
            else:
                return card._manacosts + nonMinionEffectivness(card, target, targetsBesideMain)
    except Exception, e:
        print 'effectivness()', e

def getEnemyDmg():
    try:
        minions = getEnemyMinionsInPlay()
        minionDmg = 0
        for m in minions:
            if m._windfury:
                minionDmg = minionDmg + (2 * m.getAttack())
            else:
                minionDmg = minionDmg + m.getAttack()
        weapon = getEnemyWeapon()
        try:
            return minionDmg + weapon[0].getAttack()
        except:
            return minionDmg
    except Exception, e:
        print 'getEnemyDmg()', e

def getMyDmg():
    try:
        minions = getMyMinionsInPlay()
        minionDmg = 0
        for m in minions:
            if m._windfury:
                minionDmg = minionDmg + (2 * m.getAttack())
            else:
                minionDmg = minionDmg + m.getAttack()
        weapon = getMyWeapon()
        try:
            return minionDmg + weapon[0].getAttack
        except:
            return minionDmg
    except Exception, e:
        print 'getMyDmg()', e

def hasEnemyDefense():
    try:
        minions = getEnemyMinionsInPlay()
        defense = []
        for m in minions:
            if m._taunt:
                defense.append(m)
            elif m._id == 'GVG_021':
                defense.append(m)
        if len(defense) > 0:
            return (True, defense)
        else:
            return (False, [])
    except Exception, e:
        print 'hasEnemyDefense()', e

def haveIDefense():
    try:
        minions = getMyMinionsInPlay()
        defense = []
        for m in minions:
            if m._taunt:
                defense.append(m)
            elif m._id == 'GVG_021':
                defense.append(m)
        if len(defense) > 0:
            return (True, defense)
        else:
            return (False, [])
    except Exception, e:
        print 'haveIDefense', e
        
def getPossibleEnemyTargets():
    return getEnemyMinionsInPlay().append(getEnemyHero()) 

def canEnemyDmgMe():
    try:
        defense = haveIDefense()
        if defense[0]:
            fullDefStrength = 0
            for m in defense[1]:
                fullDefStrength = fullDefStrength + m.getHealth()
            minions = getEnemyMinionsInPlay()
            weapon = getEnemyWeapon()
            enemyDmg = getEnemyDmg()
            if (fullDefStrength - enemyDmg) >= 0:
                return False
            elif len(defense[1]) >= (len(minions) + len(weapon)):
                return False
            else:
                enemies = minions + weapon
                for e in enemies:
                    lower_enemyDmg = enemyDmg - e.getAttack()
                    if fullDefStrength < lower_enemyDmg:
                        return True
                return False
        else:
            if getEnemyDmg() == 0:
                return False
            else:
                return True
    except Exception, e:
        print 'canEnemyDmgMe()', e
    
def amInStrongerPosition():
    try:
        if not canEnemyDmgMe() or getMyDmg() > getEnemyDmg():
            return True
        elif getMyDmg() > getEnemyDmg() and getMyHero().getHealth() > getEnemyDmg():
            return True
        elif len(getEnemyMinionsInPlay()) > 0 and len(getMyMinionsInPlay()) == 0:
            return False
        else:
            return False
    except Exception, e:
        print 'amInStrongerPosition()', e
           
def buildAttack(options):
    try:
        resources = getMyMana()
        handcards = getMyHandcards()
        playable = []
        strongestMinion = []
        strongestBuff = []
        for h in handcards:
            if h._manacosts <= resources:
                playable.append(h)
        for option in options:
            if option == options[0]:
                continue
            card = getCardByIngameId(option[0])
            if card in playable:
                if card.compareCardtype(Cardtype.MINION):
                    if option[2] is None:
                        eff = (effectivness(card, findTargetsInText(card), None, option[1]), option[1], card, None)
                    else:
                        eff = None
                        for Id in option[2]:
                            target = getCardByIngameId(Id)
                            tmp = (effectivness(card, getCardByIngameId(Id), None, option[1]), option[1], card, target)
                            if eff is None or tmp[0] > eff[0]:
                                eff = tmp
                    strongestMinion.append(eff)
                else:
                    if Effect.GIVE in card._text or Effect.HAVE in card._text or Effect.EQUIP in card._text or Effect.SUMMON in card._text:
                        if option[2] is None:
                            eff = (effectivness(card, findTargetsInText(card), None, option[1]), option[1], card, None)
                        else:
                            eff = None
                            for Id in option[2]:
                                target = getCardByIngameId(Id)
                                tmp = (effectivness(card, target, None, option[1]), option[1], card, target)
                                if eff is None or tmp[0] > eff[0]:
                                    eff = tmp
                        strongestBuff.append(eff)
        if (len(getMyMinionsInPlay()) <= len(getEnemyMinionsInPlay()) and len(strongestBuff) == 0) or (len(getMyMinionsInPlay()) < 3 and getMyDmg() < 5):
            i = resources
            toPlay = None
            while i >= 0:
                for s in strongestMinion:
                    if s[2]._manacosts == i and toPlay is None:
                        toPlay = s
                    elif s[2]._manacosts == i and toPlay[2]._manacosts == s[2]._manacosts and (s[0] < (toPlay[0] * 1.5) or s[2].getAttack() > toPlay[2].getAttack()):
                        toPlay = s
                    elif s[2]._manacosts == i and toPlay[2]._manacosts > s[2]._manacosts and (s[0] < (toPlay[0] * 1.5) or s[2].getAttack() > toPlay[2].getAttack()):
                        toPlay = s
                i = i - 1 
        else:
            i = 0
            toPlay = None
            while i <= resources:
                for s in strongestBuff:
                    if s[2]._manacosts == i and toPlay is None:
                        toPlay = s
                    elif s[2]._manacosts == i and toPlay[2]._manacosts < s[2]._manacosts and s[0] > (toPlay[0] * 1.5):
                        toPlay = s
                i = i + 1        
        return toPlay 
    except Exception, e:
        print 'buildAttack()', e
        
def organizeDefense(options):
    try:
        handcards = getMyHandcards()
        resources = getMyMana()
        playable_Minions = []
        playable_nonMinions = []
        for h in handcards:
            if h._manacosts <= resources:
                if h.compareCardtype(Cardtype.MINION):
                    if h._taunt:
                        playable_Minions.append(h)
                elif 'taunt' in h._text:
                    if h.compareCardtype(Cardtype.MINION):
                        playable_Minions.append(h)
                    else:
                        playable_nonMinions.append(h)
                elif 'restore' in h._text:
                    if h.compareCardtype(Cardtype.MINION):
                        playable_Minions.append(h)
                    else:
                        playable_nonMinions.append(h)
                elif 'armor' in h._text:
                    if h.compareCardtype(Cardtype.MINION):
                        playable_Minions.append(h)
                    else:
                        playable_nonMinions.append(h)
        bestOptions = []
        if len(getMyMinionsInPlay()) < 7 and len(playable_Minions) > 0:
            bestOptions = []
            for option in options:
                if option == options[0]:
                    continue
                card = getCardByIngameId(option[0])
                if card not in playable_Minions:
                    continue
                if option[2] is None:
                    eff = (effectivness(card, findTargetsInText(card), None, option[1]), option[1], card, None)
                else:
                    eff = None
                    for Id in option[2]:
                        t = getCardByIngameId(Id)
                        tmp = (effectivness(card, t, None, option[1]), option[1], card, t)
                        if eff is None or tmp[0] > eff[0]:
                            eff = tmp[0]
                for index, bo in enumerate(bestOptions):
                    if eff[0] < bo[0]:
                        bestOptions.insert(index, eff)
                        break
                    if eff[0] == bo[0]:
                        if card._manacosts > bo[2]._manacosts:
                            bestOptions.insert(index, eff)
                            break
                if eff not in bestOptions:
                    bestOptions.append(eff)
        elif len(playable_Minions) == 0 or len(getMyMinionsInPlay()) >= 7:
            for option in options:
                if option == options[0]:
                    continue
                card = getCardByIngameId(option[0])
                if card not in playable_nonMinions:
                    continue
                if option[2] is None:
                    eff = (effectivness(card, findTargetsInText(card), None, option[1]), option[1], card, None)
                else:
                    eff = None
                    for Id in option[2]:
                        t = getCardByIngameId(Id)
                        tmp = (effectivness(card, t, None, option), option[1], card, t)
                        if eff is None or tmp[0] > eff[0]:
                            eff = tmp
                for index, bo in enumerate(bestOptions):
                    if eff[0] < bo[0]:
                        bestOptions.insert(index, eff)
                        break
                    if eff[0] == bo[0]:
                        if card._manacosts > bo[2]._manacosts:
                            bestOptions.insert(index, eff)
                            break
                if eff not in bestOptions:
                    bestOptions.append(eff)
        return bestOptions
    except Exception, e:
        print 'organizeDefense()', e

def neutralizeEnemyMinion(target, options, overAllTargets):
    try:
        temp = []
        for option in options:
            if option == options[0]:
                    continue
            if option[2] is not None and target._ingameID in option[2]:
                card = getCardByIngameId(option[0])
                if option[1] == Option.PLAY:
                    if Effect.DAMAGE in card._text or Effect.DESTROY in card._text or Effect.RETURN in card._text or Effect.TRANSFORM in card._text:
                        temp.append(option)
                elif option[1] == Option.ATTACK:
                    temp.append(option)
            elif option[2] is None:
                card = getCardByIngameId(option[0])
                if card._text is not None:
                    if Effect.DAMAGE in card._text or Effect.DESTROY in card._text or Effect.RETURN in card._text or Effect.TRANSFORM in card._text:
                        targets = findTargetsInText(getCardByIngameId(option[0]))
                        if target in targets:
                            temp.append(option)
        bestOptions = []
        for option in temp:
            card = getCardByIngameId(option[0])
            eff = (effectivness(card, target, overAllTargets, option[1]), option[1], card, target)
            for index, bo in enumerate(bestOptions):
                if eff[0] < bo[0]:
                    bestOptions.insert(index, eff)
                    break
                if eff[0] == bo[0]:
                    if card._manacosts < bo[2]._manacosts:
                        bestOptions.insert(index, eff)
                        break
            if eff not in bestOptions:
                bestOptions.append(eff)
        return bestOptions
    except Exception, e:
        print 'neutralizeEnemyMinion()', e  
        
def enemyThreat():
    try:
        enemyTarget = getEnemyMinionsInPlay()
        enemyDmg = getEnemyDmg()
        biggestThreat = []
        toKill = []
        HeroLife = getMyHero().getHealth()
        for e in enemyTarget:
            for index, t in enumerate(biggestThreat):
                if e.getAttack() > t.getAttack():
                    biggestThreat.insert(index, e)
                    break
            if e not in biggestThreat:
                biggestThreat.append(e)
        if amInStrongerPosition():
            defense = hasEnemyDefense()
            if defense[0]:
                toKill = defense[1]
            elif canEnemyDmgMe():
                for t in biggestThreat:
                    if t._windfury and t.getAttack() >= 3:
                        toKill.append(t)
                    elif t.getAttack() > 5:
                        toKill.append(t)
            else:
                return toKill
        else: 
            defense = hasEnemyDefense()
            if defense[0]:
                toKill = defense[1]       
            if enemyDmg >= HeroLife:
                toKill = toKill + biggestThreat
            elif enemyDmg >= (2* round((HeroLife/10.0),0)):
                sumAtk = 0
                for t in biggestThreat:
                    if t._windfury:
                        atk = 2 * t.getAttack()
                    else:
                        atk = t.getAttack()
                    sumAtk = sumAtk + atk
                    if atk >= (0.5 * enemyDmg):
                        toKill.append(t)
                    elif sumAtk < (1.25* round((HeroLife/10.0),0)):
                        toKill.append(t)
                if toKill == []:
                    toKill = biggestThreat
        return toKill
    except Exception, e:
        print 'enemyThreat()', e
                
def doEffective(options):
    try:
        mostEffective = None
        for option in options:
            if option == options[0]:
                continue
            if option[2] is not None and option[1] == Option.ATTACK:
                for Id in option[2]:
                    if not isMyCard(Id) and getCardByIngameId(Id).compareCardtype(Cardtype.HERO):
                        eff = (0, option[1], getCardByIngameId(option[0]), getCardByIngameId(Id))
            elif getCardByIngameId(option[0]).compareCardtype(Cardtype.HERO_POWER):
                eff = None
                card = getCardByIngameId(option[0])
                if option[2] is not None:
                    for Id in option[2]:
                        t = getCardByIngameId(Id)
                        tmp = (effectivness(card, t, None, option[1]), option[1], card, t)
                        if eff is None or tmp[0] < eff[0]:
                            eff = tmp
                else:
                    eff = (effectivness(card, findTargetsInText(card), None, option[1]), option[1], card, t)
            else:
                eff = None
                card = getCardByIngameId(option[0])
                if card._text is not None:
                    if Effect.DRAW in card._text:
                        if option[2] is None:
                            tmp = (effectivness(card, findTargetsInText(card), None, option[1]), option[1], card, None)
                            if eff == None or tmp[0] < eff[0]:
                                eff = tmp
                        else:
                            for Id in option[2]:
                                t = getCardByIngameId(Id)
                                tmp = (effectivness(card, t, None, option[1]), option[1], card, t)
                                if eff is None or tmp[0] < eff[0]:
                                    eff = tmp
                    if Effect.GAIN in card._text and 'mana crystal' in card._text:
                        tmp = effectivness(card, None, None, option[1])
                        if tmp < 1:
                            eff = (tmp, option[1], card, None)
            if eff is not None:
                if mostEffective is None:
                    mostEffective = eff
                elif not mostEffective[1] == Option.ATTACK and eff[1] == Option.ATTACK:
                    mostEffective = eff
                elif mostEffective[0] > eff[0]:
                    mostEffective = eff
        return mostEffective 
    except Exception, e:
        print 'doEffective()', e
                
def putTogether(options):
    try:
        playing = None
        if amInStrongerPosition():
            playing = buildAttack(options)
            if playing is None:
                threats = enemyThreat()
                if not threats == []:
                    for t in threats:
                        playing = neutralizeEnemyMinion(t, options, (len(threats) - 1))
                        if playing == []:
                            playing = doEffective(options)
                            if playing is None:
                                return (0, Option.END, None, None)
                            else:
                                return playing
                        else:
                            return playing[0]
                else:
                    playing = doEffective(options)
                    if playing is None:
                        return (0, Option.END, None, None)
                    else:
                        return playing
            else:
                return playing
        else:
            if canEnemyDmgMe():
                threats = enemyThreat()
                if not threats == []:
                    for t in threats:
                        playing = neutralizeEnemyMinion(t, options, (len(threats) - 1))
                        if playing == []:
                            playing = organizeDefense(options)
                            if playing == []:
                                playing = buildAttack(options)
                                if playing is None:
                                    continue
                                else:
                                    return playing
                            else:
                                return playing[0]
                        else:
                            return playing[0]
                else:
                    playing = organizeDefense(options)
                    if playing == []:
                        playing = buildAttack(options)
                        if playing is None:
                            playing = doEffective(options)
                            if playing is None:
                                return (0, Option.END, None, None)
                            else:
                                return playing
                        else:
                            return playing
                    else:
                        return playing[0]
            else:
                playing = buildAttack(options)
                if playing is None:
                    playing = doEffective(options)
                    if playing is None:
                        return (0, Option.END, None, None)
                    else:
                        return playing
                else:
                    return playing
    except Exception, e:
        print 'putTogether()', e
        
def options(options):
    retVal = putTogether(options)
    return (retVal[1], retVal[2], retVal[3])