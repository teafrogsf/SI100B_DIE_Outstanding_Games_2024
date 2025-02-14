from ReceptionSystem.Page import *
from ReceptionSystem.Character import *
class Yae(Character):
    def __init__(self,id,pos):
        leafdice11=Dice(2,6,"Attack","Blunt",None,None)
        leafdice12=Dice(2,3,"Attack","Slash",None,None)

        leafdice21=Dice(4,8,"Block","Block",None,None)
        leafdice22=Dice(5,8,"Attack","Blunt",None,None)
        leafdice22.AddDiceBuff(HitExertBuffs(["Smoke"],[3]))

        leafdice31=Dice(4,8,"Evade","Evade",None,None)
        leafdice32=Dice(6,9,"Attack","Slash",None,None)
        leafdice32.AddDiceBuff(HitExertBuffs(["Smoke"],[2]))

        leafdice41=Dice(3,7,"Block","Block",None,None)
        leafdice42=Dice(3,8,"Attack","Blunt",None,None)
        leafdice42.AddDiceBuff(HitExertBuffs(["Smoke"],[3]))
        leafdice43=Dice(4,8,"Attack","Pierce",None,None)
        leafdice43.AddDiceBuff(HitExertBuffs(["Smoke"],[2]))

        leafpage1=Page(u"使用示范","Melee",[],0,None,1,"Green")
        leafpage1.AddPageBuff(UseGetBuffs(["Smoke"],[3]))
        leafpage1.AddDice(leafdice11)
        leafpage1.AddDice(leafdice12)

        leafpage2=Page(u"烟锤猛击","Melee",[],0,None,1,"Green")
        leafpage2.AddPageBuff(UseGetBuffs(["Smoke"],[3]))
        leafpage2.AddDice(leafdice21)
        leafpage2.AddDice(leafdice22)

        leafpage3=Page(u"烟锤袭击","Melee",[],1,None,1,"Blue")
        leafpage3.AddPageBuff(SmokeEnoughPower(9,2))
        leafpage3.AddDice(leafdice31)
        leafpage3.AddDice(leafdice32)

        leafpage4=Page(u"烟锤冲击","Melee",[],2,None,1,"Purple")
        leafpage4.AddPageBuff(UseGetBuffs(["Smoke"],[3]))
        leafpage4.AddDice(leafdice41)
        leafpage4.AddDice(leafdice42)
        leafpage4.AddDice(leafdice43)

        leafdice51=Dice(7,12,"Attack","Blunt",None,None)
        leafdice51.AddDiceBuff(SmokeEnoughExertBuffs(5,["Paralysis"],[5]))
        leafdice52=Dice(4,8,"Block","Block",None,None)
        leafdice53=Dice(4,8,"Attack","Pierce",None,None)
        leafpage5=Page(u"浓烟喷射","Melee",[],3,None,1,"Gold")
        leafpage5.AddPageBuff(UseGetBuffs(["Smoke"],[8]))
        leafpage5.AddDice(leafdice51)
        leafpage5.AddDice(leafdice52)
        leafpage5.AddDice(leafdice53)

        res={"Slash":1.0,"Pierce":0.5,"Blunt":1.0,"Slash_s":0.5,"Pierce_s":1.0,"Blunt_s":1.0}
        super().__init__(u"八重",150,75,res,2,6,1,3,id,pos,"Enemy")
        self.used=False
        self.AddPage(leafpage1)
        self.AddPage(leafpage1)
        self.AddPage(leafpage2)
        self.AddPage(leafpage2)
        self.AddPage(leafpage3)
        self.AddPage(leafpage3)
        self.AddPage(leafpage4)
        self.AddPage(leafpage4)
        self.AddPage(leafpage5)
        self.AddPassive(u"速战速决3")
        self.AddPassive(u"烟气缭绕")
        self.AddPassive(u"烟气过度")
        self.AddPassive(u"供应过剩")
        self.AddPassive(u"现场修整")
        self.AddPassive(u"走火入魔")
    def DoStagger(self,attacker,source="Person"):
        if self.used:
            return super().DoStagger(attacker, source)
        else:
            self.used=True
            self.stagger=self.staggerMax
class LeafFixer(Character):
    def __init__(self,id,pos):
        leafdice11=Dice(2,6,"Attack","Blunt",None,None)
        leafdice12=Dice(2,3,"Attack","Slash",None,None)

        leafdice21=Dice(4,8,"Block","Block",None,None)
        leafdice22=Dice(5,8,"Attack","Blunt",None,None)
        leafdice22.AddDiceBuff(HitExertBuffs(["Smoke"],[3]))

        leafdice31=Dice(4,8,"Evade","Evade",None,None)
        leafdice32=Dice(6,9,"Attack","Slash",None,None)
        leafdice32.AddDiceBuff(HitExertBuffs(["Smoke"],[2]))

        leafdice41=Dice(3,7,"Block","Block",None,None)
        leafdice42=Dice(3,8,"Attack","Blunt",None,None)
        leafdice42.AddDiceBuff(HitExertBuffs(["Smoke"],[3]))
        leafdice43=Dice(4,8,"Attack","Pierce",None,None)
        leafdice43.AddDiceBuff(HitExertBuffs(["Smoke"],[2]))

        leafpage1=Page(u"使用示范","Melee",[],0,None,1,"Green")
        leafpage1.AddPageBuff(UseGetBuffs(["Smoke"],[3]))
        leafpage1.AddDice(leafdice11)
        leafpage1.AddDice(leafdice12)

        leafpage2=Page(u"烟锤猛击","Melee",[],0,None,1,"Green")
        leafpage2.AddPageBuff(UseGetBuffs(["Smoke"],[3]))
        leafpage2.AddDice(leafdice21)
        leafpage2.AddDice(leafdice22)

        leafpage3=Page(u"烟锤袭击","Melee",[],1,None,1,"Blue")
        leafpage3.AddPageBuff(SmokeEnoughPower(9,2))
        leafpage3.AddDice(leafdice31)
        leafpage3.AddDice(leafdice32)

        leafpage4=Page(u"烟锤冲击","Melee",[],2,None,1,"Purple")
        leafpage4.AddPageBuff(UseGetBuffs(["Smoke"],[3]))
        leafpage4.AddDice(leafdice41)
        leafpage4.AddDice(leafdice42)
        leafpage4.AddDice(leafdice43)

        res={"Slash":1.0,"Pierce":0.5,"Blunt":1.0,"Slash_s":0.5,"Pierce_s":1.0,"Blunt_s":1.0}
        super().__init__(u"叶工坊收尾人",150,75,res,2,6,1,3,id,pos,"Enemy")
        self.AddPage(leafpage1)
        self.AddPage(leafpage1)
        self.AddPage(leafpage1)
        self.AddPage(leafpage2)
        self.AddPage(leafpage2)
        self.AddPage(leafpage3)
        self.AddPage(leafpage3)
        self.AddPage(leafpage4)
        self.AddPage(leafpage4)
        self.AddPassive(u"速战速决")
        self.AddPassive(u"烟气缭绕")
        self.AddPassive(u"烟气过度")
        self.AddPassive(u"供应过剩")