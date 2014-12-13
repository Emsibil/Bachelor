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



#takes a Screenshot of the current board, resizes it too 800x600 and cuts it into needed smaller imags
def takingScreenshot():
    img = grab.grab()
    img = img.resize((800, 600), Image.BICUBIC)
    #img = img.convert('LA') #just needed if the image should be transformed in a grayscaled image
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

#Takes a Screenshot and compares if there is an End Turn button in the image and evaluate if it's your turn or the opponents one
def isMyTurn():
<<<<<<< HEAD
    end_turn= cv2.CascadeClassifier(path("color_cascade.xml"))
=======
    end_turn= cv2.CascadeClassifier(path("data\\endturn_cascade.xml"))
>>>>>>> 519b96e1b8d49c598d1ce53a0b3545f05c1cb137
    while True:
        tmp_img = grab.grab()
        np_img = np.asarray(tmp_img)
        #gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)   #if i want to change it to grayscale images
        end = end_turn.detectMultiScale(np_img, 1.1, 1)
        count = len(end)
        if count == 1:
            print "My Turn"
        elif count == 0:
            print "His Turn or Menu"
        else:
            print "More than one End-Turn-Image. The training need to be more detailed!"
<<<<<<< HEAD
        time.sleep(1)
=======
        time.sleep(2)

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

colorValue = []
imgValue = []

#detects how many minions are on the board. "GameStart" needs to be True for the first Screenshot in a Game
def blobDetection(img, GameStart):
    w, h = img.size
    x = w - 8 
    if GameStart:
        while(x >= w/2):
            imgValue.append(img.crop((x-10, 0, x, h)))
            colorValue.append(colorAvg(img.crop((x - 10, 0, x, h))))
            x -= 29
    else:
        count = 0
        maxCount = 7
        while(x >= w/2):
            pix = img.crop((x-10, 0, x, h))
            cav = colorAvg(img.crop((x - 10, 0, x, h)))
>>>>>>> 519b96e1b8d49c598d1ce53a0b3545f05c1cb137
            
            pix = np.asarray(pix)
            base = np.asarray(imgValue[count])
            
            hist1 = cv2.calcHist([base], [0], None, [256],[0, 255])
            hist1 = cv2.normalize(hist1).flatten()
            hist2 = cv2.calcHist([pix],[0], None, [256],[0, 255])
            hist2 = cv2.normalize(hist2).flatten()
            
            result4 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_BHATTACHARYYA)
                   
            if(cav != colorValue[count]): 
                if(result4 <= 0.25):
                    maxCount -= 1
                    count += 1
                    x -= 29
                    continue
                print str(maxCount) + ' minions on board'
                return
            else:
                maxCount -= 1
                count += 1
                x -= 29     

def whoseTurn():
    while True:
        if isHearthstoneRunning():
            isMyTurn()
        else:
            time.sleep(3)

#whoseTurn()
#testing.object_detect()
#testing.screenshots()

#num = 1
#while True:
 #   time.sleep(2)
  #  testing.image_slicing(str(num))
   # num += 1

#im0 = Image.open(path("images\\enemyField\\efield1105.png")) #0
#im1 = Image.open(path("images\\enemyField\\efield1109.png")) #1
#im2 = Image.open(path("images\\enemyField\\efield1124.png")) #2
#im3 = Image.open(path("images\\enemyField\\efield1156.png")) #3
#im4 = Image.open(path("images\\enemyField\\efield1229.png")) #4
#im5 = Image.open(path("images\\enemyField\\efield1218.png")) #5
#im6 = Image.open(path("images\\enemyField\\efield1245.png")) #6
#im7 = Image.open(path("images\\enemyField\\efield1255.png")) #7
#testing.blobDetection(im0, True)
#testing.blobDetection(im1, False) #1
#testing.blobDetection(im2, False) #2
#testing.blobDetection(im3, False) #3
#testing.blobDetection(im4, False) #4
#testing.blobDetection(im5, False) #5
#testing.blobDetection(im6, False) #6
#testing.blobDetection(im7, False) #7

#testing.objdetect()

#testing.blue()
#p= path('images\\emptyHandboard')
#for file in os.listdir(p):
 #   img = Image.open(p+'\\'+file)
  #/  print str(colorAvg(img)) + '   ' + str(file)

#p2= path('images\\myHand')
#for file2 in os.listdir(p2):
#    img1 = Image.open(p2+'\\'+file2)
#    print colorAvg(img1)

im1 = Image.open(path('images\\myHand\\myHand1.png'))
im2 = Image.open(path('images\\myHand\\myHand9.png'))
im3 = Image.open(path('images\\myHand\\myHand25.png'))
im4 = Image.open(path('images\\myHand\\myHand100.png'))
im5 = Image.open(path('images\\myHand\\myHand219.png'))
testing.handcount(im1)
testing.handcount(im2)
testing.handcount(im3)
testing.handcount(im4)
testing.handcount(im5)
