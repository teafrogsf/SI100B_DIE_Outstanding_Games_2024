from ReceptionSystem.DiceBuff import *
from RenderSystem.sceneRenderer.BattleCombatRenderer import CombatType,CombatEffectType
from RenderSystem.prefab.UICharacter import CharSD,CharState
from ReceptionSystem.GenerateDict import GenerateCombatPageDict,GenerateInfoDict,GeneratespCharDict
import copy,random
from GameDataManager import gameDataManager
class Dice:
    def __init__(self,dicePointL,dicePointR,diceType,attackType,affiliatePage,affiliateCharacter,isCounter=False):
        self.dicePointL=dicePointL
        self.dicePointR=dicePointR
        self.dicePoint=0
        self.diceType=diceType
        self.attackType=attackType
        self.diceBuff=DiceBuff()
        self.diceBuff.affiliateCharacter=affiliateCharacter
        self.diceBuff.dice=self
        self.affiliatePage=affiliatePage
        self.affiliateCharacter=affiliateCharacter
        self.tmpBuff=0
        self.used=False
        self.broken=False
        self.isCounter=isCounter
    def __deepcopy__(self,memo):
        d=Dice(self.dicePointL,self.dicePointR,self.diceType,self.attackType,self.affiliatePage,self.affiliateCharacter,self.isCounter)
        d.diceBuff=copy.copy(self.diceBuff)
        d.tmpBuff=self.tmpBuff
        d.used=self.used
        d.broken=self.broken
        return d
    def ConfirmDice(self,powerBuff,getcoin=True):
        powerLR=powerBuff.CalcPowerLR()
        pL=self.dicePointL+(powerLR[0])
        pR=self.dicePointR+(powerLR[1])
        powerbuff=powerBuff.CalcPowerBuff()
        if self.affiliateCharacter.havePower:
            pb=self.DicePower(powerbuff)
        else:
            pb=0
        pb+=self.tmpBuff
        if pL>=pR:
            pL=pR
            x=pR+pb
        else :
            x=random.randint(pL,pR)
            for i in range(self.affiliateCharacter.HavePassive(u"概率变动")):
                if x==pL:
                    x=random.randint(pL,pR)
            x+=pb
        if(x>=1):
            self.dicePoint=x
            if pL!=pR and getcoin:
                if x==pL+pb:
                    self.affiliateCharacter.emotion.GetRedCoin()
                if x==pR+pb:
                    self.affiliateCharacter.emotion.GetGreenCoin()
        else:
            self.dicePoint=1
    def BreakDice(self):
        self.broken=True
    def DicePower(self,powerBuff):
        power=powerBuff[self.attackType]+powerBuff["Total"]
        if self.diceType=="Attack":
            power+=powerBuff[self.diceType]
        else :
            power+=powerBuff["Defense"]
        if self.isCounter:
            power+=powerBuff["Counter"]
        return power
    def AddDiceBuff(self,buff):
        self.diceBuff=buff
        self.diceBuff.affiliateCharacter=self.affiliateCharacter
        self.diceBuff.dice=self
