from Image import BICUBIC
from ImageGrab import grab
from random import random
from time import sleep
from Util_new import split, GameState, value, Zone
from LogInterpreter_new import GameStart_Full_Entity, setPlayer, Mulligan,\
    isMulliganOver, SubType, SubTypeMulliganTrigger, readOptions,\
    isPlayerOneInMulligan, isPlayerTwoInMulligan, setPlayerOneInMulligan, setPlayerTwoInMulligan
from Board import getMyHandcardCount, getMyCards


WAITING_FOR_MORE_LINES = False
def waitingForMoreLines():
    global WAITING_FOR_MORE_LINES
    return WAITING_FOR_MORE_LINES
def setWaitingForMoreLines(value):
    global WAITING_FOR_MORE_LINES
    WAITING_FOR_MORE_LINES = value
    
WAITING_FOR_MORE_OPTION_LINES = False
def waitingForMoreOptionLines():
    global WAITING_FOR_MORE_OPTION_LINES
    return WAITING_FOR_MORE_OPTION_LINES
def setWaitingForMoreOptionLines(value):
    global WAITING_FOR_MORE_OPTION_LINES
    WAITING_FOR_MORE_OPTION_LINES = value

TEMP_LINES = None
def getTempLines():
    global TEMP_LINES
    if TEMP_LINES is None:
        return []
    return TEMP_LINES
def setTempLines(lines):
    global TEMP_LINES
    TEMP_LINES = lines
        
JUMP_LINES = 0
def getJumpLines():
    global JUMP_LINES
    return JUMP_LINES
def setJumpLines(value):
    global JUMP_LINES
    JUMP_LINES = value
    
CUR_STATE = GameState.SEARCHING
def getCurState():
    global CUR_STATE
    return CUR_STATE
def setCurState(new_state):
    global CUR_STATE
    CUR_STATE = new_state
    print new_state 

OPTIONS = False
def findOptions():
    global OPTIONS
    return OPTIONS
def setFindOptions(value):
    global OPTIONS
    OPTIONS = value

STILL_MY_TURN = False
def setStillMyTurn(value):
    global STILL_MY_TURN
    STILL_MY_TURN = value
def isStillMyTurn():
    global STILL_MY_TURN
    return STILL_MY_TURN

def isMulligan():
    return (isPlayerOneInMulligan() and isPlayerTwoInMulligan())

def setVariablesDefault():
    setWaitingForMoreLines(False)
    setWaitingForMoreOptionLines(False)
    setPlayerOneInMulligan(False)
    setPlayerTwoInMulligan(False)
    setJumpLines(0)
    setTempLines(None)
    setStillMyTurn(False)
    
def readSubType(index, lines, numOfLines):
    try:
        i = index
        while not '- ACTION_END' in lines[i] and i < numOfLines:
            i = i + 1
        if i == numOfLines:
            setTempLines(getTempLines() + lines[index:i])
            setJumpLines(i - index)
            setWaitingForMoreLines(True)
        else:
            SubType(getTempLines() + lines[index:i])
            setTempLines(None)
            setJumpLines(i - index)
            setWaitingForMoreLines(False)
    except Exception, e:
        print 'readSubType()', e
                      
def isMyTurn():
    img = grab()
    img = img.resize((800, 600),BICUBIC)
    img = img.crop((614, 248, 685, 292))
    img = img.crop((7,19,59,33))
    img = img.convert('LA')
    pix = img.load()
    w, h = img.size
    count = 0
    for x in range(w):
        for y in range(h):
            #print pix1[x, y]
            if pix[x, y][0] == 0:
                count = count + 1
    if count < 75 or count > 85:
        return False
    else:
        print 'MyTurn Confirmed'
        return True
    
def readMyTurn(lines):
    try:
        numOfLines = len(lines) - 1
        for index, l in enumerate(lines):
            if getJumpLines() > 0:
                setJumpLines(getJumpLines() - 1)
                continue
            elif '[Power]' in l:
                #print l
                if ('- ACTION_START' in l and 'SubType=' in l and ('DEATHS' in l or not 'GameEntity' in l)) or waitingForMoreLines():
                    readSubType(index, lines, numOfLines)
                elif 'option' in l or waitingForMoreOptionLines():
                    i = index
                    while not 'm_currentTaskList' in lines[i] and i < numOfLines:
                        i = i + 1
                    if i == numOfLines:
                        setTempLines(getTempLines() + lines[index:i])
                        setJumpLines(i - index)
                        setWaitingForMoreOptionLines(True)
                    else:
                        setTempLines(getTempLines() + lines[index:i])
                        if isStillMyTurn():
                            sleep(int(random()*5 + 3))
                            readOptions(getTempLines())
                            setTempLines(None)
                        else:
                            setFindOptions(True)
                        setJumpLines(i - index)
                        setWaitingForMoreOptionLines(False)
                elif 'FINAL_GAMEOVER' in l:
                    setVariablesDefault()
                    setCurState(GameState.GAME_END)
                    return
                elif 'Entity=GameEntity tag=TURN value=' in l:
                    setVariablesDefault()
                    setCurState(GameState.ENEMY_TURN)
                    completeReading(lines[(index + 1):], getCurState())
                    return              
            elif '[Zone]' in l:
                if 'ZoneChangeList.FireCompleteCallback()' in l and findOptions():
                    if not isStillMyTurn():
                        while isMyTurn() == False:
                            continue
                    setStillMyTurn(True)
                    sleep(int(random()*5 + 3))
                    readOptions(getTempLines())
                    setFindOptions(False)
                    setTempLines(None)
    except Exception, e:
        print 'readMyTurn()', e

