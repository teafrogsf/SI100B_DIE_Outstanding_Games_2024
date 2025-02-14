from GameDataManager import gameDataManager

from RenderSystem.prefab.UISelectionBar import GenSelectBarType

from Data.instance import *
from collections import Counter
import random,time

@instance
class GenPromotion:
    def __init__(self):
        self.dicePassive = ["速战速决2","速战速决","速战速决3"]
        self.diceUpgrade = ["速战速决+","速战速决++","速战速决+++"]
        self.Random = random.Random(time.time())
    def genUpgrade(self):
        info = gameDataManager.STAGE.getStageInfo()
        _BarNum = info["upgradeBarNum"]
        _ChoiceNum = info["upgradeChoiceNum"]
        dit = {}
        for allyName,ally in gameDataManager.getAllys().items():
            dit[allyName] = []
            
            for k in range(_BarNum):
                choice = []
                if k == 0:
                    if self.dicePassive[1] in ally.Passive:
                        if self.Random.random() <= info["DiceUpgrade"][1]:
                            choice.append(self.diceUpgrade[1])
                    elif self.dicePassive[2] in ally.Passive:
                        if self.Random.random() <= info["DiceUpgrade"][2]:
                            choice.append(self.diceUpgrade[2])
                    elif not self.dicePassive[0] in ally.Passive:
                        if self.Random.random() <= info["DiceUpgrade"][0]:
                            choice.append(self.diceUpgrade[0])
                choice.extend(self.genUpgradeChoice(_ChoiceNum-len(choice)))
                dit[allyName].append({
                    "type":GenSelectBarType.Upgrade,
                    "list":choice
                })
        return dit
    def genUpgradeChoice(self,amt):
        return self.Random.sample(gameDataManager.CUSTOM_CHARUPGRADEPOOL_List,amt)
    def genPassive(self):
        info = gameDataManager.STAGE.getStageInfo()
        _BarNum = info["passiveBarNum"]
        _ChoiceNum = info["passiveChoiceNum"]
        _Curve = info["passiveCurve"]
        _curvePin = 0
        dit = {}
        for allyName,ally in gameDataManager.getAllys().items():
            dit[allyName] = []
            _psvLis = gameDataManager.getAlly(allyName).Passive
            _forbidLis = [p for p in _psvLis if gameDataManager.getCustomPassive(p)["Mutiable"] == False]
            for k in range(_BarNum):
                dit[allyName].append({
                    "type":GenSelectBarType.Passive,
                    "list":self.genPassiveChoice(_Curve[_curvePin],_ChoiceNum,_forbidLis)
                })
                if _curvePin < len(_Curve)-1:
                    _curvePin += 1
            _curvePin = 0
        return dit
    def genPassiveChoice(self,_Curve,amt,_forbidLis):
        _rawLis = []
        for lv in range(1,6):
            _rawLis.extend([lv]*(_Curve[lv-1]))
        self.Random.shuffle(_rawLis)
        _lvLis = self.Random.sample(_rawLis,amt)
        _lvLis.sort(reverse=True)
        _cnt = Counter(_lvLis)
        _deLevel = 0
        _res = []
        for lvv,vak in _cnt.items():
            _trVal = vak+_deLevel
            _safeLis = [p for p in gameDataManager.CUSTOM_PASSIVEPOOL_LevelList[lvv] if not p in _forbidLis]
            _deLevel = max(0,_trVal-len(_safeLis))
            _res.extend(self.Random.sample(_safeLis,min(len(_safeLis),_trVal)))
            #print(lvv,_trVal,_deLevel)
        return _res
    def genInitialCharData(self,name,SDname):
        from GameDataManager import CharacterData
        return CharacterData(name,SDname,self.Random.randint(80,120),self.Random.randint(40,60),self.genOriResis()
                             ,self.Random.randint(2,4),self.Random.randint(6,8),1,self.Random.randint(3,5)
                             )
    def genOriResis(self):
        res={"Slash":1,"Pierce":1,"Blunt":1,"Slash_s":1,"Pierce_s":1,"Blunt_s":1}
        _h = self.Random.randint(0,7)
        for tp in ["Slash","Pierce","Blunt"]:
            if _h&1 == 1:
                _d = self.Random.random()
                if _d >= 0.6:
                    res[tp] -= 0.5
                elif _d <= 0.4:
                    res[tp] += 0.5
            _h >>= 1
        _h = self.Random.randint(0,7)
        for tp in ["Slash_s","Pierce_s","Blunt_s"]:
            if _h&1 == 1:
                _d = self.Random.random()
                if _d >= 0.6:
                    res[tp] -= 0.5
                elif _d <= 0.4:
                    res[tp] += 0.5
            _h >>= 1
        return res            


genPromotion = GenPromotion()
            