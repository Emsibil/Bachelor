import time
from random import random
from Bachelor.Ba.Util_new import Cardtype
from Bachelor.Ba.Effective import options
#from Bachelor.Ba.LogReader import playMinionWithTarget
from Bachelor.Ba.MouseControl import mouseMove, mouseClick, getMouseMoveCoords,\
    area, mouseDown, mouseUp, getMinionBoard, getOnBoardArea, getMulliganConfirm,\
    getMulliganCardArea, getTurn, getHandcardArea
from Bachelor.Ba.Board import getMyMinionCount, getMyCards, getMyHandcardCount,\
    getEnemyMinionCount, isMyCard

def MulliganChoosing():
    cards = getMyCards()
    count = getMyHandcardCount()
    change = []
    for card in cards.values():
        if card._manacosts >= 4:
            change.append(card)
            
    for card in change:
        pos = card._zonePos
        if count == 3: 
            mouseMove(getMouseMoveCoords(area(getMulliganCardArea(pos, (count)))))
        else:
            mouseMove(getMouseMoveCoords(area(getMulliganCardArea(pos, (count - 1)))))
        time.sleep(random()*1+0.5)
        mouseClick()
        time.sleep(random()*1+0.5)

def MulliganConfirm():
    mouseMove(getMouseMoveCoords(area(getMulliganConfirm())))
    time.sleep(2)
    mouseClick()
        
def EndTurn():
    mouseMove(getMouseMoveCoords(area(getTurn())))    
    time.sleep(1)
    mouseDown()
    print "down"
    time.sleep(0.5)
    mouseUp()
    print "up"

def playMinionWithTarget(card, target):
    try:   
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        time.sleep(1)
        mouseDown()   
        time.sleep(0.5)
        zone = (random()*(getMyMinionCount() + 1)) + 1
        mouseMove(getMouseMoveCoords(area(getMinionBoard(getMyMinionCount() + 1)[zone])))
        time.sleep(0.5)
        mouseUp()
        time.sleep(0.5)
        if isMyCard(target._ingameId):
            c = getMyMinionCount()
        else:
            c = getEnemyMinionCount()
        mouseMove(getMouseMoveCoords(getOnBoardArea(c, target)))
        time.sleep(0.5)
        mouseClick()
    except Exception, e:
        print 'playMinionWithTarget()', e
        
def playCardWithTarget(card, target):
    try:   
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        time.sleep(1)
        mouseDown()   
        time.sleep(0.5)
        if isMyCard(target._ingameId):
            c = getMyMinionCount()
        else:
            c = getEnemyMinionCount()
        mouseMove(getMouseMoveCoords(getOnBoardArea(c, target)))
        time.sleep(0.5)
        mouseClick()
    except Exception, e:
        print 'playCardWithTarget()', e
        
def playCard(card):
    try:
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        time.sleep(1)
        mouseDown()   
        time.sleep(0.5)
        mouseMove(getMouseMoveCoords(area(getMinionBoard(7)[random()*7])))
        time.sleep(0.5)
        mouseUp()
    except Exception, e:
        print 'playCard()', e
        
def playMinion(card):
    try:
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        time.sleep(1)
        mouseDown()   
        time.sleep(0.5)
        zone = (random()*(getMyMinionCount() + 1)) + 1
        mouseMove(getMouseMoveCoords(area(getMinionBoard(getMyMinionCount() + 1)[zone])))
        time.sleep(0.5)
        mouseUp()
    except Exception, e:
        print 'playMinion()', e
                
def chooseOption(opt):
    if len(opt) == 1:
        EndTurn()
    else:
        card, target = options(opt)
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
            
        
    
    