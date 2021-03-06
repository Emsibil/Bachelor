from Util_new import path 
              
def CardById(ID):
    cardLib = open(path('cards/cards.info'), 'r').readlines()
    i = 0
    while len(cardLib) > i:
        if 'CardID' in cardLib[i]:
            if cardLib[i].split('CardID: ')[1].split('\n')[0] == ID:
                j = i
                while not cardLib[j] == '\n':
                    j += 1
                return cardLib[i:j]                
        i += 1

def name(card):
    return card[1].split(': ')[1].split('\n')[0]

def cardType(card):
    return card[2].split(': ')[1].split('\n')[0]

def idx(card):
    return card[0].split(': ')[1].split('\n')[0]

def manaCost(card):
    value = card[3].split(': ')[1].split('\n')[0]
    if value == 'None':
        return 0
    else:
        return int(value)
     
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

def race(card):
    r = card[6].split(': ')[1].split('\n')[0]
    if r == 'None':
        return None
    else:
        return r

def _class(card):
    c = card[8].split(': ')[1].split('\n')[0]
    if c == 'None':
        return None
    else:
        return c
    
def text(card):
    t = card[10].split('CardTextInHand: ')[1].split('\n')[0]
    if t == 'None':
        return None
    else:
        return t
    
def Abilities(card):
    try:
        abilityLine = 13
        values = []
        while 'Ability' in card[abilityLine]:
            value = card[abilityLine].split(': ')[1].split('\n')[0]
            if value == 'None':
                break
            else:
                values.append(value)
            abilityLine = abilityLine + 1
        return values
    except:
        return

def durability(card):
    return card[12].split(': ')[1].split('\n')[0]
        