from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

root = Element('Ability')
def get_root():
    global root
    return root
tree = ElementTree(root)
def get_tree():
    global tree
    return tree
card = Element('Card')
def get_card(cardID):
    global card
    card.set('id', cardID)
    return card
buff = Element('Buff')
def get_buff(value, name):
    global buff
    buff.text = name
    buff.set('value', str(value))
    return buff
debuff = Element('Debuff')
def get_debuff(value, name):
    global debuff
    debuff.text = name
    debuff.set('value', str(value))
    return debuff

def write():
    _tree = get_tree()
    _root = get_root()
    _root.append(get_card('CA_20D').append(element))
    
write()
    
    
    