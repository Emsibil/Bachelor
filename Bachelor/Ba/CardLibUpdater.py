import os
import numpy as np


def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

def translate_cardxml():
    cardxml = open(path('doc/cardxml0.txt'), 'r').readlines()
    UsContent = []
    isCopying = False
    f = open(path('doc')+'/cards.xml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    for line in cardxml:
        if isCopying:
            UsContent.append(line)
        if "</CardDefs>           enUS" in line:
            isCopying=True
        if isCopying and "</CardDefs>" in line:
            break;                
    for card in UsContent:
        f.write(card)
        f.write('\n') 

CardSet = np.array([[2, "Basic"],
                    [3 , "Classic"],
                    [4 , "Reward"],
                    [5 , "Missions"],
                    [7 , "System"],
                    [8 , "Debug"],
                    [11 , "Promotion"],
                    [12 , "Curse of Naxxramas"],
                    [13 , "Goblins vs Gnomes"],
                    [16 , "Credits"]])
def getCardSet():
    global CardSet
    return CardSet

CardType = np.array([[3 , "Hero"],
                     [4 , "Minion"],
                         [5 , "Spell"],
                         [6 , "Enchantment"],
                         [7 , "Weapon"],
                         [10 , "Hero Power"]])
def getCardType():
    global CardType
    return CardType

Fraction = np.array([[1 , "Horde"],
                        [2 , "Alliance"],
                        [3 , "Neutral"]])
def getFraction():
    global Fraction
    return Fraction

Rarity = np.array([[0 , "undefined"],
                       [1 , "Common"],
                       [2 , "Free"],
                       [3 , "Rare"],
                       [4 , "Epic"],
                       [5 , "Legendary"]])

def getRarity():
    global Fraction
    return Fraction
    
Race = np.array([[14 , "Murloc"],
                     [15 , "Demon"],
                     [20 , "Beast"],
                     [21 , "Totem"],
                     [23 , "Pirate"],
                     [24 , "Dragon"],
                     [17 , "Mech"]])

def getRace():
    global Race
    return Race

Class = np.array([[0 , "undefined"],
                      [2 , "Druid"],
                      [3 , "Hunter"],
                      [4 , "Mage"],
                      [5 , "Paladin"],
                      [6 , "Priest"],
                      [7 , "Rogue"],
                      [8 , "Shaman"],
                      [9 , "Warlock"],
                      [10 , "Warrior"],
                      [11 , "Dream"]])
def getClass():
    global Class
    return Class
    
Ability = np.array(['190', '189', '197', '194', '191', '218', '349', '217', '220', '212' ]) #Enthaelt noch nicht alle. Nur die markantesten zum Testen.
def getAbility():
    global Ability
    return Ability

enumID = np.array([[185 , "CardName"],
                       [183 , "CardSet"],
                       [202 , "CardType"],
                       [201 , "Fraction"],
                       [199 , "Class"],
                       [203 , "Rarity"],
                       [48 , "Cost"],
                       [251 , "AttackVisualType"],
                       [184 , "CardTextInHand"],
                       [47 , "Attack"],
                       [45 , "Health"],
                       [321 , "Collectible"],
                       [342 , "ArtistName"],
                       [351 , "FlavorText"],
                       [32 , "TriggerVisual"],
                       [330 , "EnchantmentBirthVisual"],
                       [331 , "EnchantmentIdleVisual"],
                       [268 , "DevState"],
                       [365 , "HowToGetThisGoldCard"],
                       [190 , "Taunt"],
                       [364 , "HowToGetThisCard"],
                       [338 , "OneTurnEffect"],
                       [293 , "Morph"],
                       [208 , "Freeze"],
                       [252 , "CardTextInPlay"],
                       [325 , "TargetingArrowText"],
                       [189 , "Windfury"],#
                       [218 , "Battlecry"],#
                       [200 , "Race"],
                       [192 , "Spellpower"],
                       [187 , "Durability"],
                       [197 , "Charge"],#
                       [362 , "Aura"],
                       [361 , "HealTarget"],
                       [349 , "ImmuneToSpellpower"],#
                       [194 , "Divine Shield"],#
                       [350 , "AdjacentBuff"],
                       [217 , "Deathrattle"],#
                       [191 , "Stealth"],#
                       [220 , "Combo"],#
                       [339 , "Silence"],
                       [212 , "Enrage"],#
                       [370 , "AffectedBySpellPower"],
                       [240 , "Cant Be Damaged"],
                       [114 , "Elite"],
                       [219 , "Secret"],
                       [363 , "Poisonous"],
                       [215 , "Recall"],
                       [340 , "Counter"],
                       [205 , "Summoned"],
                       [367 , "AIMustPlay"],
                       [335 , "InvisibleDeathrattle"],
                       [377 , "UKNOWN_HasOnDrawEffect"],
                       [388 , "SparePart"],
                       [389 , "UNKNOWN_DuneMaulShaman"]])
def getEnumId():
    global enumID
    return enumID

def read_cardxml():
    cardxml = open(path('doc/cardxml0.txt'), 'r').readlines()
    UsContent = []
    isCopying = False

    for line in cardxml:     
        if isCopying:
            UsContent.append(line)
        if isCopying and "</CardDefs>" in line:
            break;          
        if ('<CardDefs>' in line) and ('enUS' in line):
            isCopying=True      
    return np.array(UsContent)
  
#After every Update to use    
def singleCards():
    UsContent = read_cardxml()
    newCard = False
    cardContent = []
    strRepOfCards = []
    for line in UsContent:
        if '</Entity>' in line:
            newCard = False
            strRepOfCards.append(readSingleCardInfo(np.array(cardContent)))
            cardContent = []
        if newCard:
            cardContent.append(line)
        if ('<Entity' in line) and ('CardID' in line):
            newCard = True
            cardContent.append(line)
    writeCardsInFile(np.array(strRepOfCards))
    
def convertText(txt):
    if '&lt;' in txt:
        txt = txt.replace('&lt;', '')
    if 'b&gt;' in txt:
        txt = txt.replace('b&gt;', '')
    if '/b&gt;' in txt:
        txt = txt.replace('/b&gt;', '')
    if 'i&gt;' in txt:
        txt = txt.replace('i&gt;', '')
    if '/i&gt;' in txt:
        txt = txt.replace('/i&gt;', '')
    if '$' in txt:
        txt = txt.replace('$' , '')
    if '/ ' in txt:
        txt = txt.replace('/ ', ' ')
    if '/.' in txt:
        txt = txt.replace('/.', '.')
    if '/\n' in txt:
        txt = txt.replace('/\n', '')
    if '#' in txt:
        txt = txt.replace('#', '')
    return txt

def readSingleCardInfo(content):   
    CardSet = getCardSet()
    CardType = getCardType()
    Class = getClass()
    Fraction = getFraction()
    Race = getRace()
    Rarity = getRarity()
    Ability = getAbility()
    enumID = getEnumId()
    
    _ID = 'CardID: None'
    _NAME = 'CardName: None'
    _MANACOST = 'Cost: None'
    _ATTACK = 'Attack: None'
    _LIFE = 'Health: None'
    _RACE = 'Race: None'
    _CLASS = 'Class: None'
    _CARDSET = 'CardSet: None'
    _CARDTYPE = 'CardType: None'
    _FRACTION = 'Fraction: None'
    _RARITY = 'Rarity: None'
    _TEXT = 'Text: None'
    _ABILITY = []
    
    numberOfAbilities = 0
    for line in content:
        if 'enumID' in line:
            ID = str(line).split('enumID="')[1].split('"')[0]
            for id in enumID:
                if id[0] == ID:
                    if ID == '200':
                        value = str(line).split('value="')[1].split('"')[0]
                        for race in Race:
                            if race[0] == value:
                                _RACE = id[1] + ': ' + race[1]
                    elif ID == '183':
                        value = str(line).split('value="')[1].split('"')[0]
                        for card in CardSet:
                            if card[0] == value:
                                _CARDSET =id[1] + ': ' + card[1]
                    elif ID == '202':
                        value = str(line).split('value="')[1].split('"')[0]
                        for card in CardType:
                            if card[0] == value:
                                _CARDTYPE = id[1] + ': '+ card[1]
                    elif ID == '201':
                        value = str(line).split('value="')[1].split('"')[0]
                        for frac in Fraction:
                            if frac[0] == value:
                                _FRACTION = id[1] + ': ' + frac[1]
                    elif ID == '199':
                        value = str(line).split('value="')[1].split('"')[0]
                        for cl in Class:
                            if cl[0] == value:
                                _CLASS = id[1] + ': ' + cl[1]
                    elif ID == '203':
                        value = str(line).split('value="')[1].split('"')[0]   
                        for rare in Rarity:
                            if rare[0] == value:
                                _RARITY = id[1] + ': ' + rare[1]
                    elif ID in Ability:
                        numberOfAbilities += 1
                        _ABILITY.append('Ability'+str(numberOfAbilities)+': ' + id[1])
                    elif ID == '185':
                        name = str(line).split('"String">')[1].split('<')[0]
                        _NAME = id[1]+': '+name
                    elif ID == '48':
                        cost = str(line).split('value="')[1].split('"')[0]
                        _MANACOST = id[1]+': ' + cost
                    elif ID == '47':
                        atk = str(line).split('value="')[1].split('"')[0]
                        _ATTACK = id[1]+': ' + atk
                    elif ID == '45':
                        lf = str(line).split('value="')[1].split('"')[0]
                        _LIFE = id[1]+': ' + lf
                    elif ID == '184':
                        txt = str(line).split('"String">')[1].split('<')[0]
                        _TEXT = id[1]+': ' + convertText(txt)            
        if 'CardID' in line:
            ID = str(line).split('CardID="')[1].split('"')[0]
            _ID = 'CardID: ' + ID
    
    _ABIL = ''
    if len(_ABILITY) == 0:
        _ABIL = 'Ability: None \n\t'
    else:
        for a in _ABILITY:
            _ABIL += a + '\n\t'
    
    return _ID + '\n\t' + _NAME  + '\n\t' + _CARDTYPE + '\n\t'  + _MANACOST + '\n\t' + _ATTACK + '\n\t' + _LIFE + '\n\t' + _ABIL + _RACE + '\n\t' + _FRACTION  + '\n\t' + _CLASS + '\n\t' + _RARITY + '\n\t' + _TEXT + '\n\t' +_CARDSET +'\n'  
                   
def writeCardsInFile(CardArray):
    cardFile = open(path('doc')+'/cards2.info', 'w')
    for card in CardArray:
        cardFile.write(card + '\n')
        
singleCards()