from GameDataManager import gameDataManager,CharacterData

from Data.instance import *
from Data.types import *

@instance
class DealPromotion:
    def __init__(self):
        pass
    def gainUpgrade(self,charName,choice):
        char = gameDataManager.getAlly(charName)
        if isinstance(char,CharacterData):
            if choice in gameDataManager.CUSTOM_CHARUPGRADEPOOL.keys():
                content = gameDataManager.CUSTOM_CHARUPGRADEPOOL[choice]
                if "Modifier" in content.keys():
                    for modifier in content["Modifier"]:
                        if modifier["attr"] == "addPassive":
                            char.addPassive(modifier["val"],gameDataManager.CUSTOM_PASSIVEPOOL)
                            #print(char.Passive)
                        elif modifier["attr"] == "delPassive":
                            char.delPassive(modifier["val"])
                        else:
                            char.modifyAttribute(modifier["attr"],self.decodeUpgradeVal(modifier["val"]))
    def decodeUpgradeVal(self,val):
        if isinstance(val,list) and len(val) == 2:
            return Vector2(val[0],val[1])
        else:
            return val
    def gainPassive(self,charName,choice):
        char = gameDataManager.getAlly(charName)
        if isinstance(char,CharacterData):
            char.addPassive(choice,gameDataManager.CUSTOM_PASSIVEPOOL)

dealPromotion = DealPromotion()

            