def DiceClashing(dice1,dice2,powerBuff1,powerBuff2,isnotSvR=True):
    if dice1.affiliatePage.pageType=="Ranged" or dice2.affiliatePage.pageType=="Ranged":
        gameDataManager.curDict["CombatType"]=CombatType.Far
    else:
        gameDataManager.curDict["CombatType"]=CombatType.Near
    if dice1.affiliateCharacter.team=="Ally":
        gameDataManager.curDict["char2"]=dice1.affiliateCharacter.id
        gameDataManager.curDict["char1"]=dice2.affiliateCharacter.id
    else:
        gameDataManager.curDict["char1"]=dice1.affiliateCharacter.id
        gameDataManager.curDict["char2"]=dice2.affiliateCharacter.id
    gameDataManager.curDict[dice1.affiliateCharacter.id]={}
    if dice1.affiliateCharacter.JudgeDeath():
        gameDataManager.curDict[dice1.affiliateCharacter.id]["state"]=CharState.Dead
    elif dice1.affiliateCharacter.JudgeStagger():
        gameDataManager.curDict[dice1.affiliateCharacter.id]["state"]=CharState.Stagger
    else:
        gameDataManager.curDict[dice1.affiliateCharacter.id]["state"]=CharState.Common
    gameDataManager.curDict[dice1.affiliateCharacter.id]["beforeCombat"]={}
    gameDataManager.curDict[dice1.affiliateCharacter.id]["beforeCombat"]["isHaveCard"]=True
    gameDataManager.curDict[dice1.affiliateCharacter.id]["combatEffect"]=[]
    gameDataManager.curDict[dice2.affiliateCharacter.id]={}
    if dice2.affiliateCharacter.JudgeDeath():
        gameDataManager.curDict[dice2.affiliateCharacter.id]["state"]=CharState.Dead
    elif dice2.affiliateCharacter.JudgeStagger():
        gameDataManager.curDict[dice2.affiliateCharacter.id]["state"]=CharState.Stagger
    else:
        gameDataManager.curDict[dice2.affiliateCharacter.id]["state"]=CharState.Common
    gameDataManager.curDict[dice2.affiliateCharacter.id]["beforeCombat"]={}
    gameDataManager.curDict[dice2.affiliateCharacter.id]["beforeCombat"]["isHaveCard"]=True
    gameDataManager.curDict[dice2.affiliateCharacter.id]["combatEffect"]=[]
    dice1.affiliateCharacter.buffs.UseDice()
    dice2.affiliateCharacter.buffs.UseDice()
    if dice1.diceType=="Attack":
        dice1.affiliateCharacter.buffs.UseAttackDice()
    if dice2.diceType=="Attack":
        dice2.affiliateCharacter.buffs.UseAttackDice()
    dice1.diceBuff.BeforeClash(dice2)
    dice2.diceBuff.BeforeClash(dice1)
    dice1.ConfirmDice(powerBuff1)
    dice2.ConfirmDice(powerBuff2)
    gameDataManager.curDict[dice1.affiliateCharacter.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(dice1.affiliateCharacter)
    gameDataManager.curDict[dice1.affiliateCharacter.id]["beforeCombat"]["combatCard"]=GenerateCombatPageDict(dice1.affiliatePage)
    gameDataManager.curDict[dice2.affiliateCharacter.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(dice2.affiliateCharacter)
    gameDataManager.curDict[dice2.affiliateCharacter.id]["beforeCombat"]["combatCard"]=GenerateCombatPageDict(dice2.affiliatePage)
    print(f"{dice1.attackType} {dice1.dicePoint} vs {dice2.dicePoint} {dice2.attackType}")
    flg1=True
    flg2=True
    if(dice1.diceType=="Attack" and dice2.diceType=="Attack"):#Attack vs Attack
        if isnotSvR: #Melee(Ranged) vs Melee(Ranged)
            if(dice1.dicePoint>dice2.dicePoint):
                dice2.affiliateCharacter.DoDamage(dice1.dicePoint,dice1.attackType,dice1.affiliateCharacter,True,dice1.isCounter)
                dice1.affiliateCharacter.ClashWin(dice1.attackType)
                dice1.diceBuff.ClashWin(dice2)
                dice1.diceBuff.Strike(dice2)
                dice2.diceBuff.ClashLose(dice1)
                if dice1.isCounter:
                    flg1=False
                    dice1.used=True
            elif(dice1.dicePoint<dice2.dicePoint):
                dice1.affiliateCharacter.DoDamage(dice2.dicePoint,dice2.attackType,dice2.affiliateCharacter,True,dice2.isCounter)
                dice2.affiliateCharacter.ClashWin(dice2.attackType)
                dice1.diceBuff.ClashLose(dice2)
                dice2.diceBuff.ClashWin(dice1)
                dice2.diceBuff.Strike(dice1)
                if dice2.isCounter:
                    flg2=False
                    dice2.used=True
            else:
                dice1.affiliateCharacter.ClashTie(dice1.attackType)
                dice2.affiliateCharacter.ClashTie(dice2.attackType)
            if flg1:
                dice1.BreakDice()
            if flg2:
                dice2.BreakDice()
        else : #Melee vs Ranged
            if(dice1.affiliatePage.pageType=="Melee"):
                mdice=dice1
                rdice=dice2
            else :
                mdice=dice2
                rdice=dice1
            if(mdice.dicePoint>rdice.dicePoint):
                rdice.affiliateCharacter.ClashLose(rdice.attackType)
                mdice.affiliateCharacter.ClashWin(mdice.attackType)
                mdice.diceBuff.ClashWin(rdice)
                rdice.diceBuff.ClashLose(mdice)
                if mdice.isCounter:
                    mdice.used=True
                else:
                    odice=copy.deepcopy(mdice)
                    mdice.affiliatePage.AddDelayDice(odice)
                    mdice.BreakDice()
                rdice.BreakDice()
            elif(mdice.dicePoint<rdice.dicePoint):
                mdice.affiliateCharacter.DoDamage(rdice.dicePoint,rdice.attackType,rdice.affiliateCharacter,True,rdice.isCounter)
                rdice.affiliateCharacter.ClashWin(rdice.attackType)
                mdice.diceBuff.ClashLose(rdice)
                rdice.diceBuff.ClashWin(mdice)
                rdice.diceBuff.Strike(mdice)
                dice1.BreakDice()
                dice2.BreakDice()
            else:
                dice1.affiliateCharacter.ClashTie(dice1.attackType)
                dice2.affiliateCharacter.ClashTie(dice2.attackType)
                dice1.BreakDice()
                dice2.BreakDice()
    elif(dice1.diceType=="Block" and dice2.diceType=="Block"):#Block vs Block
        if(dice1.dicePoint>dice2.dicePoint):
            dice2.affiliateCharacter.DoDamage(dice1.dicePoint,dice1.attackType,dice1.affiliateCharacter,True,dice1.isCounter)
            dice1.affiliateCharacter.ClashWin(dice1.attackType)
            dice1.diceBuff.ClashWin(dice2)
            dice1.diceBuff.Strike(dice2)
            dice2.diceBuff.ClashLose(dice1)
            if dice1.isCounter:
                flg1=False
                dice1.used=True
        elif(dice1.dicePoint<dice2.dicePoint):
            dice1.affiliateCharacter.DoDamage(dice2.dicePoint,dice2.attackType,dice2.affiliateCharacter,True,dice2.isCounter)
            dice2.affiliateCharacter.ClashWin(dice2.attackType)
            dice1.diceBuff.ClashLose(dice2)
            dice2.diceBuff.ClashWin(dice1)
            dice2.diceBuff.Strike(dice1)
            if dice2.isCounter:
                flg2=False
                dice2.used=True
        else:
            dice1.affiliateCharacter.ClashTie(dice1.attackType)
            dice2.affiliateCharacter.ClashTie(dice2.attackType)
        if flg1:
            dice1.BreakDice()
        if flg2:
            dice2.BreakDice()
    elif(dice1.diceType=="Evade" and dice2.diceType=="Evade"):#Evade vs Evade
        dice1.affiliateCharacter.ClashTie(dice1.attackType)
        dice2.affiliateCharacter.ClashTie(dice2.attackType)
        dice1.BreakDice()
        dice2.BreakDice()
    elif((dice1.diceType=="Attack" and dice2.diceType=="Block")or(dice1.diceType=="Block" and dice2.diceType=="Attack")):#Attack vs Block
        if(dice1.diceType=="Attack"):
            adice=dice1
            bdice=dice2
        else :
            adice=dice2
            bdice=dice1
        if(adice.dicePoint>bdice.dicePoint):
            bdice.affiliateCharacter.DoDamage(adice.dicePoint-bdice.dicePoint,adice.attackType,adice.affiliateCharacter,True,adice.isCounter)
            adice.affiliateCharacter.ClashWin(adice.attackType)
            adice.diceBuff.ClashWin(bdice)
            adice.diceBuff.Strike(bdice)
            bdice.diceBuff.ClashLose(adice)
            if adice.isCounter:
                flg1=False
                adice.used=True
        elif(adice.dicePoint<bdice.dicePoint):
            adice.affiliateCharacter.DoDamage(bdice.dicePoint-adice.dicePoint,bdice.attackType,bdice.affiliateCharacter,True,bdice.isCounter)
            bdice.affiliateCharacter.ClashWin(bdice.attackType)
            bdice.diceBuff.ClashWin(adice)
            bdice.diceBuff.Strike(adice)
            adice.diceBuff.ClashLose(bdice)
            if bdice.isCounter:
                flg2=False
                bdice.used=True
        else:
            dice1.affiliateCharacter.ClashTie(dice1.attackType)
            dice2.affiliateCharacter.ClashTie(dice2.attackType)
        if flg1:
            adice.BreakDice()
        if flg2:
            bdice.BreakDice()
    elif((dice1.diceType=="Attack" and dice2.diceType=="Evade")or(dice1.diceType=="Evade" and dice2.diceType=="Attack")):#Attack vs Evade
        if(dice1.diceType=="Attack"):
            adice=dice1
            edice=dice2
        else :
            adice=dice2
            edice=dice1
        if(adice.dicePoint>edice.dicePoint):
            edice.affiliateCharacter.DoDamage(adice.dicePoint,adice.attackType,adice.affiliateCharacter,True,adice.isCounter)
            adice.affiliateCharacter.ClashWin(adice.attackType)
            adice.diceBuff.ClashWin(edice)
            adice.diceBuff.Strike(edice)
            edice.diceBuff.ClashLose(adice)
            edice.BreakDice()
            if not adice.isCounter:
                adice.BreakDice()
            else:
                adice.used=True
        elif(adice.dicePoint<edice.dicePoint):
            edice.affiliateCharacter.RecoverStagger(edice.dicePoint)
            edice.affiliateCharacter.ClashWin(edice.attackType)
            adice.affiliateCharacter.ClashLose(adice.attackType)
            edice.diceBuff.ClashWin(adice)
            adice.diceBuff.ClashLose(edice)
            edice.used=True
            adice.BreakDice()
        else:
            dice1.affiliateCharacter.ClashTie(dice1.attackType)
            dice2.affiliateCharacter.ClashTie(dice2.attackType)
            edice.BreakDice()
            adice.BreakDice()
    else: #Block vs Evade
        if(dice1.diceType=="Block"):
            bdice=dice1
            edice=dice2
        else :
            bdice=dice2
            edice=dice1
        if(bdice.dicePoint>edice.dicePoint):
            edice.affiliateCharacter.DoDamage(bdice.dicePoint,bdice.attackType,bdice.affiliateCharacter,True,bdice.isCounter)
            bdice.affiliateCharacter.ClashWin(bdice.attackType)
            bdice.diceBuff.ClashWin(edice)
            bdice.diceBuff.Strike(edice)
            edice.diceBuff.ClashLose(bdice)
            if not bdice.isCounter:
                bdice.BreakDice()
            else:
                bdice.used=True
            edice.BreakDice()    
        elif(bdice.dicePoint<edice.dicePoint):
            edice.affiliateCharacter.RecoverStagger(edice.dicePoint)
            edice.affiliateCharacter.ClashWin(edice.attackType)
            bdice.affiliateCharacter.ClashLose(bdice.attackType)
            edice.diceBuff.ClashWin(bdice)
            bdice.diceBuff.ClashLose(edice)
            if edice.isCounter:
                edice.used=True
            else:
                edice.BreakDice()
            bdice.BreakDice()
        else:
            dice1.affiliateCharacter.ClashTie(dice1.attackType)
            dice2.affiliateCharacter.ClashTie(dice2.attackType)
            bdice.BreakDice()
            edice.BreakDice()
    if dice1.affiliateCharacter.id not in gameDataManager.curDict:
        gameDataManager.curDict[dice1.affiliateCharacter.id] = {}
    if dice2.affiliateCharacter.id not in gameDataManager.curDict:
        gameDataManager.curDict[dice2.affiliateCharacter.id] = {}
    gameDataManager.curDict[dice1.affiliateCharacter.id]["afterCombat"]={}
    if dice1.affiliateCharacter.JudgeDeath():
        gameDataManager.curDict[dice1.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Dead
    elif dice1.affiliateCharacter.JudgeStagger():
        gameDataManager.curDict[dice1.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Stagger
    else:
        gameDataManager.curDict[dice1.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Common
    gameDataManager.curDict[dice1.affiliateCharacter.id]["afterCombat"]["infoBar"]=GenerateInfoDict(dice1.affiliateCharacter)
    gameDataManager.curDict[dice2.affiliateCharacter.id]["afterCombat"]={}
    if dice2.affiliateCharacter.JudgeDeath():
        gameDataManager.curDict[dice2.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Dead
    elif dice2.affiliateCharacter.JudgeStagger():
        gameDataManager.curDict[dice2.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Stagger
    else:
        gameDataManager.curDict[dice2.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Common
    gameDataManager.curDict[dice2.affiliateCharacter.id]["afterCombat"]["infoBar"]=GenerateInfoDict(dice2.affiliateCharacter)
    return False
def DiceAttack(dice,target,powerBuff):
    if(dice.diceType=="Attack" and not dice.isCounter):
        dice.diceBuff.BeforeAttack(target)
        if dice.affiliatePage.pageType=="Ranged":
            gameDataManager.curDict["CombatType"]=CombatType.Far
        else:
            gameDataManager.curDict["CombatType"]=CombatType.Near
        if target.team=="Ally":
            gameDataManager.curDict["char1"]=dice.affiliateCharacter.id
            gameDataManager.curDict["char2"]=target.id
        else:
            gameDataManager.curDict["char2"]=dice.affiliateCharacter.id
            gameDataManager.curDict["char1"]=target.id
        gameDataManager.curDict[dice.affiliateCharacter.id]={}
        if dice.affiliateCharacter.JudgeDeath():
            gameDataManager.curDict[dice.affiliateCharacter.id]["state"]=CharState.Dead
        elif dice.affiliateCharacter.JudgeStagger():
            gameDataManager.curDict[dice.affiliateCharacter.id]["state"]=CharState.Stagger
        else:
            gameDataManager.curDict[dice.affiliateCharacter.id]["state"]=CharState.Common
        gameDataManager.curDict[dice.affiliateCharacter.id]["beforeCombat"]={}
        gameDataManager.curDict[dice.affiliateCharacter.id]["beforeCombat"]["isHaveCard"]=True
        gameDataManager.curDict[dice.affiliateCharacter.id]["combatEffect"]=[]
        dice.affiliateCharacter.buffs.UseDice()
        dice.affiliateCharacter.buffs.UseAttackDice()
        dice.ConfirmDice(powerBuff)
        gameDataManager.curDict[dice.affiliateCharacter.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(dice.affiliateCharacter)
        gameDataManager.curDict[dice.affiliateCharacter.id]["beforeCombat"]["combatCard"]=GenerateCombatPageDict(dice.affiliatePage)
        gameDataManager.curDict[target.id]={}
        if target.JudgeDeath():
            gameDataManager.curDict[target.id]["state"]=CharState.Dead
        elif target.JudgeStagger():
            gameDataManager.curDict[target.id]["state"]=CharState.Stagger
        else:
            gameDataManager.curDict[target.id]["state"]=CharState.Common
        gameDataManager.curDict[target.id]["beforeCombat"]={}
        gameDataManager.curDict[target.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(target)
        gameDataManager.curDict[target.id]["beforeCombat"]["isHaveCard"]=False
        gameDataManager.curDict[target.id]["combatEffect"]=[]
        dic={"Slash":CharSD.Slash,"Pierce":CharSD.Pierce,"Blunt":CharSD.Blunt,"Block":CharSD.Block,"Evade":CharSD.Evade}
        gameDataManager.curDict[dice.affiliateCharacter.id]["action"]=dic[dice.attackType]
        gameDataManager.curDict["CombatWinner"]=dice.affiliateCharacter.id
        print(f"Attack {dice.attackType} {dice.dicePoint}")
        target.DoDamage(dice.dicePoint,dice.attackType,dice.affiliateCharacter,False,dice.isCounter)
        dice.diceBuff.Strike(target,False)
        if dice.affiliateCharacter.id not in gameDataManager.curDict:
            gameDataManager.curDict[dice.affiliateCharacter.id] = {}
        if target.id not in gameDataManager.curDict:
            gameDataManager.curDict[target.id] = {}
        gameDataManager.curDict[dice.affiliateCharacter.id]["afterCombat"]={}
        if dice.affiliateCharacter.JudgeDeath():
            gameDataManager.curDict[dice.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Dead
        elif dice.affiliateCharacter.JudgeStagger():
            gameDataManager.curDict[dice.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Stagger
        else:
            gameDataManager.curDict[dice.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Common
        gameDataManager.curDict[dice.affiliateCharacter.id]["afterCombat"]["infoBar"]=GenerateInfoDict(dice.affiliateCharacter)
        gameDataManager.curDict[target.id]["afterCombat"]={}
        if target.JudgeDeath():
            gameDataManager.curDict[target.id]["afterCombat"]["state"]=CharState.Dead
        elif target.JudgeStagger():
            gameDataManager.curDict[target.id]["afterCombat"]["state"]=CharState.Stagger
        else:
            gameDataManager.curDict[target.id]["afterCombat"]["state"]=CharState.Common
        gameDataManager.curDict[target.id]["afterCombat"]["infoBar"]=GenerateInfoDict(target)
        dice.BreakDice()
        return True 
    else:
        if dice.used:
            dice.used=False
        else:
            dice.affiliateCharacter.AddDefense(dice)
        dice.BreakDice()
        return False