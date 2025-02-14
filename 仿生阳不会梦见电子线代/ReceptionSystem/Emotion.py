from RenderSystem.sceneRenderer.BattleCombatRenderer import CombatType,CombatEffectType
from RenderSystem.prefab.UITeam import EmotionType
from GameDataManager import gameDataManager
class Emotion:
    def __init__(self,greenCoin,redCoin,emotionLevel=0):
        self.greenCoin=greenCoin
        self.redCoin=redCoin
        self.emotionLevel=emotionLevel
        self.coins=[]
        self.affiliateCharacter=None
    def GetGreenCoin(self,number=1,show=True):
        print(f"{self.affiliateCharacter.name} get {number} green coin")
        if show:
            dic={}
            dic["effectType"]=CombatEffectType.Emotion
            dic["type"]=EmotionType.Green
            dic["count"]=number
            if not self.affiliateCharacter.id in gameDataManager.curDict.keys():
                gameDataManager.curDict[self.affiliateCharacter.id]={}
            if not "combatEffect" in gameDataManager.curDict[self.affiliateCharacter.id].keys():
                gameDataManager.curDict[self.affiliateCharacter.id]["combatEffect"]={}
            gameDataManager.curDict[self.affiliateCharacter.id]["combatEffect"].append(dic)
        self.greenCoin+=number
        for i in range(number):
            self.coins.append("Green")
    def GetRedCoin(self,number=1,show=True):
        print(f"{self.affiliateCharacter.name} get {number} red coin")
        if show:
            dic={}
            dic["effectType"]=CombatEffectType.Emotion
            dic["type"]=EmotionType.Red
            dic["count"]=number
            if not self.affiliateCharacter.id in gameDataManager.curDict.keys():
                gameDataManager.curDict[self.affiliateCharacter.id]={}
            if not "combatEffect" in gameDataManager.curDict[self.affiliateCharacter.id].keys():
                gameDataManager.curDict[self.affiliateCharacter.id]["combatEffect"]={}
            gameDataManager.curDict[self.affiliateCharacter.id]["combatEffect"].append(dic)
        self.redCoin+=number
        for i in range(number):
            self.coins.append("Red")
    def RoundStart(self):
        if self.emotionLevel==0 and self.greenCoin+self.redCoin>=3:
            self.EmotionUpgrade()
        if self.emotionLevel==1 and self.greenCoin+self.redCoin>=3:
            self.EmotionUpgrade()
        if self.emotionLevel==2 and self.greenCoin+self.redCoin>=5:
            self.EmotionUpgrade()
        if self.emotionLevel==3 and self.greenCoin+self.redCoin>=7:
            self.EmotionUpgrade()
        if self.emotionLevel==4 and self.greenCoin+self.redCoin>=9:
            self.EmotionUpgrade()
    def EmotionUpgrade(self):
        self.ClearCoin()
        self.emotionLevel+=1
    def ClearCoin(self):
        self.greenCoin,self.redCoin=0,0
        self.coins.clear()
class NoEmotion(Emotion):
    def __init__(self):
        super().__init__(0,0)
        self.emotionLevel=0
    def GetGreenCoin(self,number=1):
        pass
    def GetRedCoin(self,number=1):
        pass
    def RoundStart(self):
        pass
    def EmotionUpgrade(self):
        pass
    def ClearCoin(self):
        pass