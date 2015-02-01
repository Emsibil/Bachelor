import numpy as np
import cv2
import ImageGrab as grab
import psutil
import testing
import Image
import time
from itertools import izip
import os

#tests if Hearthstone is already in my processlist of Windows.
def isHearthstoneRunning():
    processes = psutil.get_pid_list()
    for process in processes:
        name = psutil.Process(process).name.__str__()
        if "Hearthstone.exe" in name:
            print "is running"
            return True
    print "Hearthstone wasn't started, yet. Please start Hearthstone and restart this Script!"
    return False

#returns the full path of a special file
def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

#vars for takingScreenshot()
enemySide = None
mySide = None
turn = None
enemy = None
me = None
enemy_mana = None
my_mana = None
stack = None
my_Hand = None
enemy_Hand = None

#takes a Screenshot of the current board, resizes it too 800x600 and cuts it into needed smaller imags
def takingScreenshot():
    img = grab.grab()
    img = img.resize((800, 600), Image.BICUBIC)
    #img = img.convert('LA') #just needed if the image should be transformed in a grayscaled image
    
    global enemySide
    global mySide
    global turn
    global enemy
    global me
    global enemy_mana
    global my_mana
    global stack
    global my_Hand
    global enemy_Hand

    enemySide = img.crop((197, 177, 605, 279))
    mySide = img.crop((197 , 281, 605, 383))
    turn = img.crop((614, 248, 685, 292))
    enemy = img.crop((361, 48, 442, 167))
    me = img.crop((361, 394, 442, 513))
    enemy_mana = img.crop((490, 26, 528, 50))
    my_mana = img.crop((508, 543, 546, 567))
    stack = img.crop((118, 169, 149, 411))
    my_Hand = img.crop((246, 518, 483, 591))
    enemy_Hand = img.crop((246, 0, 483, 44))

#returns bool and detects if it's my turn
def isMyTurn(img):
    end_turn= cv2.CascadeClassifier(path("data\\turn\\turn.xml"))
    _img = np.asarray(img)
    end = end_turn.detectMultiScale(_img, 1.1, 1)
    if len(end) == 1:
        print "My Turn"
        return True
    else:
        print "Enemy Turn"
        return False
    


#Calculates the avergage colour values of the given image
def colorAvg(img):
    w, h = img.size
    pixels = img.load()
    data = []
    for x in range(w):
        for y in range(h):
            if x <= 52 and y <= 33:
                continue
            cpixel = pixels[x, y]
            data.append(cpixel)
    r = 0
    g = 0
    b = 0
    counter = 0
    for x in range(len(data)):
        r+=data[x][0]
        g+=data[x][1]
        b+=data[x][2]
        counter+=1;
 
    rAvg = r/counter
    gAvg = g/counter
    bAvg = b/counter
    
    return (rAvg, gAvg, bAvg)

#global vars for blobDetection()
colorValue = []
imgValue = []
eColorValue = []
eImgValue = []
#detects how many minions are on the board. "GameStart" needs to be True for the first Screenshot in a Game
def blobDetection(img, GameStart, side):
    
    global colorValue
    global imgValue
    global eColorValue
    global eImgValue

    innerColorValue = []
    innerImgValue = []

    w, h = img.size
    x = w - 8 

    if GameStart:
        while(x >= w/2):
            innerImgValue.append(img.crop((x-10, 0, x, h)))
            innerColorValue.append(colorAvg(img.crop((x - 10, 0, x, h))))
            x -= 29
        if side == 'ENEMY':
            eColorValue = innerColorValue
            eImgValue = innerImgValue 
        else: 
            colorValue = innerColorValue
            imgValue = innerImgValue 
    else:
        if side == 'ENEMY':
            innerColorValue = eColorValue
            innerImgValue = eImgValue
        else:
            innerColorValue = colorValue
            innerImgValue = imgValue
        count = 0
        maxCount = 7
        while(x >= w/2):
            pix = img.crop((x-10, 0, x, h))
            cav = colorAvg(img.crop((x - 10, 0, x, h)))
            
            pix = np.asarray(pix)
            base = np.asarray(innerImgValue[count])
            
            hist1 = cv2.calcHist([base], [0], None, [256],[0, 255])
            hist1 = cv2.normalize(hist1).flatten()
            hist2 = cv2.calcHist([pix],[0], None, [256],[0, 255])
            hist2 = cv2.normalize(hist2).flatten()
            
            result4 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_BHATTACHARYYA)
                   
            if(cav != innerColorValue[count]): 
                threshold = [[innerColorValue[count][0]*0.98, innerColorValue[count][1]*0.98, innerColorValue[count][2]*0.98], [innerColorValue[count][0]*1.02, innerColorValue[count][1]*1.02, innerColorValue[count][2]*1.02]]  
                if(result4 <= 0.25 or 
                   (cav[0] > threshold[0][0] and cav[0] < threshold[1][0] and cav[1] > threshold[0][1] and cav[1] < threshold[1][1] and cav[2] > threshold[0][2] and cav[2] < threshold[1][2])):
                    maxCount -= 1
                    count += 1
                    x -= 29
                    continue
                print str(maxCount) + ' minions on board'
                return maxCount
            else:
                maxCount -= 1
                count += 1
                x -= 29  
        return 0 

