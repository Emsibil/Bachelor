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
        self._damage = 0
        
    def set_pos(self, pos):
        if pos == None:
            pass
        self._zonePos = pos

    def get_pos(self):
        if self._zonePos == None:
            pass
        return self._zonePos

    def restore_Health(self, health):
        if health >= self._damage:
            self._damage = 0
        else:
            self._damage = self._damage - health
        
    def takes_Damage(self, dmg):
        self._damage = self._damage + dmg
        if self._damage >= self._health:
            self._zone = 'GRAVEYARD'
        
    def get_damage(self):
        return self._damage