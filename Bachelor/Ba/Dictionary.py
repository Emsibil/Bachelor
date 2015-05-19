import numpy as np
import os
import time

def path(fileName):
    script_dir = os.path.dirname(__file__)
    rel_path = fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

wordlist = np.array(["Hero", "Power", "Taunt", "Deal", "2", "damage", "to", "all", "enemies",
                     "Restore", "Health", "friendly", "characters", "Take", "control", "of", "an",
                     "enemy", "minion", "This", "has", "switched", "controllers", "Put", "a",
                     "copy", "random", "card", "in", "your", "opponent's", "hand", "into", "Give",
                     "+2", "hero", "Attack", "this", "turn", "and", "Armor", "8", "1", "+2/+2", 
                     "Attack+2", "4", "other", "Gain", "empty", "Mana", "Crystal", "Draw", "You", 
                     "can", "only", "have", "10", "tray", "Your", "+1", "Transform", "1/1", "Sheep",
                     "been", "transformed", "cards", "3", "character", "Freeze", "it", "minions", 
                     "Summon", "two", "0/2", "with", "6", "any", "damaged", "by", "Windfury",
                     "full", "give", "Battlecry", "+3", "Spell", "Damage", "ALL", "Choose", "At",
                     "the", "start", "destroy", "corrupting", "player's", "undamaged", "weapon", 
                     "Destroy", "Change", "minion's", "+4/+4", "+4", "Attack+4", "Whenever", 
                     "attacks", "restore", "Charge", "Raid", "Leader", "is", "granting", "Boar", 
                     "+1/+1", "Has", "for", "each", "on", "battlefield", "Increased", "stats",
                     "or", "less", "healed", "draw", "Double", "double", "you", "summon", "Beast",
                     "Beasts", "from", "Timber", "Wolf", "Tundra", "Rhino", "grants", "Look", "at",
                     "top", "three", "deck", "one", "discard", "others", "5", "2/1", "Mechanical",
                     "Dragonling", "Crystals", "Totems", "0/1", "Frog", "randomly", "split", 
                     "among", "If", "that", "kills", "Discard", "changed", "Divine", "Shield", 
                     "takes", "gain", "increased", "Murloc", "Scout", "Murlocs", "deal", "instead",
                     "Adjacent", "Flametongue", "Totem", "Return", "more", "Going", "second", "lost",
                     "coin", "flip", "but", "gained", "friend", "makes", "first", "stronger", "turns",
                     "are", "shorter", "Somehow", "USED", "deleted", "Here", "Demon", "their", "owner's",
                     "end", "Companion", "Other", "Leokk", "be", "equal", "its", "them", "was", "already",
                     "Frozen", "Deathrattle", "Resummon", "That", "costs", "One", "Stealth", "another",
                     "Combo", "+3/+3", "while", "equipped", "Durability", "2/2", "Squire", "HIMSELF",
                     "Silence", "Enrage", "Spiteful", "Smith", "cost", "Can't", "targeted", "spells",
                     "Powers", "except", "Ysera", "+5/+5", "next", "will", "destroyed", "soon", "Immune",
                     "attacking", "7", "swap", "+5", "opponent", "Bananas", "play", "Each", "player", "draws",
                     "cast", "spell", "Addict", "adjacent", "Swap", "swapped", "Crazed", "Alchemist", "The", 
                     "Secret", "played", "between", "5/5", "Devilsaur", "Squirrel", "take", "casts", "put", 
                     "player’s", "Costs", "4/5", "Baine", "Bloodhoof", "Whelps", "Force", "until", "Stealthed", 
                     "When", "Defender", "as", "new", "target", "Defias", "Bandit", "much", "dies", "return", 
                     "life", "It", "-", "Treant", "3/2", "Panther", "-3", "Dire", "Alpha", "Overload", "then", 
                     "2/3", "Spirit", "Wolves", "2-3", "Counter", "attacked", "plays", "fatal", "prevent", 
                     "become", "either", "side", "not", "than", "Then", "Horribly", "die", "horrible", "death", 
                     "Demons", "out", "demons", "least", "there", "always", "imps", "replace", "Lord", "Jaraxxus", 
                     "Copy", "Mindgames", "whiffed", "had", "no", "many", "healing", "doubled", "who", "blessed", 
                     "loses", "reduce", "reduced", "Equip", "5/3", "Ashbringer", "survives", "chosen", "12", 
                     "Otherwise", "equip", "1/3", "Attacking", "No", "durability", "loss", "Decreased", "+2/+1", 
                     "Warleader", "summoned", "he", "Hyenas", "revealed", "ones", "For", "Hound", "All", "lose", 
                     "Secrets", "Snakes", "Damaged", "Golem", "50%", "chance", "extra", "add", "Fireball", 
                     "Players", "15", "seconds", "Set", "hero's", "remaining", "set", "Treants", "Dream", 
                     "Card", "3/3", "Finkle", "Einhorn", "consumed", "Shields", "powers", "now", "it’s", "Imp", 
                     "Will", "again", "0", "earlier", "Flame", "Azzinoth", "taken", "becomes", "'Deal", "Shadowform", 
                     "attack", "Full", "After", "per", "Remove", "Violet", "Apprentice", "Pirates", "Southsea", 
                     "Captain", "Enemy", "Spells", "can't", "below", "Gruul", "growing", "Gnoll", "Just", "kidding", 
                     "He", "never", "Enrages", "Pirate", "Ninjas", "Super", "EVERY", "must", "frothy", "beverage", 
                     "5/4", "That's", "good", "notorious", "Footclapper", "Complain", "about", "bacon", "prices", 
                     "volume", "maximum", "some", "With", "pen", "C-C-C-COMBO", "FIVE", "Inventions", "TWO", "She's", 
                     "novice", "engineer", "Silenced", "Was", "successfully", "NOT", "part", "problem", "most", 
                     "time", "game", "without", "Is", "something", "barrel", "hiding", "Attack+1", "So", "strong", 
                     "And", "King", "Mukla", "+8", "Shoot", "missiles", "Until", "kill", "Cho's", "Throw", "make", 
                     "him", "able", "Enchant", "enchant", "enchantment", "does", "nothing", "enchantments", "secret", 
                     "controller", "discards", "his", "graveyard", "Crash", "five", "snakes", "long", "want", "rest", 
                     "heroes", "Enable", "emotes", "VSAI", "tutorials", "though", "Server", "DON'T", "BE", "A", 
                     "FOOL", "concede", "opponnet", "disconnect", "Become", "Hogger", "Video", "Recording", "Shuffle",
                     "30", "Steal", "AI", "use", "every", "Delete", "-1", "Pick", "Permanently", "Mega-Windfury", 
                     "+100", "Weapon", "+100/+100", "Minion", "+1000/+1000", "Minions", "controlled", "Spawn", 
                     "clear", "entire", "board", "both", "hands", "decks", "mana", "secrets", "smack", "own", "AI's", 
                     "Hand", "Deck", "Get", "ready", "testing", "AWESOME", "invention", "Stats", "transform", 
                     "Chicken", "chicken", "Hey", "players", "power", "ROCK", "Chord", "four", "Horde", "Warrior", 
                     "Spectral", "Spiders", "exact", "4/4", "Nerubian", "puts", "Add", "died", "Feugen", "also", 
                     "Thaddius", "Stalagg", "copies", "+3/+2", "trigger", "Deathrattles", "twice", "+6", "Frost", 
                     "Breath", "MINE", "Kel'Thuzad's", "kitty", "Passive", "non-Skeleton", "Both", "Spore", "Deals", 
                     "Activate", "Understudies", "Trainee", "Rider", "if", "Horsemen", "dead", "well", "Mech", 
                     "Mechs", "+2/+4", "-2", "still", "Lightwarden", "deals", "it's", "non-Mech", "Mal'Ganis", 
                     "Trigger", "Coin", "Spare", "Part", "3-6", "Wisps", "2-4", "dealt", "Multiplying", "Repeat", 
                     "wrong", "Mine", "drawn", "explodes", "Silver", "Recruits", "1/4", "7/7", "health", "they", 
                     "2-Cost", "1-Attack", "4-Cost", "same", "Cost", "Boom", "Bots", "WARNING", "may", "explode", 
                     "1-4", "form", "V-07-TR-0N", "Also", "damages", "whomever", "legendary", "Leper", "Gnome", 
                     "1-mana", "Burly", "Rockjaw", "Trogg", "Reversing", "Switch", "Someone", "remembers", "publish"])