#together with singleMinionsSupport you get an array with images for ervery single blob
def singleMinions(img, minionsOnBoard):
    minions = []   
    if minionsOnBoard == 0:
        return minions
    uneven = minionsOnBoard % 2.0
    w, h = img.size
    if uneven == 1:
        minions.append(img.crop((w/2 - 29, 0, w/2 +29, h)))
        minionsOnBoard -= 1
        if minionsOnBoard > 0:
            minions = singleMinionsSupport(img, minionsOnBoard/2, w/2 + 29, minions, h, 58)
            minions = singleMinionsSupport(img, minionsOnBoard/2, ((w/2 - 29) - (58 * (minionsOnBoard/2))), minions, h, 58)
    else:
       minions = singleMinionsSupport(img, minionsOnBoard/2, w/2, minions, h, 58)
       minions = singleMinionsSupport(img, minionsOnBoard/2, (w/2 - (58 * (minionsOnBoard/2))), minions, h, 58)
    return minions   

def singleMinionsSupport(img, count, xStart, array, height, stepRange):
    array.append(img.crop((xStart, 0, xStart + stepRange, height)))
    count -= 1
    if (count == 0):
        return array
    else:
        array = singleMinionsSupport(img, count, xStart + stepRange, array, height, stepRange)     
    return array     

#global var for saving the enemy Hero
enemyHero = None

#which hero plays the enemy
def enemyDetection(img):
    
    global enemyHero

    detected = 0
    for cascade in os.listdir(path('data\\characters')):
        casc = cv2.CascadeClassifier(path('data\\characters')+'\\'+cascade)
        _img = np.asarray(img)
        char = casc.detectMultiScale(_img, 1.1, 1)
        if len(char) == 1:
            detected += 1
            #print cascade
    if detected == 1:
        print 'Enemy Hero detected'
        name, tag = cascade.split('.')
        enemyHero = name
    elif detected == 0:
        print 'No Enemy Hero detected'
    else:
        print 'detection not clear'

#return the count of handcards you have at the moment
def countHandcards(img):
    ranges = np.array([[111,120,1],[84,90,2],[57,63,3],[27,36,4],[23,31,5],[16,23,6],[14,21,7],[7,15,8],[2, 9, 9], [3,7,10]]) 
    
    _img = np.asarray(img)
    edges = cv2.Canny(_img,237,73)
    two = 0
    leftEdges = np.array([238, 238])
    for x in range(237):
        if edges[72, x] == 255:
            if two < 2:
                #print x
                leftEdges[two] = x
                two += 1
            if two == 2:
                break
    if(leftEdges[1] > ranges[0,1]):
        #print '0 Handcards'
        return 0 
    tmp = 0
    for r in ranges:
        if(leftEdges[0] >= r[0] and leftEdges[1] <= r[1]):
            if(leftEdges[1] == 21 and r[2] == 6):
                tmp = 6
                continue
            elif (r[2] == 8):
                r[2] = testingFromRight(edges)
            if((leftEdges[1] - leftEdges[0]) <= 3):
                #print str(leftEdges[0]) + '---' + str(leftEdges[1])
                #print str(r[2]) + ' Handcards sicher'
                return r[2]
            #print str(leftEdges[0]) + '---' + str(leftEdges[1])
            #print str(r[2]) + ' Handcards'
            #return
    #print '10 Handcards'
    return 10    

#Method for more a detailled test if there are 8 or 9 handcards
def testingFromRight(edges):
    handcards = None
    count8 = 0   
    count9 = 0
    y = 51
    while y < 70:
        if edges[y, 2] == 255:
            count9 += 1
        if edges[y, 4] == 255:
            count8 += 1
        y += 1
    if count8 > count9:
        handcards = 8
    elif count8 < count9:
        handcards = 9   
    else:
        print str(count8) + '   ' + str(count9)
    return handcards

#Methods and function which needs to run at the beginning of a game
def gameStart():
    
    #global vars where Screenshots and all other information are saved
    global enemySide
    global mySide
    global turn
    global enemy
    global me
    global enemy_mana
    global my_mana
    global stack
    global my_Hand
    global enemy_Hand
    global enemyHero

    #firstScreen
    takingScreenshot()

    #save which background is used
    blobDetection(enemySide, True, 'ENEMY')
    blobDetection(mySide, True, 'MY')

    #enemy hero detection
    enemyDetection(enemy)







def whoseTurn():
    while True:
        if isHearthstoneRunning():
            isMyTurn()
        else:
            time.sleep(3)

def myEnemy():
    while True:
        takingScreenshot()
        global enemy
        testing.enemyDetection(enemy)
        time.sleep(3)
#whoseTurn()
#testing.object_detect()
#testing.screenshots()

#num = 3000
#while True:
 #   time.sleep(2)
  #  testing.image_slicing(str(num))
   # num += 1

def boardCutting():
    GameStart = True
    for pic in os.listdir(path('images\\workField')):
        print pic
        img = Image.open(path('images\\workField')+'\\'+pic)        
        if GameStart:
            blobDetection(img, GameStart, 'ENEMY')
            GameStart = False
        else: 
            testing.singleMinionsValues(testing.singleMinions(img, blobDetection(img, GameStart, 'ENEMY')))
#boardCutting()
#testing.renameAttack()
#myEnemy()

#print "ab hier 8"
#testing.edge(path('images\\myHand\\myHand27.png'))#8
#print "pic"
#testing.edge(path('images\\myHand\\myHand45.png'))
#print "pic"
#testing.edge(path('images\\myHand\\myHand46.png'))
#print 'ab hier 9'
#testing.edge(path('images\\myHand\\myHand100.png'))#9
#print "pic"
#testing.edge(path('images\\myHand\\myHand79.png'))

#testing.isMouseMoved()
#testing.boxing()
#testing.sort()
#testing.rename()
#testing.eight()
#testing.testdecolor()
#print testing.digit_data()[0]
#testing.resort_number()
testing.data()