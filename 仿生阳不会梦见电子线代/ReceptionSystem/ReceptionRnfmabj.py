from ReceptionSystem.Page import *
from ReceptionSystem.Character import *
class Rnfmabj(Character):
    def __init__(self,id,pos):
        yangd11=Dice(20,30,"Evade","Evade",None,None)
        yangd21=Dice(20,30,"Evade","Evade",None,None)
        yangd31=Dice(20,30,"Evade","Evade",None,None)
        yangd12=Dice(20,30,"Evade","Evade",None,None,True)
        yangd41=Dice(4,7,"Block","Block",None,None)
        yangmd5=Dice(18,33,"Attack","Slash",None,None)
        yangmd5.AddDiceBuff(MassHitExertBuffs(["Erosion"],[2],False))
        yangd61=Dice(20,30,"Evade","Evade",None,None)

        yangp1=Page(u"执行-进攻","Melee",[],0,None,1,"Green")
        yangp1.AddDice(yangd11)
        yangp1.AddCounterDice(yangd12)
        yangp1.AddCounterDice(yangd12)
        yangp1.pageBuff=YangStrength()

        yangp2=Page(u"执行-护卫","Melee",[],0,None,1,"Green")
        yangp2.AddDice(yangd21)
        yangp2.AddCounterDice(yangd12)
        yangp2.AddCounterDice(yangd12)
        yangp2.pageBuff=YangProtection()

        yangp3=Page(u"执行-警戒","Melee",[],0,None,1,"Green")
        yangp3.AddDice(yangd31)
        yangp3.AddCounterDice(yangd12)
        yangp3.AddCounterDice(yangd12)
        yangp3.pageBuff=YangNoPower()

        yangp4=Page(u"执行-固守","Melee",[],0,None,1,"Blue")
        yangp4.AddDice(yangd41)
        yangp4.AddDice(yangd41)
        yangp4.AddDice(yangd41)
        yangp4.AddDice(yangd41)

        yangp5=Page(u"全体修复","Melee",[],0,None,1,"Purple")
        yangp5.AddDice(yangd61)
        yangp5.pageBuff=YangAllRecover()

        yangp6=Page(u"执行-修复","Melee",[],0,None,1,"Blue")
        yangp6.AddDice(yangd61)
        yangp6.pageBuff=YangRecover()

        yangp7=Page(u"扭曲之刃","Summation",[],0,None,1,"Gold")
        yangp7.AddDice(yangmd5)

        res={"Slash":1.0,"Pierce":1.0,"Blunt":0.5,"Slash_s":1.0,"Pierce_s":1.0,"Blunt_s":0.5}
        super().__init__("rnfmabj",500,280,res,2,5,4,3,id,pos,"Enemy")
        self.AddPage(yangp1)#0
        self.AddPage(yangp2)#1
        self.AddPage(yangp3)#2
        self.AddPage(yangp6)#3
        self.AddPage(yangp6)#4
        self.AddPage(yangp5)#5
        self.AddPage(yangp4)#6
        self.AddPage(yangp4)#7
        self.AddPage(yangp4)#8
        self.AddPage(yangp4)#9
        self.AddPage(yangp7)#10
        self.leftHand=None
        self.rightHand=None
        self.countDown=6
        self.merged=False
        self.stage=1
        self.useAllrcv=False
        self.AddPassive(u"变幻莫测")
        self.AddPassive("rnfmabj")
        self.AddPassive(u"扭曲之刃")
    def EquipPage(self,dice,target,pageid,origin=False):
        for i in range(len(self.pages)):
            if self.pages[i].id==pageid:
                    id=i
                    break
        page=self.pages[id]
        dice.SelectPage(page)
        if page.pageType=="Melee" or page.pageType=="Ranged":
            dice.TargetPage(target)
        else:
            dice.MassTarget(target,self.againstTeam)
        if origin:
            dice.SetOrigin(target)
        return True
    def UnequipPage(self,dice):
        pass
    def RoundStart(self):
        if self.stage!=3 and self.health<300:
            if self.countDown>1:
                self.countDown=1
            if self.merged:
                lhand=LeftHand(102,2,True)
                self.leftHand=lhand
                rhand=RightHand(103,1,True)
                self.rightHand=rhand
                self.affiliateTeam.AddPerson(lhand)
                self.affiliateTeam.AddPerson(rhand)
                self.merged=False
            self.ClearStagger()
            self.stage=3
            self.pages[0].pageBuff.clashed=True
            self.pages[1].pageBuff.clashed=True
            self.pages[3].pageBuff.clashed=True
            self.pages[4].pageBuff.clashed=True
        else:
            if self.stage==1 and self.leftHand.health<=30 and self.rightHand.health<=30:
                self.stage=2
                if self.countDown>1:
                    self.countDown=1
                self.leftHand=None
                self.rightHand=None
                self.merged=True
                del self.affiliateTeam.characters[1]
                del self.affiliateTeam.characters[1]
        if self.stage==1:
            if not self.pages[0].pageBuff.clashed:
                if random.randint(1,2)==1:
                    self.leftHand.AddBuff("Strength",3) 
                else:
                    self.rightHand.AddBuff("Strength",3)
            if not self.pages[1].pageBuff.clashed:
                if random.randint(1,2)==1:
                    self.leftHand.AddBuff("Protection",3)
                else:
                    self.rightHand.AddBuff("Protection",3)
        elif self.stage==3:
            if not self.useAllrcv:
                if not self.pages[0].pageBuff.clashed:
                    if random.randint(1,2)==1:
                        self.leftHand.AddBuff("Strength",3) 
                    else:
                        self.rightHand.AddBuff("Strength",3)
                if not self.pages[1].pageBuff.clashed:
                    if random.randint(1,2)==1:
                        self.leftHand.AddBuff("Protection",3)
                    else:
                        self.rightHand.AddBuff("Protection",3)
                if not self.pages[3].pageBuff.clashed:
                    if self.leftHand.health<=self.rightHand.health:
                        self.leftHand.RecoverHealth(30,False)
                    else:
                        self.rightHand.RecoverHealth(30,False)
            else:
                if not self.pages[3].pageBuff.clashed:
                    if self.leftHand.health<=self.rightHand.health:
                        self.leftHand.RecoverHealth(30,False)
                    else:
                        self.rightHand.RecoverHealth(30,False)
                if not self.pages[4].pageBuff.clashed:
                    if self.leftHand.health<=self.rightHand.health:
                        self.leftHand.RecoverHealth(30,False)
                    else:
                        self.rightHand.RecoverHealth(30,False)    
                self.leftHand.RecoverHealth(40,False)
                self.rightHand.RecoverHealth(40,False)
            if self.leftHand.locked and self.rightHand.locked:
                self.useAllrcv=True
            else:
                self.useAllrcv=False
        if self.countDown==0:
            self.AddBuff("Yang_CountDown",2)
        else:
            self.AddBuff("Yang_CountDown",self.countDown)
        self.pages[0].pageBuff.clashed=False
        self.pages[1].pageBuff.clashed=False
        self.pages[3].pageBuff.clashed=False
        self.pages[4].pageBuff.clashed=False
    def RollPage(self):
        pass
    def RollBackPage(self):
        for dice in self.speedDices:
            if dice.havePage==True:
                dice.havePage=False
                dice.haveTarget=False
                dice.Target=None
                dice.massTarget.clear()
                dice.page=None
            dice.speed=-1
    def ClaimDeath(self,attacker,source="Person"):
        super().ClaimDeath(attacker, source)
