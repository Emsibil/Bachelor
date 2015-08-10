from Util_new import Zone
from Util_new import Cardtype

MY_HERO = None
MY_HERO_POWER = None
E_HERO = None
E_HERO_POWER = None
MY_CARDS = {}
E_CARDS = {}
PLAYERS = {}
MY_MANA = 0
E_MANA = 0

def getMe():
    global ME
    return ME
def getPlayer(Id):
    global PLAYERS
    return PLAYERS[Id]

def getMyHero():
    return [c for c in getMyCards().values() if c.compareCardtype(Cardtype.HERO)][0]
def getMyHeroPower():
    global MY_HERO_POWER
    return MY_HERO_POWER
def getEnemyHero():
    global E_HERO
    return E_HERO
def getEnemyHeroPower():
    global E_HERO_POWER
    return E_HERO_POWER
def getMyCards():
    global MY_CARDS
    return MY_CARDS
def setMyCards(cardDict):
    global MY_CARDS
    MY_CARDS = cardDict
def addCardToMyCards(card):
    cards = getMyCards()
    cards[card._ingameID] = card
    if card.compareZone(Zone.PLAY) and card.compareCardtype(Cardtype.WEAPON):
        card._zone = Zone.WEAPON
    elif card.compareZone(Zone.PLAY) and card.compareCardtype(Cardtype.HERO_POWER):
        card._zone = Zone.HAND
def removeMyCardByIngameId(Id):
    del getMyCards()[Id]    
def getMyHandcardCount():
    count = len([c for c in getMyCards().values() if c.compareZone(Zone.HAND)])
    return (count - 1)
def getMyMinionCount():
    count = len([c for c in getMyCards().values() if c.compareZone(Zone.PLAY)])
    return (count - 1)
def getMyCardByIngameId(Id):
    return getMyCards()[Id]
def isMyCard(Id):
    return (Id in getMyCards())
def getMyMana():
    global MY_MANA
    return MY_MANA
def setMyMana(value):
    global MY_MANA
    MY_MANA = value
def getEnemyMana():
    global E_MANA
    return E_MANA
def setEnemyMana(value):
    global E_MANA
    E_MANA = value
def getEnemyCards():
    global E_CARDS
    return E_CARDS
def setEnemyCards(cardDict):
    global E_CARDS
    E_CARDS = cardDict
def addCardToEnemyCards(card):
    cards = getEnemyCards()
    cards[card._ingameID] = card
    if card.compareZone(Zone.PLAY) and card.compareCardtype(Cardtype.WEAPON):
        card._zone = Zone.WEAPON
    elif card.compareZone(Zone.PLAY) and card.compareCardtype(Cardtype.HERO_POWER):
        card._zone = Zone.HAND
def getEnemyCardByIngameId(Id):
    return getEnemyCards()[Id]
def getEnemyMinionCount():
    count = len([c for c in getEnemyCards().values() if c._zone==Zone.PLAY])
    return (count - 1)
def getEnemyHandcardCount():
    count = len([c for c in getEnemyCards().values() if c.compareZone(Zone.HAND)])
    return (count - 1)
def getCardByIngameId(Id):
    try:
        return getMyCardByIngameId(Id)
    except:
        return getEnemyCardByIngameId(Id)    