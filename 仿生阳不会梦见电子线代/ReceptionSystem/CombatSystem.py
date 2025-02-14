import random

from RenderSystem.sceneRenderer.BattleCombatRenderer import CombatType,CombatEffectType
from ReceptionSystem.GenerateDict import GenerateCombatPageDict,GenerateInfoDict,GeneratespCharDict
from GameDataManager import gameDataManager
from ReceptionSystem.Page import *
from ReceptionSystem.Character import *
from ReceptionSystem.Team import *
from ReceptionSystem.ReceptionRnfmabj import *
from ReceptionSystem.ReceptionMyo import *
from ReceptionSystem.ReceptionLeaflet import *
from ReceptionSystem.ReceptionLiuAso import *
from ReceptionSystem.ReceptionRedMist import *
# DIVIDE HERE --------------------------------------------------------------------------------------------------------------
class BattleDisplay:#Create a log for debug
    def __init__(self):
        self.sys=None
        pass
    def DisplayCharacter(self,person):
        if person.JudgeStagger():
            print(f"   {person.name}   {person.id} {person.isStagger}(in stagger)")
        else:
            print(f"   {person.name}   {person.id}")
        print(f"   Health {person.health}/{person.healthMax}")
        print(f"   Stagger {person.stagger}/{person.staggerMax}")
        print(f"   Emotion {person.emotion.emotionLevel}",end='')
        for coin in person.emotion.coins:
            if coin=="Green":
                print("G",end="")
            else:
                print("R",end="")
        print()
        print("   Buffs:",end="")
        for buff in person.buffs.buffs:
            print(f"  {buff.name}*{buff.count}",end="")
        print()
        print("   Power Buffs:")
        for powerBuff in person.powerBuff.powerBuff:
            for key,value in powerBuff.powerBuff.items():
                if value!=(0,0):
                    print(key,end=" ")
                    print(f"{value[0]} {value[1]}")
        print()
        print(f"   Light {person.light}/{person.lightMax}")
        print("   Speed  ",end='')
        for dice in person.speedDices:
            if dice.isbreak:
                print("*       ",end='')
            elif dice.speed==-1:
                print("-       ",end='')
            else :
                print(f"{dice.speed}       ",end='')
        print()
        print("   Page   ",end='')
        for dice in person.speedDices:
            if dice.haveTarget:
                print(f"{dice.page.name}    ",end='')
            else :
                print(f"-       ",end='')
        print()
        print("   Target ",end='')
        for dice in person.speedDices:
            if dice.haveTarget:
                print(f"{dice.Target.affiliateCharacter.name}  ",end='')
            else :
                print(f"-       ",end='')
        print()
        print("   Target ",end='')        
        for dice in person.speedDices:
            if dice.haveTarget:
                print(f"{dice.Target.affiliateCharacter.FindDiceIndex(dice.Target.id)}       ",end='')
            else :
                print(f"-       ",end='')
        print()
        print("   pages:")
        for page in person.handPages:
            print(f"      {page.name}   {page.pageType}   {page.lightCost}")
            print("         ",end='')
            for dice in page.dices:
                print(f"{dice.attackType}{dice.dicePointL}/{dice.dicePointR}",end=' ')
            for dice in page.counterDices:
                print(f"ct {dice.attackType}{dice.dicePointL}/{dice.dicePointR}",end=' ')
            print()    

    def DisplayTeam(self,team):
        for person in team.characters:
            if person.JudgeDeath():
                print(f"   {person.name}    {person.id}  is dead")
            else:
                self.DisplayCharacter(person)
    def DisplayBattle(self):
        print(f"Round {self.sys.round}")
        print("Allies:")
        self.DisplayTeam(self.sys.allies)
        print("Enemies:")
        self.DisplayTeam(self.sys.enemies)
        
