from ReceptionSystem.PageBuff import *
from ReceptionSystem.Dice import *
import copy
class Page:
    def __init__(self,name,pageType,dices,lightCost,affiliateCharacter,id,quality,isCounter=False):
        self.name=name
        self.quality=quality
        self.pageType=pageType
        self.dices=dices
        self.counterDices=[]
        self.delayDices=[]
        self.pageBuff=PageBuff()
        self.pageBuff.page=name
        self.lightCost=lightCost
        self.originCost=lightCost
        self.affiliateCharacter=affiliateCharacter
        self.id=id
        self.n=0
        self.isCounter=isCounter
        self.charge=False
        self.used=True
    def AddDice(self,odice):
        dice=copy.deepcopy(odice)
        dice.affiliatePage=self
        self.n+=1
        self.dices.append(dice)
    def AddCounterDice(self,odice):
        dice=copy.deepcopy(odice)
        dice.affiliatePage=self
        self.counterDices.append(dice)
    def AddDelayDice(self,odice):
        dice=copy.deepcopy(odice)
        dice.affiliatePage=self
        self.delayDices.append(dice)
    def ClearPage(self):
        self.delayDices.clear()
        for dice in self.dices:
            dice.broken=False
            dice.used=False
            dice.tmpBuff=0
        self.used=True
        self.affiliateCharacter.ClearPowerBuff("PageBuff")
        self.affiliateCharacter.ClearDamageBuff("PageBuff")
        if self.pageBuff.special=="RedMistPage":
            if self.affiliateCharacter.passiveDit["PageDamage"]>=8:
                for page in self.affiliateCharacter.handPages:
                    if page.name==self.name:
                        print("DEBUG           FUCK")
                        if page.lightCost>0:
                            page.lightCost-=1
                self.affiliateCharacter.rollPage+=1
        if self.pageBuff.special=="RedMistLight":
            if self.affiliateCharacter.passiveDit["PageDamage"]>=8:
                for page in self.affiliateCharacter.handPages:
                    if page.name==self.name:
                        print("DEBUG           FUCK")
                        if page.lightCost>0:
                            page.lightCost-=1
                self.affiliateCharacter.getLight+=2
        self.affiliateCharacter.passiveDit["PageDamage"]=0
    def HaveDice(self):
        for dice in self.dices:
            if not dice.broken:
                return True
        for dice in self.delayDices:
            if not dice.broken:
                return True
        return False
    def FindDice(self):
        for dice in self.dices:
            if not dice.broken:
                return dice
        for dice in self.delayDices:
            if not dice.broken:
                return dice
        return None
    def AddPageBuff(self,buff):
        self.pageBuff=buff
        self.pageBuff.affiliateCharacter=self.affiliateCharacter
        self.pageBuff.page=self.name
def PageClashing(page1,page2,powerBuff1,powerBuff2):
    print(f"     {page1.affiliateCharacter.name} use page {page1.name} vs {page2.name} from {page2.affiliateCharacter.name}:")
    page1.pageBuff.BeforeUse(page2)
    page2.pageBuff.BeforeUse(page1)
    if page1.pageBuff.special=="Yang":
        page1.pageBuff.clashed=True
    if page2.pageBuff.special=="Yang":
        page2.pageBuff.clashed=True
    if page1.isCounter:
        if page2.isCounter:
            return
        else:
            PageAttack(page2,page1.affiliateCharacter,powerBuff2)
            return
    else:
        if page2.isCounter:
            PageAttack(page1,page2.affiliateCharacter,powerBuff1)
            return
        else:
            pass
    while(page1.HaveDice() or page2.HaveDice()):
        gameDataManager.curDict={}
        if(page1.HaveDice() and page2.HaveDice()):
            DiceClashing(page1.FindDice(),page2.FindDice(),powerBuff1,powerBuff2,page1.pageType==page2.pageType)
            gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        elif(page1.HaveDice()):
            if DiceAttack(page1.FindDice(),page2.affiliateCharacter,powerBuff1):
                gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        else:
            if DiceAttack(page2.FindDice(),page1.affiliateCharacter,powerBuff2):
                gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        flg=0
        if(page1.affiliateCharacter.JudgeDeath()==True):
            flg=1
            #page1.affiliateCharacter.ClaimDeath(page2.affiliateCharacter)
            while page2.HaveDice():
                dice=page2.FindDice()
                if(dice.diceType=="Block" or dice.diceType=="Evade" or dice.isCounter):
                    if not dice.used:
                        dice.affiliateCharacter.AddDefense(dice)
                dice.BreakDice()
        if(page2.affiliateCharacter.JudgeDeath()==True):
            flg=1
            #page2.affiliateCharacter.ClaimDeath(page1.affiliateCharacter)
            while page1.HaveDice():
                dice=page1.FindDice()
                if(dice.diceType=="Block" or dice.diceType=="Evade" or dice.isCounter):
                    if not dice.used:
                        dice.affiliateCharacter.AddDefense(dice)
                dice.BreakDice()
        if(flg==1):
            break
        if(page1.affiliateCharacter.JudgeStagger()==True):
            while page1.HaveDice():
                page1.FindDice().BreakDice()
        if(page2.affiliateCharacter.JudgeStagger()==True):
            while page2.HaveDice():
                page2.FindDice().BreakDice()
    page1.ClearPage()
    page2.ClearPage()
