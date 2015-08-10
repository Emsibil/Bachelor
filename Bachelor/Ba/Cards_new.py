from cardLibReader import attackValue, healthValue, manaCost,\
    CardById, cardType, text, name, durability, race, Abilities
from Util_new import Cardtype, Ability

class Card(object):
    def __init__(self, Id, ingameId, name, cardtype, manacosts):
        self._name = name
        self._id = Id
        self._cardtype = cardtype
        self._manacosts = manacosts
        self._zone = None
        self._zonePos = None
        self._ingameID = ingameId
        self._text = None
        self._exhausted = False

    def set_pos(self, pos):
        if pos == None:
            pass
        self._zonePos = pos

    def get_pos(self):
        if self._zonePos == None:
            pass
        return self._zonePos
    
    def compareZone(self, zone):
        return self._zone == zone
    
    def compareCardtype(self, cardtype):
        return self._cardtype == cardtype

    def set_exhausted(self, value):
        if value == 1:
            self._exhausted = True
        else:
            self._exhausted = False

class Minion(Card):
    def __init__(self, Id, ingameId, name, cardtype, manacosts, attack, health):
        Card.__init__(self, Id, ingameId, name, cardtype, manacosts)
        self._attack = attack
        self._health = health
        self._taunt = False
        self._stealth = False
        self._charge = False
        self._divineShield = False
        self._battlecry = False
        self._deathrattle = False
        self._windfury = False
        self._frozen = False
        self._immune = False
        self._spellDamage = 0
        self._damage = 0
        self._attackBuff = 0
        self._healthBuff = 0
        self._ingameTurns = 0
        self._race = None

        
    def restoreHealth(self, health):
        if health >= self._damage:
            self._damage = 0
        else:
            self._damage = self._damage - health
        
    def takes_Damage(self, dmg):
        self._damage = dmg
            #if self._damage >= self._health:
                #   self._zone = 'GRAVEYARD'
            
    def getHealth(self):
        return self._health + self._healthBuff
    
    def getAttack(self):
        return self._attack + self._attackBuff
    
    def get_damage(self):
        return self._damage
    
    def mayAttack(self):
        if self._ingameTurns == 0 and self._charge and not self._frozen:
            return True
        elif self._ingameTurns > 0 and not self._frozen:
            return True
        return False

    def changeAbility(self, ability, value):
        if ability == Ability.TAUNT:
            self._taunt = value
        elif ability == Ability.CHARGE:
            self._charge = value
        elif ability == Ability.WINDFURY:
            self._windfury = value
        elif ability == Ability.BATTLECRY:
            self._battlecry = value
        elif ability == Ability.DEATHRATTLE:
            self._deathrattle = value
        elif ability == Ability.DIVINESHIELD:
            self._divineShield = value
        elif ability == Ability.STEALTH:
            self._stealth = value
    
    def increaseTurns(self):
        self._ingameTurns = self._ingameTurns + 1
            
class Hero(Card):
    def __init__(self, Id, ingameId, name, cardtype, manacosts, health):
        Card.__init__(self, Id, ingameId, name, cardtype, manacosts)
        self._attack = None
        self._health = health
        self._damage = 0
        self._attackBuff = 0
        self._armor = 0
        self._frozen = False
        self._immune = False
        
    def restoreHealth(self, health):
        if health >= self._damage:
            self._damage = 0
        else:
            self._damage = self._damage - health
            
    def getHealth(self):
        return self._health

    def getAttack(self):
        if self._attack is None:
            return 0
        return self._attack
    
    def takes_Damage(self, dmg):
        self._damage = dmg
        
    def get_damage(self):
        return self._damage
                     
class Weapon(Card):
    def __init__(self, Id, ingameId, name, cardtype, manacosts, attack, durability):
        Card.__init__(self, Id, ingameId, name, cardtype, manacosts)
        self._attack = attack
        self._durability = durability
        self._deathrattle = False
        self._battlecry = False
        
    def takes_Damage(self, dmg):
        self._durability = dmg
 
def createUNKONWCard(Id):
    return Card(None, Id, None, None, None)
       
def createCard(Id, CardId):
    try:
        if CardId == '':
            return createUNKONWCard(Id)
        else:
            card = CardById(CardId)
            cardtype = cardType(card)
            _card = None
            if cardtype == Cardtype.MINION:
                _card = Minion(id(card), Id, name(card), cardtype, manaCost(card), attackValue(card), healthValue(card))
                abi = Abilities(card)
                if abi is not None:
                    for a in abi:
                        _card.changeAbility(a, True)
                _card._race = race(card)
            elif cardtype == Cardtype.HERO:
                _card = Hero(id(card), Id, name(card), cardtype, manaCost(card), healthValue(card))
            elif cardtype == Cardtype.WEAPON:
                _card = Weapon(id(card), Id, name(card), cardtype, manaCost(card), attackValue(card), durability(card))
            else:
                _card = Card(id(card), Id, name(card), cardtype, manaCost(card))
            _card._text = text(card)
            return _card
    except Exception, e:
        print 'createCard()', e
        
def editAbility(self, ability, value):
    if value == 1:
        if ability not in self._ability:
            self._ability.append(ability)
    else:
        if ability in self._ability:
            self._ability.remove(ability)