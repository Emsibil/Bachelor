class Card(object):
    def __init__(self, idx, name, cardtype, manacosts):
        self._name = name
        self._id = idx
        self._cardtype = cardtype
        self._manacosts = manacosts
        self._attack = None
        self._health = None
        self._ability = []
        self._zone = None
        self._zonePos = None
        self._ingameID = None
        self._enchanment = []
        self._durability = None
        self._takenDamage = 0
        
    def set_pos(self, pos):
        if pos == None:
            pass
        self._zonePos = pos

    def get_pos(self):
        if self._zonePos == None:
            pass
        return self._zonePos
    
    def set_takenDamage(self, dmg):
        self._takenDamage = self._takenDamage + dmg
        
    def get_takenDamage(self):
        return self._takenDamage
