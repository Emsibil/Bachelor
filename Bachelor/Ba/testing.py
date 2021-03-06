import numpy as np
import cv2
import psutil
import Image
import ImageGrab
import matplotlib.pyplot as plt
from threading import Timer
import win32api, win32con
import time
from itertools import izip
import os
import sys
from boto.dynamodb.condition import NULL
from networkx.generators.community import caveman_graph
from sympy.core.sets import imageset
from sklearn.ensemble.forest import RandomForestClassifier


def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

sys.path.insert(0, path('lib'))
import pytesser

def takingScreen():
    im = ImageGrab.grab()
    plt.imshow(im), plt.show()

def testing_img():
    image = cv2.imread("D:\\Pictures\\Hearthstone\\rdy\\rdy04.jpg")
    img_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    surf = cv2.SURF(100)
    surf.upright = True
    surf.extended = True
    kp, des = surf.detectAndCompute(img_gray,None)
    img2 = cv2.drawKeypoints(image,kp,None,(255,0,0),4)  
    plt.imshow(img2), plt.show()
    #plt.imshow(img2), plt.show()
    
    #print cv2.cv.CalcEMD2(img, sec_img, cv2.cv.CV_DIST_L2)

def testing_img2():
    time.sleep(5)
    img = cv2.imread('D:\BA\Pictures\StartScreen.png',1)
    img1 = Image.open('D:\BA\Pictures\StartScreen.png')
    img_width, img_height = img1.size
    img2 = ImageGrab.grab(bbox=(0,0,img_width,img_height))
    img_2 = np.asarray(img2)
    #imgTwo = cv2.cvtColor(img_2,cv2.COLOR_BGR2GRAY)

    hist1 = cv2.calcHist([img], [0], None, [256],[0, 255])
    hist1 = cv2.normalize(hist1).flatten()
    hist2 = cv2.calcHist([img_2],[0], None, [256],[0, 255])
    hist2 = cv2.normalize(hist2).flatten()
    result1 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CORREL)
    result2 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CHISQR)
    result3 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_INTERSECT)
    result4 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_BHATTACHARYYA)
    result5 = cv2.cv.CalcEMD2(img, img2, cv2.cv.CV_DIST_L1)
    print result1
    print result2
    print result3
    print result4
    print result5
            
# cv2.cv.CalcEMD2(img, img2, cv2.cv.CV_DIST_L1, distance_func=None, cost_matrix=None, flow=None, lower_bound=None, userdata=None) 

def mousemov(x, y):
    _x, _y = win32api.GetCursorPos()
    m = (float(_y - y) / float(_x - x))
    b = float(y - (m*x))
    i = _x
    while win32api.GetCursorPos() != (x, y):
        if i < x:
            i = i + 1
        elif i > x:
            i = i - 1  
        fx = (m*i + b)
        time.sleep(0.0009)
        win32api.SetCursorPos((i, abs(int(fx))))
        
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,500,500,0,0) #Downclick
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,500,500,0,0) #Up

def isStartScreenOpen():
    #load IMG
    startImg = cv2.imread('/BA/Pictures/StartScreen.jpg') 
    #convert IMG to gray
    startImg_gray =cv2.cvtColor(startImg,cv2.COLOR_BGR2GRAY)
    #SURF
    surf = cv2.FeatureDetector_create("SURF")
    surfDescriptorExtractor = cv2.DescriptorExtractor_create("SURF")
    kp = surf.detect(startImg_gray)
    kp, descritors = surfDescriptorExtractor.compute(startImg_gray,kp)
    

def image_percantage(): 
    time.sleep(0.5)
    i1 = Image.open("D:\BA\Pictures\StartScreen.png")
    width, height = i1.size
    i2 = ImageGrab.grab(bbox=(0,0,width,height))
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."
 
    pairs = izip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
 
    ncomponents = i1.size[0] * i1.size[1] * 3
    print "Difference (percentage):", (dif / 255.0 * 100) / ncomponents