from tables import Enum

class Target(Enum):
    MINION = 0
    FrIENDLY_MINION = 1
    ENEMY_MINION = 2
    ADJACENT_MINIONS = 3
    OPPONENT = 4
    YOUR_MINIONS = 5
    ALL_MINIONS = 6
    YOUR_HERO = 7
    ALL_OTHER = 8
    YOUR_OTHER_MINIONS = 9
    CHARACTER = 10
    ALL_ENEMY_MINIONS = 11
    ENEMY_CHARACTERS = 12
    ENEMY_HERO = 13
    ALL_CHARACTERS = 14
    RANDOM = 15
    ANY = 16
    
class ActionKeyword(Enum):
    GIVE = 0
    DEAL = 1
    GRANT = 2
    DESTROY = 3
    RESTORE = 4
    STEAL = 5
    SWAP = 6
    BECOME = 7
    TRANSFORM = 8
    RETURN = 9
    FREEZE = 10
    CHANGE = 11
    SET = 12
    DRAW = 13
    SUMMON = 14
    
def isDead(card):
    if card._health <= 0:
#        card._zone = CardState.GRAVEYARD
        return True
    else:
        return False
    
def Give(*args):
    #args[0] = Ability
    #args[1] = Target
    pass
    
def doDmg(*args): 
    dmg = 0
    randDmg = False
    dmgTxt = args[0].split('Deal ')[1].split(' damage')[0]
    for idx, char in enumerate(dmgTxt):
        if char.isdigit():
            if dmgTxt[idx+1] == '-':
                randDmg = True
            else:
                int(char)
        else:
            print 'No specified Damage. Read from Log'
    
    if randDmg:
        return
    else:
        for a in args[1]:
            a._health = a._health - dmg
            isDead(a)
            
