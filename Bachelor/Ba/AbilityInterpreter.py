from Bachelor.Ba.Util import *

def splitEffectLine(line):
    if 'Buff' in line:
        buff = True
        effect = split(line, 'Buff: ', '\tValue:')
    else:
        buff = False
        effect = split(line, 'Debuff: ', '\tValue:')
    value= split(line, 'Value: ', '\tEffect:')
    effectTime = split(line, 'EffectTime: ', '\n') 
    return (buff, effect, value, effectTime) 
    
def compare(cardProperty, value):
    if cardProperty < value:
        return (Effect.BUFF, value - cardProperty)
    elif cardProperty > value:
        return (Effect.DEBUFF, value - cardProperty)

def exists(effect):
    info = open(path('doc')+'/CardEffect.info', 'r').readlines()
    for i in info:
        if effect[0] in i:
            return True
    info.close()
    return False

def compareEffect(oldEffect, newEffect):
    n_o = len(oldEffect) - 1
    n_n = len(newEffect) - 1
    if n_n / 2 == n_o:
        i = 1
        while i <= n_n:
            if 'Buff' in oldEffect[i]:
                effect = split(oldEffect[i], 'Buff: ', '\t')
                value = split(oldEffect[i], 'Value: ', '\n')
            elif 'Debuff' in oldEffect[i]:
                effect = split(oldEffect[i], 'Debuff: ', '\t')
                value = split(oldEffect[i], 'Value: ', '\n')
            if not newEffect[i] == effect and newEffect[i+1] == value:
                return False
            i = i + 2
        return True      
    else:
        return False
    
def changeEffect(oldEffect, newEffect):
    n_o = len(oldEffect) - 1
    n_n = len(newEffect) - 1
    if n_n / 2 == n_o:
        i = 1
        while i <= n_n:
            if 'Buff' in oldEffect[i]:
                effect = split(oldEffect[i], 'Buff: ', '\t')
                value = split(oldEffect[i], 'Value: ', '\n')
            elif 'Debuff' in oldEffect[i]:
                effect = split(oldEffect[i], 'Debuff: ', '\t')
                value = split(oldEffect[i], 'Value: ', '\n')
            if not newEffect[i] == effect and newEffect[i+1] == value:
                pass
            i = i + 3     
    else:
        pass
    
def rewrite(effect): 
    info = open(path('doc')+'/CardEffect.info', 'r')
    content = info.readlines()
    info.close()
    info = open(path('doc')+'/CardEffect.info', 'w')
    old_effect = []
    for idx, line in enumerate(content):
        if effect[0] in line:
            i = idx
            while not content[i] == '\n':
                old_effect.append(content[i])
                i = i + 1
            if compareEffect(old_effect, effect):
                count = int(split(line, 'Count: ', 1, '\n', 0)) + 1
                line = effect[0] + '\tCount: '+str(count)+'\n'
            else:
                pass
    for line in content:
        info.write(line)        
                
def write(effect):
    info = open(path('doc')+'/CardEffect.info', 'a')
    info.write(effect[0] + '\tCount: 1\n')
    for idx, e in enumerate(effect):
        if idx > 0 and idx%3 == 1:
            if type(e) is Buff:
                info.write('\tBuff: ' + e + '\tValue: ' + effect[idx+1] + '\tEffectTime: ' + effect[idx+2] +'\n')
            if type(effect[idx]) is Debuff:
                info.write('\tDebuff: ' + e + '\tValue: ' + effect[idx+1] + '\tEffectTime: ' + effect[idx+2] + '\n')
    info.write('\n')
    info.close()
        