def readEnemyTurn(lines):
    try:
        numOfLines = len(lines) - 1
        for index, l in enumerate(lines):
            if getJumpLines() > 0:
                setJumpLines(getJumpLines() - 1)
                continue
            elif '[Power]' in l:
                #print l
                if ('- ACTION_START' in l and 'SubType=' in l and ('DEATHS' in l or not 'GameEntity' in l)) or waitingForMoreLines():
                    readSubType(index, lines, numOfLines)
                elif 'FINAL_GAMEOVER' in l:
                    print 'Game End'
                    setVariablesDefault()
                    setCurState(GameState.GAME_END)
                    return
                elif 'Entity=GameEntity tag=TURN value=' in l:
                    setVariablesDefault()
                    setCurState(GameState.MY_TURN)
                    completeReading(lines[(index + 1):], getCurState())
                    return       
            elif '[Zone]' in l:
                pass
    except Exception, e:
        print 'readMyTurn()', e
        
def readMulligan(lines):
    try:
        numOfLines = len(lines) - 1
        for index, l in enumerate(lines):
            if getJumpLines() > 0:
                setJumpLines(getJumpLines() - 1)
                continue
            elif '[Power]' in l:
                #print l
                if ('- ACTION_START' in l and 'SubType=TRIGGER' in l) or waitingForMoreLines():
                    i = index
                    while not '- ACTION_END' in lines[i] and i < numOfLines:
                        i = i + 1
                    if i == numOfLines:
                        setTempLines(getTempLines() + lines[index:i])
                        setJumpLines(i - index)
                        setWaitingForMoreLines(True)
                    else:
                        SubTypeMulliganTrigger(getTempLines() + lines[index:i])
                        setTempLines(None)
                        setJumpLines(i - index)
                        setWaitingForMoreLines(False)
                elif isMulliganOver():
                    if getMyHandcardCount() == 3:
                        setCurState(GameState.MY_TURN)
                    else:
                        setCurState(GameState.ENEMY_TURN)
                    print 'HandcardCount:', getMyHandcardCount()
                    print 'Cards in Hand:', [c._name for c in getMyCards().values() if c.compareZone(Zone.HAND)]
                    setVariablesDefault()
                    completeReading(lines[index:], getCurState())
                    return     
            elif '[Zone]' in l:
                if 'ZoneChangeList.FireCompleteCallback()' in l and isMulligan():
                    Mulligan()
                    setPlayerOneInMulligan(False)
                    setPlayerTwoInMulligan(False)
    except Exception, e:
        print 'readMulligan():', e             
                
def readGameStart(lines):
    try:
        numOfLines = len(lines) - 1
        for index, l in enumerate(lines):
            if getJumpLines() > 0:
                setJumpLines(getJumpLines() - 1)
                continue
            elif '[Power]' in l:
                if 'FULL_ENTITY' in l or ('tag' in l and waitingForMoreLines()):
                    if (index + 1) <= numOfLines:
                        i = index + 1
                    else:
                        i = index
                    while ('tag' in lines[i] or not '[Power]' in lines[i]) and i < numOfLines and not 'TAG_CHANGE' in l:
                        i = i + 1
                    if i == numOfLines:
                        setWaitingForMoreLines(True)
                        setTempLines(getTempLines() + lines[index:i])
                        setJumpLines(i - index)
                    else:
                        GameStart_Full_Entity(getTempLines() + lines[index:i])
                        setTempLines(None)
                        setWaitingForMoreLines(False)
                        setJumpLines(i - index - 1)
                elif 'Entity=' in l and 'PLAYER_ID' in l:
                    setPlayer(split(l, 'Entity=', ' tag'), int(value(l)))
                elif 'Entity=GameEntity tag=NEXT_STEP value=BEGIN_MULLIGAN' in l:
                    setCurState(GameState.MULLIGAN)
                    setVariablesDefault()
                    completeReading(lines[index:], getCurState())
                    return            
    except Exception, e:
        print 'readGameStart():', e
               
def completeReading(lines, state):
    try:
        if state == getCurState():
            if getCurState() == GameState.GAME_START:
                readGameStart(lines)
            elif getCurState() == GameState.MULLIGAN:
                readMulligan(lines)
            elif getCurState() == GameState.MY_TURN:
                readMyTurn(lines)
            elif getCurState() == GameState.ENEMY_TURN:
                readEnemyTurn(lines)
            elif getCurState() == GameState.GAME_END:
                setCurState(GameState.SEARCHING)
                return
        else:
            print 'no Correct State'
    except Exception, e:
        print 'completeReading()', e