from tables import Enum
from Bachelor.Ba.LogInterpreter import getOptions
from Bachelor.Ba.Board import getMyCards, getEnemyCards
from Bachelor.Ba.Util_new import Zone, Cardtype, Option
from Bachelor.Ba.Damage import dmg

OPTIONS = getOptions()

class Effectivness(Enum):
    WORSE = -2
    BAD = -1
    LOW = 0
    GOOD = 1
    GREAT = 2
    
class ThreatLvl(Enum):
    HIGH = -2
    INCREASEd = -1
    NORMAL = 0
    LOW = 1
    NONE = 2
    
def MinionDmg():
    dmg = 0 
    for c in getMyCards.values():
        if c._zone == Zone.PLAY:
            if c.mayAttack():
                if c._cardtype == Cardtype.MINION or (c._cardtype == Cardtype.HERO and c._attack > 0) or (c._cardtype == Cardtype.WEAPON): 
                    dmg = dmg + c.getAttack()
    return dmg

def EnemyMinionLife():
    life = 0
    for c in getEnemyCards.values():
        if c.compareZone(Zone.PLAY) and c.compareCardtype(Cardtype.MINION):
            life = life + c.getHealth() - c.getDamage()
    return life

def EnemyAttackPower():
    dmg = 0
    for c in getEnemyCards.values():
        if c.compareZone(Zone.PLAY):
            if c.compareCardtype(Cardtype.MINION) or c.compareCardtype(Cardtype.WEAPON):
                dmg = dmg + c.getAttack()
    return dmg

def ThreatLvlForMyHero():
    health = [(c.getHealth() + c._armor) for c in getMyCards().values() if c.compareCardtype(Cardtype.HERO)]
    return round((-4*(EnemyAttackPower()/health) + 2), 0)
   

def options(options):
    for o in options:
        if o[1] == Option.PLAY:
            if o[2] is None:
                pass
            else:
                pass
        elif o[1] == Option.ATTACK:
            pass
        else:
            pass
            

# [Power] GameState.DebugPrintOptions() -   option 0 type=END_TURN mainEntity=
# [Power] GameState.DebugPrintOptions() -   option 1 type=POWER mainEntity=[name=Acidic Swamp Ooze id=56 zone=HAND zonePos=1 cardId=EX1_066 player=2]
# [Power] GameState.DebugPrintOptions() -   option 2 type=POWER mainEntity=[name=Chillwind Yeti id=50 zone=HAND zonePos=2 cardId=CS2_182 player=2]
# [Power] GameState.DebugPrintOptions() -   option 3 type=POWER mainEntity=[name=Sludge Belcher id=47 zone=HAND zonePos=3 cardId=FP1_012 player=2]
# [Power] GameState.DebugPrintOptions() -   option 4 type=POWER mainEntity=[name=Chillwind Yeti id=62 zone=HAND zonePos=4 cardId=CS2_182 player=2]
# [Power] GameState.DebugPrintOptions() -   option 5 type=POWER mainEntity=[name=Gnomish Inventor id=45 zone=HAND zonePos=5 cardId=CS2_147 player=2]
# [Power] GameState.DebugPrintOptions() -   option 6 type=POWER mainEntity=[name=Stormpike Commando id=43 zone=HAND zonePos=6 cardId=CS2_150 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Uther Lightbringer id=4 zone=PLAY zonePos=0 cardId=HERO_04 player=1]
# [Power] GameState.DebugPrintOptions() -     target 1 entity=[name=Garrosh Hellscream id=36 zone=PLAY zonePos=0 cardId=HERO_01 player=2]
# [Power] GameState.DebugPrintOptions() -     target 2 entity=[name=Arathi Weaponsmith id=40 zone=PLAY zonePos=1 cardId=EX1_398 player=2]
# [Power] GameState.DebugPrintOptions() -   option 7 type=POWER mainEntity=[name=Shattered Sun Cleric id=64 zone=HAND zonePos=7 cardId=EX1_019 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Arathi Weaponsmith id=40 zone=PLAY zonePos=1 cardId=EX1_398 player=2]
# [Power] GameState.DebugPrintOptions() -   option 8 type=POWER mainEntity=[name=Garrosh Hellscream id=36 zone=PLAY zonePos=0 cardId=HERO_01 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Uther Lightbringer id=4 zone=PLAY zonePos=0 cardId=HERO_04 player=1]
# [Power] GameState.DebugPrintOptions() -   option 9 type=POWER mainEntity=[name=Armor Up! id=37 zone=PLAY zonePos=0 cardId=CS2_102 player=2]
# [Power] GameState.DebugPrintOptions() -   option 10 type=POWER mainEntity=[name=Arathi Weaponsmith id=40 zone=PLAY zonePos=1 cardId=EX1_398 player=2]
# [Power] GameState.DebugPrintOptions() -     target 0 entity=[name=Uther Lightbringer id=4 zone=PLAY zonePos=0 cardId=HERO_04 player=1]