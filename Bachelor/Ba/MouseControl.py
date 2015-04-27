import win32api, win32con
import numpy as np
import time

RESOLUTION = (1920, 1080)
def getResolution():
    global RESOLUTION
    return RESOLUTION
def setResolution(value):
    global RESOLUTION
    RESOLUTION = value
def area(rel_area):
    resolution = getResolution()
    x = int(resolution[0]*rel_area[0])
    y = int(resolution[1]*rel_area[1])
    width =int(resolution[0]*rel_area[2])
    hight = int(resolution[1]*rel_area[3])
    return (x, y, width, hight)

h1 = {1: np.array([(0.45, 0.8712, 0.0609, 0.1296)])}
h2 = {1: np.array([(0.4151, 0.8712, 0.0609, 0.1296)]), 
      2: np.array([(0.4854, 0.8712, 0.0609, 0.1296)])}
h3 = {1: np.array([(0.3812, 0.8722, 0.0578, 0.1277)]), 
      2: np.array([(0.4520, 0.8731, 0.0588, 0.1333)]),
      3: np.array([(0.5213, 0.8722, 0.0588,  0.125)])}
h4 = {1: np.array([(0.3489, 0.9148, 0.051, 0.0851)]), 
      2: np.array([(0.4192, 0.8861, 0.0531, 0.1148)]),
      3: np.array([(0.4838, 0.8703, 0.063, 1296)]), 
      4: np.array([(0.5593, 0.8962, 0.0546, 0.1037)])}
h5 = {1: np.array([(0.3437, 0.9064, 0.038, 0.0935)]), 
      2: np.array([(0.4, 0.8851, 0.0416, 0.1148)]),
      3: np.array([(0.452, 0.874, 0.0489, 0.1287)]), 
      4: np.array([(0.5062, 0.8805, 0.0479, 0.125)]), 
      5: np.array([(0.5682, 0.9111, 0.0526, 0.0888)])}
h6 = {1: np.array([(0.3338, 0.9296, 0.038, 0.0703)]), 
      2: np.array([(0.3848, 0.9, 0.0333, 0.1)]),
      3: np.array([(0.4302, 0.8824, 0.038, 0.1194)]), 
      4: np.array([(0.4723, 0.8703, 0.0406, 0.1296)]), 
      5: np.array([(0.5234, 0.8787, 0.0343, 0.1212)]), 
      6: np.array([(0.5734, 0.907, 0.0925)])}
h7 = {1: np.array([(0.3333, 0.925, 0.0239, 0.075),(0.325, 0.9333, 0.0354, 0.0351)]), 
      2: np.array([(0.3765, 0.9046, 0.0239, 0.0953),(0.3645, 0.9111, 0.0375, 0.0287)]),
      3: np.array([(0.4161, 0.8870, 0.0265, 0.1148),(0.4526, 0.8768, 0.0364, 0.0398)]), 
      4: np.array([(0.4526, 0.8768, 0.0322, 0.1231)]), 
      5: np.array([(0.4927, 0.8777, 0.0286, 0.1231)]), 
      6: np.array([(0.5375, 0.8898, 0.0239, 0.1101),(0.5343, 0.9138, 0.0359, 0.037)]), 
      7: np.array([(0.5786, 0.9259, 0.0505, 0.074)])}
h8 = {1: np.array([(0.3244, 0.9462, 0.0291, 0.0527)]), 
      2: np.array([(0.3661, 0.912, 0.0208, 0.087),(0.3531, 0.9194, 0.0369, 0.0259)]),
      3: np.array([(0.402, 0.8925, 0.0223, 0.1064),(0.3974, 0.8953, 0.0291, 0.0555)]), 
      4: np.array([(0.4348, 0.8759, 0.0276, 0.124)]), 
      5: np.array([(0.4661, 0.8694, 0.0307, 0.1296)]), 
      6: np.array([(0.5067, 0.8694, 0.0223, 0.1305),(0.5031, 0.9064, 0.0343, 0.0277)]), 
      7: np.array([(0.5458, 0.8787, 0.0177, 0.1212),(0.5447, 0.8925, 0.0317, 0.0444)]), 
      8: np.array([(0.5807, 0.9203, 0.0515, 0.0805)])}
