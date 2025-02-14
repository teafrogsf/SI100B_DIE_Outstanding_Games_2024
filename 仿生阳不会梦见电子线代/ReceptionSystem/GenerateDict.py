from RenderSystem.prefab.UICharacter import CharSD
from RenderSystem.prefab.UISpeedDice import StateSpeedDice
from RenderSystem.prefab.UICard import ManaIcon,CardFrame,DiceType,CardType
from RenderSystem.prefab.UITeam import EmotionType
from RenderSystem.prefab.UICombatText import DmgResis

import random,copy
def GenerateDiceDict(dice):
    typed={"Slash":DiceType.Slash,"Pierce":DiceType.Pierce,"Blunt":DiceType.Blunt,"Block":DiceType.Block,"Evade":DiceType.Evade}
    dit_dice={
        "diceType":typed[dice.attackType],
        "minDice":dice.dicePointL,
        "maxDice":dice.dicePointR,
        "dicePoint":dice.dicePoint,
        "isCounter":dice.isCounter,
        "desq":None
    }
    return dit_dice
def GeneratePageDict(page):
    from GameDataManager import gameDataManager
    colordit={"Green":(ManaIcon.Green,CardFrame.Green),"Blue":(ManaIcon.Blue,CardFrame.Blue),
              "Purple":(ManaIcon.Purple,CardFrame.Purple),"Gold":(ManaIcon.Gold,CardFrame.Gold),}
    if page.lightCost<page.originCost:
        st="Green"
    elif page.lightCost>page.originCost:
        st="Red"
    else:
        st="Common"
    tpdit={"Melee":CardType.Near,"Ranged":CardType.Range,"Individual":CardType.AOE,"Summation":CardType.AOE}
    dit_card = {
        "cardId":None,
        "mana":page.lightCost,
        "manaIcon":colordit[page.quality][0],
        "manaColor":st,
        "cardImg":gameDataManager.getPrefabCardImgPath(page.name),
        "cardFrame":colordit[page.quality][1],
        "cardTitle":page.name,
        "cardType":tpdit[page.pageType],
        "pageDesq":{
            "overall_desq":page.pageBuff.desp,
            "list":[]
        }
    }
    if page.affiliateCharacter != None:
        dit_card["cardId"] = page.affiliateCharacter.id*1000+page.id
    else:
        dit_card["cardId"] = gameDataManager.genPoolPageID()
    typed={"Slash":DiceType.Slash,"Pierce":DiceType.Pierce,"Blunt":DiceType.Blunt,"Block":DiceType.Block,"Evade":DiceType.Evade}
    for dice in page.dices:
        dit_dice={
            "diceType":typed[dice.attackType],
            "minDice":dice.dicePointL,
            "maxDice":dice.dicePointR,
            "isCounter":False,
            "desq":dice.diceBuff.desp
        }
        dit_card["pageDesq"]["list"].append(dit_dice)
    for dice in page.counterDices:
        dit_dice={
            "diceType":typed[dice.attackType],
            "minDice":dice.dicePointL,
            "maxDice":dice.dicePointR,
            "isCounter":True,
            "desq":dice.diceBuff.desp
        }
        dit_card["pageDesq"]["list"].append(dit_dice)
    return dit_card
def GenerateCombatPageDict(page,used=-1,point=-1):
    from GameDataManager import gameDataManager
    dit_card = {
        "cardImg":gameDataManager.getPrefabCardImgPath(page.name),
        "cardTitle":page.name,
        "rollingDice":{
            "diceType":DiceType.Slash,
            "minDice":3,
            "maxDice":8,
            "dicePoint":7,
            "isCounter":False
        },
        "waitDiceArray":[]
    }
    typed={"Slash":DiceType.Slash,"Pierce":DiceType.Pierce,"Blunt":DiceType.Blunt,"Block":DiceType.Block,"Evade":DiceType.Evade}
    flg=0
    for i in range(len(page.dices)):
        dice=page.dices[i]
        if used!=-1 and i<used:
            continue
        if not dice.broken:
            if flg==0:
                dit_card["rollingDice"]=GenerateDiceDict(dice)
                if(point!=-1):
                    dit_card["rollingDice"]["dicePoint"]=point
                    return dit_card
                flg=1
            else:
                dit_card["waitDiceArray"].append(GenerateDiceDict(dice))
    for dice in page.delayDices:
        if not dice.broken:
            if flg==0:
                dit_card["rollingDice"]=GenerateDiceDict(dice)
                flg=1
            else:
                dit_card["waitDiceArray"].append(GenerateDiceDict(dice))
    return dit_card
