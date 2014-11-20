import numpy as np
import cv2
import ImageGrab
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
            return process
    print "Hearthstone wasn't started, yet. Please start Hearthstone and restart this Script!"
    return -1


def image_percantage(): 
    time.sleep(0.5)
    i1 = Image.open(path("StartScreen.png"))
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

#returns the full path of a special file
def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path


from ctypes import *
from ctypes.wintypes import *

def read_memory():
    
    OpenProcess = windll.kernel32.OpenProcess
    ReadProcessMemory = windll.kernel32.ReadProcessMemory
    CloseHandle = windll.kernel32.CloseHandle

    PROCESS_ALL_ACCESS = 0x1F0FFF

    pid = isHearthstoneRunning()  # I assume you have this from somewhere.
    address = 0x1000000  # Likewise; for illustration I'll get the .exe header.

    buffer = c_char_p("The data goes here")
    bufferSize = len(buffer.value)
    bytesRead = c_ulong(0)

    processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if ReadProcessMemory(processHandle, address, buffer, bufferSize, byref(bytesRead)):
        print "Success:", processHandle
    else:
        print "Failed."

    CloseHandle(processHandle)

#isHearthstoneRunning()

#testing.testing_img2()

#testing.mousemov(100, 100)

#t = 30
#while t > 0:
 #   testing.image_percantage()
  #  t -= 1

#testing.pytesser_test()

#testing.blobs()
testing.testing_img()


