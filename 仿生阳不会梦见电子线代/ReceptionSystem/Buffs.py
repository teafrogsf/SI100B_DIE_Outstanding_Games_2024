import random
import math
class SpeedBuff:
    def __init__(self,tag):
        self.speedBuff=(0,0)
        self.tag=tag
class SpeedBuffs:
    def __init__(self):
        self.speedBuff=[]
    def CalcSpeed(self):
        tl,tr=0,0
        for tp in self.speedBuff:
            tl+=tp.speedBuff[0]
            tr+=tp.speedBuff[1]
        return (tl,tr)
    def ClearBuff(self,tag):
        i=0
        while i<len(self.speedBuff):
            if self.speedBuff[i].tag==tag:
                del self.speedBuff[i]
            else:
                i+=1
class PowerBuff:
    def __init__(self,tag):
        self.powerBuff={"Slash":(0,0),"Pierce":(0,0),"Blunt":(0,0),
                        "Block":(0,0),"Evade":(0,0),
                        "Attack":(0,0),"Defense":(0,0),
                        "Counter":(0,0),
                        "Total":(0,0)}
        self.powerLR=(0,0)
        self.tag=tag
class PowerBuffs:
    def __init__(self):
        self.powerBuff=[]
        self.powerLR=[]
    def CalcPowerBuff(self):
        dic={"Slash":0,"Pierce":0,"Blunt":0,
            "Block":0,"Evade":0,
            "Attack":0,"Defense":0,
            "Counter":0,
            "Total":0}
        if len(self.powerBuff)==0:
            return dic
        else:
            for key in self.powerBuff[0].powerBuff.keys():
                for j in range(len(self.powerBuff)):
                    dic[key]+=random.randint(self.powerBuff[j].powerBuff[key][0],self.powerBuff[j].powerBuff[key][1])
            return dic
    def CalcPowerLR(self):
        tl,tr=0,0
        for tp in self.powerLR:
            tl+=tp.powerLR[0]
            tr+=tp.powerLR[1]
        return (tl,tr)
    def ClearBuff(self,tag):
        i=0
        while i<len(self.powerBuff):
            if self.powerBuff[i].tag==tag:
                del self.powerBuff[i]
            else:
                i+=1
        i=0
        while i<len(self.powerLR):
            if self.powerLR[i].tag==tag:
                del self.powerLR[i]
            else:
                i+=1
class DamageBuff:
    def __init__(self,tag):
        self.damageBuff={"Slash":(0,0),"Pierce":(0,0),"Blunt":(0,0),
                        "Block":(0,0),"Evade":(0,0),
                        "Attack":(0,0),"Defense":(0,0),
                        "Counter":(0,0),
                        "Total":(0,0)}
        self.damagePer={"Slash":0.0,"Pierce":0.0,"Blunt":0.0,
                        "Block":0.0,"Evade":0.0,
                        "Attack":0.0,"Defense":0.0,
                        "Counter":0.0,
                        "Total":0.0}
        self.getdamageBuff={"Slash":(0,0),"Pierce":(0,0),"Blunt":(0,0),
                        "Block":(0,0),"Evade":(0,0),
                        "Attack":(0,0),"Defense":(0,0),
                        "Counter":(0,0),
                        "Total":(0,0)}   
        self.getdamagePer={"Slash":0.0,"Pierce":0.0,"Blunt":0.0,
                        "Block":0.0,"Evade":0.0,
                        "Attack":0.0,"Defense":0.0,
                        "Counter":0.0,
                        "Total":0.0}
        self.getdamage=0.0
        self.tag=tag
