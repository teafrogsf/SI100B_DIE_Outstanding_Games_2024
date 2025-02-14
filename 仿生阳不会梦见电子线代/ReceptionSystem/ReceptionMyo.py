from ReceptionSystem.Page import *
from ReceptionSystem.Character import *
class Myo(Character):
    def __init__(self,id,pos):
        myodice11=Dice(3,7,"Block","Block",None,None)
        myodice12=Dice(3,4,"Attack","Pierce",None,None)

        myodice21=Dice(6,8,"Attack","Pierce",None,None)
        myodice22=Dice(5,7,"Attack","Pierce",None,None)
        myodice23=Dice(3,7,"Block","Block",None,None)

        myodice31=Dice(3,8,"Evade","Evade",None,None)
        myodice32=Dice(4,8,"Attack","Blunt",None,None)
        myodice32.AddDiceBuff(HitExertBuffs(["Bleed"],[2]))
        myodice33=Dice(3,8,"Attack","Slash",None,None)
        myodice33.AddDiceBuff(HitExertBuffs(["Bleed"],[1]))

        myodice41=Dice(8,21,"Attack","Blunt",None,None)
        myodice41.AddDiceBuff(HitExertBuffs(["Bleed"],[3]))

        myodice51=Dice(7,10,"Block","Block",None,None)
        myodice52=Dice(4,8,"Attack","Pierce",None,None)
        myodice53=Dice(4,6,"Attack","Slash",None,None)

        myodice61=Dice(4,9,"Attack","Pierce",None,None)
        myodice62=Dice(4,9,"Attack","Slash",None,None)
        myodice63=Dice(6,10,"Attack","Slash",None,None)
        myodice63.AddDiceBuff(HitDamage(15))

        myopage1=Page(u"撕咬鲜草","Melee",[],0,None,1,"Green")
        myopage1.AddPageBuff(MyoGrass())
        myopage1.AddDice(myodice11)
        myopage1.AddDice(myodice12)

        myopage2=Page(u"火力集中","Ranged",[],2,None,1,"Blue")
        myopage2.AddPageBuff(ChargePower(5,1))
        myopage2.AddDice(myodice21)
        myopage2.AddDice(myodice22)
        myopage2.AddDice(myodice23)

        myopage3=Page(u"快速压制","Melee",[],2,None,1,"Green")
        myopage3.AddPageBuff(UseGetBuffs(["Charge"],[5],False))
        myopage3.AddDice(myodice31)
        myopage3.AddDice(myodice32)
        myopage3.AddDice(myodice33)

        myopage4=Page(u"单点射击","Ranged",[],3,None,1,"Green")
        myopage4.AddPageBuff(MyoPointShoot())
        myopage4.AddDice(myodice41)

        myopage5=Page(u"心神凝聚","Melee",[],3,None,1,"Blue")
        myopage5.AddPageBuff(UseGetBuffs(["Charge"],[8],False))
        myopage5.AddDice(myodice51)
        myopage5.AddDice(myodice52)
        myopage5.AddDice(myodice53)

        myopage6=Page(u"狂暴血刃","Individual",[],5,None,1,"Gold")
        myopage6.charge=True
        myopage6.AddDice(myodice61)
        myopage6.AddDice(myodice62)
        myopage6.AddDice(myodice63)

        res={"Slash":1.0,"Pierce":1.0,"Blunt":0.5,"Slash_s":1.0,"Pierce_s":1.0,"Blunt_s":0.5}
        super().__init__(u"缪",200,100,res,2,7,1,4,id,pos,"Enemy")
        self.AddPage(myopage1)
        self.AddPage(myopage1)
        self.AddPage(myopage1)
        self.AddPage(myopage2)
        self.AddPage(myopage3)
        self.AddPage(myopage3)
        self.AddPage(myopage5)
        self.AddPage(myopage5)
        self.AddPage(myopage6)
        self.AddPassive(u"速战速决3")
        self.AddPassive(u"Rabbit改造手术")
        self.AddPassive(u"刺激充能压缩肌肉")
        self.AddPassive(u"缪的技巧")
class Rabbit(Character):
    def __init__(self,id,pos):
        res={"Slash":0.5,"Pierce":1.0,"Blunt":1.0,"Slash_s":1.0,"Pierce_s":1.0,"Blunt_s":1.0}
        super().__init__(u"兔子",150,75,res,2,6,1,3,id,pos,"Enemy")
        myodice11=Dice(3,7,"Block","Block",None,None)
        myodice12=Dice(3,4,"Attack","Pierce",None,None)

        myodice21=Dice(6,8,"Attack","Pierce",None,None)
        myodice22=Dice(5,7,"Attack","Pierce",None,None)
        myodice23=Dice(3,7,"Block","Block",None,None)

        myodice31=Dice(3,8,"Evade","Evade",None,None)
        myodice32=Dice(4,8,"Attack","Blunt",None,None)
        myodice32.AddDiceBuff(HitExertBuffs(["Bleed"],[2]))
        myodice33=Dice(3,8,"Attack","Slash",None,None)
        myodice33.AddDiceBuff(HitExertBuffs(["Bleed"],[1]))

        myodice41=Dice(8,21,"Attack","Blunt",None,None)
        myodice41.AddDiceBuff(HitExertBuffs(["Bleed"],[3]))

        myopage1=Page(u"撕咬鲜草","Melee",[],0,None,1,"Green")
        myopage1.AddPageBuff(MyoGrass())
        myopage1.AddDice(myodice11)
        myopage1.AddDice(myodice12)

        myopage2=Page(u"火力集中","Ranged",[],2,None,1,"Blue")
        myopage2.AddPageBuff(ChargePower(5,1))
        myopage2.AddDice(myodice21)
        myopage2.AddDice(myodice22)
        myopage2.AddDice(myodice23)

        myopage3=Page(u"快速压制","Melee",[],2,None,1,"Green")
        myopage3.AddPageBuff(UseGetBuffs(["Charge"],[5],False))
        myopage3.AddDice(myodice31)
        myopage3.AddDice(myodice32)
        myopage3.AddDice(myodice33)

        myopage4=Page(u"单点射击","Ranged",[],3,None,1,"Green")
        myopage4.AddPageBuff(MyoPointShoot())
        myopage4.AddDice(myodice41)
        self.AddPage(myopage1)
        self.AddPage(myopage1)
        self.AddPage(myopage1)
        self.AddPage(myopage2)
        self.AddPage(myopage2)
        self.AddPage(myopage2)
        self.AddPage(myopage3)
        self.AddPage(myopage3)
        self.AddPage(myopage4)
        self.AddPassive(u"速战速决")
        self.AddPassive(u"Rabbit改造手术")
        self.AddPassive(u"刺激充能压缩肌肉")