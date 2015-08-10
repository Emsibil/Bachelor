from time import sleep
from LogReader_new import completeReading, setCurState, getCurState
from Util_new import GameState

def openLogFile():
    #return open('C:/Program Files (x86)/Hearthstone/Hearthstone_Data/output_log.txt' , 'r')
    return open('D:/Programme/Hearthstone/Hearthstone_Data/output_log.txt' , 'r')

def readLog():
    return openLogFile().readlines()

def Statedecision():
    log = readLog()
    nol = len(log)
    while True:
        sleep(0.04)
        new_log = readLog()
        new_nol = len(new_log)
        new_lines = new_log[nol : new_nol]
        i = 0
        while i < len(new_lines):
            if 'CREATE_GAME' in new_lines[i] and getCurState() == GameState.SEARCHING:
                setCurState(GameState.GAME_START)
                completeReading(new_lines[i:], GameState.GAME_START)
                break
            elif not getCurState() == GameState.SEARCHING: 
                completeReading(new_lines[i:], getCurState())
                break
            i += 1   
        log = new_log
        nol = new_nol
    
def Main():
    Statedecision()
    
Main()
