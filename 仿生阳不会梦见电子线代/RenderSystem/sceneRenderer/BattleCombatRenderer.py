from RenderSystem.Canvas import *
from RenderSystem.prefab.UICombatCharacter import *
from RenderSystem.prefab.UICombatText import *
from RenderSystem.prefab.UITeam import UITeamInfoBar,EmotionType,UICharacterBriefInfo
from RenderSystem.prefab.UIEmotionLine import UIEmotionLine
from .BattleMainRenderer import UIBattleBackground,BattleTeam
from AnimeSystem.AnimeManager import animeManager
from AnimeSystem.animes.CombatTimerAnime import CombatTimerAnime
from AnimeSystem.animes.CombatEffectAnime import CombatEffectAnime,CombatEmotionAnime
from AnimeSystem.animes.CombatCharAnime import *

from Data.coder import *

import random
from enum import Enum

class CombatType(Enum):
    AOE = 1
    Far = 2
    Near = 3
    RoundEnd = 4
    RoundChange = 5
    BattleResult = 6

class CombatProcess(Enum):
    EnterStage = 1
    DiceRolling = 2
    Combat = 3
    LeaveStage = 4

class CombatEffectType(Enum):
    Damage = 1
    Heal = 2
    Emotion = 3
    Buff = 4
    Stagger = 5

ProcessName = {
    1:"EnterStage",
    2:"DiceRolling",
    3:"Combat",
    4:"LeaveStage"
}

def AOELocalPosition(team,posnum):
    Team1delta = Vector2(-300,30)
    Team2delta = Vector2(300,30)
    charPosBasis = [
            Vector2(200,0),
            Vector2(120,90),
            Vector2(160,-70),
            Vector2(0,0),
            Vector2(-150,90),
            Vector2(-110,-70)
        ]
    if team == 1:
        return charPosBasis[posnum]+Team1delta
    elif team == 2:
        return charPosBasis[posnum]*Vector2(-1,1)+Team2delta
    else:
        return Vector2.Zero()