h9 = {1: np.array([(0.3255, 0.9444, 0.0203, 0.0555),(0.3187, 0.9518, 0.0286, 0.0287)]),
      2: np.array([(0.3619, 0.9166, 0.0156, 0.0833),(0.3562, 0.9481, 0.0255, 0.0259)]),
      3: np.array([(0.3947, 0.8953, 0.014, 0.1046),(0.3854, 0.9111, 0.0265, 0.0379)]), 
      4: np.array([(0.425, 0.8851, 0.0182, 0.1148),(0.4171, 0.8962, 0.0281, 0.0296)]), 
      5: np.array([(0.452, 0.8768, 0.025, 0.1240)]), 
      6: np.array([(0.4833, 0.8777, 0.0218, 0.1222)]), 
      7: np.array([(0.5177, 0.8861, 0.0166, 0.1138),(0.5171, 0.8907, 0.0302, 0.025)]), 
      8: np.array([(0.552, 0.8981, 0.0156, 0.1018),(0.552, 0.9037, 0.0291, 0.342)]), 
      9: np.array([(0.6307, 0.9425, 0.0531, 0.0574)])}
h10 = {1: np.array([(0.3177, 0.9722, 0.025, 0.0277),(0.327, 0.949, 0.0098, 0.0231)]), 
       2: np.array([(0.3546, 0.9351, 0.0135, 0.0648),(0.3453, 0.9425, 0.0244, 0.024)]),
       3: np.array([(0.3854, 0.9083, 0.0119, 0.0925),(0.3755, 0.9175, 0.0239, 0.0324)]),
       4: np.array([(0.414, 0.8925, 0.014, 0.1074),(0.4062, 0.8972, 0.0234, 0.0462)]), 
       5: np.array([(0.439, 0.8805, 0.0197, 0.1203)]), 
       6: np.array([(0.464, 0.8731, 0.0218, 0.1277)]), 
       7: np.array([(0.4947, 0.8759, 0.0161, 0.124)]), 
       8: np.array([(0.5265, 0.8824, 0.0119, 0.1175),(0.5385, 0.887, 0.0119, 0.0388)]), 
       9: np.array([(0.5572, 0.8962, 0.0104, 0.1046),(0.5677, 0.8972, 0.0161, 0.0296)]), 
       10: np.array([(0.5859, 0.9361, 0.0515, 0.0638)])}

me = (0.4666, 0.7435, 0.0697, 0.9629)
enemy = (0.4666, 0.1574, 0.0697, 0.9629)

def getMe():
    global me
    return me
def getEnemy():
    global enemy
    return enemy

even1 = (0.2973, 0.5092, 0.0453, 0.0888)
even2 = (0.3697, 0.5092, 0.0453, 0.0888)
even3 = (0.4427, 0.5092, 0.0453, 0.0888)
even4 = (0.514, 0.5092, 0.0453, 0.0888)
even5 = (0.5864, 0.5092, 0.0453, 0.0888)
even6 = (0.6588, 0.5092, 0.0453, 0.0888)
uneven1 = (0.2609, 0.5092, 0.0453, 0.0888)
uneven2 = (0.3333, 0.5092, 0.0453, 0.0888)
uneven3 = (0.4062, 0.5092, 0.0453, 0.0888)
uneven4 = (0.4791, 0.5092, 0.0453, 0.0888)
uneven5 = (0.5494, 0.5092, 0.0453, 0.0888)
uneven6 = (0.6223, 0.5092, 0.0453, 0.0888)
uneven7 = (0.6953, 0.5092, 0.0453, 0.0888)

e_uneven1 = (0.2609, 0.3333, 0.0453, 0.0888)
e_uneven2 = (0.3333, 0.3333, 0.0453, 0.0888)
e_uneven3 = (0.4062, 0.3333, 0.0453, 0.0888)
e_uneven4 = (0.4791, 0.3333, 0.0453, 0.0888)
e_uneven5 = (0.5494, 0.3333, 0.0453, 0.0888)
e_uneven6 = (0.6223, 0.3333, 0.0453, 0.0888)
e_uneven7 = (0.6953, 0.3333, 0.0453, 0.0888)
e_even1 = (0.2973, 0.3333, 0.0453, 0.0888)
e_even2 = (0.3697, 0.3333, 0.0453, 0.0888)
e_even3 = (0.4427, 0.3333, 0.0453, 0.0888)
e_even4 = (0.514, 0.3333, 0.0453, 0.0888)
e_even5 = (0.5864, 0.3333, 0.0453, 0.0888)
e_even6 =  (0.6588, 0.3333, 0.0453, 0.0888)

