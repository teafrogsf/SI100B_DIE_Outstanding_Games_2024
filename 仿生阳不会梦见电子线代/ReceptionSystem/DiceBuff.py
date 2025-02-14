dic={"Burn":u"烧伤","Bleed":u"流血","Fairy":u"妖灵","Erosion":u"腐蚀","Strength":u"强壮","Feeble":u"虚弱","Endurance":u"忍耐","Disarm":u"破绽",
    "Haste":u"迅捷","Bind":u"束缚","Fragile":u"易损","Protection":u"守护","SProtection":u"振奋","Paralysis":u"麻痹",
    "Smoke":u"烟气","Charge":u"充能"}
import math
class DiceBuff:
    def __init__(self):
        self.dice=None
        self.affiliateCharacter=None
        self.desp=" "
        self.para=[]
    def BeforeAttack(self,target):
        pass
    def BeforeClash(self,target):
        pass
    def ClashWin(self,target):
        for i in range(self.affiliateCharacter.HavePassive(u"调整呼吸")):
            self.affiliateCharacter.RecoverHealth(1)
        pass
    def ClashLose(self,target):
        pass
    def Strike(self,target,isDice=True):
        for i in range(self.affiliateCharacter.HavePassive(u"创口雕琢")):
            if (isDice and target.affiliateCharacter.buffs.GetBuffCount("Bleed")>0):
                target.affiliateCharacter.buffs.UseAttackDice()
            if((not isDice) and target.buffs.GetBuffCount("Bleed")>0):
                target.buffs.UseAttackDice()
        for i in range(self.affiliateCharacter.HavePassive(u"血肉回收")):
            self.affiliateCharacter.RecoverHealth(2)
        for i in range(self.affiliateCharacter.HavePassive(u"精神回收")):
            self.affiliateCharacter.RecoverStagger(2)
        for i in range(self.affiliateCharacter.HavePassive(u"血魔之力")):
            self.affiliateCharacter.RecoverHealth(2)
        for i in range(self.affiliateCharacter.HavePassive(u"血液吸收")):
            if (isDice and target.affiliateCharacter.buffs.GetBuffCount("Bleed")>0):
                self.affiliateCharacter.RecoverHealth(math.floor(target.affiliateCharacter.buffs.GetBuffCount("Bleed")/2.0))
            if((not isDice) and target.buffs.GetBuffCount("Bleed")>0):
                self.affiliateCharacter.RecoverHealth(math.floor(target.buffs.GetBuffCount("Bleed")/2.0))
        pass
