import numpy as np
import cv2
import ImageGrab as grab
import psutil
import testing
import Image
import time
import sys
import pyHook
import pythoncom
from itertools import izip
import os
import LogReader as log
import cardLibReader as cReader
import CardLibUpdater as cUpdater
from sklearn import svm
from sklearn.ensemble.forest import RandomForestClassifier

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

mySide = None
def get_mySide():
    global mySide
    if mySide is None:
        print 'Error'
    return mySide
enemySide = None
def get_enemySide():
    global enemySide
    if enemySide is None:
        print 'Error'
    return enemySide
turn = None
def get_turn():
    global turn
    if turn is None:
        print 'Error'
    return turn
me = None
def get_me():
    global me
    if me is None:
        print 'Error'
    return me
enemy_mana = None
def get_enemyMana():
    global enemy_mana
    if enemy_mana is None:
        print 'Error'
    return enemy_mana
my_mana = None
def get_myMana():
    global my_mana
    if my_mana is None:
        print 'Error'
    return my_mana
stack = None
def get_stack():
    global stack
    if stack is None:
        print 'Error'
    return stack
my_Hand = None
def get_myHand():
    global my_Hand
    if my_Hand is None:
        print 'Error'
    return my_Hand
enemy_Hand = None
def get_enemyHand():
    global enemy_Hand
    if enemy_Hand is None:
        print 'Error'
    return enemy_Hand
enemy = None
def get_enemy():
    global enemy
    if enemy is None:
        print 'Error'
    return enemy
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
    enemy.save(path('images/tests/enemy.png'))
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
def singleMinionsValues(minions):
    if len(minions) == 0:
        return
    for minion in minions:
        attack = minion.crop((6, 68, 21, 82))
        life = minion.crop((38, 68, 53, 82))
        
        print str(minion) + "Attack: " + str(numberClassifier(attack)) + "Life: " + str(numberClassifier(life))
enemyHero = None
def get_enemyHero():
    global enemyHero
    if enemyHero is None:
        enemyHero = enemyDetection(get_enemy())
    return enemyHero
enemy_clf = None
def get_enemyCLF():
    global enemy_clf
    if enemy_clf is None:
        enemy_clf = enemy_detection_clf()
    return enemy_clf
#which hero plays the enemy
def enemy_detection_clf():

    chars = np.array(['warrior', 'warlock', 'mage', 'druid', 'rogue', 'shaman', 'paladin', 'priest', 'hunter'])
    data = []
    target = []
    for c in chars:
        p = path('images/character/new/black')
        for f in os.listdir(p+'/'+c):
            img = Image.open(p+'/'+c+'/'+f)
            w, h = img.size
            pixel = img.load()
            tmp = []
            for y in range(h):
                for x in range(w):
                    tmp.append(np.float(pixel[x,y] / 255))
            target.append(np.str(c))
            data.append(np.array(tmp))
    data = np.array(data)
    #image = data.view()
    #image.shape = (-1, 22, 30)
    #clf = svm.SVC(gamma = 0.001)
    clf = RandomForestClassifier()
    clf.fit(data, target)
    
    return clf
def enemyDetection(img):
    clf = get_enemyCLF()
    im = img
    im = im.resize((10,10), Image.CUBIC)
    im = im.convert('1')
    data = []
    w, h = im.size
    pixel = im.load()
    for y in range(h):
        for x in range(w):
            data.append(np.float(pixel[x,y] / 255)) 
    predict = clf.predict(np.array(data))        
    return predict[0]

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
def decoloringNumbers(img):
    w, h = img.size
    pixels = img.load()
    tmp_pixels = controllingGreen(pixels, w, h)
    if(tmp_pixels == None):
        tmp_pixels = controllingRed(pixels, w, h)
    if(tmp_pixels == None):
        tmp_pixels = controllingWhite(pixels, w, h)
    
    pixels = makeBlack(tmp_pixels, w, h) 
    return pixels
def controllingGreen(pixels, w, h):    
    count = 0
    for x in range(w):
        for y in range(h):
            r, g, b, a = pixels[x,y]
            if x >= (w/2) and count == 0:
                return None;
            if r > 100 and g == 0 and b == 0:
                pixels[x,y] = (0, 0, 0)
                count += 1

    return pixels
def controllingRed(pixels, w, h):                
    count = 0
    for x in range(w):
        for y in range(h):
            r, g, b, a = pixels[x,y]
            if x >= (w/2) and count == 0:
                return None
            if r==0 and g > 100 and b == 0:
                pixels[x,y] = (0, 0, 0)
                count += 1
            
    return pixels          
def controllingWhite(pixels, w, h):             
    for x in range(w):
        for y in range(h):
            r, g, b, a = pixels[x,y]
            if (r > 150) and (b > 150) and (g > 150):
                diffrb = np.abs(r-b)
                diffrg = np.abs(r-g)
                diffgb = np.abs(g-b)
                if (diffrg < 25) and (diffrb < 25) and (diffgb < 25):
                    pixels[x,y]= (0, 0, 0)

    return pixels