def GenerateInfoDict(person):
    dit_infoBar = {
        "life":{
            "num":56,
            "maxinum":98
        },
        "stagger":{
            "num":32,
            "maxinum":80
        },
        "emotion":{
            "emoLevel":2,
            "emoMaxNum":5,
            "emoList":[]
        },
        "resis":{
            "life":{
                "slash":DmgResis.Endured,
                "pierce":DmgResis.Fatal,
                "blunt":DmgResis.Immerse
            },
            "stagger":{
                "slash":DmgResis.Ineffective,
                "pierce":DmgResis.Normal,
                "blunt":DmgResis.Weak
            }
        },
        "buff":[]
    }
    resdit={0:DmgResis.Immerse,0.25:DmgResis.Ineffective,0.5:DmgResis.Endured,1:DmgResis.Normal,1.5:DmgResis.Weak,2:DmgResis.Fatal}
    _dit_infoBar=copy.deepcopy(dit_infoBar)
    _dit_infoBar["life"]["num"]=person.health
    _dit_infoBar["life"]["maxinum"]=person.healthMax
    _dit_infoBar["stagger"]["num"]=person.stagger
    _dit_infoBar["stagger"]["maxinum"]=person.staggerMax
    _dit_infoBar["resis"]["life"]["slash"]=resdit[person.resistance["Slash"]]
    _dit_infoBar["resis"]["life"]["pierce"]=resdit[person.resistance["Pierce"]]
    _dit_infoBar["resis"]["life"]["blunt"]=resdit[person.resistance["Blunt"]]
    _dit_infoBar["resis"]["stagger"]["slash"]=resdit[person.resistance["Slash_s"]]
    _dit_infoBar["resis"]["stagger"]["pierce"]=resdit[person.resistance["Pierce_s"]]
    _dit_infoBar["resis"]["stagger"]["blunt"]=resdit[person.resistance["Blunt_s"]]
    _dit_infoBar["emotion"]["emoLevel"]=person.emotion.emotionLevel
    dic={0:3,1:3,2:5,3:7,4:9,5:0}
    _dit_infoBar["emotion"]["emoMaxNum"]=dic[person.emotion.emotionLevel]
    for i in range(min(dic[person.emotion.emotionLevel],len(person.emotion.coins))):
        if person.emotion.coins[i]=="Green":
            _dit_infoBar["emotion"]["emoList"].append(EmotionType.Green)
        else:
            _dit_infoBar["emotion"]["emoList"].append(EmotionType.Red)
    for buff in person.buffs.buffs:
        dic_buff={}
        dic_buff["buffName"]=buff.name
        dic_buff["buffLevel"]=buff.count
        dic_buff["isNext"]=False
        _dit_infoBar["buff"].append(dic_buff)
    for buff in person.nextBuffs.buffs:
        dic_buff={}
        dic_buff["buffName"]=buff.name
        dic_buff["buffLevel"]=buff.count
        dic_buff["isNext"]=True
        _dit_infoBar["buff"].append(dic_buff)
    return _dit_infoBar
