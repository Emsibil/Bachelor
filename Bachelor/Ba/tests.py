from Util_new import path
from os import listdir
def opencv():
    p1 = path('images/turn/end')
    p2 = path('images/turn/enemy')
    p3 = path('images/turn')
    info = open(p3+'/pos.info', 'w')
    txt = open(p3+'/neg.txt', 'w')
    for f in listdir(p1):
        info.write('end/'+f+' 1'+' 0'+' 0'+' 71'+' 44'+'\n')
    for f in listdir(p2):
        txt.write('enemy/'+f+'\n')
        
opencv()