def pytesser_test():
    img = Image.open("D:\\BA\\v1\\BA_v1\\BA_v1\\images\\Hearthstone_Screenshot_11.13.2014.11.09.39.png")
    width, height = img.size
    img2 = img.resize((width*4, height*4))
    str = pytesser.image_to_string(img2);
    print str

 # D:\BA\v1\BA_v1\BA_v1\images\Hearthstone_Screenshot_11.13.2014.11.04.06.png
from ctypes import *
from ctypes.wintypes import *

def isHearthstoneRunning():
    processes = psutil.get_pid_list()
    for process in processes:
        name = psutil.Process(process).name.__str__()
        if "Hearthstone.exe" in name:
            print "is running"
            return process
    print "Hearthstone wasn't started, yet. Please start Hearthstone and restart this Script!"
    return -1

def openProcess():
    
    OpenProcess = windll.kernel32.OpenProcess
    ReadProcessMemory = windll.kernel32.ReadProcessMemory
    CloseHandle = windll.kernel32.CloseHandle
    
    PROCESS_ALL_ACCESS = 0x1F0FFF

    pid = isHearthstoneRunning() 

    processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    
    print processHandle  

def blobs():
    image = cv2.imread("D:\\Pictures\\Hearthstone\\rdy\\rdy04.jpg")
    img_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    ret,thresh = cv2.threshold(img_gray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,255,0), 3)
    plt.imshow(image), plt.show()

def object_detect():
    end_turn= cv2.CascadeClassifier('D:\\BA\\Bachelor\\Bachelor\\Ba\\data\\cascade.xml')
    img = cv2.imread('D:\\BA\\Bachelor\\Bachelor\\Ba\\images\\pos\\IMG11.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    end = end_turn.detectMultiScale(gray, 1.1, 1)
    print len(end)
    for (x,y,w,h) in end:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import subprocess
def grayscale():
    path = "D:\\opencv\\build\\x64\\vc12\\bin\\pos"
    name = "grayscale"
    num = 1
    for file in os.listdir(path):
        img = Image.open(path+"\\"+file).convert('LA')
        img.save(name+str(num)+".png")
        num += 1

def screenshots():
    num = 246
    while True:
        img=ImageGrab.grab()
        img2 = img.convert('LA')
        img2.save(path('images\\Screens')+'\\Screen'+str(num)+'.png')
        num += 1
        time.sleep(2)
        
    
def image_slicing():
    #number = str(num)
    #img = Image.open(_path)
    img = ImageGrab.grab()
    img = img.resize((800, 600), Image.BICUBIC)
    #img = img.convert('LA')
    #enemySide = img.crop((197, 177, 605, 279))
    #mySide = img.crop((197 , 281, 605, 383))
    #turn = img.crop((614, 248, 685, 292))
    enemy = img.crop((361, 48, 442, 167))
    me = img.crop((361, 394, 442, 513))
    #enemy_mana = img.crop((490, 26, 528, 50))
    #my_mana = img.crop((508, 543, 546, 567))
    #stack = img.crop((118, 169, 149, 411))
    #my_Hand = img.crop((246, 518, 483, 591))
    #enemy_Hand = img.crop((246, 0, 483, 44))
    #enemySide.save(path('images\\enemyField')+'\\efield'+number+'.png')
    #mySide.save(path('images\\myField')+'\\field'+number+'.png')
    #turn.save(path('images\\turn')+'\\turn'+number+'.png')
    num1 = len(os.listdir(path('images\\character\\new\\tmp')))
    enemy.save(path('images\\character\\new\\tmp')+'\\rogue'+str(num1)+'.png')
    me.save(path('images\\character\\new\\tmp')+'\\shaman'+str(num1 + 1)+'.png')
    #enemy_mana.save(path('images\\mana')+'\\e_mana'+number+'.png')
    #my_mana.save(path('images\\mana')+'\\mana'+number+'.png')
    #stack.save(path('images\\stack')+'\\stack'+number+'.png')
    #my_Hand.save(path('images\\myHand')+'\\myhand'+number+'.png')
    #enemy_Hand.save(path('images\\enemyHand')+'\\enemyhand'+number+'.png')
    print 'Done'
    
def colorAvg(img):
    w, h = img.size
    pixels = img.load()
    data = []
    for x in range(w):
        for y in range(h):
            cpixel = pixels[x, y]
            data.append(cpixel)
    r = 0
    g = 0
    b = 0
    counter = 0
    for x in range(len(data)):
        #if data[x][3] > 200:
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

def blobDetection(img, GameStart):
    w, h = img.size
    x = w - 8 
    if GameStart:
        while(x >= w/2):
            imgValue.append(img.crop((x-10, 0, x, h)))
            colorValue.append(colorAvg(img.crop((x - 10, 0, x, h))))
            x -= 29
        return 0
        #for x in colorValue: print x
    else:
        count = 0
        maxCount = 7
        while(x >= w/2):
            pix = img.crop((x-10, 0, x, h))
            cav = colorAvg(img.crop((x - 10, 0, x, h)))
            
            pix = np.asarray(pix)
            base = np.asarray(imgValue[count])
            
            hist1 = cv2.calcHist([base], [0], None, [256],[0, 255])
            hist1 = cv2.normalize(hist1).flatten()
            hist2 = cv2.calcHist([pix],[0], None, [256],[0, 255])
            hist2 = cv2.normalize(hist2).flatten()
            
            #result1 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CORREL)
            #result2 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_CHISQR)
            #result3 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_INTERSECT)
            result4 = cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_BHATTACHARYYA)
            
            #print cav
            #print colorValue[count]
            if(cav != colorValue[count]): 
                if(result4 <= 0.25):
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
        