class BattleSystem:
    def __init__(self,name):
        self.name=name
        self.enemies=Team("Enemy")
        self.allies=Team("Ally")
        self.enemies.against=self.allies
        self.allies.against=self.enemies
        self.round=0
        self.display=BattleDisplay()
        self.display.sys=self
        self.Pages=[]
        self.Characters=[]
    def ReceptionInit(self,nam = "redMist",receptionList=[]):
        self.name = nam
        if self.name=="rnfmabj":
            yang=Rnfmabj(101,3)
            lhand=LeftHand(102,2)
            rhand=RightHand(103,1)
            yang.leftHand=lhand
            yang.rightHand=rhand
            yang.pages[0].pageBuff.clashed=True
            yang.pages[1].pageBuff.clashed=True
            yang.pages[3].pageBuff.clashed=True
            yang.pages[4].pageBuff.clashed=True
            self.enemies.AddPerson(yang)
            self.enemies.AddPerson(lhand)
            self.enemies.AddPerson(rhand)
        elif self.name=="myo":
            self.enemies.AddPerson(Myo(101,3))
            self.enemies.AddPerson(Rabbit(102,1))
            self.enemies.AddPerson(Rabbit(103,2))
            self.enemies.AddPerson(Rabbit(104,4))
            self.enemies.AddPerson(Rabbit(105,5))
        elif self.name=="leaflet":
            self.enemies.AddPerson(Yae(101,3))
            self.enemies.AddPerson(LeafFixer(102,1))
            self.enemies.AddPerson(LeafFixer(103,2))
            self.enemies.AddPerson(LeafFixer(104,4))
            self.enemies.AddPerson(LeafFixer(105,5))
        elif self.name=="liuaso":
            self.enemies.AddPerson(Lowell(101,3))
            self.enemies.AddPerson(Mei(102,1))
            self.enemies.AddPerson(LiuFixer(103,2))
            self.enemies.AddPerson(LiuFixer(104,4))
            self.enemies.AddPerson(LiuFixer(105,5))
        elif self.name=="redmist":
            self.enemies.AddPerson(RedMist(101,3))
        elif self.name=="special":
            t=101
            for person in receptionList:
                if isinstance(person,str):
                    chardit={"Rnfmabj":Rnfmabj,"LeftHand":LeftHand,"RightHand":RightHand,"Myo":Myo,"Rabbit":Rabbit,
                             "Yae":Yae,"LeafFixer":LeafFixer,"Lowell":Lowell,"Mei":Mei,"LiuFixer":LiuFixer,"RedMist":RedMist}
                    self.enemies.AddPerson(chardit[person](t,t%100))
                    t+=1
                else:
                    per=Character(person.name,person.healthMax,person.staggerMax,person.originResistance,person.speedL,person.speedR,person.countDices,
                                person.countDice,t,t%100,"Enemy")
                    for psv in person.Passive:
                        per.AddPassive(psv)
                    for page in person.Page:
                        #pg=gameDataManager.getPage(page["name"])
                        pg=gameDataManager.getPage(page)
                        per.AddPage(pg)
                    t+=1
                    self.enemies.AddPerson(per)
    def Init(self,dit={"Ally":[],"Enemy":[],"Reception":"redmist"}):
        #modified by NH37
        from GameDataManager import CharacterData
        DEBUG = True
        t=201
        allyList=dit["Ally"]
        for person in allyList:
            if isinstance(person,str):
                chardit={"Rnfmabj":Rnfmabj,"LeftHand":LeftHand,"RightHand":RightHand,"Myo":Myo,"Rabbit":Rabbit,
                             "Yae":Yae,"LeafFixer":LeafFixer,"Lowell":Lowell,"Mei":Mei,"LiuFixer":LiuFixer,"RedMist":RedMist}
                per=chardit[person](t,t%100)
                per.team="ally"
                self.allies.AddPerson(per)
                t+=1
            elif isinstance(person,CharacterData):
                per=Character(person.name,person.healthMax,person.staggerMax,person.originResistance,person.speedL,person.speedR,person.countDices,
                                person.lightMax,t,t%100,"Ally",person.SDname)
                for psv in person.Passive:
                    per.AddPassive(psv)
                for page in person.Page:
                    #pg=gameDataManager.getPage(page["name"])
                    pg=gameDataManager.getPage(page)
                    per.AddPage(pg)
                t+=1
                #if DEBUG:
                #    per.AddPowerLR(20,20,"debug")
                self.allies.AddPerson(per)
        
        self.ReceptionInit(dit["Reception"],dit["Enemy"])
        #self.DebugInit()

        for person in self.allies.characters:
            person.InitPassive()
        for person in self.enemies.characters:
            person.InitPassive()
        for person in self.allies.characters:
            person.RollPage()
            person.RollPage()
            person.RollPage()
        for person in self.enemies.characters:
            person.RollPage()
            person.RollPage()
            person.RollPage()
    def DebugInit(self):
        stdResistance={"Slash":1.0,"Pierce":1.0,"Blunt":1.0,"Slash_s":1.0,"Pierce_s":1.0,"Blunt_s":1.0}
        debugResistance={"Slash":0,"Pierce":0,"Blunt":0,"Slash_s":0,"Pierce_s":0,"Blunt_s":0}
        debugResistance2={"Slash":2,"Pierce":2,"Blunt":2,"Slash_s":2,"Pierce_s":2,"Blunt_s":2}
        myo=Myo(201,1)
        myo.team="Ally"
        #myo.resistance=debugResistance
        rb=Rabbit(202,2)
        rb.team="Ally"
        rb.resistance=debugResistance2
        #sb
        myo.AddPowerLR(50,50,"debug")
        rb.AddPowerLR(50,50,"debug")
        myo.lightMax=6
        myo.light=6
        myo.buffs.AddBuff("Charge",20)
        myo.AddPassive(u"Reindeer改造手术")
        myo.AddPassive(u"脑波充能集束犄角")
        myo.AddPassive(u"Rhino改造手术")
        myo.AddPassive(u"生物充能同步外皮")
        myo.AddPassive(u"极限冲击")
        myo.AddPassive(u"第4集团军总指挥")
        rb.AddPassive(u"强化充能")
        rb.AddPassive(u"进阶充能")
        yae=Yae(203,3)
        yae.team="Ally"
        yae.AddPowerLR(10,10,"debug")
        yae.AddPassive(u"围捕烟气")
        yae.AddPassive(u"致瘾烟气")
        yae.AddPassive(u"清醒烟气")
        lowell=Lowell(204,4)
        lowell.team="Ally"
        lowell.AddPowerLR(10,10,"debug")
        lowell.AddPassive(u"不稳定的神采")
        lowell.AddPassive(u"炽热之刃")
        lowell.AddPassive(u"凤翎之盾")
        lowell.AddPassive(u"拥火卧薪")
        lowell.AddPassive(u"狻猊騰雲")
        redmist=RedMist(205,5)
        redmist.team="Ally"
        redmist.AddPowerLR(10,10,"debug")
        redmist.AddPassive(u"冲锋姿态")
        redmist.AddPassive(u"概率变动")
        redmist.AddPassive(u"调整呼吸")
        redmist.AddPassive(u"高难杂技")
        redmist.AddPassive(u"血液爆炸")
        for i in range(9):
            rb.RollPage()
            myo.RollPage()
            yae.RollPage()
            lowell.RollPage()
            redmist.RollPage()
        self.name="redmist"
        self.ReceptionInit()
        self.allies.AddPerson(myo)
        self.allies.AddPerson(rb)
        self.allies.AddPerson(redmist)
    def FindAlly(self,id):
        return self.allies.FindCharacter(id)
    def FindEnemy(self,id):
        return self.enemies.FindCharacter(id)
    def JudgeVictory(self):
        return self.enemies.JudgeDeath()
    def JudgeDefeat(self):
        return self.allies.JudgeDeath()
    def RollSpeed(self):
        self.allies.RollSpeed()
        self.enemies.RollSpeed()
    def RandGen(self):
        for character in self.enemies.characters:
            if character.JudgeStagger() or character.JudgeDeath():
                continue
            for i in range(100):
                sdice=None
                for dice in character.speedDices:
                    if not dice.haveTarget:
                        sdice=dice
                        break
                if not self.allies.JudgeDeath():
                    n=len(self.allies.characters)
                    targetC=self.allies.characters[random.randint(0,n-1)]
                    while targetC.JudgeDeath():
                        targetC=self.allies.characters[random.randint(0,n-1)]
                    m=len(targetC.speedDices)
                    target=targetC.speedDices[random.randint(0,m-1)]
                    k=len(character.handPages)
                    if sdice!=None and k!=0:
                        character.EquipPage(dice,target,character.handPages[random.randint(0,k-1)].id,True)  
    def AutoBattle(self):
        for character in self.allies.characters:
            if character.JudgeStagger() or character.JudgeDeath():
                continue
            for i in range(100):
                sdice=None
                for dice in character.speedDices:
                    if not dice.haveTarget:
                        sdice=dice
                        break
                if not self.enemies.JudgeDeath():
                    n=len(self.enemies.characters)
                    targetC=self.enemies.characters[random.randint(0,n-1)]
                    while targetC.JudgeDeath():
                        targetC=self.enemies.characters[random.randint(0,n-1)]
                    m=len(targetC.speedDices)
                    target=targetC.speedDices[random.randint(0,m-1)]
                    k=len(character.handPages)
                    if sdice!=None and k!=0:
                        character.EquipPage(dice,target,character.handPages[random.randint(0,k-1)].id,True)
    def GenerateRandomDice(self):
        if not self.allies.JudgeDeath():
            n=len(self.allies.characters)
            targetC=self.allies.characters[random.randint(0,n-1)]
            while targetC.JudgeDeath():
                targetC=self.allies.characters[random.randint(0,n-1)]
            m=len(targetC.speedDices)
            target=targetC.speedDices[random.randint(0,m-1)]
            return target
        return None
    def GenerateStrategy(self):
        #non llm
        if self.name=="rnfmabj":
            yang=self.enemies.characters[0]
            if yang.stage==1:
                lhand=yang.leftHand
                rhand=yang.rightHand
                if not self.allies.JudgeDeath():
                    if not yang.JudgeStagger():
                        target=self.GenerateRandomDice()
                        yang.EquipPage(yang.speedDices[0],target,yang.pages[0].id,True)  
                        target=self.GenerateRandomDice()
                        yang.EquipPage(yang.speedDices[1],target,yang.pages[1].id,True)  
                        target=self.GenerateRandomDice()
                        yang.EquipPage(yang.speedDices[2],target,yang.pages[2].id,True)
                    if self.round%4==1:
                        llst=[lhand.pages[0].id,lhand.pages[2].id,lhand.pages[1].id]
                    elif self.round%4==2:
                        llst=[lhand.pages[4].id,lhand.pages[2].id,lhand.pages[0].id]
                    elif self.round%4==3:
                        llst=[lhand.pages[2].id,lhand.pages[1].id,lhand.pages[3].id]
                    else:
                        llst=[lhand.pages[0].id,lhand.pages[1].id,lhand.pages[5].id]
                    if self.round%4==1:
                        rlst=[rhand.pages[1].id,rhand.pages[2].id,rhand.pages[0].id]
                    elif self.round%4==2:
                        rlst=[rhand.pages[0].id,rhand.pages[1].id,rhand.pages[2].id]
                    elif self.round%4==3:
                        rlst=[rhand.pages[0].id,rhand.pages[2].id,rhand.pages[3].id]
                    else:
                        rlst=[rhand.pages[5].id,rhand.pages[0].id,rhand.pages[2].id]
                    n=3
                    if self.round==1:
                        n=2
                    for i in range(n):
                        if not lhand.locked:
                            target=self.GenerateRandomDice()
                            lhand.EquipPage(lhand.speedDices[i],target,llst[i],True)
                        if not rhand.locked:
                            target=self.GenerateRandomDice()
                            rhand.EquipPage(rhand.speedDices[i],target,rlst[i],True)
            elif yang.stage==2:
                if not self.allies.JudgeDeath():
                    if not yang.JudgeStagger():
                        target=self.GenerateRandomDice()
                        yang.EquipPage(yang.speedDices[0],target,yang.pages[6].id,True)  
                        target=self.GenerateRandomDice()
                        yang.EquipPage(yang.speedDices[1],target,yang.pages[7].id,True)  
                        target=self.GenerateRandomDice()
                        yang.EquipPage(yang.speedDices[2],target,yang.pages[8].id,True) 
            else:
                lhand=yang.leftHand
                rhand=yang.rightHand
                if not self.allies.JudgeDeath():
                    if not yang.JudgeStagger():
                        if yang.useAllrcv:
                            target=self.GenerateRandomDice()
                            yang.EquipPage(yang.speedDices[0],target,yang.pages[3].id,True)  
                            target=self.GenerateRandomDice()
                            yang.EquipPage(yang.speedDices[1],target,yang.pages[4].id,True)  
                            target=self.GenerateRandomDice()
                            yang.EquipPage(yang.speedDices[2],target,yang.pages[5].id,True)
                        else:
                            target=self.GenerateRandomDice()
                            yang.EquipPage(yang.speedDices[0],target,yang.pages[0].id,True)  
                            target=self.GenerateRandomDice()
                            yang.EquipPage(yang.speedDices[1],target,yang.pages[1].id,True)  
                            target=self.GenerateRandomDice()
                            yang.EquipPage(yang.speedDices[2],target,yang.pages[3].id,True)
                    if self.round%2==0:
                        llst=[lhand.pages[4].id,lhand.pages[2].id,lhand.pages[0].id]
                    else:
                        llst=[lhand.pages[0].id,lhand.pages[1].id,lhand.pages[5].id]
                    if self.round%2==0:
                        rlst=[rhand.pages[0].id,rhand.pages[1].id,rhand.pages[2].id]
                    else:
                        rlst=[rhand.pages[5].id,rhand.pages[0].id,rhand.pages[2].id]
                    for i in range(3):
                        if not lhand.locked:
                            target=self.GenerateRandomDice()
                            lhand.EquipPage(lhand.speedDices[i],target,llst[i],True)
                        if not rhand.locked:
                            target=self.GenerateRandomDice()
                            rhand.EquipPage(rhand.speedDices[i],target,rlst[i],True)
            if yang.countDown==0 and not yang.JudgeStagger():
                yang.EquipPage(yang.speedDices[3],target,yang.pages[10].id,True)  
                yang.countDown=2  
            yang.countDown-=1       
            yang.countDown=max(yang.countDown,0)
        elif self.name=="myo":
            myo=self.enemies.characters[0]
            flg=False
            for page in myo.handPages:
                if page.name==u"狂暴血刃":
                    id=page.id
                    flg=True
            if myo.light>=6 and flg and myo.buffs.GetBuffCount("Charge")==20 and (not myo.JudgeStagger()) and (not myo.JudgeDeath()):
                target=self.GenerateRandomDice()
                myo.EquipPage(myo.speedDices[0],target,id,True)
            self.RandGen()
        elif self.name=="redmist":
            red=self.enemies.characters[0]
            if red.countDown==0:
                flg=False
                for page in red.handPages:
                    if page.name==u"尸横遍野":
                        id=page.id
                        flg=True
                if red.light>=6 and flg and (not red.JudgeStagger()) and (not red.JudgeDeath()):
                    target=self.GenerateRandomDice()
                    red.EquipPage(red.speedDices[0],target,id,True)
                    red.countDown=2
            self.RandGen()
        else:
            self.RandGen()
        #Waiting for llm to generate
        pass
    def RoundStart(self):
        self.round+=1
        if gameDataManager.GAME_DIFFICULTY==0:
            for person in self.allies.characters:
                person.AddBuff("Strength",2) 
                person.AddBuff("Endurance",2) 
        elif gameDataManager.GAME_DIFFICULTY==2:
            for person in self.enemies.characters:
                if gameDataManager.STAGE.getStageIndex() >= 2:
                    person.AddBuff("Strength",1) 
                    person.AddBuff("Endurance",1) 
                if gameDataManager.STAGE.getStageIndex() >= 4:
                    person.AddBuff("Strength",1) 
                    person.AddBuff("Endurance",1) 
                if gameDataManager.STAGE.getStageIndex() >= 5:
                    person.AddBuff("Strength",1) 
                    person.AddBuff("Endurance",1) 
        self.allies.RoundStart()
        self.enemies.RoundStart()
        self.display.DisplayBattle()#----------
    def FirstSpace(self):
        self.RollSpeed()
        self.GenerateStrategy()
        self.display.DisplayBattle()#----------
    def CheckPage(self,ally,page):
        Ally=self.FindAlly(ally)
        pg=Ally.FindPage(page)
        if pg.charge and Ally.buffs.GetBuffCount("Charge")!=20:
            return False
        return pg.lightCost<=Ally.light
    def SelectPage(self,ally,enemy,allydice,enemydice,page):
        Ally=self.FindAlly(ally)
        Enemy=self.FindEnemy(enemy)
        Allydice=Ally.FindDice(allydice)
        Enemydice=Enemy.FindDice(enemydice)
        return Ally.EquipPage(Allydice,Enemydice,page)
    def DeselectPage(self,ally,allydice):
        Ally=self.FindAlly(ally)
        Allydice=Ally.FindDice(allydice)
        Ally.UnequipPage(Allydice)
    def SecondSpace(self):
        gameDataManager.Dit={"combatPlayer":[],"combatList":[]}
        battlelist=[]
        aoelist=[]
        for person in self.allies.characters:
            gameDataManager.Dit["combatPlayer"].append(GeneratespCharDict(person))
        for person in self.enemies.characters:
            gameDataManager.Dit["combatPlayer"].append(GeneratespCharDict(person))
        for person in self.allies.characters:
            for dice in person.speedDices:
                if not dice.haveTarget:
                    continue
                dice.page.used=False
                dice.page.pageBuff.StartBattle()
                for cdice in dice.page.counterDices:
                    person.AddDefense(cdice)
                if dice.page.pageType=="Individual" or dice.page.pageType=="Summation":
                    aoelist.append(dice)
                    continue
                if dice.IsClashing():
                    if(dice.Target.speed>dice.speed):
                        dice.Target.CalcWeight()
                        battlelist.append(dice.Target)
                    else:
                        dice.CalcWeight()
                        battlelist.append(dice)
                else:
                    dice.CalcWeight()
                    battlelist.append(dice)
        for person in self.enemies.characters:
            for dice in person.speedDices:
                if not dice.haveTarget:
                    continue
                dice.page.used=False
                dice.page.pageBuff.StartBattle()
                if dice.page.pageType=="Individual" or dice.page.pageType=="Summation":
                    aoelist.append(dice)
                    continue
                if dice.page.pageBuff.special=="YangNoPower":
                    dice.Target.affiliateCharacter.havePower=False
                for cdice in dice.page.counterDices:
                    person.AddDefense(cdice)
                if dice.IsClashing():
                    continue
                else:
                    dice.CalcWeight()
                    battlelist.append(dice)
        aoelist=sorted(aoelist,key=lambda x:x.speed,reverse=True)
        for dice in aoelist:
            if dice.affiliateCharacter.JudgeStagger() or dice.affiliateCharacter.JudgeDeath():
                continue
            if dice.affiliateCharacter.HavePassive(u"缪的技巧")>0:
                if dice.Target.isbreak:
                    dsp=0
                else:
                    dsp=dice.Target.speed
                pb=min(max(math.floor((dice.speed-dsp)/2),0),5)
                if pb!=0:
                    dice.affiliateCharacter.AddPowerBuff("Total",pb,pb,"Myo")
            char=[]
            dices=[]
            pbl=[]
            pbd={}
            for character in dice.affiliateCharacter.againstTeam.characters:
                if character.JudgeDeath():
                    continue
                char.append(character)
                if(dice.Target.affiliateCharacter.id==character.id):
                    dices.append(dice.Target)
                for tdice in dice.massTarget:
                    if tdice.affiliateCharacter.id==character.id:
                        dices.append(tdice)
            for tdice in dices:
                if tdice.haveTarget and tdice.affiliateCharacter.HavePassive(u"缪的技巧")>0:
                    if tdice.Target.isbreak:
                        dsp=0
                    else:
                        dsp=tdice.Target.speed
                    pb=min(max(math.floor((tdice.speed-dsp)/2),0),5)
                    if pb!=0:
                        tdice.affiliateCharacter.AddPowerBuff("Total",pb,pb,"Myo")
                pbd[tdice.affiliateCharacter.id]=tdice.affiliateCharacter.powerBuff
            for character in char:
                pbl.append(pbd[character.id])
            PageMassAttack(dice.page,char,dices,dice.affiliateCharacter.powerBuff,pbl)
            dice.affiliateCharacter.ClearPowerBuff("Myo")
            for character in dice.affiliateCharacter.againstTeam.characters:
                character.ClearPowerBuff("Myo")
        #AOE  ^
        battlelist=sorted(battlelist,key=lambda x:x.weight,reverse=True)
        for dice in battlelist:
            #print(f"{dice.id}debug")
            if dice.affiliateCharacter.JudgeStagger() or dice.affiliateCharacter.JudgeDeath():
                continue
            if dice.IsClashing():
                if dice.Target.affiliateCharacter.JudgeDeath():
                    continue
                elif dice.Target.affiliateCharacter.JudgeStagger():
                    if dice.affiliateCharacter.HavePassive(u"缪的技巧")>0:
                        if dice.Target.isbreak:
                            dsp=0
                        else:
                            dsp=dice.Target.speed
                        pb=min(max(math.floor((dice.speed-dsp)/2),0),5)
                        if pb!=0:
                            dice.affiliateCharacter.AddPowerBuff("Total",pb,pb,"Myo")
                    if dice.page.pageBuff.special=="MyoPointShoot" and dice.speed>=6:
                        dice.affiliateCharacter.AddPowerBuff("Total",2,2,"Myo")
                    PageAttack(dice.page,dice.Target.affiliateCharacter,dice.affiliateCharacter.powerBuff)
                else:
                    if dice.affiliateCharacter.HavePassive(u"缪的技巧")>0:
                        if dice.Target.isbreak:
                            dsp=0
                        else:
                            dsp=dice.Target.speed
                        pb=min(max(math.floor((dice.speed-dsp)/2),0),5)
                        if pb!=0:
                            dice.affiliateCharacter.AddPowerBuff("Total",pb,pb,"Myo")
                    if dice.Target.affiliateCharacter.HavePassive(u"缪的技巧")>0:
                        if dice.Target.Target.isbreak:
                            dsp=0
                        else:
                            dsp=dice.Target.Target.speed
                        pb=min(max(math.floor((dice.Target.speed-dsp)/2),0),5)
                        if pb!=0:
                            dice.Target.affiliateCharacter.AddPowerBuff("Total",pb,pb,"Myo")
                    if dice.page.pageBuff.special=="MyoPointShoot" and dice.speed>=6:
                        dice.affiliateCharacter.AddPowerBuff("Total",2,2,"Myo")
                    if dice.Target.page.pageBuff.special=="MyoPointShoot" and dice.Target.speed>=6:
                        dice.Target.affiliateCharacter.AddPowerBuff("Total",2,2,"Myo")
                    PageClashing(dice.page,dice.Target.page,dice.affiliateCharacter.powerBuff,dice.Target.affiliateCharacter.powerBuff)
            else:
                if dice.Target.affiliateCharacter.JudgeDeath():
                    continue
                if dice.affiliateCharacter.HavePassive(u"缪的技巧")>0:
                    if dice.Target.isbreak:
                        dsp=0
                    else:
                        dsp=dice.Target.speed
                    pb=min(max(math.floor((dice.speed-dsp)/2),0),5)
                    if pb!=0:
                        dice.affiliateCharacter.AddPowerBuff("Total",pb,pb,"Myo")
                if dice.page.pageBuff.special=="MyoPointShoot" and dice.speed>=6:
                    dice.affiliateCharacter.AddPowerBuff("Total",2,2,"Myo")
                PageAttack(dice.page,dice.Target.affiliateCharacter,dice.affiliateCharacter.powerBuff)
            dice.affiliateCharacter.ClearPowerBuff("Myo")
            dice.Target.affiliateCharacter.ClearPowerBuff("Myo")
        fdit=None
        for dit in reversed(gameDataManager.Dit["combatList"]):
            if dit["CombatType"]==CombatType.AOE:
                break
            if fdit==None:
                dit["consist"]="Null"
                fdit=dit
            else:
                if (fdit["char1"]==dit["char1"] and fdit["char2"]==dit["char2"])or(fdit["char1"]==dit["char2"] and fdit["char2"]==dit["char1"]):
                    dit["consist"]="All"
                elif(fdit["char1"]==dit["char1"] or fdit["char2"]==dit["char1"]):
                    dit["consist"]="char1"
                elif(fdit["char1"]==dit["char2"] or fdit["char2"]==dit["char2"]):
                    dit["consist"]="char2"
                else:
                    dit["consist"]="Null"
                fdit=dit
        self.display.DisplayBattle()#----------
    def RoundEnd(self):
        gameDataManager.curDict={}
        gameDataManager.curDict["CombatType"]=CombatType.RoundEnd
        gameDataManager.curDict["RoundEndAnime"]={"lasFrame":30,"dmgDelay":5}
        gameDataManager.curDict["joiner"]=[]
        for person in self.allies.characters:
            if not person.JudgeDeath():
                gameDataManager.curDict["joiner"].append({"id": person.id, "pos": person.pos})
                gameDataManager.curDict[person.id] = {}
                gameDataManager.curDict[person.id]["action"] = CharSD.Common
                if person.JudgeStagger():
                    gameDataManager.curDict[person.id]["action"]=CharSD.Hurt
                gameDataManager.curDict[person.id]["beforeCombat"]={}
                gameDataManager.curDict[person.id]["beforeCombat"]["isHaveCard"]=False
                gameDataManager.curDict[person.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(person)
                gameDataManager.curDict[person.id]["combatEffect"]=[]
        for person in self.enemies.characters:
            if not person.JudgeDeath():
                gameDataManager.curDict["joiner"].append({"id":person.id,"pos":person.pos})
                gameDataManager.curDict[person.id]={}
                gameDataManager.curDict[person.id]["action"]=CharSD.Common
                if person.JudgeStagger():
                    gameDataManager.curDict[person.id]["action"]=CharSD.Hurt
                gameDataManager.curDict[person.id]["beforeCombat"]={}
                gameDataManager.curDict[person.id]["beforeCombat"]["isHaveCard"]=False
                gameDataManager.curDict[person.id]["beforeCombat"]["infoBar"]=GenerateInfoDict(person)
                gameDataManager.curDict[person.id]["combatEffect"]=[]
        self.allies.RoundEnd()
        self.enemies.RoundEnd()
        for person in self.allies.characters:
            flg=False
            for dit in gameDataManager.curDict["joiner"]:
                if dit["id"]==person.id:
                    flg=True
            if not flg:
                continue
            if person.id not in gameDataManager.curDict:
                gameDataManager.curDict[person.id] = {}
            gameDataManager.curDict[person.id]["afterCombat"] = {}
            if person.JudgeDeath():
                gameDataManager.curDict[person.id]["afterCombat"]["state"]=CharState.Dead
            elif person.JudgeStagger():
                gameDataManager.curDict[person.id]["afterCombat"]["state"]=CharState.Stagger
            else:
                gameDataManager.curDict[person.id]["afterCombat"]["state"]=CharState.Common
            gameDataManager.curDict[person.id]["afterCombat"]["infoBar"]=GenerateInfoDict(person)
        for person in self.enemies.characters:
            flg=False
            for dit in gameDataManager.curDict["joiner"]:
                if dit["id"]==person.id:
                    flg=True
            if not flg:
                continue
            if person.id not in gameDataManager.curDict:
                gameDataManager.curDict[person.id] = {}
            gameDataManager.curDict[person.id]["afterCombat"] = {}
            if person.JudgeDeath():
                gameDataManager.curDict[person.id]["afterCombat"]["state"]=CharState.Dead
            elif person.JudgeStagger():
                gameDataManager.curDict[person.id]["afterCombat"]["state"]=CharState.Stagger
            else:
                gameDataManager.curDict[person.id]["afterCombat"]["state"]=CharState.Common
            gameDataManager.curDict[person.id]["afterCombat"]["infoBar"]=GenerateInfoDict(person)
        gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        if self.JudgeVictory():
            from SceneSystem.BattleScene import BattleResult
            gameDataManager.curDict={}
            gameDataManager.curDict["CombatType"]=CombatType.BattleResult
            gameDataManager.curDict["result"]=BattleResult.Win
            gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        if self.JudgeDefeat():
            from SceneSystem.BattleScene import BattleResult
            gameDataManager.curDict={}
            gameDataManager.curDict["CombatType"]=CombatType.BattleResult
            gameDataManager.curDict["result"]=BattleResult.Defeat
            gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        gameDataManager.curDict={}
        gameDataManager.curDict["CombatType"]=CombatType.RoundChange
        gameDataManager.Dit["combatList"].append(gameDataManager.curDict)
        return gameDataManager.Dit