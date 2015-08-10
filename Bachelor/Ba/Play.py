from time import sleep
from random import random
from Util_new import Cardtype, Zone, Option
from Effectivness import options
from MouseControl import mouseMove, mouseClick, getMouseMoveCoords,\
    area, mouseDown, mouseUp, getMinionBoard, getOnBoardArea, getMulliganConfirm,\
    getMulliganCardArea, getTurn, getHandcardArea
from Board import getMyMinionCount, getMyCards, getMyHandcardCount,\
    getEnemyMinionCount, isMyCard
    
OPTIONS = []
def addOption(option):
    global OPTIONS
    OPTIONS.append(option)
def getOption(nr):
    global OPTIONS
    return OPTIONS[nr]
def getOptions():
    global OPTIONS
    return OPTIONS
def clearOptions():
    global OPTIONS
    OPTIONS = []

def MulliganChoosing():
    try:
        cards = getMyCards()
        count = getMyHandcardCount()
        change = []
        for card in cards.values():
            if card._id is not None:
                if card.compareZone(Zone.HAND) and card._manacosts >= 4:
                    change.append(card)
                
        for card in change:
            pos = card.get_pos()
            if count == 3: 
                mouseMove(getMouseMoveCoords(area(getMulliganCardArea(pos, (count)))))
            else:
                mouseMove(getMouseMoveCoords(area(getMulliganCardArea(pos, (count - 1)))))
            sleep(random()*1+0.5)
            mouseClick()
            sleep(random()*1+0.5)
    except Exception, e:
        print 'MulliganChoosing()', e
def MulliganConfirm():
    mouseMove(getMouseMoveCoords(area(getMulliganConfirm())))
    sleep(2)
    mouseClick()
        
def EndTurn():
    mouseMove(getMouseMoveCoords(area(getTurn())))    
    sleep(1)
    mouseDown()
    print "down"
    sleep(0.5)
    mouseUp()
    print "up"

def playMinionWithTarget(card, target):
    try:   
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        sleep(1)
        mouseDown()   
        sleep(0.5)
        zone = int((random()*(getMyMinionCount() + 1))) + 1
        mouseMove(getMouseMoveCoords(area(getMinionBoard(getMyMinionCount() + 1)[zone])))
        sleep(0.5)
        mouseUp()
        sleep(0.5)
        if isMyCard(target._ingameId):
            c = getMyMinionCount()
        else:
            c = getEnemyMinionCount()
        mouseMove(getMouseMoveCoords(getOnBoardArea(c, target)))
        sleep(0.5)
        mouseClick()
    except Exception, e:
        print 'playMinionWithTarget()', e
        
def playCardWithTarget(card, target):
    try:   
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        sleep(1)
        mouseDown()   
        sleep(0.5)
        if isMyCard(target._ingameID):
            c = getMyMinionCount()
        else:
            c = getEnemyMinionCount()
        mouseMove(getMouseMoveCoords(getOnBoardArea(c, target)))
        sleep(0.5)
        mouseClick()
    except Exception, e:
        print 'playCardWithTarget()', e
        
def playCard(card):
    try:
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        sleep(1)
        mouseDown()   
        sleep(0.5)
        mouseMove(getMouseMoveCoords(area(getMinionBoard(7)[int(random()*7)])))
        sleep(0.5)
        mouseUp()
    except Exception, e:
        print 'playCard()', e
        
def playMinion(card):
    try:
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        sleep(1)
        mouseDown()   
        sleep(0.5)
        zone = int((random()*(getMyMinionCount() + 1))) + 1
        mouseMove(getMouseMoveCoords(area(getMinionBoard(getMyMinionCount() + 1)[zone])))
        sleep(0.5)
        mouseUp()
    except Exception, e:
        print 'playMinion()', e
                
def attack(card, target):
    try:
        mouseMove(getMouseMoveCoords(getOnBoardArea(getMyMinionCount(), card)))
        sleep(1)
        mouseClick()   
        sleep(0.5)
        mouseMove(getMouseMoveCoords(getOnBoardArea(getEnemyMinionCount(), target)))
        sleep(0.5)
        mouseClick()
    except Exception, e:
        print 'attack()', e
        
def chooseOption(opt):
    try:
        if len(opt) == 1:
            EndTurn()
        else:
            try:
                option, card, target = options(opt)
                clearOptions()
            except:
                EndTurn()
                return
            if option == Option.PLAY:
                if target is None:
                    if card.compareCardtype(Cardtype.MINION):
                        playMinion(card)
                    else:
                        playCard(card)
                else:
                    if card.compareCardtype(Cardtype.MINION):
                        playMinionWithTarget(card, target)
                    else:
                        playCardWithTarget(card, target)
            elif option == Option.ATTACK:
                attack(card, target)
            else:
                EndTurn()
    except Exception, e:
        print 'chooseOption()', e        
        
    
    