def objdetect():
    s_arr = ['paladin', 'priest', 'shaman', 'warrior', 'warlock', 'mage', 'druid', 'hunter', 'rogue']
    px = path('images\\character\\new\\small')
    file3 = open(px+'\\counter.txt', 'w')
    for s in s_arr:
        p = path('images\\character\\new\\small')
        file = open(p+'\\pos_'+s+'.info', 'w')
        file2 = open(p+'\\bad'+s+'.txt', 'w')  
        p = p + '\\' + s
        num = 0
        num2 = 0
        counter1= 0
        for f in os.listdir(p):
            if counter1 >= 504:
                break
            num += 1
            img = Image.open(p + '\\' + f)
            w, h = img.size
            file.write(s+'/'+f+ ' 1 0 0 ' + str(w) + ' ' + str(h) + '\n')
            counter1 += 1
        file3.write(s + ": pos: " + str(num))
        for s2 in s_arr:
            if s == s2:
                continue
            p2 = path('images\\character\\new\\small\\' + s2)
            counter2 = 0
            for f2 in os.listdir(p2):
                if counter2 >= 63:
                    continue
                num2 += 1
                img2 = Image.open(p2 + '\\' + f2)
                w, h = img2.size
                file2.write(s2+'/'+f2 + '\n')
                counter2 += 1
        file3.write(' neg: ' + str(num2) + '\n')            
            
def blue():
    img = Image.open(path('images\\Handtest.png'))
    img.show()
    pix = img.load()
    w, h = img.size
    count = 0
    for x in range(w):
        for y in range(h):
            data = pix[x,y]
            if data[2] > 200:
                #print '('+str(x)+' '+str(y)+')'
                pix[x,y] = (255, 0, 0)
                count += 1
    print count
    #img.show()

def handcount(img):
    w,h = img.size
    pixels = img.load()
    x = 0
    while x < w:
        
        r = 0
        g = 0
        b = 0
        rows = 0

        if(x >= 52):
            y = 0
            h2 = 0
        else:
            y = 33
            h2 = 33
        while y < h:
            if x >= 52:
                inner_x = 4
            else:
                inner_x = 3
            rows = inner_x + 1 
            while inner_x >= 0:
                tmp_x = x + inner_x
                r += pixels[tmp_x,y][0]
                g += pixels[tmp_x,y][1]
                b += pixels[tmp_x,y][2]
                inner_x -= 1
            y += 1
        count = (h - h2) * rows
        avgR = r/count
        avgG = g/count
        avgB = b/count
        print x
        x += rows
        print '(' + str(avgR) + ' ' + str(avgG) + ' ' + str(avgB) + ')'