class HitGetBuffs(DiceBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[命中时] 下一幕使自身获得"
        else:
            self.desp=u"[命中时] 使自身获得"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        for i in range(len(self.buffs)):
            if self.isNext:
                self.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
            else:
                self.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
class HitExertBuffs(DiceBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[命中时] 下一幕中对目标施加"
        else:
            self.desp=u"[命中时] 对目标施加"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        if isDice:
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
class WinGetBuffs(DiceBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[拼点胜利时] 下一幕使自身获得"
        else:
            self.desp=u"[拼点胜利时] 使自身获得"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def ClashWin(self,target):
        super().ClashWin(target)
        for i in range(len(self.buffs)):
            if self.isNext:
                self.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
            else:
                self.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
class WinExertBuffs(DiceBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[拼点胜利时] 下一幕中对目标施加"
        else:
            self.desp=u"[拼点胜利时] 对目标施加"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def ClashWin(self,target):
        super().ClashWin(target)
        for i in range(len(self.buffs)):
            if self.isNext:
                target.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
            else:
                target.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
class LoseGetBuffs(DiceBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[拼点失败时] 下一幕使自身获得"
        else:
            self.desp=u"[拼点失败时] 使自身获得"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def ClashLose(self,target):
        for i in range(len(self.buffs)):
            if self.isNext:
                self.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
            else:
                self.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
class LoseExertBuffs(DiceBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[拼点失败时] 下一幕中对目标施加"
        else:
            self.desp=u"[拼点失败时] 对目标施加"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def ClashLose(self,target):
        for i in range(len(self.buffs)):
            if self.isNext:
                target.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
            else:
                target.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
class HitDamage(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[命中时] 追加"
        self.desp+=str(count)
        self.desp+=u"点伤害"
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        if isDice:
            target.affiliateCharacter.DoDamage2(self.count,"Person",self.affiliateCharacter)
        else :
            print("DEBUG   SHIT")
            target.DoDamage2(self.count,"Person",self.affiliateCharacter)
class HitStaggerDamage(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[命中时] 追加"
        self.desp+=str(count)
        self.desp+=u"点混乱伤害"
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        if isDice:
            target.affiliateCharacter.DoStaggerDamage2(self.count,"Person",self.affiliateCharacter)
        else:
            target.DoStaggerDamage2(self.count,"Person",self.affiliateCharacter)
class HitRecover(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[命中时] 恢复"
        self.desp+=str(count)
        self.desp+=u"点体力"
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        self.affiliateCharacter.RecoverHealth(self.count)
class HitRecoverStagger(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[命中时] 恢复"
        self.desp+=str(count)
        self.desp+=u"点混乱抗性"
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        self.affiliateCharacter.RecoverStagger(self.count)
class HitLight(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[命中时] 回复"
        self.desp+=str(count)
        self.desp+=u"点光芒"
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        self.affiliateCharacter.getLight+=self.count
class WinLight(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[拼点胜利时] 回复"
        self.desp+=str(count)
        self.desp+=u"点光芒"
    def ClashWin(self,target):
        super().ClashWin(target)
        self.affiliateCharacter.getLight+=self.count
class HitPage(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[命中时] 抽取"
        self.desp+=str(count)
        self.desp+=u"张书页"
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        self.affiliateCharacter.rollPage+=self.count
class WinPage(DiceBuff):
    def __init__(self,count):
        super().__init__()
        self.count=count
        self.para=[count]
        self.desp=u"[拼点胜利时] 抽取"
        self.desp+=str(count)
        self.desp+=u"张书页"
    def ClashWin(self,target):
        super().ClashWin(target)
        self.affiliateCharacter.rollPage+=self.count
class WinBreakNextDice(DiceBuff):
    def __init__(self):
        super().__init__()
        self.desp=u"[拼点胜利时] 摧毁目标书页中的下一颗骰子"
    def ClashWin(self,target):
        page=target.affiliatePage
        flg=0
        for dice in page.dices:
            if not dice.broken:
                if flg==0:
                    flg=1
                else:
                    dice.BreakDice()
                    break
class MassHitExertBuffs(DiceBuff):
    def __init__(self,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.para=[buffs,counts,isNext]
        if isNext:
            self.desp=u"[命中时] 下一幕中对目标施加"
        else:
            self.desp=u"[命中时] 对目标施加"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def Strike(self,target,isDice=False):
        if not isDice:
            for i in range(len(self.buffs)):
                if self.isNext:
                    target.AddNextBuff(self.buffs[i],self.counts[i])
                else:
                    target.AddBuff(self.buffs[i],self.counts[i])
        else:
            for i in range(len(self.buffs)):
                if self.isNext:
                    target.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
                else:
                    target.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
class SmokeEnoughExertBuffs(DiceBuff):
    def __init__(self,scnt,buffs,counts,isNext=True):
        super().__init__()
        self.buffs=buffs
        self.counts=counts
        self.isNext=isNext
        self.scnt=scnt
        self.para=[scnt,buffs,counts,isNext]
        self.desp=u"[命中时] 若目标至少拥有"+str(scnt)
        if isNext:
            self.desp+=u"层烟气 则下一幕中对其施加"
        else:
            self.desp+=u"层烟气 则对其施加"
        for i in range(len(buffs)):
            if i!=0:
                self.desp=self.desp+","
            self.desp+=str(counts[i])
            self.desp+=u"层"
            self.desp+=dic[buffs[i]]
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        if isDice:
            if target.affiliateCharacter.buffs.GetBuffCount("Smoke")<self.scnt:
                return
            for i in range(len(self.buffs)):
                if self.isNext:
                    target.affiliateCharacter.AddNextBuff(self.buffs[i],self.counts[i])
                else:
                    target.affiliateCharacter.AddBuff(self.buffs[i],self.counts[i])
        else:
            if target.buffs.GetBuffCount("Smoke")<self.scnt:
                return
            for i in range(len(self.buffs)):
                if self.isNext:
                    target.AddNextBuff(self.buffs[i],self.counts[i])
                else:
                    target.AddBuff(self.buffs[i],self.counts[i])
class HitExertEmotionBuff(DiceBuff):
    def __init__(self,buff,isNext=True):
        super().__init__()
        self.buff=buff
        self.isNext=isNext
        self.para=[buff,isNext]
        if isNext:
            self.desp=u"[命中时] 下一幕中对目标施加(自身情感等级+1)层"
        else:
            self.desp=u"[命中时] 对目标施加(自身情感等级+1)层"
        self.desp+=dic[buff]
    def Strike(self,target,isDice=True):
        super().Strike(target,isDice)
        cnt=self.affiliateCharacter.emotion.emotionLevel+1
        if isDice:
            if self.isNext:
                target.affiliateCharacter.AddNextBuff(self.buff,cnt)
            else:
                target.affiliateCharacter.AddBuff(self.buff,cnt)
        else:
            if self.isNext:
                target.AddNextBuff(self.buff,cnt)
            else:
                target.AddBuff(self.buff,cnt)
class ReduceDefensePower(DiceBuff):
    def __init__(self,cnt):
        super().__init__()
        self.cnt=cnt
        self.para=[cnt]
        self.desp=u"若目标使用防御型骰子则使其威力-"
        self.desp+=str(cnt)
    def BeforeClash(self,target):
        target.tmpBuff-=self.cnt