def PageAttack(page,target,powerBuff):
    print(f"     {page.affiliateCharacter.name} use page {page.name} to attack {target.name}:")
    if(len(target.defense)>0):
        dpage=Page("Defense","Melee",[],0,None,-1,"Green")
        print(f"     {target.name} have defense:",end='')
        for dice in target.defense:
            print(f"   {dice.attackType} {dice.dicePointL}/{dice.dicePointR}",end='')
            dpage.AddDice(dice)
        print()
        target.AddPage(dpage,True)
        target.ClearDefense()
        PageClashing(page,dpage,powerBuff,target.powerBuff)
        return
    page.pageBuff.BeforeUse(target,False)
    while page.HaveDice():
        gameDataManager.curDict={}
        if DiceAttack(page.FindDice(),target,powerBuff):
            gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        if(target.JudgeDeath()==True):
            #target.ClaimDeath(page.affiliateCharacter)
            while page.HaveDice():
                dice=page.FindDice()
                if(dice.diceType=="Block" or dice.diceType=="Evade"):
                    dice.affiliateCharacter.AddDefense(dice)
                dice.BreakDice()
            break
    page.ClearPage()
def PageMassAttack(page,characters,dices,powerBuff,powerBuffs):
    print(f"     {page.affiliateCharacter.name} use mass attack page {page.name}:")
    used=[]
    for i in range(len(dices)):
        used.append(0)
        if dices[i].havePage and (dices[i].page.pageType=="Melee" or dices[i].page.pageType=="Ranged"):
            print(f"          {dices[i].affiliateCharacter.name} use page {dices[i].page.name} to response")
        else :
            print(f"          {characters[i].name} has no page to response")
    adic={u"扭曲之刃":"WarpedBlade",u"狂暴血刃":"FrenziedBloodBlade",u"燎原烈火":"RangingInferno",u"尸横遍野":"LandscapeOfDeath"}
    if page.pageType=="Individual":
        for i in range(len(page.dices)):
            tdic={"Slash":CharSD.Slash,"Pierce":CharSD.Pierce,"Blunt":CharSD.Blunt,"Block":CharSD.Block,"Evade":CharSD.Evade}
            gameDataManager.curDict={}
            gameDataManager.curDict["CombatType"]=CombatType.AOE
            gameDataManager.curDict["attacker"]=page.affiliateCharacter.id
            gameDataManager.curDict["AoeAnime"]=gameDataManager.getAoeAnime(adic[page.name])
            gameDataManager.curDict["joiner"]=[{"id":page.affiliateCharacter.id,"pos":page.affiliateCharacter.pos}]
            gameDataManager.curDict["receiver"]=[]
            gameDataManager.curDict[page.affiliateCharacter.id]={}
            gameDataManager.curDict[page.affiliateCharacter.id]["action"]=tdic[page.dices[i].attackType]
            gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]={}
            gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]["isHaveCard"]=True
            gameDataManager.curDict[page.affiliateCharacter.id]["combatEffect"]=[]
            page.dices[i].ConfirmDice(powerBuff,False)
            gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(page.affiliateCharacter)
            gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]["combatCard"]=GenerateCombatPageDict(page)
            for j in range(len(characters)):
                if characters[j].JudgeDeath():
                    continue
                gameDataManager.curDict["joiner"].append({"id":characters[j].id,"pos":characters[j].pos})
                gameDataManager.curDict["receiver"].append(characters[j].id)
                if characters[j].id not in gameDataManager.curDict:
                    gameDataManager.curDict[characters[j].id] = {}
                gameDataManager.curDict[characters[j].id]["beforeCombat"]={}
                gameDataManager.curDict[characters[j].id]["combatEffect"]=[]
                if ((not dices[j].havePage) or used[j]==dices[j].page.n or characters[j].JudgeStagger() 
                    or dices[j].page.pageType=="Individual" or dices[j].page.pageType=="Summation"):
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["isHaveCard"]=False
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["infoBar"]=GenerateInfoDict(characters[j])
                    page.dices[i].diceBuff.Strike(characters[j],False)
                    characters[j].DoDamage(page.dices[i].dicePoint,page.dices[i].attackType,page.dices[i].affiliateCharacter,False)
                else:
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["isHaveCard"]=True
                    dices[j].page.dices[used[j]].ConfirmDice(powerBuffs[j],False)
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["infoBar"]=GenerateInfoDict(characters[j])
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["combatCard"]=GenerateCombatPageDict(dices[j].page,used[j])
                    if dices[j].page.dices[used[j]].dicePoint<page.dices[i].dicePoint:
                        page.dices[i].diceBuff.Strike(characters[j],False)
                        dices[j].page.dices[used[j]].BreakDice()
                        characters[j].DoDamage(page.dices[i].dicePoint,page.dices[i].attackType,page.dices[i].affiliateCharacter,False)
                    else:
                        gameDataManager.curDict[characters[j].id]["action"]=tdic[dices[j].page.dices[used[j]].attackType]
                        pass
                gameDataManager.curDict[characters[j].id]["afterCombat"]={}
                if page.affiliateCharacter.JudgeDeath():
                    gameDataManager.curDict[characters[j].id]["afterCombat"]["state"]=CharState.Dead
                elif page.affiliateCharacter.JudgeStagger():
                    gameDataManager.curDict[characters[j].id]["afterCombat"]["state"]=CharState.Stagger
                else:
                    gameDataManager.curDict[characters[j].id]["afterCombat"]["state"]=CharState.Common
                gameDataManager.curDict[characters[j].id]["afterCombat"]["infoBar"]=GenerateInfoDict(characters[j])
                if characters[j].JudgeDeath():
                    pass
                    #characters[j].ClaimDeath(page.affiliateCharacter)
                elif characters[j].JudgeStagger():
                    if dices[j].havePage:
                        while dices[j].page.HaveDice():
                            dices[j].page.FindDice().BreakDice()
                if dices[j].havePage and not(dices[j].page.pageType=="Individual" or dices[j].page.pageType=="Summation"):
                    if used[j]!=dices[j].page.n:
                        used[j]+=1
                    while used[j]!=dices[j].page.n and dices[j].page.dices[used[j]].broken:
                        used[j]+=1 
            if page.affiliateCharacter.id not in gameDataManager.curDict:
                gameDataManager.curDict[page.affiliateCharacter.id] = {}
            gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]={}
            if page.affiliateCharacter.JudgeDeath():
                gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Dead
            elif page.affiliateCharacter.JudgeStagger():
                gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Stagger
            else:
                gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Common
            gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["infoBar"]=GenerateInfoDict(page.affiliateCharacter)
            page.dices[i].BreakDice()
            gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
    else:
        tdic={"Slash":CharSD.Slash,"Pierce":CharSD.Pierce,"Blunt":CharSD.Blunt,"Block":CharSD.Block,"Evade":CharSD.Evade}
        gameDataManager.curDict={}
        gameDataManager.curDict["CombatType"]=CombatType.AOE
        gameDataManager.curDict["attacker"]=page.affiliateCharacter.id
        gameDataManager.curDict["AoeAnime"]=gameDataManager.getAoeAnime(adic[page.name])
        gameDataManager.curDict["joiner"]=[{"id":page.affiliateCharacter.id,"pos":page.affiliateCharacter.pos}]
        gameDataManager.curDict["receiver"]=[]
        gameDataManager.curDict[page.affiliateCharacter.id]={}
        gameDataManager.curDict[page.affiliateCharacter.id]["action"]=tdic[page.dices[0].attackType]
        gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]={}
        gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]["isHaveCard"]=True
        gameDataManager.curDict[page.affiliateCharacter.id]["combatEffect"]=[]
        page.dices[0].ConfirmDice(powerBuff,False)
        gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(page.affiliateCharacter)
        gameDataManager.curDict[page.affiliateCharacter.id]["beforeCombat"]["combatCard"]=GenerateCombatPageDict(page)
        for j in range(len(characters)):
                if characters[j].JudgeDeath():
                    continue
                gameDataManager.curDict["joiner"].append({"id":characters[j].id,"pos":characters[j].pos})
                gameDataManager.curDict["receiver"].append(characters[j].id)
                if characters[j].id not in gameDataManager.curDict:
                    gameDataManager.curDict[characters[j].id] = {}
                gameDataManager.curDict[characters[j].id]["beforeCombat"]={}
                gameDataManager.curDict[characters[j].id]["combatEffect"]=[]
                if ((not dices[j].havePage) or (not dices[j].page.HaveDice()) or characters[j].JudgeStagger() 
                    or dices[j].page.pageType=="Individual" or dices[j].page.pageType=="Summation"):
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["isHaveCard"]=False
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["infoBar"]=GenerateInfoDict(characters[j])
                    page.dices[0].diceBuff.Strike(characters[j])
                    characters[j].DoDamage(page.dices[0].dicePoint,page.dices[0].attackType,page.dices[0].affiliateCharacter,False)
                else:
                    point=0
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["isHaveCard"]=True
                    for dice in dices[j].page.dices:
                        dice.ConfirmDice(powerBuffs[j])
                        point+=dice.dicePoint
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["infoBar"]=GenerateInfoDict(characters[j])
                    gameDataManager.curDict[characters[j].id]["beforeCombat"]["combatCard"]=GenerateCombatPageDict(dices[j].page,-1,point)
                    if point<page.dices[0].dicePoint:
                        for dice in dices[j].page.dices:
                            dice.BreakDice()
                        page.dices[0].diceBuff.Strike(characters[j])
                        characters[j].DoDamage(page.dices[0].dicePoint,page.dices[0].attackType,page.dices[0].affiliateCharacter,False)
                    else:
                        gameDataManager.curDict[characters[j].id]["action"]=tdic[dices[j].page.dices[0].attackType]
                        pass
                gameDataManager.curDict[characters[j].id]["afterCombat"]={}
                if page.affiliateCharacter.JudgeDeath():
                    gameDataManager.curDict[characters[j].id]["afterCombat"]["state"]=CharState.Dead
                elif page.affiliateCharacter.JudgeStagger():
                    gameDataManager.curDict[characters[j].id]["afterCombat"]["state"]=CharState.Stagger
                else:
                    gameDataManager.curDict[characters[j].id]["afterCombat"]["state"]=CharState.Common
                gameDataManager.curDict[characters[j].id]["afterCombat"]["infoBar"]=GenerateInfoDict(characters[j])
                if characters[j].JudgeDeath():
                    #characters[j].ClaimDeath(page.affiliateCharacter)
                    pass
                elif characters[j].JudgeStagger():
                    if dices[j].havePage:
                        while dices[j].page.HaveDice():
                            dices[j].page.FindDice().BreakDice()
        if page.affiliateCharacter.id not in gameDataManager.curDict:
            gameDataManager.curDict[page.affiliateCharacter.id] = {}
        gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]={}
        if page.affiliateCharacter.JudgeDeath():
            gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Dead
        elif page.affiliateCharacter.JudgeStagger():
            gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Stagger
        else:
            gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["state"]=CharState.Common
        gameDataManager.curDict[page.affiliateCharacter.id]["afterCombat"]["infoBar"]=GenerateInfoDict(page.affiliateCharacter)
        gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
    page.ClearPage()