def edge(p):
    ranges = np.array([[111,120,1],[84,90,2],[57,63,3],[27,36,4],[23,31,5],[16,23,6],[14,21,7],[7,15,8],[2, 9, 9], [3,7,10]]) 
    
    img = cv2.imread(p,0)
    edges = cv2.Canny(img,237,73)
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

def singleMinionsValues(minions):
    if len(minions) == 0:
        return
    num = len(os.listdir(path('images\\attack')))
    for minion in minions:
        attack = minion.crop((6, 68, 21, 82))
        life = minion.crop((38, 68, 53, 82))
        attack.save(path('images\\attack')+'\\attack'+ str(num) +'.tif')
        life.save(path('images\\life')+'\\life'+ str(num) +'.tif')
        num += 1
        
def enemyDetection(img):
    detected = 0
    for cascade in os.listdir(path('data\\characters')):
        casc = cv2.CascadeClassifier(path('data\\characters')+'\\'+cascade)
        _img = np.asarray(img)
        char = casc.detectMultiScale(_img, 1.1, 1)
        if len(char) == 1:
            detected += 1
            print cascade
    if detected == 1:
        print 'Enemy Hero detected'
    elif detected == 0:
        print 'No Enemy Hero detected'
    else:
        print 'detection not clear'

def renameAttack():
    p = path('images\\attack')
    num = 1
    for file in os.listdir(p):
        s, end = file.split('.')
        name = s[:6] + str(num) + '.' + end
        Image.open(p+'\\'+file).save(p+'\\'+name)
        num += 1
    p = path('images\\life')
    num = 1
    for file in os.listdir(p):
        s, end = file.split('.')
        name = s[:4] + str(num) + '.' + end
        Image.open(p+'\\'+file).save(p+'\\'+name)
        num += 1
            
def isMouseMoved():
    NotMoved = True
    pos =  win32api.GetCursorPos()
    oldpos = pos
    count = 0
    while NotMoved:
        pos = win32api.GetCursorPos()
        if not pos == oldpos:
            NotMoved = False
            print NotMoved
            isMouseMoved()
        count += 1
        if count == 30:
            return True
        time.sleep(0.1)
        print NotMoved

def boxing():
    p = path('images\\attack')
    for file in os.listdir(p):
        name, end = file.split('.')
        box = name + '.box'
        if end == 'tif' and not (box in os.listdir(p)):
            newBox = open(p + '\\' + name + '.box', 'w')
            
            input = raw_input('Enter the number: ')
            print 'number: ' + str(input)
            newBox.write(str(input) + ' 0 0 15 14 0')


def sort():
     p = path('images\\attack')
     toDel = []
     for file in os.listdir(p):
        name, end = file.split('.')
        if end == 'box':
            file2 = open(p+'\\'+file, 'r')
            content = file2.read()
            if '?' in content:
                print name
                toDel.append(p+'\\'+name+'.tif')
                toDel.append(p+'\\'+name+'.box')
            file2.close()
     for k in toDel:
         print k
         os.remove(k)
        

     p = path('images\\life')
     toDel = []
     for file in os.listdir(p):
        name, end = file.split('.')
        if end == 'box':
            file2 = open(p+'\\'+file, 'r')
            content = file2.read()
            if '?' in content:
                print name
                toDel.append(p+'\\'+name+'.tif')
                toDel.append(p+'\\'+name+'.box')
                file2.close()
     for k in toDel:
         print k
         os.remove(k)

def rename():
    p = path('images\\combined')
    num = 0
    name = 'hearth'
    for file in os.listdir(p):
        front , dict, end = file.split('.')
        os.rename(p+'\\'+file, p+'\\'+front+'.'+name+'.exp'+str(num)+'.'+end)
        if end == 'tif':
            num +=1

