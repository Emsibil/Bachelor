import os

def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path    

              
def CardById(ID):
    cardLib = open(path('doc/cards.info'), 'r').readlines()
    i = 0
    while len(cardLib) > i:
        if 'CardID' in cardLib[i]:
            if cardLib[i].split('CardID: ')[1].split('\n')[0] == ID:
                j = i
                while not cardLib[j] == '\n':
                    j += 1
                return cardLib[i:j]                
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
    