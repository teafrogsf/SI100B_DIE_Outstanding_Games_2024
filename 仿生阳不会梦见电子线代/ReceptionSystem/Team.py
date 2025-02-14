from ReceptionSystem.SpeedDice import SpeedDice
class Team:
    def __init__(self,team):
        self.characters=[]
        self.team=team
        self.emotionLevel=0
        self.against=None
    def FindCharacter(self,id):
        for person in self.characters:
            if(person.id==id):
                return person
        return None
    def JudgeDeath(self):
        flg=0
        for person in self.characters:
            if(not person.JudgeDeath()):
                flg=1
        return flg==0
    def RollSpeed(self):
        for person in self.characters:
            person.RollSpeed(person.speedBuff)
    def AddPerson(self,character):
        self.characters.append(character)
        character.affiliateTeam=self
        character.againstTeam=self.against
    def GetEmotion(self):
        s=0
        n=0
        for person in self.characters:
            if person.JudgeDeath==False:
                s+=person.emotion.emotionLevel
                n+=1
        if n==0:
            return -1
        else:
            return s//n
    def UpgadeEmotion(self):
        self.emotionLevel+=1
    def RoundStart(self):
        for person in reversed(self.characters):
            person.RollBackPage()
            person.ClearDefense()
        for person in reversed(self.characters):    
            person.RoundStart()
        for person in reversed(self.characters):
            person.buffs.RoundStart()
        flg=0
        while(self.emotionLevel<self.GetEmotion()):
            flg=1
            self.UpgadeEmotion()
        for person in self.characters:
            el=person.emotion.emotionLevel
            person.emotion.RoundStart()
            if person.HavePassive(u"卡莉")>0:
                person.getLight+=1
                person.rollPage+=1
            if(el<person.emotion.emotionLevel):
                for page in person.handPages:
                    if page.pageBuff.special=="EmotionLevelDecost":
                        if el<page.pageBuff.elv and person.emotion.emotionLevel>=page.pageBuff.elv:
                            page.lightCost-=page.pageBuff.cos
                for page in person.pages:
                    if page.pageBuff.special=="EmotionLevelDecost":
                        if el<page.pageBuff.elv and person.emotion.emotionLevel>=page.pageBuff.elv:
                            page.lightCost-=page.pageBuff.cos
                if el<3 and person.emotion.emotionLevel>=3 and person.HavePassive(u"速战速决3")>0:
                    person.countDices+=1
                    person.speedDices.append(SpeedDice(person.speedL,person.speedR,person,person.countDices))
                    if person.JudgeStagger():
                        person.speedDices[len(person.speedDices)-1].isBreak=True
                        person.speedDices[len(person.speedDices)-1].speed=-1
                if el<4 and person.emotion.emotionLevel>=4:
                    person.countDices+=1
                    person.speedDices.append(SpeedDice(person.speedL,person.speedR,person,person.countDices))
                    if person.JudgeStagger():
                        person.speedDices[len(person.speedDices)-1].isBreak=True
                        person.speedDices[len(person.speedDices)-1].speed=-1
                for i in range(person.HavePassive(u"所向无前")):
                    person.AddBuff("Strength",1)
                    person.AddBuff("Endurance",1)
                if person.HavePassive(u"坚如磐石")>0:
                    hl=min(int(person.healthMax*0.15),20)
                    person.RecoverHealth(hl,False)
                if person.HavePassive(u"常备不懈")>0:
                    if not person.JudgeStagger():
                        hl=int(person.healthMax*0.25)
                        person.RecoverStagger(hl,False)
                if el<1 and person.emotion.emotionLevel>=1 and person.HavePassive(u"卡莉")>0:
                    person.countDices+=1
                    person.speedDices.append(SpeedDice(person.speedL,person.speedR,person,person.countDices))
                    if person.JudgeStagger():
                        person.speedDices[len(person.speedDices)-1].isBreak=True
                        person.speedDices[len(person.speedDices)-1].speed=-1
                if el<2 and person.emotion.emotionLevel>=2 and person.HavePassive(u"卡莉")>0:
                    person.countDices+=1
                    person.speedDices.append(SpeedDice(person.speedL,person.speedR,person,person.countDices))
                    if person.JudgeStagger():
                        person.speedDices[len(person.speedDices)-1].isBreak=True
                        person.speedDices[len(person.speedDices)-1].speed=-1
                if el<3 and person.emotion.emotionLevel>=3 and person.HavePassive(u"十二收尾人")>0:
                    person.AddPowerLR(0,1,"passive")
                person.lightMax+=1
                person.light=person.lightMax
                person.RollPage()
            else:
                person.light+=person.getLight
                person.getLight=1 #Here
                person.light=min(person.light,person.lightMax)
            for i in range(person.rollPage):
                person.RollPage()
            if person.HavePassive(u"不完整的调律者"):
                for i in range(100):
                    if len(person.handPages)>=5:
                        break
                    person.RollPage()
            person.rollPage=1
            if(person.isStagger==1):
                person.isStagger=2
            elif(person.isStagger==2):
                person.ClearStagger()
            person.lightHave=person.light
    def RoundEnd(self):
        for person in reversed(self.characters):
            person.havePower=True
            person.RoundEnd()
            person.buffs.RoundEnd()
            for buff in reversed(person.nextBuffs.buffs):
                person.AddBuff(buff.name,buff.count)
            person.ClearDamageBuff("roundend")
            person.nextBuffs.Clear()