import time
from Util_new import isOptionCalc, setOptionsCalc, Player, SubType, setPlayerID, GameState, getCurState, setCurState, getTmp, setTmp, isMulligan, isWaiting, setWaiting, setFound, isFound, setVariablesDefault
from LogInterpreter import *

def readingMyTurn(cont):
    jump = 0
    Power = '[Power]'
    #Zone = '[Zone]'
    for idx, line in enumerate(cont):
        if not jump == 0:
            jump = jump - 1
            continue
        if '[Power]' in line or '[Zone]' in line:
            try:
                if Power in line and 'm_currentTaskList' in line:
                    continue
                elif Power in line and'FINAL_GAMEOVER' in line:
                    print 'Game End'
                    setCurState(GameState.GAME_END)
                    return
                elif Power in line and'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState(GameState.ENEMY_TURN)
                    setVariablesDefault()
                    print 'Turn Change'
                    completeReading(cont[(idx+1):], getCurState())
                    return
                elif Power in line and 'TAG_CHANGE' in line and 'RESOURCES' in line:
                    setMyMana(int(split(line, 'value=', '\n')))
                elif Power in line and 'SHOW_ENTITY' in line:
                    drawCard(line)
                elif Power in line and 'option' in line:
                    i = idx
                    nxt = 0
                    while i <len(cont):
                        if 'm_currentTaskList' in cont[i]:
                            showOptions(cont[idx:(i-1)])
                            nxt = i - idx
                            break
                        i += 1
                        if i == len(cont):
                            showOptions(cont[idx:])
                            nxt = (i - 1) - idx
                            break
                    print 'Waiting for PlayingOptions'
                    jump = nxt
                    setOptionsCalc(True)
                elif isOptionCalc() and 'ZoneChangeList.FireCompleteCallback' in line:
                    time.sleep(10)
                    choosePlayingCard()
                    clearOptions()
                    setOptionsCalc(False)
                elif Power in line and '- ACTION_START' in line and 'SubType=PLAY' in line:
                    jump = interpretingSubType(idx, cont, SubType.PLAY)
                elif isWaiting():
                    jump = interpretingSubType2(cont, SubType.PLAY)   
                elif Power in line and '- ACTION_START' in line and 'SubType=ATTACK' in line:
                    attack(line)
                    i = idx
                    jump = 0
                    while i < len(cont):
                        i += 1
                        if '- ACTION_END' in cont[i]:
                            jump = i - idx
                            break
                    nxt = jump  
            except Exception, e:
                print 'MY TURN:', line, e
                
def readingEnemyTurn(cont):
    jump = 0
    for idx, line in enumerate(cont):
        if not jump == 0:
            jump = jump - 1
            continue
        if '[Power]' in line:
            try:
                if 'm_currentTaskList' in line:
                    continue
                elif 'FINAL_GAMEOVER' in line:
                    print 'Game End'
                    setCurState(GameState.GAME_END)
                    return
                elif 'Entity=GameEntity tag=STEP value=MAIN_END' in line:
                    setCurState(GameState.MY_TURN)
                    setVariablesDefault()
                    print 'Turn Change'
                    completeReading(cont[(idx+1):], getCurState())
                    return
                elif '- ACTION_START' in line and 'SubType=PLAY' in line:
                    jump = interpretingSubType(idx, cont, SubType.PLAY)
                elif isWaiting():
                    jump = interpretingSubType2(cont, SubType.PLAY)
                elif '_ACTION_START' in line and 'SubType=TRIGGER' in line:
                    jump = interpretingSubType(idx, cont, SubType.TRIGGER)
                elif '_ACTION_START' in line and 'SubType=DEATHS' in line:
                    jump = interpretingSubType(idx, cont, SubType.DEATH)
                elif 'Entity='+getEnemyPlayerName() in line and 'RESOURCES' in line:
                    readingMana(line, Player.ENEMY)
            except Exception, e:
                print 'ENEMY TURN:', line, e
                
def readingMulligan(cont):
    for idx, line in enumerate(cont):
        if '[Power]' in line:
            try:
                if 'MULLIGAN_STATE' in line and 'DONE' in line:
                    setWaiting(False)
                    changingToTurns(line)
                    completeReading(cont[idx:], getCurState())
                    return
                elif 'MULLIGAN_STATE' in line and 'INPUT' in line: 
                    MulliganStates(line, 'INPUT')                    
                    continue     
                elif 'MULLIGAN_STATE' in line and 'DEALING' in line:
                    MulliganStates(line, 'DEALING')
                    continue
                elif isMulligan():
                    MulliganCardsChanging()
                elif isWaiting() and 'SHOW_ENTITY' in line:
                    setTmp((split(line, 'CardID=', '\n'), gameId(line)))
                    setFound(True)    
                elif isFound() and isWaiting() and 'HIDE_ENTITY' in line:
                    setFound(False)
                    changingMulliganCard(getTmp(), line)
                elif 'TAG_CHANGE' in line and 'CONTROLLER' in line and 'Entity=' in line:
                    setPlayerName(line)
                    continue
            except Exception, e:
                print 'MULLIGAN:', line, e 
                 
def readGameStartPowerLines(cont):
    for idx, line in enumerate(cont):
        if '[Power]' in line:
            try:
                if 'GameEntity tag=NEXT_STEP value=BEGIN_MULLIGAN' in line:
                    setCurState(GameState.MULLIGAN)
                    setVariablesDefault()
                    completeReading(cont[idx:], getCurState())
                    return
                elif 'CardID=HERO_' in line:
                    setFound(True)
                    setWaiting(True)
                    setTmp((split(line, 'CardID=', '\n'), int(split(line, 'ID=', ' '))))
                elif isFound() and 'tag=CONTROLLER' in line:
                    setFound(False)
                    setPlayerID(int(split(line, 'value=', '\n')))
                    heroInfo = getTmp()
                    setHero(getPlayerID(), heroInfo[1], heroInfo[2])
                elif isWaiting() and not isFound() and 'CardID=' in line:
                    setWaiting(False)
                    setHeroPower(getPlayerID(), int(split(line, 'ID=', ' ')), split(line, 'CardID=', '\n'))
                elif not isWaiting() and 'CardID=' in line and not 'HERO' in line:
                    cardId = split(line, 'CardID=')  
                    if '\n' == cardId:
                        continue
                    else:
                        idx = int(split(line, 'ID=', ' '))
                        setWaiting(True)
                        setTmp((cardId.split('\n')[0], idx))
                elif isWaiting() and 'ZONE_POSITION' in line:
                    setWaiting(False)
                    cardInfo = getTmp()
                    addMulliganCards(cardInfo, int(split(line, 'value=', '\n')))
                elif 'TAG_CHANGE' in line and 'CONTROLLER' in line and 'Entity=' in line:
                    setPlayerName(line)
                    continue
            except Exception, e:
                print 'GAME START', line, e   
                
def completeReading(cont, state):
    if state == getCurState():
        if getCurState() == GameState.GAME_START:
            readGameStartPowerLines(cont)
        elif getCurState() == GameState.MULLIGAN:
            readingMulligan(cont)
        elif getCurState() == GameState.MY_TURN:
            readingMyTurn(cont)
        elif getCurState() == GameState.ENEMY_TURN:
            readingEnemyTurn(cont)
        elif getCurState() == GameState.GAME_END:
            setCurState(GameState.SEARCHING)
            return
    else:
        print 'no Correct State'
