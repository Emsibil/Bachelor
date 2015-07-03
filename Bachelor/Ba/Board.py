from Util_new import Zone

ME = 'Emsibil'
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
def getPlayers():
    global PLAYERS
    return PLAYERS
def isMe(Id):
    return getPlayers[Id] == getMe()
def getMyHero():
    global MY_HERO
    return MY_HERO
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
def addMinionToMyCards(card, pos):
    cards = getMyCards()
    card.set_pos(pos)
    card._zone = Zone.PLAY
    cards[card._ingameID] = card
def addHandcardToMyCards(card, pos):
    cards = getMyCards()
    card.set_pos(0)
    card._zone = Zone.HAND
    cards[card._ingameID] = card
def removeMyCardByIngameId(Id):
    del getMyCards()[Id]    
def getMyHandcardCount():
    count = len([c for c in getMyCards().values() if c._zone== Zone.HAND])
    return (count - 1)
def getMyMinionCount():
    count = len([c for c in getMyCards().values() if c._zone==Zone.PLAY])
    return (count - 1)
def getMyCardByIngameId(Id):
    return getMyCards()[Id]
def reorderMyHandcards(pos):
    cards = getMyCards()
    for c in cards:
        if cards[c]._zone == Zone.HAND and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1
def isMyCard(Id):
    return (Id in getMyCards())
def getMyMana():
    global MY_MANA
    return MY_MANA
def getEnemyMana():
    global E_MANA
    return E_MANA

def getEnemyCards():
    global E_CARDS
    return E_CARDS
def addMinionToEnemyCards(card, pos):
    cards = getEnemyCards()
    card.set_pos(pos)
    card._zone = Zone.PLAY
    cards[card._ingameID] = card
def addHandcardToEnemyCards(card, pos):
    cards = getEnemyCards()
    card.set_pos(0)
    card._zone = Zone.HAND
    cards[card._ingameID] = card
def getEnemyCardByIngameId(Id):
    return getEnemyCards()[Id]
def reorderEnemyMinionsOnBoard(pos):
    cards = getEnemyCards()
    for c in cards:
        if cards[c]._zone == Zone.PLAY and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1
def reorderMyMinionsOnBoard(pos):
    cards = getMyCards()
    for c in cards:
        if cards[c]._zone == Zone.PLAY and cards[c]._zonePos > pos:
            cards[c]._zonePos = cards[c]._zonePos - 1
def getEnemyMinionCount():
    count = len([c for c in getEnemyCards().values() if c._zone==Zone.PLAY])
    return (count - 1)

def getCardByIngameId(Id):
    try:
        return getMyCardByIngameId(Id)
    except:
        return getEnemyCardByIngameId(Id)
        