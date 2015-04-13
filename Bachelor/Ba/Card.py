class Card(object):
    def __init__(self, id, name, cardtype, manacosts):
        self._name = name
        self._id = id
        self._cardtype = cardtype
        self._manacosts = manacosts
        self._attack = None
        self._health = None
        self._ability = []
        self._zone = None
        self._zonePos = None
        self._ingameID = None

    #def __setattr__(self, name, value):
     #   if name == 'zone':
      #      try:
       #         if value == 'DECK' or value == 'PLAY' or value == 'HAND':
         #           super(Card, self).__setattr__(name, value)
        #    except:
          #          print 'There is no zone called ' + str(value)
  #      if name == 'zonePos':
   #         try:
    #            if not self._zone == None:
     #               if self._zone == 'PLAY':
      #                  if self._cardtype == 'Minion' and value < 7 and value >= 1:
       #                     super(Card, self).__setattr__(name, value)
        #                elif self._cardtype == 'Hero' and value == 0:
         #                   super(Card, self).__setattr__(name, value)
          #          elif self._zone == 'HAND':
           #             if value >= 1 and value < 11:
            #                super(Card, self).__setattr__(name, value)
           # except: 
            #    print 'Wrong Position or wrong Zone'     