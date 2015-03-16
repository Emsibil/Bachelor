import os
import time

def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

class Card(dict):
     def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self      

def CardById(ID):
    cardLib = open(path('doc/cards.info'), 'r').readlines()
    i = 0
    while len(cardLib) > i:
        if 'CardID' in cardLib[i]:
            if cardLib[i].split('CardID: ')[1].split('\n')[0] == ID:
                j = i
                while not cardLib[j] == '\n':
                    j += 1
                    return Card(card = cardLib[i:j])
        i += 1

def manaCost(card):
    return int(card[3].split(': ')[1].split('\n')[0])

def name(card):
    return card[1].split(': ')[1].split('\n')[0]

def id(card):
    return card[0].split(': ')[1].split('\n')[0]

def cardType(card):
    return card[2].split(': ')[1].split('\n')[0]

