import numpy as np
import cv2
import ImageGrab as grab
import psutil
import testing
import Image
import time
from itertools import izip

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
    end_turn= cv2.CascadeClassifier(path("cascade.xml"))
    while True:
        tmp_img = grab.grab()
        np_img = np.asarray(tmp_img)
        #gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)   if i want to change it to grayscale images
        end = end_turn.detectMultiScale(np_img, 1.1, 1)
        count = len(end)
        if count == 1:
            print "My Turn"
        elif count == 0:
            print "His Turn or Menu"
        else:
            print "More than one End-Turn-Image. The training need to be more detailed!"
        time.sleep(5)
            

def whoseTurn():
    while True:
        if isHearthstoneRunning():
            isMyTurn()
        else:
            time.sleep(10)

whoseTurn()



