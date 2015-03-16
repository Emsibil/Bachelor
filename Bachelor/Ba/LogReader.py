import os
import time
import numpy as np
import cardLibReader as cReader

#path = 'C:/Program Files (x86)'  #Uni
path = 'D:/Programme' #Home

#returns the full path of a special file
def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

def getPath():
    global path
    return path

def openLogFile():
    return open('D:/Programme/Hearthstone/Hearthstone_Data/output_log.txt' , 'r')

def readLog():
    return openLogFile().readlines()
    
def realTimeReader():
    content = readLog()
    numberOfLines = len(content)
   # for line in content:
    #    print str(line)
    while True:
        time.sleep(0.1)
        new_content = readLog()
        if not content == new_content:
            toPrint = len(new_content) - numberOfLines
            i = 0
            while toPrint > i:
                lineNumber = numberOfLines + i
                #print new_content[lineNumber]
                new_line = new_content[lineNumber]
                if '[Zone]' in new_line:
                    print 'True'
                    logInterpreter(new_line)                    
                i += 1
                time.sleep(0.01)  
            content = new_content
            numberOfLines = len(new_content)
                

Handcards = np.array(['None','None','None','None','None','None','None','None','None','None'])
def getHandcards():
    global Handcards
    return Handcards

def setHandcards(handcardArray):
    global Handcards
    Handcards = handcardArray

def getHandcardCount():
    Handcards = getHandcards()
    count = 0
    for card in Handcard:
        if not card == 'None':
            count += 1
        else:
            return count
    return count

def reOrderHandcards(handcards, pos):
    while pos < (len(handcards) - 1):
        if handcards[pos + 1] == 'None':
            handcards[pos] = 'None'
            break;
        handcards[pos] = handcards[pos + 1]
        if (pos + 1) == 9:
            handcards[9] = 'None'
    return handcards

MinionsOnMySide = np.array([[1, 'None'], [2, 'None'], [3, 'None'], [4, 'None'], [5, 'None'], [6, 'None'], [7, 'None']])

def getMyMinions():
    global MinionsOnMySide
    return MinionsOnMySide

def setMyMinions(MinionArray):
    global MinionsOnMySide
    MinionsOnMySide = MinionArray

def reorderMyMinions(Array, pos):
    i = (len(Array) - 1)
    while i >= pos:
        Array[i, 1] = Array[i - 1, 1] 
        i -= 1    
    Array[pos, 1] = 'None' 
            
Mulligan = False
def isMulligan():
    global Mulligan
    return Mulligan

def setMulligan(binary):
    global Mulligan
    Mulligan = binary

TurnChanged = False

def setTurnChanged(binary):
    global TurnChanged
    TurnChanged = binary

def isTurnChanged():
    global TurnChanged
    return TurnChanged

myTurn = False

def setMyTurn(binary):
    global myTurn
    myTurn = binary

def isMyTurn():
    global myTurn
    return myTurn
    
def cardName(line):
    return line.split('name=')[1].split(' id')[0]

def cardId(line):
    return line.split('cardId=')[1].split(' ')[0]

def getPosition(line):
    return int(line.split('pos from 0 -> ')[1])

def isTaskListIdChangeTurn(line):
    return int(line.split('tasListId=')[1].split(' ')[0]) > 17

def logInterpreter(line):
    Handcards = getHandcards()
    MyMinios = getMyMinions()
    if 'taskListId=1 ' in line:
         print 'GameStarted'
         setMulligan(True)
    if 'taskListId=17 ' in line:
         print 'MULLIGAN is over'
         if getHandCardCount() == 3:
             setMyTurn(True)
         setMulligan(False)
    #TurnChanging Start
    if 'AddServerZoneChanges' in line and not isTurnChanged() and isTaskListIdChangeTurn(line):
        setTurnChanged(True)
        print 'Turn is changing'
    if 'AddServerZoneChanges' in line and isTurnChanged() and isTaskListIdChangeTurn(line):
        setTurnChanged(False)
        print 'Turn changed'
        if isMyTurn():
            setMyTurn(False)
            print 'Opponent Turn'
        else:
            setMyTurn(True)
            print 'My Turn'      
    #TurnChanging End
    if ('TRANSITIONING card' in line) and 'zone=HAND' in line and 'to FRIENDLY HAND' in line:
        print 'YOUR TURN'
        print 'YOU DRAW: ', cardName(line)
        #here handcards + 1
    if 'CreateLocalChangesFromTrigger' in line and 'srcZone=HAND' in line and 'dstZone=PLAY' in line:
        print 'YOU PLAY: ', cardName(line)
        Handcards = reOrderHandcards(Handcards, int(line.split('srcPos=')[1].split(' ')[0]))
        card = cReader.cardById(cardId(line))
        #if you play a minion
        if cReader.cardType(card) == 'Minion':
            pos = (int(line.split('desPos=')[1].split(' ')[0]) - 1)
            if MyMinions[pos, i] == 'None':
                MyMinions[pos, i] = card                
            else:
                reorderMyMinions(MyMinions, pos)
                MyMinions[pos, i] = card            
    if ('ProcessChange' in line) and ('player=1' in line) and ('pos from 0' in line) and isMulligan():
        print 'MULLIGAN CARD: ', cardName(line), ' AT LINE: ', getPosition(line)
        Handcards[getPosition(line) - 1] = cReader.CardById(cardId(line))