def readingLines(card, lines):
    try:
        info = open(path('doc')+'/CardEffect.info', 'r')
        info.close()
    except:
        info = open(path('doc')+'/CardEffect.info', 'w')
        info.close()
    effect = []    
    for idx, l in enumerate(lines):
        if 'SubType=PLAY' in l:
            if 'Target' in l:
                TargetTxt = split(l, 'SubType=PLAY')
                targetId = split(TargetTxt, 'id=', ' ')
                Target = targetId #in real search card in cards
        elif 'SubType=Power' in l:
            pass
                #read detailed
        elif 'FULL_ENTITY' in l:
            cardID = split(l, 'ID=', ' ')
            idx = split(l, 'CardID=' ,'\n')
            zone = split(lines[idx+1], 'value=', '\n')
        elif 'TAG_CHANGE Entity=' + idx in l:
            if 'ATTACHED' in l:
                t_id = int(split(l, 'value=', '\n'))
        elif 'id='+targetId in l:
            if 'tag=HEALTH' in l:
                value = int(split(l, 'value=', '\n'))
                comp = compare(card._health, value)
                effect.append(comp[0], Buff.HEALTH, comp[1], EffectTime.ON_PLAY)
            if 'tag=ATTACK' in l:
                value = int(split(l, 'value=', '\n'))
                comp = compare(card._attack, value)
                effect.append(comp[0], Buff.ATTACK, comp[1], EffectTime.ON_PLAY)
            if 'tag=CHARGE' in l:
                effect.append(Effect.BUFF, Buff.CHARGE, 0, EffectTime.ON_PLAY)
            if 'tag=TAUNT' in l:
                effect.append(Effect.BUFF, Buff.TAUNT, 0, EffectTime.ON_PLAY) 
            if 'tag=STEALTH' in l:
                effect.append(Effect.BUFF, Buff.STEALTH, 0, EffectTime.ON_PLAY)
            if 'tag=DIVINE SHIELD' in l:
                effect.append(Effect.BUFF, Buff.DIVINE_SHIELD, 0, EffectTime.ON_PLAY)
        elif 'SubType=DEATHS' in l:
            pass
        elif 'SubType=TRIGGER' in l:
            card = getCardByIngameId(gameId(l))
            if card._zone == Zone.GRAVEYARD:
                pass                       
    write(effect)
    
def editAbility(target, ability):
    if ability not in target._ability:
        target._ability.append(ability)
        
def BuffTarget(target, effect, value):
    if effect == Buff.ATTACK:
        target._attack = target._attack + value 
    elif effect == Buff.HEALTH:
        target._health = target._health + value  
    elif effect == Buff.TAUNT:
        editAbility(target, effect)  
    elif effect == Buff.DIVINE_SHIELD:
        editAbility(target, effect)    
    elif effect == Buff.STEALTH:
        editAbility(target, effect)    
    elif effect == Buff.CHARGE:
        editAbility(target, effect)    
    elif effect == Buff.DRAW:
        pass 
    elif effect == Buff.COPY:
        pass  
    elif effect == Buff.SPELLDAMAGE:
        editAbility(target, effect)    
   
def DebuffTarget(target, effect, value):
    if Debuff.ATTACK == effect:
        target._attack = target._attack - value 
    elif Debuff.HEALTH == effect:
        target._health = target._health - value
    elif Debuff.SILENCE == effect:
        target._ability = []
        target._enchanment = []
    elif Debuff.DESTROY == effect:
        target._zone = Zone.GRAVEYARD
    elif Debuff.TRANSFORM == effect:
        pass

def readInterpreter(card, target, effectTime):
    cardId = card._id
    info = open(path('doc/CardEffect.info'), 'r').readlines()
    cardInfo = []
    for idx, i in enumerate(info):
        if cardId in info:
            j = idx
            while not info[j] == '\n':
                cardInfo.append(info[j])
                j = j + 1
            break
    for info in cardInfo:
        if 'Buff' in info or 'Debuff' in info:
            isBuff, effect, value, effTime = splitEffectLine(info)
        if effTime == effectTime:
            if isBuff:
                BuffTarget(target, effect, value)
            else:
                DebuffTarget(target, effect, value)
                
def readingFULL_ENTITY(lines):
    card = None
    isMyCard = False
    for l in lines:
        if 'CREATOR' in l: 
            break
        elif 'FULL_ENTITY' in l:
            idx = split(l, 'ID=', ' ')
            cardID = split(l, 'CardID=', '\n')
            card = createCard(cardID)
            card._ingameID = idx
        elif 'tag=ZONE' in l:
            if split(l, 'value=', '\n') == 'PLAY':
                card._zone = Zone.PLAY
        elif 'tag=CONTROLLER' in l:
            if int(split(l, 'value=', '\n')) == 1:
                isMyCard = True
        elif 'tage=ZONE_POSITION' in l:
            card.set_pos(int(split(l, 'value=', '\n')))
    if isMyCard and card._zone == Zone.PLAY:
        addMyMinonToField(card, card.get_pos())
    elif not isMyCard and card._zone == Zone:
        addEnemyMinonToField(card, card.get_pos())
    elif card._zone == Zone.HAND:
        addHandcardAtPosition(card._id, card.get_pos, card._ingameID)