def eight():
   # p= path('images\\attack')
    p2 = path('images\\attack_grey')
   # for file in os.listdir(p):
    #    name, end = file.split('.')
     #   if end == 'tif':
        #    img = Image.open(p +'\\' + file)
           # img.save(p2+'\\'+name+'.png')
    
    for file in os.listdir(p2):
        img = Image.open(p2+'\\'+file)
        img = img.resize((8,8), Image.BICUBIC)
        img =  img.convert('LA')
        img.save(p2+'\\'+file)
        
def decoloringNumbers(img):
    w, h = img.size
    pixels = img.load()
    tmp_pixels = controllingGreen(pixels, w, h)
    if(tmp_pixels == None):
        tmp_pixels = controllingRed(pixels, w, h)
    if(tmp_pixels == None):
        tmp_pixels = controllingWhite(pixels, w, h)
    
    pixels = makeBlack(tmp_pixels, w, h)
    num = len(os.listdir(path('images/handcardnumbers/numbers')))
    img.save(path('images/handcardnumbers/numbers')+'/num'+str(num)+'.png')
    

def controllingGreen(pixels, w, h):    
    count = 0
    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x,y]
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
            r, g, b = pixels[x,y]
            if x >= (w/2) and count == 0:
                return None
            if r==0 and g > 100 and b == 0:
                pixels[x,y] = (0, 0, 0)
                count += 1
            
    return pixels 
          
def controllingWhite(pixels, w, h):             
    for x in range(w):
        for y in range(h):
            r, g, b = pixels[x,y]
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

def testdecolor():
    p= path('images\\attack')
    for file in os.listdir(p):
        name, end = file.split('.')
        if end == 'tif':
            img = Image.open(p+'\\'+file)
            decoloringNumbers(img)
            
    p2= path('images\\life')
    for file2 in os.listdir(p2):
        name, end = file2.split('.')
        if end == 'tif':
            img = Image.open(p2+'\\'+file2)
            decoloringNumbers(img)  


import pylab as pl
from sklearn import datasets, svm, metrics

def digits():
    # The digits dataset
    digits = datasets.load_digits()

    # To apply a classifier on this data, we need to flatten the image, to
    # turn the data in a (samples, feature) matrix:
    n_samples = len(digits.images)
    data = digits.images.reshape((n_samples, -1))
    print data
    print data.shape
    print digits.images.shape
    
    # Create a classifier: a support vector classifier
    classifier = svm.SVC(gamma=0.001)

    # We learn the digits on the first half of the digits
    classifier.fit(data[:n_samples / 2], digits.target[:n_samples / 2])

    # Now predict the value of the digit on the second half:
    expected = digits.target[n_samples / 2:]
    predicted = classifier.predict(data[n_samples / 2:])

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

def  resort_number():
    p = path('images/black_white')
    f = open(p+'/target.info', 'w')
    arr = []
    n = 0
    while n <= 3243:
        for file in os.listdir(p):
            name, end = file.split('.')
            if str(n) == name[3:]:
                num = raw_input(str(n) + ' -- Number: ')
                arr.append((n, num))
        n += 1
    for i in arr:
        f.write(str(i[0]) + ' ' + str(i[1]) +'\n')
  
def naming():
    file = open(path('images/black_white/target.info'), 'w')
    arr = ['0','1','2','3','4','5','6','7','8','9','0','x']
    for s in arr:
        p = path('images/'+s)
        for f in os.listdir(p):
            name, end = f.split('.')
            file.write(str(name[3:]) + ' ' + s + '\n')

def resort():
    f = open(path('images/black_white/target.info'), 'r')
    c = f.readlines()

    start = (0, 0)

    arr1 = []

    for l in c:     
        arr1.append(str(l))

    arr = np.array(arr1)
    arr.sort()
    
    f2 = open(path('images/black_white/target3.info'), 'w')
    for a in arr:
        f2.write(a.split(' ')[1])