class DamageBuffs:
    def __init__(self):
        self.damageBuff=[]
        self.damagePer=[]
        self.getdamageBuff=[]
        self.getdamagePer=[]
        self.getdamage=[]
    def CalcDamageBuff(self):
        dic={"Slash":0,"Pierce":0,"Blunt":0,
            "Block":0,"Evade":0,
            "Attack":0,"Defense":0,
            "Counter":0,
            "Total":0}
        if len(self.damageBuff)==0:
            return dic
        else:
            for key in self.damageBuff[0].damageBuff.keys():
                for j in range(len(self.damageBuff)):
                    dic[key]+=random.randint(self.damageBuff[j].damageBuff[key][0],self.damageBuff[j].damageBuff[key][1])
            return dic
    def CalcGetDamageBuff(self):
        dic={"Slash":0,"Pierce":0,"Blunt":0,
            "Block":0,"Evade":0,
            "Attack":0,"Defense":0,
            "Counter":0,
            "Total":0}
        if len(self.getdamageBuff)==0:
            return dic
        else:
            for key in self.getdamageBuff[0].getdamageBuff.keys():
                for j in range(len(self.getdamageBuff)):
                    dic[key]+=random.randint(self.getdamageBuff[j].getdamageBuff[key][0],self.getdamageBuff[j].getdamageBuff[key][1])
            return dic
    def CalcDamagePer(self):
        dic={"Slash":0.0,"Pierce":0.0,"Blunt":0.0,
            "Block":0.0,"Evade":0.0,
            "Attack":0.0,"Defense":0.0,
            "Counter":0.0,
            "Total":0.0}
        if len(self.damagePer)==0:
            return dic
        else:
            for key in self.damagePer[0].damagePer.keys():
                for j in range(len(self.damagePer)):
                    dic[key]+=self.damagePer[j].damagePer[key]
            return dic
    def CalcGetDamagePer(self):
        dic={"Slash":0.0,"Pierce":0.0,"Blunt":0.0,
            "Block":0.0,"Evade":0.0,
            "Attack":0.0,"Defense":0.0,
            "Counter":0.0,
            "Total":0.0}
        if len(self.getdamagePer)==0:
            return dic
        else:
            for key in self.getdamagePer[0].getdamagePer.keys():
                for j in range(len(self.getdamagePer)):
                    dic[key]+=self.getdamagePer[j].getdamagePer[key]
            return dic
    def CalcGetDamage(self):
        pt=0.0
        for i in self.getdamage:
            pt+=i.getdamage
        return pt
    def ClearBuff(self,tag):
        i=0
        while i<len(self.damageBuff):
            if self.damageBuff[i].tag==tag:
                del self.damageBuff[i]
            else:
                i+=1
        i=0
        while i<len(self.damagePer):
            if self.damagePer[i].tag==tag:
                del self.damagePer[i]
            else:
                i+=1
        i=0
        while i<len(self.getdamageBuff):
            if self.getdamageBuff[i].tag==tag:
                del self.getdamageBuff[i]
            else:
                i+=1
        i=0
        while i<len(self.getdamagePer):
            if self.getdamagePer[i].tag==tag:
                del self.getdamagePer[i]
            else:
                i+=1
        i=0
        while i<len(self.getdamage):
            if self.getdamage[i].tag==tag:
                del self.getdamage[i]
            else:
                i+=1
class DamageBuffss:
    def __init__(self):
        self.damageBuff=DamageBuffs()
        self.SdamageBuff=DamageBuffs()
    def ClearBuff(self,tag):
        self.damageBuff.ClearBuff(tag)
        self.SdamageBuff.ClearBuff(tag)
class Buff:
    def __init__(self,name,limit=-1):
        self.count=0
        self.affiliateCharacter=None
        self.affiliateList=None
        self.name=name
        self.limit=limit
    def AddCount(self,num):
        self.count+=num
        if self.count<=0:
            self.DelBuff()
        if self.limit!=-1 and self.count>self.limit:
            self.count=self.limit
    def ChangeCountDown(self,mul):
        self.count=math.floor(self.count*mul)
        if self.count<=0:
            self.DelBuff()
        if self.limit!=-1 and self.count>self.limit:
            self.count=self.limit
    def ChangeCountUp(self,mul):
        self.count=math.ceil(self.count*mul)
    def RoundStart(self):
        pass
    def UseAttackDice(self):
        pass
    def UseDice(self):
        pass
    def GetDamage(self):
        pass
    def RoundEnd(self):
        self.DelBuff()
    def DelBuff(self):
        self.affiliateList.DelBuff(self.name)