def liveReader():
    content = readLog()
    numberOfLines = len(content)
    foundGame = False
    isMulligan = False
    while True:
        time.sleep(0.05)
        new_content = readLog()
        if not content == new_content:
            toPrint = len(new_content) - numberOfLines
            i = 0
            while toPrint > i:
                lineNumber = numberOfLines + i
                new_line = new_content[lineNumber]
                if 'CREATE_GAME' in line:
                    foundGame = True
                if 'BEGIN_MULLIGAN' in line:
                    print 'MULLIGAN STARTED'
                    isMulligan = True
                if foundGame and '[Zone]' in new_line:
                    Zone.write(new_line)
                elif foundGame and '[Power]' in new_line:
                    Power.write(new_line)
                i += 1
                time.sleep(0.01)  
            content = new_content
            numberOfLines = len(new_content)

#def interpretZone(line):
PLAYER_NAMES = np.array(['NONE','NONE'])
def getPlayerName(PlayerID):
    global PLAYER_NAMES
    return PLAYER_NAMES[PlayerID - 1]

def setPlayerName(PlayerID, Name):
    global PLAYER_NAMES
    PLAYER_NAMES[PlayerID - 1] = Name

MULLIGAN_STATE = np.array(['INPUT', 'DEALING', 'WAITING', 'DONE'])
def getMulliganState(index):
    global MULLIGAN_STATE
    return MULLIGAN_STATE[index]

MULLIGAN_STATE_OF_ENEMY = 'NONE'
def getEnemyMulliganState():
    global MULLIGAN_STATE_OF_ENEMY
    return MULLIGAN_STATE_OF_ENEMY

def setEnemyMulliganState(State):
    global MULLIGAN_STATE_OF_ENEMY
    MULLIGAN_STATE_OF_ENEMY = State

def interpretMulligan(line):
    if 'BEGIN_MULLIGAN' in line:
        print 'MULLIGAN STARTED'
    if getPlayerName(1) in line and getMullingState(0) in line:
        print 'Input'
    if getPlayerName(1) in line and getMullingState(1) in line:
        print 'Here you have something to do like waiting for CardInput or wait for next Zonecommand'
    if getPlayerName(1) in line and getMullingState(2) in line:
        print 'Nothing really important till now'
    if getPlayerName(1) in line and getMullingState(3) in line:
        print 'You finished your MULLIGAN'
    if getPlayerName(1) in line and getMullingState(3) in line and getEnemyMulliganState() == getMulliganState(3):
        print 'MULLING is OVER'

    
      

def splitInfo():
     log = open(path('doc/output_log_fullInfo.txt'), 'r').readlines()
     Zone = open(path('doc')+'/Zone.txt', 'w')
     Power= open(path('doc')+'/Power.txt', 'w')
     for l in log:
         if '[Zone]' in l:
             Zone.write(l) 
         if '[Power]' in l:
             Power.write(l)    
                                                                                                                                                                                                                     


   #-----TESTREADER-----#
def testReader():
    content = readLog()
    numberOfLines = len(content)
    for line in content:
        print str(line)
    while True:
        time.sleep(0.1)
        new_content = readLog()
        if not content == new_content:
            toPrint = len(new_content) - numberOfLines
            i = 0
            while toPrint > i:
                lineNumber = numberOfLines + i
                print new_content[lineNumber]
                new_line = new_content[lineNumber]                              
                i += 1
                time.sleep(0.01)  
            content = new_content
            numberOfLines = len(new_content)