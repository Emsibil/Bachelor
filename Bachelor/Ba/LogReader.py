import sys
import os

path = 'D:/Programme/'

def getPath():
    global path
    return path

def openLogFile():
    return open(getPath()+'Hearthstone/Hearthstone_Data/output_log.txt' , 'r')

def readLog():
    return openLogFile().readlines()
    
def realTimeReader():
    content = readLog()
    numberOfLines = len(content)
    for line in content:
        print str(line)
    while True:
        new_content = readLog()
        if not content == new_content:
            toPrint = len(new_Content) - numberOfLines
            i = 0
            while toPrint >= i:
                print new_content[numberOfLines + i]
                i += 1
            conntent = new_content
            numberOfLines = len(new_Content)






    

        
        
    
    