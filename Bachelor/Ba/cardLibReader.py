import os


def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path    

class Card(object):
    def __init__(self, id, name, cardtype, manacosts):
        self.name = name
        self.id = id
        self.cardtype = cardtype
        self.manacosts = manacosts
        self.attack = None
        self.health = None
        self.ability = []
        self.zone = None
        self.zonePos = None

    def __setattr__(self, name, value):
        if name == 'zone':
            try:
                if value == 'DECK' or value == 'PLAY' or value == 'HAND':
                    super(Card, self).__setattr__(name, value)
            except:
                    print 'There is no zone called ' + str(value)
        if name == 'zonePos':
            try:
                if not self.zone == None:
                    if self.zone == 'PLAY':
                        if self.cardtype == 'Minion' and value < 7 and value >= 1:
                            super(Card, self).__setattr__(name, value)
                        elif self.cardtype == 'Hero' and value == 0:
                            super(Card, self).__setattr__(name, value)
                    elif self.zone == 'HAND':
                        if value >= 1 and value < 11:
                            super(Card, self).__setattr__(name, value)
            except: 
                print 'Wrong Position or wrong Zone' 
                
def CardById(ID):
    cardLib = open(path('doc/cards.info'), 'r').readlines()
    i = 0
    while len(cardLib) > i:
        if 'CardID' in cardLib[i]:
            if cardLib[i].split('CardID: ')[1].split('\n')[0] == ID:
                j = i
                while not cardLib[j] == '\n':
                    j += 1
                createCard(cardLib[i:j])
                break
        i += 1

def manaCost(card):
    value = card[3].split(': ')[1].split('\n')[0]
    if value == 'None':
        return 0
    else:
         return int(value)

def name(card):
    return card[1].split(': ')[1].split('\n')[0]

def id(card):
    return card[0].split(': ')[1].split('\n')[0]

def cardType(card):
    return card[2].split(': ')[1].split('\n')[0]

def attackValue(card):
    value = card[4].split(': ')[1].split('\n')[0]
    if value == 'None':
        return 0
    else:
        return int(value)

def healthValue(card):
    value = card[5].split(': ')[1].split('\n')[0]
    if value == 'None':
        return 0
    else:
        return int(value)
    
def createCard(card):
    cardtype = cardType(card)
    _card = Card(id(card), name(card), cardtype, manaCost(card))
    if cardtype == 'Minion':
        _card.attack = attackValue(card)
        _card.health = healthValue(card)
    if cardtype == 'Hero':
        _card.health = healthValue(card)