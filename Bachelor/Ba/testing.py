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
sys.path.insert(0, 'D:\\BA\\v1\\BA_v1\\BA_v1\\lib')
import pytesser


def takingScreen():
    im = ImageGrab.grab()
    plt.imshow(im), plt.show()

def testing_img():
    time.sleep(5)
   # img = cv2.imread('D:\BA\Pictures\StartScreen.png',0)
    _img = Image.open('D:\BA\Pictures\StartScreen.png')
    imgwidth, imgheight = _img.size
    print _img.size
    surf = cv2.SURF(1000)
    kp, des = surf.detectAndCompute(img,None)
    kp, des = surf.detectAndCompute(img,None)
    surf.upright = True
    kp = surf.detect(img,None)
    surf.extended = True
    kp, des = surf.detectAndCompute(img,None)
    img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)  
    im = ImageGrab.grab(bbox=(0,0,imgwidth,imgheight))
    print im.size
    sec_img = numpy.asarray(im)
    sec_img_gray =cv2.cvtColor(sec_img,cv2.COLOR_BGR2GRAY)
    kp2, des2 = surf.detectAndCompute(sec_img_gray,None)
    secImg = cv2.drawKeypoints(sec_img_gray,kp2,None,(255,0,0),4)

    #plt.imshow(secImg), plt.show()
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
  