class Bunch(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self

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

    


    #while n < len(data):
     #  dataset[0].append(data[n])
      # dataset[1].append(numbers[n])
       #n += 1
   # return Bunch(data = dataset[0]
    #             target = 
     #            target_names =
      #           images =
       #          DESCR =
        #)

def my_digits():
    digits = _data()
    
    n_samples = len(digits.images)
    datas = digits.images.reshape((n_samples, -1))
    #classifier = svm.SVC(gamma=0.001)
    classifier = RandomForestClassifier()
    classifier.fit(datas[:n_samples / 2], digits.target[:n_samples / 2])

    expected = digits.target[n_samples / 2:]
    predicted = classifier.predict(datas[n_samples / 2:])
    
    n = 0
    count = 0
    while n < len(predicted):
        if not predicted[n] == expected[n]:
            print predicted[n], expected[n]
            count += 1
        n += 1
    print len(predicted)
    print 'wrong: ' + str(count)
     
def biggerThanNine(new_digit, clf):
    zeroArr = np.zeros(15)
    images = new_digit.images
    for array in images:
        for i in range(2, len(array) - 3):
            if array[i] == 0:
                zeroArr[i] += 1
    indexOfMax = np.argwhere(zeroArr == np.amax(zeroArr))
    image_one = []
    image_two = []
    for array in images:
        i = 0
        tmp_arr1 = []
        tmp_arr2 = []
        while i < len(array):
            if i < indexOfMax:
                tmp_arr1.append(array[i])
            elif i == indexOfMax:
                tmp_arr1.append(array[i])
                tmp_arr2.append(array[i])
            else:
                tmp_arr2.append(array[i])
            i += 1
        image_one.append(np.array(tmp_arr1))
        image_two.append(np.array(tmp_arr2))
    image_one = np.array(image_one)
    image_two = np.array(image_two)
    
    for arr in image_one:
        half = (15 - len(arr))/2
        while half > 0:
            np.insert(arr, 0, 0)
            arr.append(0)
            half -= 1
        if not len(arr) == 15:
            arr.append(0)
            
    for arr in image_two:
        half = (15 - len(arr))/2
        while half > 0:
            np.insert(arr, 0, 0)
            arr.append(0)
            half -= 1
        if not len(arr) == 15:
            arr.append(0)
    
    dataOne = image_one.flatten(),
                   
    dataTwo =image_two.flatten()
        
    pr1 = clf.predict(dataOne)
    pr2 = clf.predict(dataTwo)
    
    return int(str(pr1)+str(pr2))    

def enemyDetection():
    chars = np.array(['warrior', 'warlock', 'mage', 'druid', 'rogue', 'shaman', 'paladin', 'priest', 'hunter'])   
    data = []
    target = []
    for c in chars:
        p = path('images/character/new/small')
        p = p + '/' + c
        for f in os.listdir(p):
            img = Image.open(p+'/'+f)
            w, h = img.size
            pixel = img.load()
            tmp = []
            for y in range(h):
                for x in range(w):
                    #print pixel[x,y]
                    #time.sleep(30)
                    tmp.append(np.float(pixel[x,y][0] / 16))
            target.append(np.str(c))
            data.append(np.array(tmp))
        #print tmp, c
    data = np.array(data)
    #image = data.view()
    #image.shape = (-1, 22, 30)
    #clf = svm.SVC(gamma = 0.001)
    clf = RandomForestClassifier()
    clf.fit(data, target)

    im = Image.open(path('images/character/Warlock/warlock151.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    expected = np.array([np.str('Warlock')])
    print("Classification report for classifier %s:\n%s\n"
      % (clf, metrics.classification_report(expected, predict)))
    print "Warlock: ", predict[0]

    im = Image.open(path('images/character/Hunter/hunter5.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(np.float(pixel[x,y][0] / 16))
    predict = clf.predict(np.array(arr))
    print "Hunter: ",predict[0]

    im = Image.open(path('images/character/Paladin/paladin1101.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    print "Paladin: ",predict[0]

    im = Image.open(path('images/character/Priest/priest750.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    print "Priest: ", predict[0]

    im = Image.open(path('images/character/Mage/mage980.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    print "Mage: ", predict[0]

    im = Image.open(path('images/character/Shaman/shaman56.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    print "Shaman: ", predict[0]

    im = Image.open(path('images/character/Warrior/warrior970.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    print "Warrior: ", predict[0]

    im = Image.open(path('images/character/Druid/druid1.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    print "Druid: ", predict[0]

    im = Image.open(path('images/character/Rogue/rogue10.png'))
    w, h = img.size
    arr = []
    for y in range(h):
        for x in range(w):
            arr.append(pixel[x,y][0] / 16)
    predict = clf.predict(np.array(arr))
    print "Rogue: ", predict[0]

def new_images():
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

    #for c in chars:
     #   p = path('images/character/new/black')
      #  for f in os.listdir(p+'/'+c):
       #     img = Image.open(p+'/'+c+'/'+f)
        #    w, h = img.size
         #   pixel = img.load()
          #  arr = []
           # for y in range(h):
            #    for x in range(w):
             #       arr.append(np.float(pixel[x,y] / 255))
          #  predict = clf.predict(np.array(arr))
           # if not c == predict[0]:
            #    print c, predict[0]
    
def enemyDetection1(img):
    
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

    
def cardDetectScreenshot():
    img = ImageGrab()
    img = img.resize((800,600), Image.CUBIC)
    img = img.crop((206, 301, 502, 580))
    
def cutForSingleCard(img):
    w, h = img.size
    im = np.asarray(img)
    edges = cv2.Canny(im, 200, 100)

    row_1_count = 0
    row_2_count = 0
    for x in range(w - 1):
        y = 50
        while y < 180:
            if edges[y][x] == 255:
                row_1_count += 1
            y += 1 
        row_count = row_1_count + row_2_count
        if row_count >= 100:
            print x
            img = img.crop(((x-6), 0, (x+141), h))
            n = np.asarray(img)
            plt.imshow(n), plt.show()
            valuesOfSingleCard(img)
            break;
        else:
            row_2_count = row_1_count
            row_1_count = 0
         

def valuesOfSingleCard(img):
    attack = img.crop((8, 240, 33, 271)) #25x31
    life = img.crop((120, 240, 145, 271)) #25x31
    mana = img.crop((2, 13, 32, 46)) # 30x33
    #erstellen von clf bzw. zusehen wie ich den schon erstellten clf darauf anweden kann?!

def ScreenForCardNum():
    img = ImageGrab.grab()
    img = img.resize((800,600), Image.CUBIC)
    img = img.crop((206, 301, 560, 580))
    num = len(os.listdir(path('images/handcardnumbers/wholehand/')))
    img.save(path('images/handcardnumbers/wholehand/wholehand'+str(num)+'.png'))
    w, h = img.size
    im = np.asarray(img)
    edges = cv2.Canny(im, 200, 100)
    row_1_count = 0
    row_2_count = 0
    for x in range(w - 1):
        y = 50
        while y < 180:
            if edges[y][x] == 255:
                row_1_count += 1
            y += 1 
        row_count = row_1_count + row_2_count
        if row_count >= 100:
            img = img.crop(((x-6), 0, (x+141), h))
            img.save(path('images/handcardnumbers/wholecard/wholecard'+str(num)+'.png'))
            attack = img.crop((8, 240, 33, 271))
            life = img.crop((120, 240, 145, 271))
            mana = img.crop((2, 13, 32, 46))
            attack = attack.resize((15,14), Image.CUBIC)
            life = life.resize((15,14), Image.CUBIC)
            mana = mana.resize((15,14), Image.CUBIC)
            decoloringNumbers(mana)
            decoloringNumbers(attack)
            decoloringNumbers(life)
            break;
        else:
            row_2_count = row_1_count
            row_1_count = 0
            
    






  
        


            


    

    