def makeBlack(pixels, w, h):
    for x in range(w):
        for y in range(h):
            if not pixels[x,y] == (0, 0, 0):
                pixels[x, y] = (255, 255, 255)
    return pixels
class Bunch(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self      
def formatImageToSVCData(img):
    w, h = img.size
    pixel = decoloringNumbers(img)
    y_arr = []
    for y in range(h):
        for x in range(w):
            y_arr.append(np.float(((255 - (pixel[x,y][0] + pixel[x,y][1] + pixel[x,y][2])/3) / 255)))  
    y_arr = np.array(y_arr)
        
    image = y_arr.view()
    image.shape = (-1, 14, 15)
    
    return Bunch(data = np.array(y_arr),
                 target = np.int(0),
                 target_name = np.arange(0),
                 image = image,
                 DESCR = 'my digits')
def digit_data():
    p = path('images/black_white')
    img_arr = []
    for f in os.listdir(p):
        name, end = f.split('.')
        if end == 'png':
            img = Image.open(p+'/'+f)
            w, h = img.size
            pixel = img.load()
            y_arr = []
            for y in range(h):
                #x_arr = []
                for x in range(w):
                    r , g, b = pixel[x,y]
                    sum = ((255 - (r + g + b)/3) / 255)
                    y_arr.append(np.float(sum))
                #x_arr = np.array(x_arr)
                #y_arr.append(x_arr)
            y_arr = np.array(y_arr)
            img_arr.append(y_arr)
    return np.array(img_arr)
def _data():
    f = open(path('images/black_white/target4.info'), 'r')
    content = f.readlines()
    numbers = []
    for l in content:
        num = str(l).split(' ')[1]
        num = num[:1]
        if num == 'x':
            num = 10
        numbers.append(np.int(num))
    target = np.array(numbers)
    data = np.array(digit_data())
    images = data.view()
    images.shape = (-1, 14, 15)
    
    return Bunch(data = data,
                 target = target.astype(np.int),
                 target_names=np.arange(11),
                 images=images,
                 DESCR = 'my digits')
number_clf = None
def get_numberCLF():
    global number_clf
    if number_clf is None:
        number_clf = my_digits()
    return number_clf
def my_digits():
    digits = _data()
    
    n_samples = len(digits.images)
    datas = digits.images.reshape((n_samples, -1))

    classifier = RandomForestClassifier()
    classifier.fit(datas, digits.target)
    
    return classifier
def numberClassifier(img):

    clf = get_numberCLF()
    
    digit = formatImageToSVCData(img)
    
    predict = clf.predict(digit.data)
    
    if predict == 10:
        predict = testing.biggerThanNine(digit, clf)
    
    return predict[0]
def cardDetectScreenshot():
    img = grab.grab()
    img = img.resize((800,600), Image.CUBIC)
    img = img.crop((206, 301, 502, 580))



def GameStart():   
    #firstScreen
    takingScreenshot()
    print 'Your opponent plays: ' + str(get_enemyHero())
    
    #save which background is used
    blobDetection(get_enemySide(), True, 'ENEMY')
    blobDetection(get_mySide(), True, 'MY')
#Methods and function which needs to run at the beginning of a game
def gameControl():
    #global vars where Screenshots and all other information are saved
    global me
    global enemy_mana
    global my_mana
    global stack
    global enemy_Hand

    #firstScreen
    takingScreenshot()
    
    isMyTurn(get_turn())
    
    minionsOnEnemySide = blobDetection(get_enemySide(), False, 'ENEMY')
    minionsOnMySide = blobDetection(get_mySide(), False, 'MY')
    
    print 'Minions on enemy Side: ' + str(minionsOnEnemySide)
    print 'Minions on my side: ' + str(minionsOnMySide)
    
    #singleMinionsValues(singleMinions(enemySide, minionsOnEnemySide))
    #singleMinionsValues(singleMinions(mySide, minionsOnMySide))
    
    print countHandcards(get_myHand())
def OnKeyBoardEvent(event):
    c = chr(event.Ascii)
    if c == 'p':
        print 'Screen'
        gameControl()
    if c == 's':
        print 'StartScreen'
        GameStart()
def Main():
    get_numberCLF()
    #get_enemyCLF()
    
    while True:   
        hm = pyHook.HookManager()
        hm.KeyDown = OnKeyBoardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()        

#Main()

#------------------------------#

def testOnKeyBoardEvent(event):
    c = chr(event.Ascii)
    if c == 's':
        print 'Screenshot'
        testing.ScreenForCardNum()
        
def testingMain():
    while True:   
        hm = pyHook.HookManager()
        hm.KeyDown = testOnKeyBoardEvent
        hm.HookKeyboard()
        pythoncom.PumpMessages()

#testingMain()
#num = 3000
#while True:
 #   time.sleep(2)
  #  testing.image_slicing(str(num))
   # num += 1
#img = Image.open(path('images/attack.png'))
#img1 = Image.open(path('images/manacosts.png'))
#get_numberCLF()
#print numberClassifier(img)
#print numberClassifier(img1)
#print 'Done'

#log.testReader()
#log.testLines()
log.Statedecision()
#cReader.CardById('CS1_042')
#cUpdater.singleCards()

print 'done'
