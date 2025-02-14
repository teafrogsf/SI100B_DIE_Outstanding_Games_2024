dic={"Burn":u"烧伤","Bleed":u"流血","Fairy":u"妖灵","Erosion":u"腐蚀","Strength":u"强壮","Feeble":u"虚弱","Endurance":u"忍耐","Disarm":u"破绽",
    "Haste":u"迅捷","Bind":u"束缚","Fragile":u"易损","Protection":u"守护","SProtection":u"振奋","Paralysis":u"麻痹",
    "Smoke":u"烟气","Charge":u"充能"}
import math
class PageBuff:
    def __init__(self):
        self.page=None
        self.affiliateCharacter=None
        self.special="None"
        self.desp=" "
        self.para=[]
    def StartBattle(self):
        pass
    def BeforeUse(self,target,isPage=True):
        for i in range(self.affiliateCharacter.HavePassive(u"不稳定的神采")):
            if ((isPage and target.affiliateCharacter.buffs.GetBuffCount("Burn")>0) or
                ((not isPage) and target.buffs.GetBuffCount("Burn")>0)):
                self.affiliateCharacter.AddPowerBuff("Attack",1,1,"PageBuff")
        if self.affiliateCharacter.HavePassive(u"过度呼吸")>0:
            for page in self.affiliateCharacter.pageStock:
                if page.name==self.page:
                    if page.originCost>=4:
                        self.affiliateCharacter.getLight+=2
        if self.affiliateCharacter.HavePassive(u"高难杂技")>0:
            for page in self.affiliateCharacter.pageStock:
                if page.name==self.page:
                    if page.originCost>=3:
                        self.affiliateCharacter.AddPowerBuff("Total",1,1,"PageBuff")
        if self.affiliateCharacter.HavePassive(u"血液爆炸")>0:
            for page in self.affiliateCharacter.pageStock:
                if page.name==self.page:
                    if page.originCost<=1:
                        if isPage:
                            target.affiliateCharacter.AddBuff("Bleed",3)
                        else:
                            target.AddBuff("Bleed",3)
    def AfterUse(self):
        pass
