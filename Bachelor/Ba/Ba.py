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

#Takes a Screenshot and compares if there is an End Turn button in the image and evaluate if it's your turn or the opponents one
def isMyTurn():
    end_turn= cv2.CascadeClassifier(path("data\\endturn_cascade.xml"))
    while True:
        tmp_img = grab.grab()
        np_img = np.asarray(tmp_img)
        gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)   #if i want to change it to grayscale images
        end = end_turn.detectMultiScale(gray, 1.1, 1)
        count = len(end)
        if count == 1:
            print "My Turn"
        elif count == 0:
            print "His Turn or Menu"
        else:
            print "More than one End-Turn-Image. The training need to be more detailed!"
        time.sleep(2)
            

def whoseTurn():
    while True:
        if isHearthstoneRunning():
            isMyTurn()
        else:
            time.sleep(3)

#whoseTurn()
#testing.object_detect()
#testing.screenshots()

#num = 1100
#while True:
#    time.sleep(2)
#    testing.image_slicing(str(num))
#    num += 1
im0 = Image.open(path("images\\enemyField\\efield1105.png")) #0
im1 = Image.open(path("images\\enemyField\\efield1109.png")) #1
im2 = Image.open(path("images\\enemyField\\efield1124.png")) #2
im3 = Image.open(path("images\\enemyField\\efield1156.png")) #3
im4 = Image.open(path("images\\enemyField\\efield1229.png")) #4
im5 = Image.open(path("images\\enemyField\\efield1218.png")) #5
im6 = Image.open(path("images\\enemyField\\efield1245.png")) #6
im7 = Image.open(path("images\\enemyField\\efield1255.png")) #7
testing.blobDetection(im0, True)
testing.blobDetection(im1, False) #1
testing.blobDetection(im2, False) #2
testing.blobDetection(im3, False) #3
testing.blobDetection(im4, False) #4
testing.blobDetection(im5, False) #5
testing.blobDetection(im6, False) #6
testing.blobDetection(im7, False) #7
