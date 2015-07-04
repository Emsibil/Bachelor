from Util_new import path
from tables import Enum
 
f = open(path('cards/cards.info'), 'r').readlines()
nf = open(path('cards')+'/whenever.txt', 'w')
for l in f:
    if 'CardTextInHand' in l:
        if 'Whenever' in l or 'whenever' in l:
            txt = l.split('CardTextInHand:')[1]
            nf.write(txt) 

        
#print round(1.9, 0)
#print round(-1.9, 0)