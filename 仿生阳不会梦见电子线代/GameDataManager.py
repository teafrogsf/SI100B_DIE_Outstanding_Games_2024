from Data.instance import *
from RenderSystem.Sprite import LoadImage
from RogueSystem.StageSetting import *

from Data.types import *

import Data.fonts
import copy,os,json
import random,time

class CharacterData:
    def __init__(self,name,SDname,healthMax,staggerMax,originResistance,speedL,speedR,countDices,lightMax):
        self.name = name
        self.SDname = SDname
        
        self.healthOri = healthMax
        self.staggerOri = staggerMax
        self.healthModifier = Vector2(1,0)
        self.staggerModifier = Vector2(1,0)

        self.healthMax = healthMax
        self.staggerMax = staggerMax

        self.originResistance = originResistance

        self.speedL = speedL 
        self.speedR = speedR

        self.countDices = countDices
        self.lightMax = lightMax

        self.Page = []
        self.Passive = []

        self.Util_ResTransUp = {
            0:0,0.25:0.25,0.5:0.25,1:0.5,1.5:1,2:1.5
        }
        self.Util_ResTransDown = {
            0:0.25,0.25:0.5,0.5:1,1:1.5,1.5:2,2:2
        }
    def __copy__(self):
        _data = CharacterData(self.name,self.SDname,self.healthMax,self.staggerMax,copy.deepcopy(self.originResistance)
                              ,self.speedL,self.speedR,self.countDices,self.lightMax)
        _data.Page = [pg["name"] for pg in self.Page]
        _data.Passive = copy.deepcopy(self.Passive)
        return _data
    def calcHealth(self):
        self.healthMax = int(self.healthOri*self.healthModifier.x + self.healthModifier.y)
    def calcStagger(self):
        self.staggerMax = int(self.staggerOri*self.staggerModifier.x + self.staggerModifier.y)
    def mapResistance(self,mapp):
        return {
                "life":{
                    "slash":mapp[self.originResistance["Slash"]],
                    "pierce":mapp[self.originResistance["Pierce"]],
                    "blunt":mapp[self.originResistance["Blunt"]]
                },
                "stagger":{
                    "slash":mapp[self.originResistance["Slash_s"]],
                    "pierce":mapp[self.originResistance["Pierce_s"]],
                    "blunt":mapp[self.originResistance["Blunt_s"]]
                }
            }
    def mapAbility(self,mapp):
        lis = []
        for pas in self.Passive:
            if pas in mapp.keys():
                lis.append(mapp[pas])
            else:
                lis.append(pas)
        return lis
    def modifyAttribute(self,attr,val):
        if attr == "health":
            self.healthModifier += val()
            self.calcHealth()
        elif attr == "stagger":
            self.staggerModifier += val()
            self.calcStagger()
        elif attr == "speed":
            self.speedL += val().x
            self.speedR += val().y
            if self.speedL < 1:
                self.speedL = 1
            if self.speedR < 1:
                self.speedR = 1
        elif attr == "light":
            self.lightMax += val
        elif attr == "resis":
            self.alterResis(val["type"],val["category"],val["val"])
    def alterResis(self,dmgType,dmgCategory,val):
        if not dmgCategory in ["Slash","Pierce","Blunt"]:
            return
        if not dmgType in ["Life","Stagger"]:
            return
        _innerName = dmgCategory+("" if dmgType == "Life" else "_s")
        if val > 0:
            for i in range(val):
                self.originResistance[_innerName] = self.Util_ResTransUp[self.originResistance[_innerName]]
        else:
            for i in range(-val):
                self.originResistance[_innerName] = self.Util_ResTransDown[self.originResistance[_innerName]]
    def addPassive(self,nam,psvPool):
        if nam in psvPool.keys():
            val = psvPool[nam]
            if "Mutiable" in val.keys() and val["Mutiable"] == False and nam in self.Passive:
                return
            self.Passive.append(nam)
            self.Passive.sort()
    def delPassive(self,nam):
        if nam in self.Passive:
            self.Passive.remove(nam)