class LeftHand(Character):
    def __init__(self,id,pos,revived=False):
        handd11=Dice(9,17,"Attack","Pierce",None,None)
        handd11.AddDiceBuff(HitDamage(5))
        handd12=Dice(5,8,"Block","Block",None,None)
        handd13=Dice(4,7,"Attack","Pierce",None,None,True)

        handd21=Dice(6,9,"Block","Block",None,None)
        handd22=Dice(6,10,"Attack","Blunt",None,None)
        handd22.AddDiceBuff(HitExertBuffs(["Paralysis"],[2]))
        handd23=Dice(4,8,"Attack","Blunt",None,None)
        handd23.AddDiceBuff(HitExertBuffs(["Feeble"],[1]))
        handd24=Dice(3,7,"Attack","Blunt",None,None,True)

        handd31=Dice(4,8,"Attack","Pierce",None,None)
        handd31.AddDiceBuff(HitDamage(3))
        handd32=Dice(4,7,"Attack","Pierce",None,None)
        handd32.AddDiceBuff(HitDamage(3))
        handd33=Dice(3,7,"Attack","Pierce",None,None)
        handd33.AddDiceBuff(HitDamage(3))

        handd41=Dice(4,8,"Attack","Slash",None,None)
        handd42=Dice(6,10,"Attack","Pierce",None,None)
        handd42.AddDiceBuff(HitExertBuffs(["Erosion"],[2],False))
        handd43=Dice(5,9,"Block","Block",None,None)

        handd51=Dice(7,9,"Block","Block",None,None)
        handd52=Dice(12,19,"Attack","Blunt",None,None)
        handd52.AddDiceBuff(WinBreakNextDice())

        handp1=Page(u"巨拳轰击","Melee",[],0,None,1,"Purple")
        handp1.AddDice(handd11)
        handp1.AddDice(handd12)
        handp1.AddCounterDice(handd13)

        handp2=Page(u"巨掌拍打","Melee",[],0,None,1,"Purple")
        handp2.AddDice(handd21)
        handp2.AddDice(handd22)
        handp2.AddDice(handd23)
        handp2.AddCounterDice(handd24)

        handp3=Page(u"乱拳痛殴","Melee",[],0,None,1,"Purple")
        handp3.AddDice(handd31)
        handp3.AddDice(handd32)
        handp3.AddDice(handd33)

        handp4=Page(u"不祥烙印","Melee",[],0,None,1,"Gold")
        handp4.AddDice(handd41)
        handp4.AddDice(handd42)
        handp4.AddDice(handd43)

        handp5=Page(u"封锁目标","Melee",[],0,None,1,"Gold")
        handp5.AddDice(handd51)
        handp5.AddDice(handd52)
        if revived:
            hl=80
        else:
            hl=200
        res={"Slash":1.0,"Pierce":0.5,"Blunt":1.0,"Slash_s":0,"Pierce_s":0,"Blunt_s":0}
        super().__init__(u"左手",200,0,res,2,7,3,3,id,pos,"Enemy")
        self.health=hl
        self.AddPage(handp1)
        self.AddPage(handp2)
        self.AddPage(handp3)
        self.AddPage(handp3)
        self.AddPage(handp4)
        self.AddPage(handp5)
        self.locked=False
        self.emotion=NoEmotion()
        self.AddPassive(u"变幻莫测")
        self.AddPassive(u"手")
    def DoStagger(self,attacker,source="Person"):
        pass
    def JudgeStagger(self):
        return False
    def JudgeDeath(self):
        for per in self.affiliateTeam.characters:
            if per.name=="rnfmabj":
                return per.JudgeDeath()
        return False
    def EquipPage(self,dice,target,pageid,origin=False):
        for i in range(len(self.pages)):
            if self.pages[i].id==pageid:
                    id=i
                    break
        page=self.pages[id]
        dice.SelectPage(page)
        if page.pageType=="Melee" or page.pageType=="Ranged":
            dice.TargetPage(target)
        else:
            dice.MassTarget(target,self.againstTeam)
        if origin:
            dice.SetOrigin(target)
        return True
    def UnequipPage(self,dice):
        pass
    def DoDamage(self,dicePoint,attackType,attacker,redcoin,isCounter=False):
        super().DoDamage(dicePoint,attackType,attacker,redcoin,isCounter)
        if self.health<1:
            self.health=1
        if self.stagger!=0:
            self.stagger=0
    def DoDamage2(self,point,source,attacker=None):
        super().DoDamage2(point,source,attacker)
        if self.health<1:
            self.health=1
    def DoStaggerDamage2(self,point,source,attacker=None):
        super().DoStaggerDamage2(point,source,attacker)
        if self.stagger!=0:
            self.stagger=0
    def RollPage(self):
        pass
    def RollBackPage(self):
        for dice in self.speedDices:
            if dice.havePage==True:
                dice.havePage=False
                dice.haveTarget=False
                dice.Target=None
                dice.massTarget.clear()
                dice.page=None
            dice.speed=-1
    def RoundStart(self):
        if self.health<=30:
            self.locked=True
        else:
            self.locked=False