def interpretingTarget(cardText):
    if 'random' in cardText:
        return Target.RANDOM
    elif 'a minion' in cardText:
        return Target.MINION
    elif 'a friendly minion' in cardText:
        return Target.FRIENDLY_MINION
    elif 'an enemy minion' in cardText:
        return Target.ENEMY_MINION
    elif 'adjacent minions' in cardText:
        return Target.ADJACENT_MINIONS
    elif 'opponent' in cardText:
        return Target.OPPONENT
    elif 'your minions' in cardText:
        return Target.YOUR_MINIONS
    elif 'ALL other' in cardText:
        return Target.ALL_OTHER
    elif 'your hero' in cardText:
        return Target.YOUR_HERO
    elif 'your other minions' in cardText:
        return Target.YOUR_OTHER_MINIONS
    elif 'a character' in cardText:
        return Target.CHARACTER
    elif 'all minions' in cardText:
        return Target.ALL_MINIONS
    elif 'all enemy minions' in cardText:
        return Target.ALL_ENEMY_MINIONS
    elif 'enemy characters' in cardText:
        return Target.ENEMY_CHARACTERS
    elif 'enemy hero' in cardText:
        return Target.ENEMY_HERO
    elif 'ALL characters' in cardText:
        return Target.ALL_CHARACTERS
    else:
        return Target.ANY
    
def interpretText(cardText):
    actions = []
    if 'Give' in cardText or 'give' in cardText:
        actions.append(ActionKeyword.GIVE)
    if 'Deal' in cardText or 'deal' in cardText:
        actions.append(ActionKeyword.DEAL)
    if 'Restore' in cardText or 'restore' in cardText:
        actions.append(ActionKeyword.RESTORE)
    if 'Grant' in cardText or 'grant' in cardText:
        actions.append(ActionKeyword.GRANT)
    if 'Destroy' in cardText or 'destroy' in cardText:
        actions.append(ActionKeyword.DESTROY)
    if 'Return' in cardText or 'return' in cardText:
        actions.append(ActionKeyword.RETURN)
    if 'Swap' in cardText or 'swap' in cardText:
        actions.append(ActionKeyword.SWAP)
    if 'Transform' in cardText or 'transform' in cardText:
        actions.append(ActionKeyword.TRANSFORM)
    if 'Steal ' in cardText or 'steal ' in cardText:
        actions.append(ActionKeyword.STEAL)
    if 'Freeze' in cardText:
        actions.append(ActionKeyword.FREEZE)
    if 'Change' in cardText or 'change' in cardText:
        actions.append(ActionKeyword.CHANGE)
    if 'Set' in cardText or 'set' in cardText:
        actions.append(ActionKeyword.SET)
    if 'Become' in cardText:
        actions.append(ActionKeyword.BECOME)
    if 'Draw' in cardText or 'draw' in cardText:
        actions.append(ActionKeyword.DRAW)
    if 'Summon' in cardText or 'summon' in cardText
        actions.append(ActionKeyword.SUMMON)
    return actions
        
        
        
        
