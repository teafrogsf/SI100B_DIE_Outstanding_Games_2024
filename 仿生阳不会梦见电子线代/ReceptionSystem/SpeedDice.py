import random
class SpeedDice:
    def __init__(self,speedL,speedR,affiliateCharacter,id):
        self.speedL=speedL
        self.speedR=speedR
        self.affiliateCharacter=affiliateCharacter
        self.havePage=False
        self.haveTarget=False
        self.isbreak=False
        self.id=id
        self.Target=None
        self.massTarget=[]
        self.originTarget=None
        self.speed=-1
        self.weight=0
    def SetOrigin(self,target):
        self.originTarget=target
    def ConfirmDice(self,speedBuff):
        tp=speedBuff.CalcSpeed()
        sL=self.speedL+tp[0]
        sR=self.speedR+tp[1]
        if sL>=sR:
            sL=sR
            x=sR
        else :
            x=random.randint(sL,sR)
        if x>=1:
            self.speed=x
        else:
            self.speed=1
    def SelectPage(self,page):
        self.page=page
        self.havePage=True
    def DownPage(self):
        self.havePage=False
        self.page=None
        self.Target.Target=self.Target.originTarget
        self.massTarget.clear()
        self.haveTarget=False
    def TargetPage(self,target):
        self.haveTarget=True
        self.Target=target
        if target.speed<self.speed:
            if (not self.Target.havePage) or self.Target.page.pageType=="Melee" or self.Target.page.pageType=="Ranged":
                target.Target=self
    def MassTarget(self,target,team):
        self.haveTarget=True
        self.Target=target
        for character in team.characters:
            if character.JudgeDeath():
                continue
            if character.id==target.affiliateCharacter.id:
                continue
            n=len(character.speedDices)
            self.massTarget.append(character.speedDices[random.randint(0,n-1)])
    def IsClashing(self):
        if self.haveTarget==False:
            return False
        if self.Target.haveTarget==False:
            return False
        if self.page.pageType=="Individual" or self.page.pageType=="Summation":
            return False
        if self.Target.page.pageType=="Individual" or self.Target.page.pageType=="Summation":
            return False
        return (self.Target.Target.id==self.id and self.Target.Target.affiliateCharacter.id==self.affiliateCharacter.id)
    def CalcWeight(self):
        self.weight=self.speed
        if self.haveTarget==False:
            pass
        elif self.Target.haveTarget==False:
            if self.page.pageType=="Ranged":
                self.weight+=100
        else:
            if self.page.pageType=="Ranged":
                self.weight+=100
            if self.Target.page.pageType=="Ranged":
                self.weight+=100