def GenerateCharDict(person):
    from GameDataManager import gameDataManager
    dit_cardarr = {
        "cardArray":[
            
        ]
    }
    dit_character = {
        "isDead":False,
        "charId":1,
        "char":{
            "name":"Malkuth",
            "state":CharSD.Common
        },
        "speedL":0,
        "sppedR":0,
        "resistance":{},
        "infoBar":None,
        "diceArray":None,
        "lightBlock":None
    }
    dit_lightBlock = {
        "amt":17,
        "full":3,
        "onuse":6,
        "empty":2,
        "selected":0
    }
    dit_dice = {
        "diceId":0,
        "spd":2,
        "state":StateSpeedDice.Unrolled,
        "cardDit":None
    }
    dit_diceArray = {
        "amt":3,
        "list":[
        ]
    }
    namedit={"rnfmabj":"Yan",u"左手":"Hand",u"右手":"Hand",u"缪":"Myo",u"兔子":"Rabbit",u"八重":"Yae",u"叶工坊收尾人":"Leaflet",
             u"罗威尔":"Lowell",u"梅":"Mei",u"六协会2科收尾人":"LiuAso",u"卡莉":"RedMist"}
    psvdit=gameDataManager.psvdit
    _dit_char = copy.deepcopy(dit_character)
    if person.JudgeDeath():
        _dit_char["isDead"] = True
    _dit_char["charId"] = person.id
    _dit_char["pos"] = person.pos

    #modified by NH37
    if person.SDname == None:
        if person.name in namedit.keys():
            _dit_char["char"]["name"]=namedit[person.name]
        else:
            _dit_char["char"]["name"]= "Rabbit"
    else:
        _dit_char["char"]["name"]=person.SDname
    
    if person.name=="rnfmabj" and person.merged:
        _dit_char["char"]["name"]="Union"
    if person.name==u"卡莉" and person.ego:
        _dit_char["char"]["name"]=u"RedMistEgo"
    _dit_char["abilityDesq"]=[]
    for psv in person.passive:
        _dit_char["abilityDesq"].append(psvdit[psv])
    _dit_char["speedL"]=person.speedL
    _dit_char["speedR"]=person.speedR
    _dit_char["resistance"]=person.resistance
    if person.JudgeStagger():
        _dit_char["char"]["state"]=CharSD.Hurt
    else:
        _dit_char["char"]["state"]=CharSD.Common
    _dit_char["infoBar"]=GenerateInfoDict(person)
    _dit_lightBlock=copy.deepcopy(dit_lightBlock)
    _dit_lightBlock["amt"]=person.lightMax
    _dit_lightBlock["full"]=person.light
    _dit_lightBlock["onuse"]=person.lightHave-person.light
    _dit_lightBlock["empty"]=person.lightMax-person.lightHave
    _dit_char["lightBlock"]=_dit_lightBlock
    _dit_diceArray=copy.deepcopy(dit_diceArray)
    _dit_diceArray["amt"]=person.countDices
    for dice in person.speedDices:
        _dit_dice = copy.deepcopy(dit_dice)
        _dit_dice["diceId"] = person.id*1000+dice.id
        _dit_dice["speedL"]=person.speedL
        _dit_dice["speedR"]=person.speedR
        if dice.isbreak:
            _dit_dice["state"] = StateSpeedDice.Broken
        elif dice.speed==-1:
            _dit_dice["state"] = StateSpeedDice.Unrolled
        else:
            _dit_dice["state"] = StateSpeedDice.Rolled
            _dit_dice["spd"]=dice.speed
        _dit_dice["havePage"]=dice.havePage
        if dice.havePage:
            _dit_dice["cardDit"]=GeneratePageDict(dice.page)
            if dice.page.pageType=="Individual" or dice.page.pageType=="Summation":
                _dit_dice["target"]=[dice.Target.affiliateCharacter.id*1000+dice.Target.id]
                for tar in dice.massTarget:
                    _dit_dice["target"].append(tar.affiliateCharacter.id*1000+tar.id)
            else:
                _dit_dice["target"]=dice.Target.affiliateCharacter.id*1000+dice.Target.id
            _dit_dice["isClashing"]=dice.IsClashing()
        _dit_diceArray["list"].append(_dit_dice)
    _dit_char["diceArray"]=_dit_diceArray
    _dit_char["cardArray"] = copy.deepcopy(dit_cardarr)
    for page in person.handPages:
        _dit_char["cardArray"]["cardArray"].append(GeneratePageDict(page))
    return _dit_char
def GeneratespCharDict(person):
    dit_character = {
        "charId":1,
        "char":{
            "name":"Malkuth",
            "state":CharSD.Common
        },
        "infoBar":None,
    }
    namedit={"rnfmabj":"Yan",u"左手":"Hand",u"右手":"Hand",u"缪":"Myo",u"兔子":"Rabbit",u"八重":"Yae",u"叶工坊收尾人":"Leaflet",
             u"罗威尔":"Lowell",u"梅":"Mei",u"六协会2科收尾人":"Liuaso",u"卡莉":"RedMist"}
    _dit_char = copy.deepcopy(dit_character)
    _dit_char["charId"] = person.id

    #modified by NH37
    if person.SDname == None:
        if person.name in namedit.keys():
            _dit_char["char"]["name"]=namedit[person.name]
        else:
            _dit_char["char"]["name"]= "Rabbit"
    else:
        _dit_char["char"]["name"]=person.SDname

    if person.name=="rnfmabj" and person.merged:
        _dit_char["char"]["name"]="Union"
    if person.name==u"卡莉" and person.ego:
        _dit_char["char"]["name"]=u"RedMistEgo"
    if person.JudgeStagger():
        _dit_char["char"]["state"]=CharSD.Hurt
    else:
        _dit_char["char"]["state"]=CharSD.Common
    _dit_char["infoBar"]=GenerateInfoDict(person)
    return _dit_char
def GenerateDict(bt):
    dit_team = {
        "teamName":"malkuths",
        "charList":[
        ]
    }
    dit_battleSys = {
        "BG":"BG.png",
        "charTeam1":{

        },
        "charTeam2":{

        }
    }
    teams=[bt.enemies,bt.allies]
    t=1
    for team in teams:
        _dit_Team = copy.deepcopy(dit_team)
        for person in team.characters:
            _dit_Team["charList"].append(GenerateCharDict(person))
        dit_battleSys["charTeam"+str(t)] = _dit_Team
        t+=1
    #print(dit_battleSys)
    return dit_battleSys