class BattleCombatRenderer(Canvas):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        self.combatEffects = {}
        super().__init__(name, screen, priority)
    def init(self):
        for i in range(0,12):
            self.addChild(UICombatCharacter("preName"+str(i),self.screen,0))
            self.findChild("preName"+str(i)).setActive(False)
            self.findChild("preName"+str(i)).setScale(Vector2(0.7,0.7))
        self.addChild(UIBattleBackground("BG",self.screen,-100))
        self.addChild(UITeamInfoBar("infoTeam1",self.screen,10))
        self.addChild(UITeamInfoBar("infoTeam2",self.screen,10))

        self.controlSys = {
            "ReadyForAnime":True,
            "InAnime": True
        }
        self.storedData = {
            "AnimeProcess":1
        }
        self.combatList = []
        self.combatPin = -1

        self.curCombat = None
        self.curInfo = None

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.setPos(Vector2(720,360))
        self.findChild("infoTeam1").setPos(Vector2(-620,180))
        self.findChild("infoTeam2").setPos(Vector2(620,180))
    def update(self):
        super().update()
        #print("uodate")
        if self.controlSys["ReadyForAnime"] == False:
            self.prepareNextCombat()
        elif self.controlSys["InAnime"] == False:
            self.PushCombatProcess(self.storedData["AnimeProcess"])
    def Render(self):
        self.screen.fill([255,255,255])
        self.draw()
        self.drawCombatEffect()
    def setValue(self,dit):
        self.backgroundLis = dit["BG"]
        self.initInfoBar(dit["combatPlayer"])
        self.initPlayer(dit["combatPlayer"])
        self.combatList = dit["combatList"]
        self.combatPin = -1
    def storeCombatEffect(self,com,process,anime):
        if not ("anime" in com[process]):
            com[process]["anime"] = []
        anime.Object.setParent(self)
        com[process]["anime"].append(anime)
    def activateCombatEffect(self,com,process):
        if "anime" in com[process]:
            for anime in com[process]["anime"]:
                self.combatEffects[anime.start()[0]] = anime
            com[process]["anime"].clear()
    def drawCombatEffect(self):
        for anime in self.combatEffects.values():
            anime.Object.draw()
    def delCombatEffect(self,id):
        if id in self.combatEffects.keys():
            self.combatEffects.pop(id)
    def PlayBattleAnime(self):
        animeManager.ResetTimer()
        self.controlSys["ReadyForAnime"] = False
        self.controlSys["InAnime"] = False
        self.curCombat = None
        self.curInfo = None
    def EndBattleAnime(self,info):
        if info["CombatType"] == CombatType.BattleResult:
            self.scene.AtBattleEnd(info)
        elif info["CombatType"] == CombatType.RoundChange:
            self.scene.OnRoundChange()
        '''
        elif info["CombatType"] == CombatType.RoundEnd:
            self.scene.OnRoundEnd()
            self.scene.OnRoundChange()
        '''
    def initInfoBar(self,listPlayer):
        char1 = []
        char2 = []
        for ditChar in listPlayer:
            if decodeCharIdInfo(ditChar["charId"]) == BattleTeam.Enemy.value:
                char1.append(ditChar)
            else:
                char2.append(ditChar)
        self.findChild("infoTeam1").setInitValue(CharFace.Left,char1)
        self.findChild("infoTeam2").setInitValue(CharFace.Right,char2)
    def initPlayer(self,listPlayer):#here load all the sd of the character
        for ditChar in listPlayer:
            if not self.findChild(ditChar["charId"]):
                for child in self.children:
                    if isinstance(child.name,str) and child.name[:7] == "preName":
                        child.name = ditChar["charId"]
                        child.setValue(ditChar)
                        child.setActive(False)
                        break
            else:
                self.findChild(ditChar["charId"]).setValue(ditChar)
                self.findChild(ditChar["charId"]).setActive(False)
    def nextCombatInfo(self):
        self.combatPin += 1
        if self.combatPin >= len(self.combatList):
            raise ValueError("Stop!")
        return self.combatList[self.combatPin]
    def prepareNextCombat(self):
        self.curInfo = self.nextCombatInfo()
        if self.curInfo == None:
            return
        if self.curInfo["CombatType"] == CombatType.BattleResult or self.curInfo["CombatType"] == CombatType.RoundChange:
            self.prepareGroupExit()
            self.EndBattleAnime(self.curInfo)
        
        if self.curInfo["CombatType"] == CombatType.AOE or self.curInfo["CombatType"] == CombatType.RoundEnd:
            #print(self.curInfo)
            self.prepareGroupEnter(self.curInfo)
        elif self.curCombat != None:
            if self.curCombat["CombatType"] == CombatType.AOE:
                self.prepareGroupExit()
        
        if self.curCombat == None:
            self.prepareFirstCombat()
        
        self.preparePlayer(self.curInfo)
        com = {}
        com["CombatType"] = self.curInfo["CombatType"]
        if self.curInfo["CombatType"] == CombatType.Near or self.curInfo["CombatType"] == CombatType.Far:
            com["char1"] = self.curInfo["char1"]
            com["char2"] = self.curInfo["char2"]
        elif self.curInfo["CombatType"] == CombatType.AOE:
            com["joiner"] = self.curInfo["joiner"]
            com["attacker"] = self.curInfo["attacker"]
            com["receiver"] = self.curInfo["receiver"]
        elif self.curInfo["CombatType"] == CombatType.RoundEnd:
            com["joiner"] = self.curInfo["joiner"]
        self.prepareEnterStage(self.curInfo,com)
        self.curCombat = com
        self.controlSys["ReadyForAnime"] = True
    def preparePlayer(self,info):
        if info["CombatType"] == CombatType.Near or info["CombatType"] == CombatType.Far:
            self.findChild(info["char1"]).setValue(info[info["char1"]]["beforeCombat"])
            self.findChild(info["char2"]).setValue(info[info["char2"]]["beforeCombat"])

            self.findChild("infoTeam1").setValue(info["char1"],info[info["char1"]]["beforeCombat"])
            self.findChild("infoTeam2").setValue(info["char2"],info[info["char2"]]["beforeCombat"])
        elif info["CombatType"] == CombatType.AOE or info["CombatType"] == CombatType.RoundEnd:
            for char in info["joiner"]:
                self.findChild(char["id"]).setValue(info[char["id"]]["beforeCombat"])
                if decodeCharIdInfo(char["id"]) == 1:
                    self.findChild("infoTeam1").setValue(char["id"],info[char["id"]]["beforeCombat"])
                else:
                    self.findChild("infoTeam2").setValue(char["id"],info[char["id"]]["beforeCombat"])
    def preparePlayerAfterCombat(self,info):
        if info["CombatType"] == CombatType.Near or info["CombatType"] == CombatType.Far:
            self.findChild(info["char1"]).setValue(info[info["char1"]]["afterCombat"])
            self.findChild(info["char2"]).setValue(info[info["char2"]]["afterCombat"])

            self.findChild("infoTeam1").setValue(info["char1"],info[info["char1"]]["afterCombat"])
            self.findChild("infoTeam2").setValue(info["char2"],info[info["char2"]]["afterCombat"])
            
            if "state" in info[info["char1"]]["afterCombat"].keys():
                self.curCombat["state"]["char1"] = info[info["char1"]]["afterCombat"]["state"]
            if "state" in info[info["char2"]]["afterCombat"].keys():
                self.curCombat["state"]["char2"] = info[info["char2"]]["afterCombat"]["state"]
        elif info["CombatType"] == CombatType.AOE or info["CombatType"] == CombatType.RoundEnd:
            for char in info["joiner"]:
                self.findChild(char["id"]).setValue(info[char["id"]]["afterCombat"])
                if decodeCharIdInfo(char["id"]) == 1:
                    self.findChild("infoTeam1").setValue(char["id"],info[char["id"]]["afterCombat"])
                else:
                    self.findChild("infoTeam2").setValue(char["id"],info[char["id"]]["afterCombat"])
    def prepareEnterStage(self,info,com):
        com["EnterStage"] = {}
        com["state"] = {}
        if info["CombatType"] == CombatType.Near or info["CombatType"] == CombatType.Far:
            #EnterStage
            com["state"]["char1"] = info[info["char1"]]["state"]
            com["state"]["char2"] = info[info["char2"]]["state"]
            if True:
                if self.curCombat["LeaveStage"]["consist"] == "All":#判是否为上一轮的人继续拼点
                    if info["CombatType"] == CombatType.Near:
                        for tgt in ["char1","char2"]:
                            if info["CombatWinner"] == info[tgt]:
                                opp = {"char1":"char2","char2":"char1"}
                                delta = {"char1":Vector2(170,0),"char2":Vector2(-170,0)}
                                com["EnterStage"][tgt] = {
                                    "sprite":CombatCharAnime_SimpleAct(self.findChild(info[tgt]).findChild("charImg"),
                                                               self.curCombat["LeaveStage"]["approachFlame"],
                                                               (CharSD.Move if com["state"][tgt] == CharState.Common else CharSD.Hurt)),
                                    "move":CombatCharAnime_CharMove(self.findChild(info[tgt]),
                                                            self.curCombat["LeaveStage"]["approachFlame"],
                                                            self.curCombat["LeaveStage"]["Point"][tgt](),
                                                            self.curCombat["LeaveStage"]["Point"][opp[tgt]]()+delta[opp[tgt]],
                                                            CharActionType.EnterStage)
                                    }
                            else:
                                com["EnterStage"][tgt] = {}
                    else:
                        com["EnterStage"]["char1"] = {}
                        com["EnterStage"]["char2"] = {}
                elif self.curCombat["LeaveStage"]["consist"] == "Null":#判是否为全部离场
                    end_pos = Vector2(100*random.uniform(-1.0,1.0),30*random.uniform(-1.0,1.0))
                    sat_pos = Vector2(-720-200*(1 if info["CombatType"] == CombatType.Near else 4),0)*self.curCombat["LeaveStage"]["leftDirection"]()
                    delta = {"char1":Vector2(-100*(1 if info["CombatType"] == CombatType.Near else 4),0),
                             "char2":Vector2(100*(1 if info["CombatType"] == CombatType.Near else 4),0)}
                    for tgt in ["char1","char2"]:
                        com["EnterStage"][tgt] = {
                                "sprite":CombatCharAnime_SimpleAct(self.findChild(info[tgt]).findChild("charImg"),5
                                                                   ,(CharSD.Move if com["state"][tgt] == CharState.Common else CharSD.Hurt)),
                                "move":CombatCharAnime_CharMove(self.findChild(info[tgt]),15,sat_pos()+delta[tgt](),end_pos()+delta[tgt](),
                                                                CharActionType.EnterStage)
                        }
                else:
                    end_pos = Vector2(100*random.uniform(-1.0,1.0),self.curCombat["LeaveStage"]["consistPos"]().y)
                    delta = {"char1":Vector2(-100*(1 if info["CombatType"] == CombatType.Near else 3),0),
                             "char2":Vector2(100*(1 if info["CombatType"] == CombatType.Near else 3),0)}
                    st_pos = {"char1":Vector2(-820,0),"char2":Vector2(820,0)}
                    for tgt in ["char1","char2"]:
                        if self.curCombat["LeaveStage"]["consist"] == tgt:
                            com["EnterStage"][tgt] = {
                                "sprite":CombatCharAnime_SimpleAct(self.findChild(info[tgt]).findChild("charImg"),15,
                                                                   (CharSD.Move if com["state"][tgt] == CharState.Common else CharSD.Hurt)),
                                "move":CombatCharAnime_CharMove(self.findChild(info[tgt]),15,
                                                                self.curCombat["LeaveStage"]["consistPos"](),end_pos()+delta[tgt](),
                                                                CharActionType.EnterStage)
                            }
                        else:
                            com["EnterStage"][tgt] = {
                                "sprite":CombatCharAnime_SimpleAct(self.findChild(info[tgt]).findChild("charImg"),15,
                                                                   (CharSD.Move if com["state"][tgt] == CharState.Common else CharSD.Hurt)),
                                "move":CombatCharAnime_CharMove(self.findChild(info[tgt]),15,
                                                                st_pos[tgt]()+delta[tgt](),end_pos()+delta[tgt](),
                                                                CharActionType.EnterStage)
                            }
    def prepareDiceRolling(self,info,com):
        com["DiceRolling"] = {}
    def prepareCombat(self,info,com):
        com["Combat"] = {}
        if info["CombatType"] == CombatType.Near or info["CombatType"] == CombatType.Far:
            for tgt in ["char1","char2"]:
                com["Combat"][tgt] = {
                    "sprite":CombatCharAnime_SimpleAct(self.findChild(info[tgt]).findChild("charImg"),3,info[info[tgt]]["action"])
                }
                if info["CombatLoser"] == info[tgt]:
                    pos = self.findChild(info[tgt]).localPosition()
                    end_pos = Vector2(max(pos.x-(min(max(info["MainDmg"]*10,80),250)
                                            *(0.2 if info["CombatType"] == CombatType.Far else 1)
                                            ),-520) 
                                        if tgt == "char1" else 
                                      min(pos.x+(min(max(info["MainDmg"]*10,80),250)
                                            *(0.2 if info["CombatType"] == CombatType.Far else 1)
                                            ),520)
                                    ,pos.y)
                    com["Combat"][tgt].update({
                                    "move":CombatCharAnime_CharMove(self.findChild(info[tgt]),8,pos,end_pos)
                                    })
                
                if "state" in info[info[tgt]]["afterCombat"].keys():
                    com["state"][tgt] = info[info[tgt]]["afterCombat"]["state"]
                    if com["state"][tgt] == CharState.Dead:
                        com["Combat"]["death"] = True
                        com["Combat"][tgt]["move"] = CombatCharAnime_Death(self.findChild(info[tgt]))
                        self.storeCombatEffect(com,"Combat",CombatCharAnime_DeathBook(
                            AnimeSprite_DeathBook("ani_deathbook",self.screen,0,self.findChild(info[tgt]).localPosition())))

                if "combatEffect" in info[info[tgt]].keys():
                    for dit in info[info[tgt]]["combatEffect"]:
                        #print(dit)
                        if dit["effectType"] == CombatEffectType.Damage:
                            self.createDmgEffect(com,"Combat",dit,info[tgt],tgt == "char1",Vector2.One())
                        elif dit["effectType"] == CombatEffectType.Buff:
                            self.createBuffDmgEffect(com,"Combat",dit,info[tgt],tgt == "char1",Vector2.One())
                        elif dit["effectType"] == CombatEffectType.Stagger:
                            self.createCombatTextEffect(com,"Combat",{"txt":"陷入混乱！","color":Data.fonts.ColorYellow},
                                                    info[tgt],tgt == "char1")
                        elif dit["effectType"] == CombatEffectType.Heal:
                            self.createHealEffect(com,"Combat",dit,info[tgt],tgt == "char1")
                        elif dit["effectType"] == CombatEffectType.Emotion:
                            self.createEmotionEffect(com,"Combat",dit,info[tgt],tgt == "char1")
                            '''
                            self.storeCombatEffect(com,"Combat",CombatEffectAnime(20,UICombatCommonDmg(
                                "dmgEffect",self.screen,random.randint(-10,10),dit["dmgType"],dit["dmgResis"],dit["dmgVal"]
                            ),(lambda pos = self.findChild(info[tgt]).localPosition(): 
                               pos + ((
                                   Vector2(100*random.uniform(0.8,1.2),100*random.uniform(1,1.5)) if dit["dmgType"] == DmgType.Stagger else
                                   Vector2(100*random.uniform(1.2,1.6),100*random.uniform(0,0.5))
                               )*(Vector2(-1,1) if tgt == "char1" else Vector2.One())))(),
                               (Vector2(30*random.uniform(0.5,2),-30*random.uniform(0.5,2))*Vector2((-1 if tgt == "char1" else 1),1)
                                if dit["dmgType"] == DmgType.Life else Vector2.Zero())
                            ))
                            '''
        
        elif info["CombatType"] == CombatType.AOE or info["CombatType"] == CombatType.RoundEnd:
            if info["CombatType"] == CombatType.AOE:
                _delay = (0 if info["AoeAnime"]["dmgDelay"] == None else info["AoeAnime"]["dmgDelay"])
                com["Combat"]["lasFrame"] = 20 if info["AoeAnime"]["lasFrame"] == None else info["AoeAnime"]["lasFrame"]
            elif info["CombatType"] == CombatType.RoundEnd:
                _delay = (5 if info["RoundEndAnime"]["dmgDelay"] == None else info["RoundEndAnime"]["dmgDelay"])
                com["Combat"]["lasFrame"] = 20 if info["RoundEndAnime"]["lasFrame"] == None else info["RoundEndAnime"]["lasFrame"]
            
            for char in info["joiner"]:
                charId = char["id"]
                com["Combat"][charId] = {
                    "sprite":CombatCharAnime_SimpleAct(self.findChild(charId).findChild("charImg"),3,info[charId]["action"])
                }

                if "state" in info[charId]["afterCombat"].keys():  
                    com["state"][charId] = info[charId]["afterCombat"]["state"]
                    if com["state"][charId] == CharState.Dead:
                        com["Combat"]["death"] = True
                        com["Combat"][charId]["move"] = CombatCharAnime_Death(self.findChild(charId),_delay)
                        self.storeCombatEffect(com,"Combat",CombatCharAnime_DeathBook(
                            AnimeSprite_DeathBook("ani_deathbook",self.screen,0,self.findChild(charId).localPosition(),Vector2(0.6,0.6)),_delay))
                
                if "combatEffect" in info[charId].keys():
                    for dit in info[charId]["combatEffect"]:
                        #print(dit)
                        if dit["effectType"] == CombatEffectType.Damage:
                            self.createDmgEffect(com,"Combat",dit,charId,decodeCharIdInfo(charId) == 1,Vector2(0.6,0.6), _delay)
                        elif dit["effectType"] == CombatEffectType.Buff:
                            self.createBuffDmgEffect(com,"Combat",dit,charId,decodeCharIdInfo(charId) == 1,Vector2(0.6,0.6),_delay)
                        elif dit["effectType"] == CombatEffectType.Stagger:
                            self.createCombatTextEffect(com,"Combat",{"txt":"陷入混乱！","color":Data.fonts.ColorYellow},
                                                    charId,decodeCharIdInfo(charId) == 1,Vector2(0.6,0.6),_delay)
                        elif dit["effectType"] == CombatEffectType.Heal:
                            self.createHealEffect(com,"Combat",dit,charId,decodeCharIdInfo(charId) == 1,Vector2(0.6,0.6), _delay)
            
            if info["CombatType"] == CombatType.RoundEnd:
                return
            
            #aoeAnime 的 attacker Anime 留attacker的uiCombatCharacter实例化
            #effect anime 留 effect的中心点实例化 默认双方team的中心点
            if info["AoeAnime"]["attacker"] != None:
                com["Combat"][com["attacker"]].update({
                    "move":info["AoeAnime"]["attacker"](self.findChild(com["attacker"]),self,self.scene.rendererTempObject,info)
                })
            for effect in info["AoeAnime"]["effects"]:
                self.storeCombatEffect(com,"Combat",effect(Vector2(300,30) if decodeCharIdInfo(com["attacker"]) == 1 else Vector2(-300,30)
                                                           ,self,self.scene.rendererTempObject,info))


    def prepareLeaveStage(self,info,com):
        com["LeaveStage"] = {}
        if info["CombatType"] == CombatType.Near or info["CombatType"] == CombatType.Far:
            self.curCombat["LeaveStage"]["consist"] = info["consist"]
            if info["consist"] == "Null":
                midx = (self.findChild(info["char1"]).localPosition().x+self.findChild(info["char2"]).localPosition().x)/2
                end_pos = Vector2(820*(-1 if midx<0 else 1),30*random.uniform(-1.0,1.0))
                self.curCombat["LeaveStage"]["leftDirection"] = Vector2((-1 if midx<0 else 1),1)
                for tgt in ["char1","char2"]:
                    com["LeaveStage"][tgt] = {
                            "sprite":CombatCharAnime_SimpleAct(self.findChild(info[tgt]).findChild("charImg"),15,
                                                               (CharSD.Move if com["state"][tgt] == CharState.Common else CharSD.Hurt)),
                            "move":CombatCharAnime_CharMove(self.findChild(info[tgt]),15,
                                                            self.findChild(info[tgt]).localPosition(),
                                                            end_pos(),CharActionType.LeaveStage)
                    }
            elif info["consist"] == "All":
                self.curCombat["LeaveStage"]["approachFlame"] = 5
                self.curCombat["LeaveStage"]["Point"] = {}
                for tgt in ["char1","char2"]:
                    self.curCombat["LeaveStage"]["Point"][tgt] = self.findChild(info[tgt]).localPosition()
                for tgt in ["char1","char2"]:
                    com["LeaveStage"][tgt] = {}
            else:
                self.curCombat["LeaveStage"]["consistPos"] = self.findChild(info[info["consist"]]).localPosition()
                end_pos = {"char1":Vector2(-820,0),"char2":Vector2(820,0)}
                opp = {"char1":"char2","char2":"char1"}
                com["LeaveStage"][info["consist"]] = {}
                _id = info[opp[info["consist"]]]
                com["LeaveStage"][opp[info["consist"]]] = {
                    "sprite":CombatCharAnime_SimpleAct(self.findChild(_id).findChild("charImg"),15,
                                                       (CharSD.Move if com["state"][opp[info["consist"]]] == CharState.Common else CharSD.Hurt)),
                    "move":CombatCharAnime_CharMove(self.findChild(_id),15,
                                                    self.findChild(_id).localPosition(),
                                                    end_pos[opp[info["consist"]]],CharActionType.LeaveStage
                                                    )
                }

    def prepareFirstCombat(self):
        self.findChild("BG").setValue(self.backgroundLis[1])
        self.curCombat = {}
        self.curCombat["LeaveStage"] = {}
        self.curCombat["LeaveStage"]["consist"] = "Null"
        self.curCombat["LeaveStage"]["leftDirection"] = Vector2(-1,1)
    def prepareGroupEnter(self,info):
        #print(self.curInfo["CombatType"])
        self.curCombat = "Null"
        self.findChild("BG").setValue(self.backgroundLis[0])
        for child in self.children:
            if isinstance(child,UICombatCharacter):
                child.setActive(False)
        for char in info["joiner"]:
            if self.findChild(char["id"]) != None:
                self.findChild(char["id"]).setActive(True)
                self.findChild(char["id"]).setScale(Vector2(0.4,0.4))
                #print(char["id"],self.findChild(char["id"]).worldScale())
                if isinstance(char["pos"],Vector2):
                    self.findChild(char["id"]).setPos(char["pos"])
                else:
                    self.findChild(char["id"]).setPos(AOELocalPosition(decodeCharIdInfo(char["id"]),char["pos"]))
    def prepareGroupExit(self):
        for child in self.children:
            if isinstance(child,UICombatCharacter):
                child.setActive(False)
                child.setScale(Vector2(0.7,0.7))
        self.curCombat = None
    def createDmgEffect(self,com,phase,dit,charId,faceflag,scale = Vector2.One(),delay=0):
        self.storeCombatEffect(com,phase,CombatEffectAnime(20,UICombatCommonDmg(
                                "dmgEffect",self.screen,random.randint(-10,10),dit["dmgType"],dit["dmgResis"],dit["dmgVal"],scale
                            ),(lambda pos = self.findChild(charId).localPosition(): 
                               pos + ((
                                   Vector2(100*random.uniform(0.8,1.2),100*random.uniform(1,1.5))*scale() if dit["dmgType"] == DmgType.Stagger else
                                   Vector2(100*random.uniform(1.2,1.6),100*random.uniform(0,0.5))*scale()
                               )*(Vector2(-1,1) if faceflag else Vector2.One())))(),
                               (Vector2(30*random.uniform(0.5,2),-30*random.uniform(0.5,2))*Vector2((-1 if faceflag else 1),1)
                                if dit["dmgType"] == DmgType.Life else Vector2.Zero()),delay
                            ))
    def createBuffDmgEffect(self,com,phase,dit,charId,faceflag,scale = Vector2.One(),delay = 0):
        self.storeCombatEffect(com,phase,CombatEffectAnime(20,UICombatBuffDmg(
            "buffDmgEffect",self.screen,random.randint(-20,20),dit["buffType"],dit["dmgVal"],scale
        ),(lambda pos = self.findChild(charId).localPosition():
           pos + ((Vector2(-100*random.uniform(0.5,1),100*random.uniform(-0.5,0.5))*scale()
                )*(Vector2(-1,1) if faceflag else Vector2.One())))(),
                (Vector2(-30*random.uniform(0.5,1),30*random.uniform(0.5,1))*scale()*Vector2((-1 if faceflag else 1),1)),delay))
    def createCombatTextEffect(self,com,phase,dit,charId,faceflag,scale = Vector2.One(),delay = 0):
        self.storeCombatEffect(com,phase,CombatEffectAnime(20,UICombatCommonText(
            "combatTextEffect",self.screen,random.randint(-20,0),dit["txt"],dit["color"],scale
        ),(lambda pos = self.findChild(charId).localPosition():
           pos + ((Vector2(100*random.uniform(0.5,1),100*random.uniform(-0.5,0.5))*scale()
                )*(Vector2(-1,1) if faceflag else Vector2.One())))(),Vector2.Zero(),delay))
    def createHealEffect(self,com,phase,dit,charId,faceflag,scale = Vector2.One(),delay = 0):
        self.storeCombatEffect(com,phase,CombatEffectAnime(10,UICombatCommonHeal(
            "healEffect",self.screen,random.randint(-20,20),dit["healType"],dit["healVal"],scale
        ),(lambda pos = self.findChild(charId).localPosition():
           pos + ((Vector2(100*random.uniform(0,1),100*random.uniform(-1,0))*scale()
                )*(Vector2(-1,1) if faceflag else Vector2.One())))(),
                (Vector2(15*random.uniform(0.5,1),-15*random.uniform(0.5,1))*scale()*Vector2((-1 if faceflag else 1),1)),delay))
    def createEmotionEffect(self,com,phase,dit,charId,faceflag,delay=0):
        _num = 1
        if "count" in dit.keys():
            _num = dit["count"]
        for _k in range(_num):
            self.storeCombatEffect(com,phase,CombatEmotionAnime(UIEmotionLine("emo",self.screen,random.randint(10,30),
                                self.findChild(charId).localPosition()+Vector2(0,-100),(Vector2(-620,180) if faceflag else Vector2(620,180)),
                                Data.fonts.ColorEmotionGreen if (not "type" in dit.keys() or dit["type"] == EmotionType.Green) else 
                                Data.fonts.ColorEmotionRed)))
    def ChangeAnimeProcess(self,process):
        #print("timerEnd")
        if process <= CombatProcess.LeaveStage.value:
            self.storedData["AnimeProcess"] = process
            self.controlSys["InAnime"] = False
        else:
            self.storedData["AnimeProcess"] = 1
            self.controlSys["ReadyForAnime"] = False
            self.controlSys["InAnime"] = False
    def PushCombatProcess(self,process):
        if process == CombatProcess.LeaveStage.value:
            self.preparePlayerAfterCombat(self.curInfo)
        if process == CombatProcess.Combat.value:
            self.prepareCombat(self.curInfo,self.curCombat)
        elif process == CombatProcess.LeaveStage.value:
            self.prepareLeaveStage(self.curInfo,self.curCombat)
        elif process == CombatProcess.DiceRolling.value:
            self.prepareDiceRolling(self.curInfo,self.curCombat)
        deltaFrame = 1
        self.controlSys["InAnime"] = True
        if process >= CombatProcess.EnterStage.value and process <= CombatProcess.LeaveStage.value:
            self.activateCombatEffect(self.curCombat,ProcessName[process])
            if process == CombatProcess.Combat.value:
                if "death" in self.curCombat["Combat"].keys():
                    #print("chipichipi chapachapa")
                    CombatSlowTimerAnime(15,1/30).start()
            if process == CombatProcess.DiceRolling.value:
                if self.curCombat["CombatType"] == CombatType.Near or self.curCombat["CombatType"] == CombatType.Far:
                    for tgt in ["char1","char2"]:
                        self.findChild(self.curCombat[tgt]).AniActivate(process)
                    CombatTimerAnime(self,20,process+1).start()
                elif self.curCombat["CombatType"] == CombatType.AOE:
                    for char in self.curCombat["joiner"]:
                        self.findChild(char["id"]).AniActivate(process)
                    CombatTimerAnime(self,15,process+1).start()
                elif self.curCombat["CombatType"] == CombatType.RoundEnd:
                    CombatTimerAnime(self,2,process+1).start()
            elif self.curCombat["CombatType"] == CombatType.Near or self.curCombat["CombatType"] == CombatType.Far:
                for tgt in ["char1","char2"]:
                    maxF = self.findChild(self.curCombat[tgt]).AniCreate(process,self.curCombat[ProcessName[process]][tgt])
                    self.findChild(self.curCombat[tgt]).AniActivate(process)
                    if maxF != None:
                        deltaFrame = max(deltaFrame,maxF)
                if process == CombatProcess.Combat.value:
                    CombatTimerAnime(self,15,process+1).start()
                else:
                    CombatTimerAnime(self,deltaFrame,process+1).start()
            elif self.curCombat["CombatType"] == CombatType.AOE or self.curCombat["CombatType"] == CombatType.RoundEnd:
                if process == CombatProcess.EnterStage.value or process == CombatProcess.LeaveStage.value:
                    CombatTimerAnime(self,2,process+1).start()
                elif process == CombatProcess.Combat.value:
                    for char in self.curCombat["joiner"]:
                        charId = char["id"]
                        self.findChild(charId).AniCreate(process,self.curCombat["Combat"][charId])
                        self.findChild(charId).AniActivate(process)
                    CombatTimerAnime(self,self.curCombat["Combat"]["lasFrame"],process+1).start()