class UseGetBuffs(PageBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[使用时] 下一幕使自身获得"
        else:
            self.desp=u"[使用时] 使自身获得"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def BeforeUse(self,target,isPage=True):
        for i in range(len(self.buffs)):
            if self.isNext:
                self.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
            else:
                self.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
        super().BeforeUse(target,isPage)
class UseExertBuffs(PageBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[使用时] 下一幕中对目标施加"
        else:
            self.desp=u"[使用时] 对目标施加"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def BeforeUse(self,target,isPage=True):
        if isPage:
            for i in range(len(self.buffs)):
                if self.isNext:
                    target.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
                else:
                    target.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
        else:
            for i in range(len(self.buffs)):
                if self.isNext:
                    target.AddNextBuff(self.buffs[i],self.counts[i])
                else:
                    target.AddBuff(self.buffs[i],self.counts[i])
        super().BeforeUse(target,isPage)
class UseLight(PageBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[使用时] 回复"
        self.desp+=str(count)
        self.desp+=u"点光芒"
    def BeforeUse(self,target,isPage=True):
        self.affiliateCharacter.getLight+=self.count
        super().BeforeUse(target,isPage)
class UsePage(PageBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[使用时] 抽取"
        self.desp+=str(count)
        self.desp+=u"张书页"
    def BeforeUse(self,target,isPage=True):
        self.affiliateCharacter.rollPage+=self.count
class YangStrength(PageBuff):
    def __init__(self):
        super().__init__()
        self.clashed=False
        self.special="Yang"
        self.desp=u"若本书页未参与拼点，则下一幕中使随机一只手获得3层强壮"
class YangProtection(PageBuff):
    def __init__(self):
        super().__init__()
        self.clashed=False
        self.special="Yang"
        self.desp=u"若本书页未参与拼点，则下一幕中使随机一只手获得3层守护"
class YangNoPower(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="YangNoPower"
        self.desp=u"这一幕中使目标的骰子不受威力增减效果影响"
class YangRecover(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="Yang"
        self.desp=u"若本书页未参与拼点，则下一幕中为体力较低的手恢复30点体力"
class YangAllRecover(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="YangAllRecover"
        self.desp=u"下一幕为所有其他友军恢复40点体力"
class MyoGrass(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="MyoGrass"
        self.desp=u"[使用时] 使自身获得3层充能并恢复1点光芒"
    def BeforeUse(self,target,isPage=True):
        self.affiliateCharacter.AddBuff("Charge",3)
        self.affiliateCharacter.getLight+=1
        super().BeforeUse(target,isPage)
class ChargePower(PageBuff):
    def __init__(self,ccnt,pcnt):
        super().__init__()
        self.special="ChargePower"
        self.ccnt=ccnt
        self.pcnt=pcnt
        self.para=[ccnt,pcnt]
        self.desp=u"[使用时] 消耗"
        self.desp+=str(ccnt)
        self.desp+=u"层充能并使本书页所有骰子威力+"
        self.desp+=str(pcnt)
    def BeforeUse(self,target,isPage=True):
        if self.affiliateCharacter.buffs.GetBuffCount("Charge")>=self.ccnt:
            self.affiliateCharacter.AddBuff("Charge",-self.ccnt)
            self.affiliateCharacter.AddPowerBuff("Total",self.pcnt,self.pcnt,"PageBuff")
        super().BeforeUse(target,isPage)
class MyoPointShoot(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="MyoPointShoot"
        self.desp=u"[使用时] 若自身速度不低于6点则使本书页的所有骰子威力+2"
class SmokeEnoughPower(PageBuff):
    def __init__(self,scnt,pcnt):
        super().__init__()
        self.special="ChargePower"
        self.scnt=scnt
        self.pcnt=pcnt
        self.para=[scnt,pcnt]
        self.desp=u"[使用时] 若自身至少拥有"
        self.desp+=str(scnt)
        self.desp+=u"层烟气 则使本书页所有骰子威力+"
        self.desp+=str(pcnt)
    def BeforeUse(self,target,isPage=True):
        if self.affiliateCharacter.buffs.GetBuffCount("Smoke")>=self.scnt:
            self.affiliateCharacter.AddPowerBuff("Total",self.pcnt,self.pcnt,"PageBuff")
        super().BeforeUse(target,isPage)
class UseGetGreenCoin(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="UseGetGreenCoin"
        self.desp=u"[使用时] 使自身获得1点正面情感"
    def BeforeUse(self,target,isPage=True):
        self.affiliateCharacter.emotion.GetGreenCoin(1,False)
        super().BeforeUse(target,isPage)
class EmotionLevelDecost(PageBuff):
    def __init__(self,elv,cos):
        super().__init__()
        self.elv=elv
        self.cos=cos
        self.para=[elv,cos]
        self.special="EmotionLevelDecost"
        self.desp=u"若自身情感等级达到"
        self.desp+=str(elv)
        self.desp+=u"级则使本书页费用-"
        self.desp+=str(cos)
class EmotionPower(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="EmotionPower"
        self.desp=u"[使用时] 自身每有2级情感等级便使本书页的所有骰子威力+1"
    def BeforeUse(self,target,isPage=True):
        pw=math.floor(self.affiliateCharacter.emotion.emotionLevel/2)
        if pw>0:
            self.affiliateCharacter.AddPowerBuff("Total",pw,pw,"PageBuff")
        super().BeforeUse(target,isPage)
class RoundAttackDamageBuff(PageBuff):
    def __init__(self,cnt):
        super().__init__()
        self.special="RoundDamageBuff"
        self.cnt=cnt
        self.para=[cnt]
        self.desp=u"[战斗开始] 这一幕中使自身的进攻型骰子伤害+"
        self.desp+=str(cnt)
    def StartBattle(self):
        self.affiliateCharacter.AddDamageBuff("Attack",self.cnt,self.cnt,"roundend")
class RedMistPage(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="RedMistPage"
        self.desp="若至少造成8点伤害则抽取1张书页并使其余同名书页费用-1"
class RedMistLight(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="RedMistLight"
        self.desp="若至少造成8点伤害则恢复2点光芒并使其余同名书页费用-1"
class RedMistBreakPage(PageBuff):
    def __init__(self):
        super().__init__()
        self.special="RedMistBreakPage"
        self.desp="[使用时] 随机摧毁目标即将使用的1张书页"
    def BeforeUse(self,target,isPage=True):
        super().BeforeUse(target,isPage)
        if isPage:
            for dice in target.affiliateCharacter.speedDices:
                if not dice.havePage:
                    continue
                if dice.page.used==False:
                    for adice in dice.page.dices:
                        adice.BreakDice()
                    return 
        else:
            for dice in target.speedDices:
                if not dice.havePage:
                    continue
                if dice.page.used==False:
                    for adice in dice.page.dices:
                        adice.BreakDice()
                    return         
        
        