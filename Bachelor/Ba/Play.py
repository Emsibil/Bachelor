import time
from MouseControl import *
from random import random
from Board import *
from Util_new import Ability, Cardtype
from AbilityInterpreter import *

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
    
def playHandcard(card, targetArea):
    try:
        count = getMyHandcardCount()
        mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
        time.sleep(1)
        mouseDown()   
        time.sleep(0.5)
        mouseMove(targetArea)
        if card._cardtype == Cardtype.MINION:
            addMyMinonToMyCards(card, (int(getMyMinionCount()/2) + 1))
            if hasAbility(card, Ability.BATTLECRY):
                pass
        if not card._cardtype == Cardtype.HERO_POWER:
            card._zone = Zone.PLAY
            reorderMyHandcards(card._zonePos)
        time.sleep(2)
        mouseUp()
    except Exception, e:
        print 'playHandcards()', e
    
def drawAttack(ownMinion ,target):
    try:
        mouseMove(getMouseMoveCoords(getOnBoardArea(getMyMinionCount(), ownMinion)))
        time.sleep(1)
        mouseDown()
        time.sleep(0.5)
        mouseMove(getMouseMoveCoords(getOnBoardArea(getEnemyMinionCount(), target)))
        time.sleep(1)
        mouseUp()
        ownMinion.takes_Damage(target._attack)
        target.takes_Damage(ownMinion._attack)
        if ownMinion._zone == Zone.GRAVEYARD:
                reorderMyMinionsOnBoard(ownMinion._zonePos)
        if target._zone == Zone.GRAVEYARD:
            reorderEnemyMinionsOnBoard(target._zonePos)
    except Exception, e:
        print 'drawAttack()', e

def playMinionWithTarget(card, playZone, targetArea):
    count = getMyHandcardCount()
    mouseMove(getMouseMoveCoords(getHandcardArea(count, card.get_pos())))
    time.sleep(1)
    mouseDown()   
    time.sleep(0.5)
    mouseMove(getMouseMoveCoords(area(getUneven1())))
    addMyMinonToMyCards(card, playZone)
    time.sleep(1)
    mouseUp()
    time.sleep(0.5)
    mouseMove(targetArea)
    time.sleep(1)
    mouseDown()
    time.sleep(0.5)
    mouseUp()
        
def EndTurn():
    mouseMove(getMouseMoveCoords(area(getTurn())))    
    time.sleep(1)
    mouseDown()
    print "down"
    time.sleep(0.5)
    mouseUp()
    print "up"
    
    
 # NEUER ANSATZ


def playableCards(options):
    handcards = [c for c in getMyCards().values() if c._zone == Zone.HAND]
    playable = []
    for o in options:
        for h in handcards:
            if o[0] == h._ingameId:
                playable.append(h)
                handcards.remove(h)
                break
    return playable
        
def choosingCard(options):
    playable = playableCards(options)
    for card in playable:
        if (card._cardtype == Cardtype.MINION and card.hasBattlecry()) or card._cardtype == Cardtype.SPELL:
            targets = needsTargets(options, card)
            if targets[0]:
                targetSide = possibleTargetSide(targets[1], card)
                if isCardListed(card):             
                    if targetSide == TargetSide.MY:
                        if isBuff(card):
                            target = mostEffectiveTarget(targets[1], card)
                    elif targetSide == TargetSide.ENEMY:
                        if not isBuff(card):
                            target = mostEffectiveEnemyTarget(targets[1], card)
                    else:
                        if isBuff(card):
                            target = targetFromMySide(targets[1])
                        else:
                            target = targetFromEnemySide(targets[1])
                else:
                    target = getCardByIngameId(targets[1][random()*len(targets[1])]) #randomTarget
                    
                    
        
            
   
    
    