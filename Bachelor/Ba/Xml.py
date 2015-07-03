from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from Util_new import Effect, path
import xml.etree.ElementTree as etree
import os

root = Element('Ability')
def get_root():
    global root
    return root
tree = None
def get_tree():
    global tree
    if tree is None:
        tree = ElementTree(root)
    return tree
edited = Element('Edited')
def get_edited():
    global edited
    edited.text = '1'
card = Element('Card')
def get_card(cardID, *args):
    global card
    card.set('id', cardID)
    for a in args:
        card.append(a)
    card.append(get_edited())
    return card
buff = Element('Buff')
def get_buff(value, name, time):
    global buff
    buff.text = name
    buff.set('value', str(value))
    buff.set('effectTime', time)
    return buff
debuff = Element('Debuff')
def get_debuff(value, name, time):
    global debuff
    debuff.text = name
    debuff.set('value', str(value))
    debuff.set('effectTime', time)
    return debuff
def appendCard(Id, *args):
    abilities = []
    for a in args:
        if a[0] == Effect.Buff:
            abilities.append(get_buff(a[1], a[2]))
        else:
            abilities.append(get_debuff(a[1], a[2]))
    get_root().append(get_card(Id, abilities))

def compareAttribValues(oldValue, newValue):
    if '-' in oldValue:
        v1, v2 = oldValue.split('-')
        v1 = int(v1)
        v2 = int(v2)
        if v1 <= newValue and v2 >= newValue:
            return 0
        elif v1 > newValue:
            v1 = newValue
        elif v2 < newValue:
            v2 = newValue
        return str(v1)+'-'+str(v2)
    else:
        v = int(oldValue)
        if v == newValue:
            return 0
        elif v < newValue:
            return str(v)+'-'+str(newValue)
        elif v > newValue:
            return str(newValue)+'-'+str(v)
    
def rewrite(Id, _tree, *args):
    _root = _tree.getroot()
    for card in tree:
        if card.attrib['id'] == Id:
            change = False
            found = False
            for a in args:
                for child in card:
                    if a[0] == child.tag and a[2] == child.text:
                        found = True
                        changes = compareAttribValues(child.attrib['value'], a[1])
                        if not changes == 0:
                            change = True
                if not found:
                    change = True
                    if a[0] == Effect.Buff:
                        card.append(get_buff(a[1], a[2], a[3]))
                    else:
                        card.append(get_debuff(a[1], a[2], a[3]))
            if not card[len(card) - 1].tag == 'edited':
                tmp = None
                i = 0 
                editIndex = -1
                while i < len(child):
                    if child[i].tag == 'edited':
                        if change:
                            child[i].text = str(int(child[i].text) + 1)
                        editIndex = i
                        tmp = child[i]
                    if i > editIndex:
                        child[i-1] = child[i]
                card[len(card) - 1] = tmp
                
def addInfo(Id, _tree, *args):
    _root = _tree.getroot()
    _root.appendCard(Id, *args)
 
def XML_write(Id, *args):
    if os.path.isfile(path('doc/Ability.xml')):
        _tree = etree.parse(path('doc/Ability.xml'))
        _root = _tree.getroot()
        for card in root:
            if Id in card.attrib:
                rewrite(Id, _tree, *args)
            else:
                addInfo(Id, _tree, *args)
    else:
        appendCard(Id, *args)
        _tree = get_tree()
        _tree.write(path('doc')+'/Ability.xml')        

def readCard(Id):
    _root = get_tree().getroot()
    effects = []
    for card in _root:
        if card.attrib['id'] == Id:
            for effect in card:
                if effect.Tag == Effect.Buff:
                    effects.append((Effect.Buff, effect.attrib['value'], effect.text, effect.attrib['effectTime']))
                else:
                    effects.append((Effect.Debuff, effect.attrib['value'], effect.text, effect.attrib['effectTime']))
        return effects
    
def existCardinfo(Id):
    _root = get_tree().getroot()
    for card in _root:
        if card.attrib['id'] == Id:
            return True
    return False