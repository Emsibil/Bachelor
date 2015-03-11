import sys
import os
from astropy import log

def openLogFile():
    path = '' +'Hearthstone/Hearthstone_Data/output_log.txt' 
    return  open(path, 'r')

def readLog():
    return openLogFile().readlines()
    
def GameStartingLine():
    content = readLog()
    i = (len(content) - 1)
    while i > 0:
        if 'MULLIGAN_STATE' in str(content[i])
            return i
        i -= 1

    

        
        
    
    