def getEven1():
    global even1
    return even1
def getEven2():
    global even2
    return even2
def getEven3():
    global even3
    return even3
def getEven4():
    global even4
    return even4
def getEven5():
    global even5
    return even5
def getEven6():
    global even6
    return even6
def getUneven1():
    global uneven1
    return uneven1
def getUneven2():
    global uneven2
    return uneven2
def getUneven3():
    global uneven3
    return uneven3
def getUneven4():
    global uneven4
    return uneven4
def getUneven5():
    global uneven5
    return uneven5
def getUneven6():
    global uneven6
    return uneven6
def getUneven7():
    global uneven7
    return uneven7
def getE_Uneven1():
    global e_uneven1
    return e_uneven1
def getE_Uneven2():
    global e_uneven2
    return e_uneven2
def getE_Uneven3():
    global e_uneven3
    return e_uneven3
def getE_Uneven4():
    global e_uneven4
    return e_uneven4
def getE_Uneven5():
    global e_uneven5
    return e_uneven5
def getE_Uneven6():
    global e_uneven6
    return e_uneven6
def getE_Uneven7():
    global e_uneven7
    return e_uneven7
def getE_Even1():
    global e_even1
    return e_even1
def getE_Even2():
    global e_even2
    return e_even2
def getE_Even3():
    global e_even3
    return e_even3
def getE_Even4():
    global e_even4
    return e_even4
def getE_Even5():
    global e_even5
    return e_even5
def getE_Even6():
    global e_even6
    return e_even6

Minions0 = {0: getMe()}
Minions1 = {0: getMe(), 1: getUneven4()}
Minions2 = {0: getMe(), 1: getEven3(), 2: getEven4()}
Minions3 = {0: getMe(), 1: getUneven3(), 2: getUneven4(), 3: getUneven5()}
Minions4 = {0: getMe(), 1: getEven2(), 2: getEven3(), 3: getEven3(), 4: getEven4()}
Minions5 = {0: getMe(), 1: getUneven2(), 2: getUneven3(), 3: getUneven4(), 4: getUneven5(), 5: getUneven6()}
Minions6 = {0: getMe(), 1: getEven1(), 2: getEven2(), 3: getEven3(), 4: getEven4(), 5: getEven5(), 6: getEven6()}
Minions7 = {0: getMe(), 1: getUneven1(), 2: getUneven2(), 3: getUneven3(), 4: getUneven4(), 5: getUneven5(), 6: getUneven6(), 7: getUneven7()}
eMinions0 = {0: getEnemy()}
eMinions1 = {0: getEnemy(), 1: getE_Uneven4()}
eMinions2 = {0: getEnemy(), 1: getE_Even3(), 2: getE_Even4()}
eMinions3 = {0: getEnemy(), 1: getE_Uneven3(), 2: getE_Uneven4(), 3: getE_Uneven5()}
eMinions4 = {0: getEnemy(), 1: getE_Even2(), 2: getE_Even3(), 3: getE_Even3(), 4: getE_Even4()}
eMinions5 = {0: getEnemy(), 1: getE_Uneven2(), 2: getE_Uneven3(), 3: getE_Uneven4(), 4: getE_Uneven5(), 5: getE_Uneven6()}
eMinions6 = {0: getEnemy(), 1: getE_Even1(), 2: getE_Even2(), 3: getE_Even3(), 4: getE_Even4(), 5: getE_Even5(), 6: getE_Even6()}
eMinions7 = {0: getEnemy(), 1: getE_Uneven1(), 2: getE_Uneven2(), 3: getE_Uneven3(), 4: getE_Uneven4(), 5: getE_Uneven5(), 6: getE_Uneven6(), 7: getE_Uneven7()}

def getMinions0():
    global Minions0
    return Minions0
def getMinions1():
    global Minions1
    return Minions1
def getMinions2():
    global Minions2
    return Minions2
def getMinions3():
    global Minions3
    return Minions3
def getMinions4():
    global Minions4
    return Minions4
def getMinions5():
    global Minions5
    return Minions5
def getMinions6():
    global Minions6
    return Minions6
def getMinions7():
    global Minions7
    return Minions7
def getEMinions0():
    global eMinions0
    return eMinions0
def getEMinions1():
    global eMinions1
    return eMinions1
def getEMinions2():
    global eMinions2
    return eMinions2
