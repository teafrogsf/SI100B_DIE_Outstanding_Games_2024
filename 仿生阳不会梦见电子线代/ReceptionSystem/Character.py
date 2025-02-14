from ReceptionSystem.Dice import Dice
from ReceptionSystem.Buffs import *
from ReceptionSystem.SpeedDice import *
from ReceptionSystem.Emotion import *
from GameDataManager import gameDataManager
from RenderSystem.sceneRenderer.BattleCombatRenderer import CombatType,CombatEffectType
from RenderSystem.prefab.UICombatText import DmgType,DmgResis
from RenderSystem.prefab.UICharacter import CharSD,CharState
import copy,math
class Character:
    #About initialize
    def __init__(self,name,healthMax,staggerMax,originResistance,speedL,speedR,countDices,lightMax,id,pos,team,SDname=None):
        #modified by NH37
        self.SDname = SDname
        
        self.name=name
        self.healthMax=healthMax
        self.health=healthMax
        self.staggerMax=staggerMax
        self.stagger=staggerMax
        self.originResistance=originResistance
        self.resistance=copy.deepcopy(originResistance)
        self.speedL=speedL
        self.speedR=speedR
        self.countDices=countDices
        self.speedDices=[]
        for i in range(0,countDices):
            self.speedDices.append(SpeedDice(speedL,speedR,self,i))
        self.pageStock=[]
        self.pages=[]
        self.handPages=[]
        self.isStagger=0
        self.light=lightMax
        self.lightMax=lightMax
        self.lightHave=lightMax
        self.buffs=Buffs()
        self.nextBuffs=Buffs()
        self.buffs.affiliateCharacter=self
        self.nextBuffs.affiliateCharacter=self
        self.speedBuff=SpeedBuffs()
        self.powerBuff=PowerBuffs()
        self.damageBuff=DamageBuffss()
        self.id=id
        self.pos=pos
        self.team=team
        self.affiliateTeam=None
        self.againstTeam=None
        self.defense=[]
        self.emotion=Emotion(0,0,0)
        self.emotion.affiliateCharacter=self
        self.rollPage=1 #Here
        self.getLight=1
        self.havePower=True
        self.special=None
        self.passive=[]
        self.passiveDit={"Burnt":False,"PageDamage":0,"TotalDamage":0,"Recover":0}
    def HavePassive(self,name):
        t=0
        for passive in self.passive:
            if passive==name:
                t+=1
        return t
    def AddPassive(self,name):
        self.passive.append(name)
    def AddPage(self,opage,defense=False):
        if not defense:
            page=copy.deepcopy(opage)
            if page.name==u"狂暴血刃":
                page.charge=True
            page.affiliateCharacter=self
            page.pageBuff.affiliateCharacter=self
            for dice in page.dices:
                dice.affiliatePage=page
                dice.affiliateCharacter=self
                dice.diceBuff.affiliateCharacter=self
            page.id=len(self.pageStock)+1
            self.pages.append(page)
            self.pageStock.append(page)
        else:
            opage.affiliateCharacter=self
            opage.pageBuff.affiliateCharacter=self
            for dice in opage.dices:
                dice.affiliateCharacter=self
                dice.diceBuff.affiliateCharacter=self
    #About buff
    def AddBuff(self,name,count):
        for i in range(self.HavePassive(u"强化充能")):
            if name=="Charge" and count>0:
                if not self.passiveDit[u"强化充能"]:
                 self.AddNextBuff("Endurance",1)
        for i in range(self.HavePassive(u"进阶充能")):
            if name=="Charge" and count<0:
                if not self.passiveDit[u"进阶充能"]:
                 self.AddNextBuff("Strength",1)
        for buff in self.buffs.buffs:
            if buff.name==name:
                buff.AddCount(count)
                return
        if count<=0:
            return
        self.buffs.AddBuff(name,count)
    def AddNextBuff(self,name,count):
        for buff in self.nextBuffs.buffs:
            if buff.name==name:
                buff.AddCount(count)
                return
        self.nextBuffs.AddBuff(name,count)
    #About speed buff
    def AddSpeedBuff(self,pointL,pointR,tag):
        speedBuff=SpeedBuff(tag)
        speedBuff.speedBuff=(pointL,pointR)
        self.speedBuff.speedBuff.append(speedBuff)
    def ClearSpeedBuff(self,tag):
        self.speedBuff.ClearBuff(tag)
    #About power buff
    def AddPowerBuff(self,powerType,pointL,pointR,tag):
        powerBuff=PowerBuff(tag)
        powerBuff.powerBuff[powerType]=(pointL,pointR)
        self.powerBuff.powerBuff.append(powerBuff)
    def AddPowerLR(self,pointL,pointR,tag):
        powerBuff=PowerBuff(tag)
        powerBuff.powerLR=(pointL,pointR)
        self.powerBuff.powerLR.append(powerBuff)
    def ClearPowerBuff(self,tag):
        self.powerBuff.ClearBuff(tag)
    #About damage buff
    def AddDamageBuff(self,damageType,pointL,pointR,tag,isStagger=False):
        damageBuff=DamageBuff(tag)
        damageBuff.damageBuff[damageType]=(pointL,pointR)
        if isStagger:
            self.damageBuff.SdamageBuff.damageBuff.append(damageBuff)
        else:
            self.damageBuff.damageBuff.damageBuff.append(damageBuff)
    def AddGetDamageBuff(self,getdamageType,pointL,pointR,tag,isStagger=False):
        getdamageBuff=DamageBuff(tag)
        getdamageBuff.getdamageBuff[getdamageType]=(pointL,pointR)
        if isStagger:
            self.damageBuff.SdamageBuff.getdamageBuff.append(getdamageBuff)
        else:
            self.damageBuff.damageBuff.getdamageBuff.append(getdamageBuff)
    def AddDamagePer(self,damageType,per,tag,isStagger=False):
        damagePer=DamageBuff(tag)
        damagePer.damagePer[damageType]=per
        if isStagger:
            self.damageBuff.SdamageBuff.damagePer.append(damagePer)
        else:
            self.damageBuff.damageBuff.damagePer.append(damagePer)
    def AddGetDamagePer(self,getdamageType,per,tag,isStagger=False):
        getdamagePer=DamageBuff(tag)
        getdamagePer.getdamagePer[getdamageType]=per
        if isStagger:
            self.damageBuff.SdamageBuff.getdamagePer.append(getdamagePer)
        else:
            self.damageBuff.damageBuff.getdamagePer.append(getdamagePer)
    def AddGetDamage(self,per,tag,isStagger=False):
        getdamage=DamageBuff(tag)
        getdamage.getdamage=per
        if isStagger:
            self.damageBuff.SdamageBuff.getdamage.append(getdamage)
        else:
            self.damageBuff.damageBuff.getdamage.append(getdamage)
    def ClearDamageBuff(self,tag):
        self.damageBuff.ClearBuff(tag)
    #About dealing with id
    def FindDice(self,id):
        id%=1000
        for dice in self.speedDices:
            if(dice.id==id):
                return dice
        return None
    def FindDiceIndex(self,id):
        n=len(self.speedDices)
        for i in range(n):
            if(self.speedDices[i].id==id):
                return i+1
        return None
    def FindPage(self,id):
        id%=1000
        for page in self.pageStock:
            if(page.id==id):
                return page
        return None
    #Functions for getting status
    def JudgeDeath(self):
        return self.health<=0
    def JudgeStagger(self):
        return self.isStagger>0
    #About defense page
    def AddDefense(self,odice):
        if self.JudgeStagger():
            return 
        dice=copy.deepcopy(odice)
        self.defense.append(dice)
    def ClearDefense(self):
        self.defense.clear()
    #About stagger
    def DoStagger(self,attacker,source="Person"):
        if source=="Person":
            print(f"{self.name} stuck in stagger, beaten by {attacker.name}")
        else:
            print(f"{self.name} stuck in stagger because of {source}")
        dic={}
        dic["effectType"]=CombatEffectType.Stagger
        if (self.id in gameDataManager.curDict):
            gameDataManager.curDict[self.id]["combatEffect"].append(dic)
        self.isStagger=1
        self.resistance={"Slash":2.0,"Pierce":2.0,"Blunt":2.0,"Slash_s":2.0,"Pierce_s":2.0,"Blunt_s":2.0}
        for dice in self.speedDices:
            dice.isbreak=True
    def ClearStagger(self):
        self.isStagger=0
        self.resistance=self.originResistance
        self.stagger=self.staggerMax
        for dice in self.speedDices:
            dice.isbreak=False
    def ClaimDeath(self,attacker,source="Person"):
        if source=="Person":
            print(f"{self.name} was killed by {attacker.name}")
            if attacker.HavePassive(u"殷红迷雾") and attacker.ego:
                attacker.AddBuff("BloodMist",1)
            attacker.emotion.GetGreenCoin(3)
            #for character in self.affiliateTeam.characters:
            #    if character.JudgeDeath()==False:
            #        character.emotion.GetRedCoin(3)
        else :
            print(f"{self.name} was killed by {source}")
    #About damage calculation
    def CalcDamageBuff(self,attacker,attackType,isStagger=False,isCounter=False):
        if isStagger:
            db=self.damageBuff.SdamageBuff
            adb=attacker.damageBuff.SdamageBuff
        else:
            db=self.damageBuff.damageBuff
            adb=attacker.damageBuff.damageBuff
        damageBuff=adb.CalcDamageBuff()
        getdamageBuff=db.CalcGetDamageBuff()
        dm=damageBuff[attackType]+damageBuff["Total"]
        if attackType=="Block":
            dm+=damageBuff["Defense"]
        else :
            dm+=damageBuff["Attack"]
        if isCounter:
            dm+=damageBuff["Counter"]
        dm+=getdamageBuff[attackType]+getdamageBuff["Total"]
        if attackType=="Block":
            dm+=getdamageBuff["Defense"]
        else :
            dm+=getdamageBuff["Attack"]
        if isCounter:
            dm+=getdamageBuff["Counter"]
        return dm    
    def CalcDamagePer(self,attacker,attackType,isStagger=False,isCounter=False):
        if isStagger:
            db=self.damageBuff.SdamageBuff
            adb=attacker.damageBuff.SdamageBuff
        else:
            db=self.damageBuff.damageBuff
            adb=attacker.damageBuff.damageBuff
        damageBuff=adb.CalcDamagePer()
        getdamageBuff=db.CalcGetDamagePer()
        dm=damageBuff[attackType]+damageBuff["Total"]
        if attackType=="Block":
            dm+=damageBuff["Defense"]
        else :
            dm+=damageBuff["Attack"]
        if isCounter:
            dm+=damageBuff["Counter"]
        dm+=getdamageBuff[attackType]+getdamageBuff["Total"]
        if attackType=="Block":
            dm+=getdamageBuff["Defense"]
        else :
            dm+=getdamageBuff["Attack"]
        if isCounter:
            dm+=getdamageBuff["Counter"]
        return dm
    def CalcGetDamage(self,isStagger=False):
        if isStagger:
            db=self.damageBuff.SdamageBuff
        else:
            db=self.damageBuff.damageBuff
        return db.CalcGetDamage()
    #About damage and recover stagger resistance by clashing and attack, call function to display that
    def DoDamage(self,dicePoint,attackType,attacker,redcoin,isCounter=False):
        for i in range(attacker.HavePassive(u"致瘾烟气")):
            if self.buffs.GetBuffCount("Smoke")>=8:
                self.AddNextBuff("Paralysis",2)
        for i in range(attacker.HavePassive(u"炽热之刃")):
            self.AddBuff("Burn",2)
        for i in range(self.HavePassive(u"凤翎之盾")):
            attacker.AddBuff("Burn",2)
        if attacker.HavePassive(u"拥火卧薪")>0:
            self.passiveDit["Burnt"]=True
        if redcoin: 
            self.emotion.GetRedCoin()
        self.buffs.GetDamage()
        if self.id in gameDataManager.curDict:
            gameDataManager.curDict[self.id]["action"]=CharSD.Hurt
            gameDataManager.curDict["MainDmg"]=dicePoint
            gameDataManager.curDict["CombatLoser"]=self.id
        dicS={}
        dic={}
        if(attackType=="Block"):
            damageS=math.floor((dicePoint+self.CalcDamageBuff(attacker,attackType,True,isCounter))*
                        (1.0+self.CalcDamagePer(attacker,attackType,True,isCounter))*
                        (1.0-self.CalcGetDamage(True)))
            print(f"{self.name} get {damageS} {attackType} stagger damage")
            dicS["effectType"]=CombatEffectType.Damage
            dicS["dmgType"]=DmgType.Stagger
            dicS["dmgResis"]=DmgResis.Null
            dicS["dmgVal"]=damageS
            if self.id in gameDataManager.curDict:
                gameDataManager.curDict[self.id]["combatEffect"].append(dicS)
            self.stagger-=damageS
            if(self.stagger<0):
                self.stagger=0
            if(self.stagger==0):
                if not self.JudgeStagger():
                    self.DoStagger(attacker)
        else:
            damage=math.floor((dicePoint+self.CalcDamageBuff(attacker,attackType,False,isCounter))*
                        (1.0+self.CalcDamagePer(attacker,attackType,False,isCounter))*
                        (1.0-self.CalcGetDamage())*
                        self.resistance[attackType])
            damage=max(0,damage)
            damageS=math.floor((dicePoint+self.CalcDamageBuff(attacker,attackType,True,isCounter))*
                        (1.0+self.CalcDamagePer(attacker,attackType,True,isCounter))*
                        (1.0-self.CalcGetDamage(True))*
                        self.resistance[attackType+"_s"])
            damageS=max(0,damageS)
            print(f"{self.name} get {damage}/{damageS} {attackType} damage")
            rdic={0:DmgResis.Null,0.25:DmgResis.Ineffective,0.5:DmgResis.Endured,1:DmgResis.Normal,1.5:DmgResis.Weak,2:DmgResis.Fatal}#Here
            dicS["effectType"]=CombatEffectType.Damage
            dicS["dmgType"]=DmgType.Stagger
            dicS["dmgResis"]=rdic[self.resistance[attackType+"_s"]]
            dicS["dmgVal"]=damageS
            if self.id in gameDataManager.curDict:
                gameDataManager.curDict[self.id]["combatEffect"].append(dicS)
            dic["effectType"]=CombatEffectType.Damage
            dic["dmgType"]=DmgType.Life
            dic["dmgResis"]=rdic[self.resistance[attackType]]
            dic["dmgVal"]=damage
            if self.id in gameDataManager.curDict:
                gameDataManager.curDict[self.id]["combatEffect"].append(dic)
            self.stagger-=damageS
            self.health-=damage
            attacker.passiveDit["PageDamage"]+=damage
            attacker.passiveDit["TotalDamage"]+=damage
            if(self.stagger<0):
                self.stagger=0
            if(self.stagger==0):
                if not self.JudgeStagger():
                    self.DoStagger(attacker)
            if(self.JudgeDeath()):
                self.ClaimDeath(attacker,"Person")
    def RecoverStagger(self,dicePoint,needDit=True):
        if self.JudgeStagger():
            return 
        print(f"{self.name} get {dicePoint} stagger resistance recovered")
        if needDit:
            dic={}
            dic["effectType"]=CombatEffectType.Heal
            dic["healType"]=DmgType.Stagger
            dic["healVal"]=dicePoint
            if self.id in gameDataManager.curDict:
                gameDataManager.curDict[self.id]["combatEffect"].append(dic)
        self.stagger+=dicePoint
        self.stagger=min(self.stagger,self.staggerMax)
    def RecoverHealth(self,dicePoint,needDit=True):
        if self.JudgeDeath():
            return 
        print(f"{self.name} get {dicePoint} health recovered")
        self.passiveDit["Recover"]+=dicePoint
        if needDit:
            dic={}
            dic["effectType"]=CombatEffectType.Heal
            dic["healType"]=DmgType.Life
            dic["healVal"]=dicePoint
            if self.id in gameDataManager.curDict:
                gameDataManager.curDict[self.id]["combatEffect"].append(dic)
        self.health+=dicePoint
        self.health=min(self.health,self.healthMax)
    #About call function to display attack and deal with dice buff and emotion coins
    def ClashWin(self,attackType):
        dic={"Slash":CharSD.Slash,"Pierce":CharSD.Pierce,"Blunt":CharSD.Blunt,"Block":CharSD.Block,"Evade":CharSD.Evade}
        if self.id in gameDataManager.curDict:
            gameDataManager.curDict[self.id]["action"]=dic[attackType]
            gameDataManager.curDict["CombatWinner"]=self.id
        print(f"{self.name} attack with {attackType}")
        self.emotion.GetGreenCoin()
    def ClashTie(self,attackType):
        dic={"Slash":CharSD.Slash,"Pierce":CharSD.Pierce,"Blunt":CharSD.Blunt,"Block":CharSD.Block,"Evade":CharSD.Evade}
        if self.id in gameDataManager.curDict:
            gameDataManager.curDict[self.id]["action"]=dic[attackType]
            gameDataManager.curDict["MainDmg"]=0
            gameDataManager.curDict["CombatLoser"]=None
            gameDataManager.curDict["CombatWinner"]=None
        print(f"{self.name} attack with {attackType},but tied")
    def ClashLose(self,attackType):
        dic={"Slash":CharSD.Slash,"Pierce":CharSD.Pierce,"Blunt":CharSD.Blunt,"Block":CharSD.Block,"Evade":CharSD.Evade}
        if self.id in gameDataManager.curDict:
            gameDataManager.curDict[self.id]["action"]=dic[attackType]
            gameDataManager.curDict["MainDmg"]=0
            gameDataManager.curDict["CombatLoser"]=self.id
        print(f"{self.name} attack with {attackType},but evaded")
        self.emotion.GetRedCoin()
    #About damage and recover from other ways
    def DoDamage2(self,point,source,attacker=None):
        if self.JudgeDeath():
            return
        if source=="Person":
            print(f"{self.name} get {point} damage from {attacker.name}")
        else:
            print(f"{self.name} get {point} damage from {source}")
        self.health-=point
        dic={}
        if source=="Person":
            dic["effectType"]=CombatEffectType.Damage
            dic["dmgResis"]=DmgResis.Null
            dic["dmgType"]=DmgType.Life
        else:
            dic["effectType"]=CombatEffectType.Buff
            dic["buffType"]=source
        dic["dmgVal"]=point
        if self.id in gameDataManager.curDict:
            gameDataManager.curDict[self.id]["combatEffect"].append(dic)
        if self.JudgeDeath():
            self.ClaimDeath(attacker,source)
    def DoStaggerDamage2(self,point,source,attacker=None):
        if self.JudgeDeath():
            return
        if source=="Person":
            print(f"{self.name} get {point} stagger damage from {attacker.name}")
        else:
            print(f"{self.name} get {point} stagger damage from {source}")
        self.stagger-=point
        dic={}
        if source=="Person":
            dic["effectType"]=CombatEffectType.Damage
            dic["dmgType"]=DmgType.Stagger
            dic["dmgResis"]=DmgResis.Null
            dic["dmgVal"]=point
            if self.id in gameDataManager.curDict:
                gameDataManager.curDict[self.id]["combatEffect"].append(dic)
        if(self.stagger<0):
                self.stagger=0
        if(self.stagger==0):
                if not self.JudgeStagger():
                    self.DoStagger(attacker,source)
    #About speed dice
    def RollSpeed(self,speedBuff):
        if self.JudgeStagger():
            for dice in self.speedDices:
                dice.isbreak=True
        else:
            mi=99
            for dice in self.speedDices:
                dice.isbreak=False
                dice.ConfirmDice(speedBuff)
                mi=min(mi,dice.speed)
            if self.HavePassive(u"最强之人")>0:
                for dice in self.speedDices:
                    if dice.speed==mi:
                        dice.speed=99
            self.speedDices=sorted(self.speedDices,key=lambda x:x.speed,reverse=True)
    #About pages
    def RollPage(self):
        if len(self.pages)>1:
            x=random.randint(0,len(self.pages)-1)
            self.handPages.append(self.pages[x])
            del self.pages[x]
    #About actions after round
    def RollBackPage(self):
        for dice in self.speedDices:
            if dice.havePage==True:
                dice.page.lightCost=dice.page.originCost
                self.pages.append(dice.page)
                dice.havePage=False
                dice.haveTarget=False
                dice.Target=None
                dice.massTarget.clear()
                dice.page=None
            dice.speed=-1
    #About page selecting
    def EquipPage(self,dice,target,pageid,origin=False):
        pageid%=1000
        for i in range(len(self.handPages)):
            if self.handPages[i].id==pageid:
                    id=i
                    break
        page=self.handPages[id]
        if(self.light>=page.lightCost):
            if page.charge==True and self.buffs.GetBuffCount("Charge")!=20:
                return False
            self.light-=page.lightCost
            dice.SelectPage(page)
            if page.pageType=="Melee" or page.pageType=="Ranged":
                dice.TargetPage(target)
            else:
                dice.MassTarget(target,self.againstTeam)
            if origin:
                dice.SetOrigin(target)
            del self.handPages[id]
            return True
        else:
            return False
    def UnequipPage(self,dice):
        self.light+=dice.page.lightCost
        self.handPages.append(dice.page)
        dice.DownPage()
    def RoundStart(self):
        self.passiveDit["Burnt"]=False
        self.passiveDit["TotalDamage"]=0
        self.passiveDit["Recover"]=0
        if self.JudgeDeath():
            return
        for i in range(self.HavePassive(u"刺激充能压缩肌肉")):
            if self.buffs.GetBuffCount("Charge")>=11:
                self.AddBuff("Haste",1)
        for i in range(self.HavePassive(u"Rabbit改造手术")):
            hl=self.healthMax-self.health
            cnt=math.floor(hl/self.healthMax*10/3)
            if cnt!=0:
                self.AddBuff("Haste",cnt)
        for i in range(self.HavePassive(u"脑波充能集束犄角")):
            if self.buffs.GetBuffCount("Charge")>=11:
                self.AddDamageBuff("Total",2,2,"roundend",True)
        for i in range(self.HavePassive(u"Reindeer改造手术")):
            hl=self.healthMax-self.health
            cnt=math.floor(hl/self.healthMax*10/3)
            if cnt!=0:
                self.AddBuff("Strength",min(cnt,2))
        for i in range(self.HavePassive(u"生物充能同步外皮")):
            if self.buffs.GetBuffCount("Charge")>=11:
                self.AddBuff("Protection",2)
        for i in range(self.HavePassive(u"Rhino改造手术")):
            hl=self.healthMax-self.health
            cnt=math.floor(hl/self.healthMax*10/3)
            if cnt!=0:
                self.AddBuff("Endurance",min(cnt,2))
        if self.HavePassive(u"极限冲击")>0:
            if self.buffs.GetBuffCount("Charge")>=11:
                self.AddDamagePer("Total",0.5,"roundend")
                self.AddDamagePer("Total",0.5,"roundend",True)
                self.AddGetDamage(0.3,"roundend")
                self.AddGetDamage(0.3,"roundend",True)
        for i in range(self.HavePassive(u"第4集团军总指挥")):
            if self.buffs.GetBuffCount("Charge")>=11:
                for character in self.affiliateTeam.characters:
                    character.AddBuff("Endurance",1)
                    character.AddBuff("Strength",1)
        if self.HavePassive(u"强化充能")>0:
            self.passiveDit[u"强化充能"]=False
        if self.HavePassive(u"进阶充能")>0:
            self.passiveDit[u"进阶充能"]=False
        
        for i in range(self.HavePassive(u"烟气过度")):
            if self.buffs.GetBuffCount("Smoke")>=8:
                self.AddBuff("Strength",1) 
        for i in range(self.HavePassive(u"供应过剩")):
            self.ClearDamageBuff("smokeenough")
            if self.buffs.GetBuffCount("Smoke")>=9:
                self.AddDamageBuff("Total",3,3,"smokeenough")
        for i in range(self.HavePassive(u"走火入魔")):   
            x=random.randint(1,4)
            if x==1:
                self.AddBuff("Strength",2)
            elif x==2:
                self.AddBuff("Endurance",2)
            elif x==3:
                self.AddBuff("Haste",2)
            else:
                self.AddBuff("Fragile",5)
        if self.HavePassive(u"围捕烟气")>0:
            s=self.buffs.GetBuffCount("Smoke")
            if s>0:
                self.AddDamagePer("Total",s*1.0/10,"roundend",True)
        for i in range(self.HavePassive(u"清醒烟气")):
            s=self.buffs.GetBuffCount("Smoke")
            if s>0:
                dice=Dice(1,s,"Block","Block",None,self)
                self.AddDefense(dice)

        for i in range(self.HavePassive(u"满腔热血")):
            if self.emotion.emotionLevel>=3:
                self.AddPowerBuff("Total",1,1,"passive")
        for i in range(self.HavePassive(u"狻猊騰雲")):
            for person in self.againstTeam.characters:
                person.AddBuff("Burn",2)

        for i in range(self.HavePassive(u"后发制敌")):
            dice=Dice(4,8,"Attack","Slash",None,self,True)
            self.AddDefense(dice)

        for i in range(self.HavePassive(u"冲锋姿态")):
            self.AddBuff("Fragile",4)   
            self.AddBuff("Strength",1)   
        for i in range(self.HavePassive(u"血魔之力")):
            if self.passiveDit["Recover"]>3:
                self.AddBuff("Strength",1)   
        for i in range(self.HavePassive(u"深呼吸")):
            self.getLight+=1
    def RoundEnd(self):
        pass
    def InitPassive(self):
        if self.HavePassive(u"速战速决")>0 or self.HavePassive(u"速战速决3")>0:
            self.countDices+=1
            self.speedDices.append(SpeedDice(self.speedL,self.speedR,self,self.countDices))
        if self.HavePassive(u"速战速决2")>0:
            self.countDices+=1
            self.speedDices.append(SpeedDice(self.speedL,self.speedR,self,self.countDices))
            self.countDices+=1
            self.speedDices.append(SpeedDice(self.speedL,self.speedR,self,self.countDices))
        for i in range(self.HavePassive(u"斩击精通")):
            self.AddPowerBuff("Slash",1,1,"passive")
        for i in range(self.HavePassive(u"突刺精通")):
            self.AddPowerBuff("Pierce",1,1,"passive")
        for i in range(self.HavePassive(u"打击精通")):
            self.AddPowerBuff("Blunt",1,1,"passive")
        for i in range(self.HavePassive(u"斩击精通2")):
            self.AddPowerBuff("Slash",2,2,"passive")
        for i in range(self.HavePassive(u"突刺精通2")):
            self.AddPowerBuff("Pierce",2,2,"passive")
        for i in range(self.HavePassive(u"打击精通2")):
            self.AddPowerBuff("Blunt",2,2,"passive")

        for i in range(self.HavePassive(u"强力斩击")):
            self.AddDamageBuff("Slash",1,1,"passive")
        for i in range(self.HavePassive(u"强力突刺")):
            self.AddDamageBuff("Pierce",1,1,"passive")
        for i in range(self.HavePassive(u"强力打击")):
            self.AddDamageBuff("Blunt",1,1,"passive")
        for i in range(self.HavePassive(u"强力斩击2")):
            self.AddDamageBuff("Slash",2,2,"passive")
        for i in range(self.HavePassive(u"强力突刺2")):
            self.AddDamageBuff("Pierce",2,2,"passive")
        for i in range(self.HavePassive(u"强力打击2")):
            self.AddDamageBuff("Blunt",2,2,"passive")

        for i in range(self.HavePassive(u"震撼斩击")):
            self.AddDamageBuff("Slash",1,1,"passive",True)
        for i in range(self.HavePassive(u"震撼突刺")):
            self.AddDamageBuff("Pierce",1,1,"passive",True)
        for i in range(self.HavePassive(u"震撼打击")):
            self.AddDamageBuff("Blunt",1,1,"passive",True)
        for i in range(self.HavePassive(u"震撼斩击2")):
            self.AddDamageBuff("Slash",2,2,"passive",True)
        for i in range(self.HavePassive(u"震撼突刺2")):
            self.AddDamageBuff("Pierce",2,2,"passive",True)
        for i in range(self.HavePassive(u"震撼打击2")):
            self.AddDamageBuff("Blunt",2,2,"passive",True)   

        if self.HavePassive(u"十二收尾人")>0:
            self.AddPowerLR(2,0,"passive")
        if self.HavePassive(u"指令通览")>0:
            self.RollPage()
        if self.HavePassive(u"未雨绸缪")>0:
            self.RollPage()
            self.RollPage()