import numpy
import cv2
import psutil
from PIL import Image
from PIL import ImageGrab
import matplotlib.pyplot as plt
from threading import Timer
import win32api, win32con
import time
from itertools import izip
import os
import sys
sys.path.insert(0, 'D:\\BA\\Bachelor\\Bachelor\\Ba\\lib')
import pytesser

def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

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
    
    print cv2.cv.CalcEMD2(img, sec_img, cv2.cv.CV_DIST_L2)

def testing_img2():
    time.sleep(5)
    img = cv2.imread('D:\BA\Pictures\StartScreen.png',1)
    img1 = Image.open('D:\BA\Pictures\StartScreen.png')
    img_width, img_height = img1.size
    img2 = ImageGrab.grab(bbox=(0,0,img_width,img_height))
    img_2 = numpy.asarray(img2)
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