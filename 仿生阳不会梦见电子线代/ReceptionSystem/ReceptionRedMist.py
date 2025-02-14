from ReceptionSystem.Page import *
from ReceptionSystem.Character import *
class RedMist(Character):
    def __init__(self,id,pos):
        reddice11=Dice(6,10,"Attack","Slash",None,None)
        reddice11.AddDiceBuff(HitExertBuffs(["Bleed"],[1]))
        reddice12=Dice(6,9,"Attack","Slash",None,None)
        reddice12.AddDiceBuff(HitExertBuffs(["Bleed"],[1]))
        redpage1=Page(u"大刀纵劈","Melee",[],2,None,1,"Green")
        redpage1.AddPageBuff(RedMistPage())
        redpage1.AddDice(reddice11)
        redpage1.AddDice(reddice12)

        reddice21=Dice(3,8,"Attack","Pierce",None,None)
        reddice21.AddDiceBuff(HitExertBuffs(["Bleed"],[1]))
        reddice22=Dice(3,7,"Attack","Pierce",None,None)
        reddice22.AddDiceBuff(HitExertBuffs(["Bleed"],[1]))
        reddice23=Dice(3,7,"Attack","Pierce",None,None)
        reddice23.AddDiceBuff(HitExertBuffs(["Bleed"],[1]))
        redpage2=Page(u"大刀直刺","Melee",[],2,None,1,"Green")
        redpage2.AddPageBuff(RedMistPage())
        redpage2.AddDice(reddice21)
        redpage2.AddDice(reddice22)
        redpage2.AddDice(reddice23)

        reddice31=Dice(5,9,"Attack","Blunt",None,None)
        reddice31.AddDiceBuff(HitExertBuffs(["Bleed"],[3]))
        reddice32=Dice(5,8,"Attack","Blunt",None,None)
        reddice32.AddDiceBuff(HitExertBuffs(["Bleed"],[3]))
        redpage3=Page(u"大刀横斩","Melee",[],2,None,1,"Green")
        redpage3.AddPageBuff(RedMistLight())
        redpage3.AddDice(reddice31)
        redpage3.AddDice(reddice32)

        reddice41=Dice(8,12,"Block","Block",None,None)
        reddice42=Dice(5,7,"Attack","Slash",None,None)
        reddice42.AddDiceBuff(HitGetBuffs(["Strength"],[3]))
        redpage4=Page(u"屏息凝神","Melee",[],2,None,1,"Purple")
        redpage4.AddDice(reddice41)
        redpage4.AddDice(reddice42)

        reddice51=Dice(20,39,"Attack","Slash",None,None)
        reddice51.AddDiceBuff(HitExertBuffs(["Bleed"],[3]))
        redpage5=Page(u"血雾弥漫","Melee",[],5,None,1,"Gold")
        redpage5.AddPageBuff(RedMistBreakPage())
        redpage5.AddDice(reddice51)

        reddice61=Dice(28,42,"Attack","Slash",None,None)
        reddice61.AddDiceBuff(MassHitExertBuffs(["Bleed"],[5]))
        redpage6=Page(u"尸横遍野","Summation",[],6,None,1,"Gold")
        redpage6.AddDice(reddice61)
        self.egoPage=redpage6

        res={"Slash":1.0,"Pierce":1.0,"Blunt":0.5,"Slash_s":1.0,"Pierce_s":1.0,"Blunt_s":0.5}
        super().__init__(u"卡莉",700,270,res,1,7,2,6,id,pos,"Enemy")
        self.AddPage(redpage1)
        self.AddPage(redpage1)
        self.AddPage(redpage1)
        self.AddPage(redpage2)
        self.AddPage(redpage2)
        self.AddPage(redpage3)
        self.AddPage(redpage3)
        self.AddPage(redpage4)
        self.AddPage(redpage5)
        self.AddPassive(u"卡莉")
        self.AddPassive(u"后发制敌")
        self.AddPassive(u"最强之人")
        self.ego=False
        self.egod=False
        self.countDown=0
    def RoundStart(self):
        super().RoundStart()
        res1={"Slash":1.0,"Pierce":0.5,"Blunt":0.5,"Slash_s":1.0,"Pierce_s":0.5,"Blunt_s":0.5}
        res2={"Slash":0.5,"Pierce":1.0,"Blunt":0.5,"Slash_s":0.5,"Pierce_s":1.0,"Blunt_s":0.5}
        res3={"Slash":0.5,"Pierce":0.5,"Blunt":1.0,"Slash_s":0.5,"Pierce_s":0.5,"Blunt_s":1.0}
        if self.health<=350 and not self.ego and not self.egod:
            self.ego=True
            self.egod=True
            self.isStagger=0
            self.AddPassive(u"殷红迷雾")
            self.AddPowerBuff("Total",2,2,"Ego")
            self.ClearStagger()
            self.AddPage(self.egoPage)
        if self.JudgeStagger():
            self.ClearPowerBuff("Ego")
            self.AddBuff("BloodMist",-5)
            self.ego=False
            self.resistance=self.originResistance
        if self.ego:
            x=random.randint(1,3)
            if x==1:
                self.resistance=res1
            elif x==2:
                self.resistance=res2
            else:
                self.resistance=res3
        self.RollPage()
    def RoundEnd(self):
        if self.JudgeDeath():
            return 
        if self.countDown>0:
            self.countDown-=1
        if self.passiveDit["TotalDamage"]<40 and self.ego:
            self.DoStaggerDamage2(int(self.staggerMax*0.4),"Passive")