@instance
class GameDataManager:
    def __init__(self):
        self.FLAG_VICTORY = False
        self.FLAG_DEFEAT = False

        self.NEXT_SCENE = None

        self.PATH_CWD = os.getcwd()

        self.TIME_START = time.time()
        self.GAME_DIFFICULTY = 1

        self.RANDOM = random.Random(time.time())
        
        self.STAGE = StageSetting()

        self.PAGE_POOL_ID = 0
        self.PAGE_POOL = {

        }
        self.CUSTOM_PAGEPOOL = []

        self.DYNAMIC_GEN_PAGEPOOL = []

        self.CHARACTER_POOL = {

        }

        self.ALLY_TEAM = {

        }

        self.SAFE_IMGPATH = "testcard.png"
        self.PREFAB_CARD_IMGPATH_DICT = {

        }

        self.curDict={}
        self.Dit={"combatPlayer":[],"combatList":[]}

        self.loadUtils()
        self.loadCharSDAlter()
        self.loadBuffs()
        self.loadExtendBuffs()
        self.loadBackground()
        self.loadLang()
        self.loadMapTile()
        self.loadPrefabCardImgPath()
        self.loadAoeAnime()
        self.loadResisIcon()
        self.loadCharUpgrade()
        self.loadPassive()
        print("INIT: Gdata I & Classes")
    def has(self,name):
        return hasattr(self,name)
    def loadPrefabPage(self):
        import ReceptionSystem.PageCoding
        from ReceptionSystem.Page import Page
        path = os.path.join(self.PATH_CWD,"Assets","Gdata","Card")
        files = os.listdir(path)
        for file in files:
            if file.lower().endswith(".json"):
                js = os.path.join(path,file)
                pageLis = ReceptionSystem.PageCoding.ReadCardJson(js)
                for page in pageLis:
                    if isinstance(page,Page):
                        self.addPage(page.name,page,True)
                        self.modifyCustomPageAmt(page.name,(
                        5 if page.quality == "Green" else
                        3 if page.quality == "Blue" else
                        2 if page.quality == "Purple" else
                        1 
                    ))
        #print(self.PAGE_POOL)
        #print("modify")
    def loadGenPage(self):
        import ReceptionSystem.PageCoding
        from ReceptionSystem.GenerateDict import GeneratePageDict
        from ReceptionSystem.Page import Page
        path = os.path.join(self.PATH_CWD,"Assets","Gdata","Card","Gen","DYNAMICGENPAGE.json")
        try:
            pageLis = ReceptionSystem.PageCoding.ReadCardJson(path)
        except:
            print("Fatal Error Occurred when decoding Gen Page, safety action starting")
            pageLis = [self.PAGE_POOL[i["name"]]["page"] for i in self.RANDOM.sample(self.CUSTOM_PAGEPOOL,3)]
        self.DYNAMIC_GEN_PAGEPOOL.clear()
        for page in pageLis:
            if isinstance(page,Page):
                if not page.name in self.GEN_CARD_IMGPATH_DICT.keys():
                    self.GEN_CARD_IMGPATH_DICT[page.name] = self.genRandomCardImg()
                self.DYNAMIC_GEN_PAGEPOOL.append({
                    "name":page.name,
                    "page":page,
                    "card":GeneratePageDict(page),
                    "isCustom":True,
                    "amt":(
                        5 if page.quality == "Green" else
                        3 if page.quality == "Blue" else
                        2 if page.quality == "Purple" else
                        1 
                    )
                })
    def getGenPage(self):
        return self.DYNAMIC_GEN_PAGEPOOL
    def injectGenPage(self,nam):
        for page in self.DYNAMIC_GEN_PAGEPOOL:
            if page["name"] == nam:
                _pgcls = page["page"]
                _pgamt = page["amt"]
                if nam in self.PAGE_POOL.keys():
                    self.modifyCustomPageAmt(nam,_pgamt)
                else:
                    self.addPage(nam,_pgcls,True)
                    self.modifyCustomPageAmt(nam,_pgamt)
                if page["name"] in self.GEN_CARD_IMGPATH_DICT.keys():
                    self.PREFAB_CARD_IMGPATH_DICT[page["name"]] = self.GEN_CARD_IMGPATH_DICT[page["name"]]
            else:
                if page["name"] in self.GEN_CARD_IMGPATH_DICT.keys():
                    self.GEN_CARD_IMGPATH_SET.insert(0,self.GEN_CARD_IMGPATH_DICT[page["name"]])
                    #print("delete",page["name"])
        self.DYNAMIC_GEN_PAGEPOOL.clear()
        self.GEN_CARD_IMGPATH_DICT.clear()
    def genPoolPageID(self):
        self.PAGE_POOL_ID += 1
        return self.PAGE_POOL_ID
    def addPage(self,pageName,pageClass,isCustom):
        self.PAGE_POOL[pageName] = {
            "page":pageClass,
            "isCustom":isCustom,
            "amt":0
        }
        if isCustom:
            self.CUSTOM_PAGEPOOL.append({
                "name":pageName,
                "sortKey":pageClass.lightCost
            })
            self.CUSTOM_PAGEPOOL = sorted(self.CUSTOM_PAGEPOOL,key = lambda x : (x["sortKey"],x["name"]))
    def modifyCustomPageAmt(self,pageName,damt):
        if pageName in self.PAGE_POOL.keys():
            if self.PAGE_POOL[pageName]["isCustom"]:
                self.PAGE_POOL[pageName]["amt"] += damt
    def getPage(self,name):
        if name in self.PAGE_POOL.keys():
            return self.PAGE_POOL[name]["page"]
    def getCustomCardsOnPage(self,index):
        from ReceptionSystem.GenerateDict import GeneratePageDict
        lis = []
        for k in self.CUSTOM_PAGEPOOL[index*9:min((index+1)*9,len(self.CUSTOM_PAGEPOOL))]:
            lis.append({
                "name":k["name"],
                "card":GeneratePageDict(self.PAGE_POOL[k["name"]]["page"]),
                "amt":self.PAGE_POOL[k["name"]]["amt"]
            })
        return lis
    def getCustomCardsPageRange(self):
        return (0,len(self.CUSTOM_PAGEPOOL)//9 + (0 if len(self.CUSTOM_PAGEPOOL)%9 != 0 else -1))
    def getCustomCard(self,name):
        from ReceptionSystem.GenerateDict import GeneratePageDict
        if name in self.PAGE_POOL.keys():
            return {
                "name":name,
                "sortKey":self.PAGE_POOL[name]["page"].lightCost,
                "card":GeneratePageDict(self.PAGE_POOL[name]["page"]),
                "amt":self.PAGE_POOL[name]["amt"]
            }
    def addAllyCharacter(self,charData):
        if isinstance(charData, CharacterData):
            self.ALLY_TEAM[charData.name] = charData
    def getAllys(self):
        return self.ALLY_TEAM
    def genBattleAllys(self):
        _lis = []
        for char in self.ALLY_TEAM.values():
            if isinstance(char,CharacterData):
                _lis.append(copy.copy(char))
        return _lis
    def getAlly(self,name):
        if name in self.ALLY_TEAM:
            return self.ALLY_TEAM[name]
    def getAllyCards(self,name):
        if name in self.ALLY_TEAM:
            return (name,self.ALLY_TEAM[name].Page)
    def modifyAllyCards(self,name,lis):
        if name in self.ALLY_TEAM:
            self.ALLY_TEAM[name].Page = sorted(lis,key = lambda x : (x["sortKey"],x["name"]))
        return self.getAllyCards(name)
    def loadUtils(self):
        from RenderSystem.prefab.UICombatText import DmgResis
        self.resdit={0:DmgResis.Immerse,0.25:DmgResis.Ineffective,0.5:DmgResis.Endured,1:DmgResis.Normal,1.5:DmgResis.Weak,2:DmgResis.Fatal}
    def loadCharSDAlter(self):
        path = os.path.join(self.PATH_CWD,"Assets","Image","character","CharImgPosAlter.json")
        if os.path.exists(path):
            with open(path,"r",encoding="utf-8") as f:
                self.CharSDAlter = json.load(f)
    def getCharSDAlter(self,char,sd) -> dict:
        if char in self.CharSDAlter.keys():
            if sd in self.CharSDAlter[char].keys():
                return copy.deepcopy(self.CharSDAlter[char][sd])
        return None
    def loadBuffs(self):

        self.Buffs = {
        "Bind":{
            "Name":"Bind",
            "Icon":LoadImage("Buff\\Bind.png")
            },
        "Bleed":{
            "Name":"Bleed",
            "Icon":LoadImage("Buff\\Bleed.png")
            },
        "Burn":{
            "Name":"Burn",
            "Icon":LoadImage("Buff\\Burn.png")
            },
        "Charge":{
            "Name":"Charge",
            "Icon":LoadImage("Buff\\Charge20.png")
            },
        "Disarm":{
            "Name":"Disarm",
            "Icon":LoadImage("Buff\\Disarm.png")
            },
        "Endurance":{
            "Name":"Endurance",
            "Icon":LoadImage("Buff\\Endurance.png")
            },
        "Erosion":{
            "Name":"Erosion",
            "Icon":LoadImage("Buff\\Erosion.png"),
            "Color":Data.fonts.ColorBlack
            },
        "Fairy":{
            "Name":"Fairy",
            "Icon":LoadImage("Buff\\Fairy.png")
            },
        "Feeble":{
            "Name":"Feeble",
            "Icon":LoadImage("Buff\\Feeble.png")
            },
        "Fragile":{
            "Name":"Fragile",
            "Icon":LoadImage("Buff\\Fragile.png")
            },
        "Haste":{
            "Name":"Haste",
            "Icon":LoadImage("Buff\\Haste.png")
            },
        "Paralysis":{
            "Name":"Paralysis",
            "Icon":LoadImage("Buff\\Paralysis.png")
            },
        "Protection":{
            "Name":"Protection",
            "Icon":LoadImage("Buff\\Protection.png")
            },
        "SProtection":{
            "Name":"SProtection",
            "Icon":LoadImage("Buff\\SProtection.png")
            },
        "Smoke":{
            "Name":"Smoke",
            "Icon":LoadImage("Buff\\Smoke.png")
            },
        "Strength":{
            "Name":"Strength",
            "Icon":LoadImage("Buff\\Strength.png")
            },
        "Stun":{
            "Name":"Stun",
            "Icon":LoadImage("Buff\\Stun.png")
            }
        }
    def loadExtendBuffs(self):
        self.Buffs.update({
            "Yang_CountDown":{
                "Name":"Yang_CountDown",
                "Icon":LoadImage("Buff\\Yang_CountDown.png")
            },
            "BloodMist":{
                "Name":"RedMist",
                "Icon":LoadImage("Buff\\RedMist.png")
            }
        }) 
    def getBuff(self,bufName):
        if bufName in self.Buffs.keys():
            _buf = self.Buffs[bufName]
            _buf["Icon"] = self.Buffs[bufName]["Icon"].copy()
            return _buf
    def loadLang(self):
        self.Lang = {
            "Ending":{
                "Victory":{
                    "Title":u"平凡即是喜乐",
                    "Sentence":[
                        u"出发时预想的目标在终点达成，介于扭曲体与人类之间的生物准备在饱餐一顿后迎来明天。日常是命运赐予生灵最大的善意，平凡，即是喜乐。"
                    ]
                },
                "Defeat":{
                    "Title":u"戛然而止",
                    "Sentence":[
                        [u"水面随着思绪融化产生的波纹摊开，边界再一次得到了扩展。"],
                        [u"真正的捕食者从不亲自动手，名为好奇心的无形助力会让食物将自己送入口中。"],
                        [u"越过边界的勇气或许会被常人斥为鲁莽，但自然从来一言不发，无论它收留了什么。",u"风浪卷住你的脚踝，轻轻将你拉离陆地，拥入它的怀抱。"],
                        [u"那城市//残骸//宫殿//村庄拒绝了你，不再因你的劝解而发生改变。"],
                        [u"不必再用冰杖敲敲打打，你沉入其中，和过往的时间一同被影子覆盖，而冰原永无尽头。",u"那远见于你而言仍是未来。"],
                        [u"一粒沙尘仍然太过沉重，你不曾预期，也不曾后悔。",u"“莲瓣入水而不苦根茎，勿执着。”"]
                    ]
                },
                "Desq":[
                    "您(点击输入文字)使用",
                    ["静音小队","蓝图测绘分队","堡垒战术分队"],
                    "历时",
                    "于",
                    ["驻足于","通过了"]
                ]
            },
            "Difficulty":{
                0:{
                    "Title":u"静音小队",
                    "Desq":[u"己方角色初始体力+30%，混乱抗性+30%",u"己方角色初始混乱伤害抗性+1级",u"己方角色初始光芒+1，且速度骰最小值/最大值获得+1/+2",u"己方角色每回合获得2层“强壮”和2层“忍耐”"]
                },
                1:{
                    "Title":u"蓝图测绘分队",
                    "Desq":[u"蓝图没给你削弱不错了，反正该削的也不是蓝图了"]
                },
                2:{
                    "Title":u"堡垒战术分队",
                    "Desq":[u"己方角色初始体力-15%，混乱抗性-15%",u"己方角色初始体力伤害抗性-1级",u"己方角色速度骰最小值/最大值获得-2/-1（不会小于1）",u"自LR-3起的敌方角色每回合获得2层“强壮”和“忍耐”,LR-5中敌人额外获得1层"]
                }
            },
            "ReceptionBackWord":{
                "rnfmabj":[
                    "致……制作便当，在下午1点时于11区内的垃圾桶上享用它。",
                    "致……在时针位于7与8之间时制作蛋白酥皮奶油卷筒并一边看电影一边享用它。",
                    "致……和你今天遇到的前五个人中的第5位进行折手指游戏。手指折下去时需要被折断。",
                    "致……将你所遇到的第62个人的指甲修剪整齐。",
                    "致……抚摸5次用四足行走的动物。",
                    "致……通过旋转转盘选出某个被指定的人并朝他扔蛋糕。",
                    "致……吃放置在常温环境下的螃蟹与熟透了的柿子，每样各吃8个。",
                    "致……在屋顶的围栏上大声喊出你所厌恶的人的名字后跳下屋顶。屋顶距离地面的高度无关紧要。",
                    "致……将用餐后余下的碗全部丢弃。",
                    "致……于接受指令后的第二天早上睁开眼睛时便立刻喝下3杯水。",
                    "致……与居住在同一栋楼中的居民们一同进行一场目的地为7区的赛跑比赛。每隔23分钟便测量一次距离，测量距离时与7区相距最远的人将会被淘汰。",
                    "致……在3天内织好一条带有蝴蝶图案的围巾。",
                    "致……随意地拨一通电话。为接电话的人送上新年贺词。",
                    "致……在白色的墙壁上看到绿色。",
                    "致……在你肚子饿时吃添加了洋葱的鸡肉奶酪汉堡。",
                    "致……折39个纸鹤并令它们在屋顶上飞扬。",
                    "致……把首个在职场中大声训斥你的人的耳朵剪掉。",
                    "致……与和自己视线相交了的人打招呼。",
                    "致……立刻回家。有狗在家门前叫过一次后才可以出来。",
                    "致……身着淡绿色的衣物并在三角形的街道上走十步。"
                ]
            }
        }
    def loadAoeAnime(self):
        from AnimeSystem.animes.AoeAnime_FrenziedBloodBlade import AoeAnime_FrenziedBloodBlade_Attacker
        from AnimeSystem.animes.AoeAnime_WarpedBlade import AoeAnime_WarpedBlade_SpellCircle,AoeAnime_WarpedBlade_Blade
        from AnimeSystem.animes.AoeAnime_LandscapeOfDeath import AoeAnime_LandscapeOfDeath_Attacker,AoeAnime_LandscapeOfDeath_BG,AoeAnime_LandscapeOfDeath_Light,AoeAnime_LandscapeOfDeath_Mask,AoeAnime_LandscapeOfDeath_Mimic
        from AnimeSystem.animes.AoeAnime_RangingInferno import AoeAnime_RangingInferno_Attacker
        self.AoeAnime = {
            "FrenziedBloodBlade":{
                "lasFrame":60,
                "dmgDelay":40,
                "attacker":AoeAnime_FrenziedBloodBlade_Attacker,
                "effects":[]
            },
            "WarpedBlade":{
                "lasFrame":65,
                "dmgDelay":53,
                "attacker":None,
                "effects":[
                    AoeAnime_WarpedBlade_Blade,
                    AoeAnime_WarpedBlade_SpellCircle
                ]
            },
            "LandscapeOfDeath":{
                "lasFrame":95,
                "dmgDelay":50,
                "attacker":AoeAnime_LandscapeOfDeath_Attacker,
                "effects":[
                    AoeAnime_LandscapeOfDeath_BG,
                    AoeAnime_LandscapeOfDeath_Mimic,
                    AoeAnime_LandscapeOfDeath_Light,
                    AoeAnime_LandscapeOfDeath_Mask
                ]
            },
            "RangingInferno":{
                "lasFrame":45,
                "dmgDelay":40,
                "attacker":AoeAnime_RangingInferno_Attacker,
                "effects":[]
            }
        }
    def getAoeAnime(self,nam):
        if nam in self.AoeAnime.keys():
            return self.AoeAnime[nam]
    def loadResisIcon(self):
        from RenderSystem.prefab.UICombatText import DmgResis,DmgType
        from RenderSystem.prefab.UICard import DiceType
        self.ResisIcon = LoadImage("resisIcons.png")
        self.mapDmgTyp = {
            DmgType.Life:0,
            DmgType.Stagger:60
        }
        self.mapDmgCate = {
            DiceType.Slash:0,
            DiceType.Pierce:120,
            DiceType.Blunt:240
        }
        self.mapDmgResis = {
            DmgResis.Fatal:0,
            DmgResis.Weak:65,
            DmgResis.Normal:130,
            DmgResis.Endured:195,
            DmgResis.Ineffective:260,
            DmgResis.Immerse:325
        }
    def getResisIcon(self,dmgTyp,dmgCate,dmgResis):
        return self.ResisIcon.subsurface(self.mapDmgTyp[dmgTyp]+self.mapDmgCate[dmgCate],self.mapDmgResis[dmgResis],60,65).copy()
    def loadMapTile(self):
        self.MAPTILE_POOL = {
            "1":{
                "Background":{
                    "Folder":"grass",
                    "Amt":2
                },
                "Road":{
                    "Folder":"ground",
                    "Amt":8
                }
            },
            "2":{
                "Background":{"Folder":"snow","Amt":1},
                "Road":{"Folder":"ground","Amt":8}
            },
            "3":{
                "Background":{"Folder":"grassred","Amt":2},
                "Road":{"Folder":"180726","Amt":12}
            },
            "4":{
                "Background":{"Folder":"grassred","Amt":2},
                "Road":{"Folder":"dirt","Amt":8}
            },
            "Yang":{
                "Background":{"Folder":"fb","Amt":3},
                "Road":{"Folder":"forsaken","Amt":8}
            }
        }
    def getMapTile(self,ky):
        if ky in self.MAPTILE_POOL.keys():
            dit = {}
            for key,val in self.MAPTILE_POOL[ky].items():
                dit[key] = ["mapTile\\{0}\\{0} ({1}).png".format(val["Folder"],i) for i in range(1,val["Amt"]+1)]
            return dit
    def loadBackground(self):
        self.BACKGROUND_POOL = {
            "Beginning":[
                "beginningBG{0}.png".format(i) for i in range(1,6)
            ],
            "Battle":{
                "1":[
                    "battleMainBG1.png",
                    "battleCombatBG1.png"
                ],
                "2":[
                    "battleMainBG2.png",
                    "battleCombatBG2.png"
                ],
                "3":[
                    "battleMainBG3.png",
                    "battleCombatBG3.png"
                ],
                "4":[
                    "battleMainBG4.png",
                    "battleCombatBG4.png"
                ],
                "Yang":[
                    "battleMainBGYang.png",
                    "battleCombatBGYang.png"
                ]
            }
        }
    def getBackground(self,scene,req=None):
        if scene == "Beginning":
            return "background\\"+self.RANDOM.sample(self.BACKGROUND_POOL[scene],1)[0]
        elif scene == "Battle":
            if req in self.BACKGROUND_POOL[scene].keys():
                return ["background\\"+x for x in self.BACKGROUND_POOL[scene][req]]
    def genRandomCardImg(self):
        if len(self.GEN_CARD_IMGPATH_SET) == 0:
            self.GEN_CARD_IMGPATH_SET.extend(["GEN\\125_{0}.png".format(i) for i in range(420)])
            self.RANDOM.shuffle(self.GEN_CARD_IMGPATH_SET)
        return self.GEN_CARD_IMGPATH_SET.pop()
    def loadPrefabCardImgPath(self):
        self.GEN_CARD_IMGPATH_SET = []
        self.GEN_CARD_IMGPATH_DICT = {}
        self.PREFAB_CARD_IMGPATH_DICT.update({
            u"使用示范":"Leaflet\\work1.png",
            u"烟锤猛击":"Leaflet\\work2.png",
            u"烟锤袭击":"Leaflet\\work1.png",
            u"烟锤冲击":"Leaflet\\work3.png",
            u"浓烟喷射":"Leaflet\\work4.png",
            u"长驱直入":"Liu\\Liu2_7.png",
            u"一决雌雄":"Liu\\Liu2_13.png",
            u"剑之所向":"Liu\\Liu2_3.png",
            u"慷慨激昂":"Liu\\Liu2_1.png",
            u"燎原烈火":"Liu\\Liu2_8.png",
            u"神龍抬首":"Liu\\Liu2_11.png",
            u"铁山靠":"Liu\\Liu2_9.png",
            u"碧血丹心":"Liu\\Liu2_2.png",
            u"破竹之势":"Liu\\Liu2_6.png",
            u"刀光剑影":"Liu\\Liu2_5.png",
            u"牢不可破":"Liu\\Liu2_4.png",
            u"大刀纵劈":"RedMist\\RedMist3.png",
            u"大刀直刺":"RedMist\\RedMist4.png",
            u"大刀横斩":"RedMist\\RedMist5.png",
            u"屏息凝神":"RedMist\\RedMist6.png",
            u"血雾弥漫":"RedMist\\RedMist2.png",
            u"尸横遍野":"RedMist\\RedMist1.png",
            u"撕咬鲜草":"RRR\\Rcorp14.png",
            u"火力集中":"RRR\\Rcorp7.png",
            u"快速压制":"RRR\\Rcorp13.png",
            u"单点射击":"RRR\\Rcorp8.png",
            u"心神凝聚":"RRR\\Rcorp15.png",
            u"狂暴血刃":"RRR\\Rcorp1.png",
            u"执行-进攻":"Yan\\Yan5.png",
            u"执行-护卫":"Yan\\Yan_guard.png",
            u"执行-警戒":"Yan\\Yan4.png",
            u"执行-固守":"Yan\\Yan_union.png",
            u"全体修复":"Yan\\Yan_recover.png",
            u"执行-修复":"Yan\\Yan_recover.png",
            u"扭曲之刃":"Yan\\Yan1.png",
            u"巨拳轰击":"Yan\\Yan_punch.png",
            u"巨掌拍打":"Yan\\Yan_hand.png",
            u"乱拳痛殴":"Yan\\Yan_move.png",
            u"不祥烙印":"Yan\\Yan2.png",
            u"封锁目标":"Yan\\Yan3.png",
            #这里放卡牌key 对 path的映射
        })
    def getPrefabCardImgPath(self,nam):
        #调用这个获得路径 键为上面那个函数传的键
        if nam in self.PREFAB_CARD_IMGPATH_DICT.keys():
            return self.PREFAB_CARD_IMGPATH_DICT[nam]
        elif nam in self.GEN_CARD_IMGPATH_DICT.keys():
            return self.GEN_CARD_IMGPATH_DICT[nam]
        else:
            return self.SAFE_IMGPATH
    def loadCharUpgrade(self):
        self.CUSTOM_CHARUPGRADEPOOL = {}
        self.CUSTOM_CHARUPGRADEPOOL_List = []

        path = os.path.join(self.PATH_CWD,"Assets","Gdata","CharUpgrade")
        files = os.listdir(path)
        for file in files:
            if file.lower().endswith(".json"):
                js = os.path.join(path,file)
                dit = {}
                with open(js,"r",encoding="utf-8") as f:
                    dit = json.load(f)
                for key,val in dit.items():
                    self.CUSTOM_CHARUPGRADEPOOL[key] = val
                    if "InPool" in val.keys() and val["InPool"] == False:
                        continue
                    self.CUSTOM_CHARUPGRADEPOOL_List.append(key)
    def getCustomPassive(self,nam):
        if nam in self.CUSTOM_PASSIVEPOOL:
            return self.CUSTOM_PASSIVEPOOL[nam]
    def loadPassive(self):
        self.psvdit = {}
        self.CUSTOM_PASSIVEPOOL = {}
        self.CUSTOM_PASSIVEPOOL_LevelList = {}
        for i in range(1,6):
            self.CUSTOM_PASSIVEPOOL_LevelList[i] = []

        path = os.path.join(self.PATH_CWD,"Assets","Gdata","Passive")
        files = os.listdir(path)
        for file in files:
            if file.lower().endswith(".json"):
                js = os.path.join(path,file)
                dit = {}
                with open(js,"r",encoding="utf-8") as f:
                    dit = json.load(f)
                for key,val in dit.items():
                    self.psvdit[key] = val["Desq"] + (u"（同名天赋不生效）" if ("Mutiable" in val.keys() and val["Mutiable"] == False) else "")
                    if val["Level"] >= 0 and val["Level"] <= 5:
                        self.CUSTOM_PASSIVEPOOL[key] = {
                            "name":key,
                            "level":val["Level"],
                            "Desq":self.psvdit[key],
                            "Mutiable":(False if ("Mutiable" in val.keys() and val["Mutiable"] == False) else True)
                        }
                        if val["Level"] >= 1:
                            self.CUSTOM_PASSIVEPOOL_LevelList[val["Level"]].append(key)

gameDataManager = GameDataManager()