if 'META_DAMAGE' in l:
    pass
if 'META_HEALING' in l:
    pass
if 'FULL_ENTITY' in l:
    pass
if 'SHOW_ENTITY' in l:
    pass
# [Power] GameState.DebugPrintPower() - ACTION_START Entity=[name=Shattered Sun Cleric id=64 zone=HAND zonePos=2 cardId=EX1_019 player=2] SubType=PLAY Index=0 Target=[name=Haunted Creeper id=38 zone=PLAY zonePos=1 cardId=FP1_002 player=2]
# [Power] GameState.DebugPrintPower() -     ACTION_START Entity=[name=Shattered Sun Cleric id=64 zone=HAND zonePos=2 cardId=EX1_019 player=2] SubType=POWER Index=-1 Target=[name=Haunted Creeper id=38 zone=PLAY zonePos=1 cardId=FP1_002 player=2]
# [Power] GameState.DebugPrintPower() -         META_DATA - Meta=META_TARGET Data=0 Info=1
# [Power] GameState.DebugPrintPower() -         FULL_ENTITY - Creating ID=81 CardID=EX1_019e
# [Power] GameState.DebugPrintPower() -             tag=ZONE value=SETASIDE
# [Power] GameState.DebugPrintPower() -             tag=CONTROLLER value=2
# [Power] GameState.DebugPrintPower() -             tag=ENTITY_ID value=81
# [Power] GameState.DebugPrintPower() -             tag=CARDTYPE value=ENCHANTMENT
# [Power] GameState.DebugPrintPower() -             tag=CREATOR value=64
# [Power] GameState.DebugPrintPower() -         TAG_CHANGE Entity=81 tag=ATTACHED value=38
# [Power] GameState.DebugPrintPower() -         TAG_CHANGE Entity=81 tag=ZONE value=PLAY
# [Power] GameState.DebugPrintPower() -     ACTION_END        
# [Power] GameState.DebugPrintPower() -     TAG_CHANGE Entity=[name=Haunted Creeper id=38 zone=PLAY zonePos=1 cardId=FP1_002 player=2] tag=HEALTH value=3
# [Power] GameState.DebugPrintPower() -     TAG_CHANGE Entity=[name=Haunted Creeper id=38 zone=PLAY zonePos=1 cardId=FP1_002 player=2] tag=ATK value=2        
# 
# ACTION_START Entity=[name=Dark Cultist id=24 zone=PLAY zonePos=3 cardId=FP1_023 player=1] SubType=TRIGGER Index=0 Target=0
# [Power] GameState.DebugPrintPower() -         META_DATA - Meta=META_TARGET Data=0 Info=1
# [Power] GameState.DebugPrintPower() -         FULL_ENTITY - Creating ID=91 CardID=
# [Power] GameState.DebugPrintPower() -             tag=ZONE value=SETASIDE
# [Power] GameState.DebugPrintPower() -             tag=CONTROLLER value=1
# [Power] GameState.DebugPrintPower() -             tag=ENTITY_ID value=91
# [Power] GameState.DebugPrintPower() -             tag=ZONE_POSITION value=0
# [Power] GameState.DebugPrintPower() -             tag=CANT_PLAY value=0
# [Power] GameState.DebugPrintPower() -         SHOW_ENTITY - Updating Entity=91 CardID=FP1_023e
# [Power] GameState.DebugPrintPower() -             tag=ATTACHED value=23
# [Power] GameState.DebugPrintPower() -             tag=ZONE value=PLAY
# [Power] GameState.DebugPrintPower() -             tag=CARDTYPE value=ENCHANTMENT
# [Power] GameState.DebugPrintPower() -             tag=CREATOR value=24
# [Power] GameState.DebugPrintPower() -     ACTION_END