class RightHand(Character):
    def __init__(self,id,pos,revived=False):
        handd11=Dice(9,17,"Attack","Pierce",None,None)
        handd11.AddDiceBuff(HitDamage(5))
        handd12=Dice(5,8,"Block","Block",None,None)
        handd13=Dice(4,7,"Attack","Pierce",None,None,True)

        handd21=Dice(6,9,"Block","Block",None,None)
        handd22=Dice(6,10,"Attack","Blunt",None,None)
        handd22.AddDiceBuff(HitExertBuffs(["Paralysis"],[2]))
        handd23=Dice(4,8,"Attack","Blunt",None,None)
        handd23.AddDiceBuff(HitExertBuffs(["Feeble"],[1]))
        handd24=Dice(3,7,"Attack","Blunt",None,None,True)

        handd31=Dice(4,8,"Attack","Pierce",None,None)
        handd31.AddDiceBuff(HitDamage(3))
        handd32=Dice(4,7,"Attack","Pierce",None,None)
        handd32.AddDiceBuff(HitDamage(3))
        handd33=Dice(3,7,"Attack","Pierce",None,None)
        handd33.AddDiceBuff(HitDamage(3))

        handd41=Dice(4,8,"Attack","Slash",None,None)
        handd42=Dice(6,10,"Attack","Pierce",None,None)
        handd42.AddDiceBuff(HitExertBuffs(["Erosion"],[2],False))
        handd43=Dice(5,9,"Block","Block",None,None)

        handd51=Dice(7,9,"Block","Block",None,None)
        handd52=Dice(12,19,"Attack","Blunt",None,None)
        handd52.AddDiceBuff(WinBreakNextDice())

        handp1=Page(u"巨拳轰击","Melee",[],0,None,1,"Purple")
        handp1.AddDice(handd11)
        handp1.AddDice(handd12)
        handp1.AddCounterDice(handd13)

        handp2=Page(u"巨掌拍打","Melee",[],0,None,1,"Purple")
        handp2.AddDice(handd21)
        handp2.AddDice(handd22)
        handp2.AddDice(handd23)
        handp2.AddCounterDice(handd24)

        handp3=Page(u"乱拳痛殴","Melee",[],0,None,1,"Purple")
        handp3.AddDice(handd31)
        handp3.AddDice(handd32)
        handp3.AddDice(handd33)

        handp4=Page(u"不祥烙印","Melee",[],0,None,1,"Gold")
        handp4.AddDice(handd41)
        handp4.AddDice(handd42)
        handp4.AddDice(handd43)

        handp5=Page(u"封锁目标","Melee",[],0,None,1,"Gold")
        handp5.AddDice(handd51)
        handp5.AddDice(handd52)
        if revived:
            hl=80
        else:
            hl=200
        res={"Slash":0.5,"Pierce":1.0,"Blunt":1.0,"Slash_s":0,"Pierce_s":0,"Blunt_s":0}
        super().__init__(u"右手",200,0,res,2,7,3,3,id,pos,"Enemy")
        self.health=hl
        self.AddPage(handp1)
        self.AddPage(handp2)
        self.AddPage(handp3)
        self.AddPage(handp3)
        self.AddPage(handp4)
        self.AddPage(handp5)
        self.locked=False
        self.emotion=NoEmotion()
        self.AddPassive(u"变幻莫测")
        self.AddPassive(u"手")
    def DoStagger(self,attacker,source="Person"):
        pass
    def JudgeStagger(self):
        return False
    def JudgeDeath(self):
        for per in self.affiliateTeam.characters:
            if per.name=="rnfmabj":
                return per.JudgeDeath()
        return False
    def EquipPage(self,dice,target,pageid,origin=False):
        for i in range(len(self.pages)):
            if self.pages[i].id==pageid:
                    id=i
                    break
        page=self.pages[id]
        dice.SelectPage(page)
        if page.pageType=="Melee" or page.pageType=="Ranged":
            dice.TargetPage(target)
        else:
            dice.MassTarget(target,self.againstTeam)
        if origin:
            dice.SetOrigin(target)
        return True
    def UnequipPage(self,dice):
        pass
    def DoDamage(self,dicePoint,attackType,attacker,redcoin,isCounter=False):
        super().DoDamage(dicePoint,attackType,attacker,redcoin,isCounter)
        if self.health<1:
            self.health=1
        if self.stagger!=0:
            self.stagger=0
    def DoDamage2(self,point,source,attacker=None):
        super().DoDamage2(point,source,attacker)
        if self.health<1:
            self.health=1
    def DoStaggerDamage2(self,point,source,attacker=None):
        super().DoStaggerDamage2(point,source,attacker)
        if self.stagger!=0:
            self.stagger=0
    def RollPage(self):
        pass
    def RollBackPage(self):
        for dice in self.speedDices:
            if dice.havePage==True:
                dice.havePage=False
                dice.haveTarget=False
                dice.Target=None
                dice.massTarget.clear()
                dice.page=None
            dice.speed=-1
    def RoundStart(self):
        if self.health<=30:
            self.locked=True
        else:
            self.locked=False