class Burn(Buff):
    def __init__(self):
        super().__init__("Burn")
    def RoundEnd(self):
        if not self.affiliateCharacter.HavePassive(u"蚣蝮避水")>0:
            self.affiliateCharacter.DoDamage2(self.count,self.name)
            if self.affiliateCharacter.passiveDit["Burnt"]:
                self.affiliateCharacter.DoStaggerDamage2(self.count//2,self.name)
        super().ChangeCountDown(2/3)
class Bleed(Buff):
    def __init__(self):
        super().__init__("Bleed")
    def UseAttackDice(self):
        self.affiliateCharacter.DoDamage2(self.count,self.name)
        super().ChangeCountUp(2/3)
class Fairy(Buff):#妖灵
    def __init__(self):
        super().__init__("Fairy")
    def UseDice(self):
        self.affiliateCharacter.DoDamage2(self.count,self.name)
    def RoundEnd(self):
        self.affiliateCharacter.DoDamage2(self.count,self.name)
        super().ChangeCountDown(1/2)
class Erosion(Buff):#腐蚀
    def __init__(self):
        super().__init__("Erosion")
    def GetDamage(self):
        self.affiliateCharacter.DoDamage2(self.count,self.name)
        self.affiliateCharacter.DoStaggerDamage2(self.count,self.name)
    def RoundEnd(self):
        self.affiliateCharacter.DoDamage2(self.count,self.name)
        super().AddCount(-1)
class Strength(Buff):#强壮
    def __init__(self):
        super().__init__("Strength")
    def RoundStart(self):
        self.affiliateCharacter.AddPowerBuff("Attack",self.count,self.count,"Strength")
    def RoundEnd(self):
        self.affiliateCharacter.ClearPowerBuff("Strength")
        super().RoundEnd()
class Feeble(Buff):#虚弱
    def __init__(self):
        super().__init__("Feeble")
    def RoundStart(self):
        self.affiliateCharacter.AddPowerBuff("Attack",-self.count,-self.count,"Feeble")
    def RoundEnd(self):
        self.affiliateCharacter.ClearPowerBuff("Feeble")
        super().RoundEnd()
class Endurance(Buff):#坚韧
    def __init__(self):
        super().__init__("Endurance")
    def RoundStart(self):
        self.affiliateCharacter.AddPowerBuff("Defense",self.count,self.count,"Endurance")
    def RoundEnd(self):
        self.affiliateCharacter.ClearPowerBuff("Endurance")
        super().RoundEnd()
class Disarm(Buff):#破绽
    def __init__(self):
        super().__init__("Disarm")
    def RoundStart(self):
        self.affiliateCharacter.AddPowerBuff("Defense",-self.count,-self.count,"Disarm")
    def RoundEnd(self):
        self.affiliateCharacter.ClearPowerBuff("Disarm")
        super().RoundEnd()
class Haste(Buff):#迅捷
    def __init__(self):
        super().__init__("Haste")
    def RoundStart(self):
        self.affiliateCharacter.AddSpeedBuff(self.count,self.count,"Haste")
    def RoundEnd(self):
        self.affiliateCharacter.ClearSpeedBuff("Haste")
        super().RoundEnd()
class Bind(Buff):#束缚
    def __init__(self):
        super().__init__("Bind")
    def RoundStart(self):
        self.affiliateCharacter.AddSpeedBuff(-self.count,-self.count,"Bind")
    def RoundEnd(self):
        self.affiliateCharacter.ClearSpeedBuff("Bind")
        super().RoundEnd()
class Fragile(Buff):#易损
    def __init__(self):
        super().__init__("Fragile")
    def RoundStart(self):
        self.affiliateCharacter.AddGetDamageBuff("Total",self.count,self.count,"Fragile")
    def RoundEnd(self):
        self.affiliateCharacter.ClearDamageBuff("Fragile")
        super().RoundEnd()
class Protection(Buff):#守护
    def __init__(self):
        super().__init__("Protection")
    def RoundStart(self):
        self.affiliateCharacter.AddGetDamageBuff("Total",-self.count,-self.count,"Protection")
    def RoundEnd(self):
        self.affiliateCharacter.ClearDamageBuff("Protection")
        super().RoundEnd()
class SProtection(Buff):#振奋
    def __init__(self):
        super().__init__("SProtection")
    def RoundStart(self):
        self.affiliateCharacter.AddGetDamageBuff("Total",-self.count,-self.count,"SProtection",True)
    def RoundEnd(self):
        self.affiliateCharacter.ClearDamageBuff("SProtection")
        super().RoundEnd()
class Paralysis(Buff):#麻痹
    def __init__(self):
        super().__init__("Paralysis")
    def RoundStart(self):
        self.affiliateCharacter.AddPowerLR(0,-3,"Paralysis")
    def UseDice(self):
        if self.count==1:
            self.affiliateCharacter.ClearPowerBuff("Paralysis")
        super().AddCount(-1)
    def RoundEnd(self):
        self.affiliateCharacter.ClearPowerBuff("Paralysis")
        super().RoundEnd()
class Smoke(Buff):
    def __init__(self):
        super().__init__("Smoke",10)
    def RoundStart(self):
        if self.affiliateCharacter.HavePassive(u"烟气缭绕")>0:
            per=0.05*self.count
            self.affiliateCharacter.AddDamagePer("Total",per,"Smoke")
        else:
            per=0.05*self.count
            self.affiliateCharacter.AddGetDamagePer("Total",per,"Smoke")
    def RoundEnd(self):
        self.affiliateCharacter.ClearDamageBuff("Smoke")
        super().AddCount(-1)
class Charge(Buff):
    def __init__(self):
        super().__init__("Charge",20)
    def RoundEnd(self):
        pass
class BloodMist(Buff):#强壮
    def __init__(self):
        super().__init__("BloodMist")
    def RoundStart(self):
        self.affiliateCharacter.AddPowerBuff("Total",self.count,self.count,"BloodMist")
    def RoundEnd(self):
        self.affiliateCharacter.ClearPowerBuff("BloodMist")
class Yang_CountDown(Buff):
    def __init__(self):
        super().__init__("Yang_CountDown")
class Buffs():
    def __init__(self):
        self.buffs=[]
        self.affiliateCharacter=None
    def AddBuff(self,name,count):
        dic={"Burn":Burn,"Bleed":Bleed,"Fairy":Fairy,"Erosion":Erosion,"Strength":Strength,"Feeble":Feeble,"Endurance":Endurance,"Disarm":Disarm,
             "Haste":Haste,"Bind":Bind,"Fragile":Fragile,"Protection":Protection,"SProtection":SProtection,"Paralysis":Paralysis,
             "Smoke":Smoke,"Charge":Charge,"BloodMist":BloodMist,"Yang_CountDown":Yang_CountDown}
        buff=dic[name]()
        buff.affiliateCharacter=self.affiliateCharacter
        buff.count=count
        if buff.limit!=-1:
            buff.count=min(buff.count,buff.limit)
        buff.affiliateList=self
        self.buffs.append(buff)
    def GetBuffCount(self,name):
        for buff in self.buffs:
            if buff.name==name:
                return buff.count
        return 0
    def RoundStart(self):
        for buff in reversed(self.buffs):
            buff.RoundStart()
    def UseAttackDice(self):
        for buff in reversed(self.buffs):
            buff.UseAttackDice()
    def UseDice(self):
        for buff in reversed(self.buffs):
            buff.UseDice()
    def GetDamage(self):
        for buff in reversed(self.buffs):
            buff.GetDamage()
    def RoundEnd(self):
        for buff in reversed(self.buffs):
            buff.RoundEnd()
    def DelBuff(self,name):
        i=0
        while i<len(self.buffs):
            if self.buffs[i].name==name:
                del self.buffs[i]
            else:
                i+=1
    def Clear(self):
        self.buffs.clear()