def getEMinions3():
    global eMinions3
    return eMinions3
def getEMinions4():
    global eMinions4
    return eMinions4
def getEMinions5():
    global eMinions5
    return eMinions5
def getEMinions6():
    global eMinions6
    return eMinions6
def getEMinions7():
    global eMinions7
    return eMinions7

MinionBoard = {0: getMinions0(), 1: getMinions1(), 2: getMinions2(), 3: getMinions3(), 4: getMinions4(), 5: getMinions5(), 6: getMinions6(), 7: getMinions7()}
eMinionBoard = {0: getEMinions0(),1: getEMinions1(), 2: getEMinions2(), 3: getEMinions3(), 4: getEMinions4(), 5: getEMinions5(), 6: getEMinions6(), 7: getEMinions7()}

def getMinionBoard(minionsOnBoard):
    global MinionBoard
    return MinionBoard[minionsOnBoard]
def getEnemyMinionBoard(minionsOnBoard):
    global eMinionBoard
    return eMinionBoard[minionsOnBoard]

turn = (0.7843, 0.4361, 0.0567, 0.0296)
heroPower = (0.5666, 0.7259, 0.0468, 0.0722)
enemyHeroPower = (0.5666, 0.1824, 0.0468, 0.0722)
Mulligan = {3: np.array([(0.2734, 0.3472, 0.0989, 0.2638), (0.4505, 0.3472, 0.0989, 0.2638), (0.6302, 0.3472, 0.0989, 0.2638)]),
            4: np.array([(0.2526, 0.3472, 0.0989, 0.2638), (0.3541, 0.3472, 0.0989, 0.2638), (0.5182, 0.3472, 0.0989, 0.2638), (0.651, 0.3472, 0.0989, 0.2638)])}
MulliganConfirm = (0.4687, 0.7731, 0.0703, 0.037)

def getH10():
    global h10
    return h10
def getH9():
    global h9
    return h9  
def getH8():
    global h8
    return h8  
def getH7():
    global h7
    return h7  
def getH6():
    global h6
    return h6  
def getH5():
    global h5
    return h5  
def getH4():
    global h4
    return h4  
def getH3():
    global h3
    return h3  
def getH2():
    global h2
    return h2  
def getH1():
    global h1
    return h1  

Handcard = np.array([getH1(), getH2(), getH3(), getH4(), getH5(), getH6(), getH7(), getH8(), getH9(), getH10()])

def getHeroPower():
    global heroPower
    return heroPower
def getEnemyHeroPoer():
    global enemyHeroPower
    return enemyHeroPower
def getTurn():
    global turn
    return turn
def getMulliganConfirm():
    global MulliganConfirm
    return MulliganConfirm
def getMulligan(numberOfCards):
    global Mulligan
    try:
        if numberOfCards == 3 or numberOfCards == 4:
            return Mulligan[numberOfCards]
    except:
        print 'There is no Mulligan with ' + str(numberOfCards) + 'Handcards'

def getMulliganCardArea(CardPos, numberOfMulliganCards):   
    try:
        if numberOfMulliganCards >= CardPos:
            mul = getMulligan(numberOfMulliganCards)
            return mul[CardPos - 1]
    except:         
        print 'There is no Mulligancard at Pos: ' + str(CardPos)

def getHand(handcount):
    global Handcard
    return Handcard[handcount - 1]

def getHandcardArea(handcount, zonePos):
    print "get hand area"
    print handcount
    print zonePos
    if zonePos == 0:
        return area(getHeroPower())
    hand = getHand(handcount)
    rel_area = hand[zonePos]
    _area = area(rel_area[0])
    return _area

def getOnBoardArea(minionsOnBoard, card):
    area(getMinionBoard(minionsOnBoard)[card.get_pos()])
    
def getMouseMoveCoords(area):
    x = np.random.random_integers(area[0], area[0]+area[2])
    y = np.random.random_integers(area[1], area[1]+area[3])
    return (x, y)
    
def mouseMove(coords):
    win32api.SetCursorPos(coords)
    print 'Moved'
    
def mouseDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,500,500,0,0)

def mouseUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,500,500,0,0)

def mouseClick():
    mouseDown()
    time.sleep(0.01)
    mouseUp()

    
    
    #win32api.SetCursorPos((i, abs(int(fx)))) 
    #_x, _y = win32api.GetCursorPos()  
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,500,500,0,0) #Downclick
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,500,500,0,0) #Up