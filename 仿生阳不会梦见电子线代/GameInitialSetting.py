from GameDataManager import gameDataManager as gdm
from GameDataManager import CharacterData
from RogueSystem.GenPromotion import genPromotion

from Data.instance import *
import copy,random

@instance
class GdataDecoder:
    def __init__(self):
        print("INIT: GData decode II")
        gdm.loadPrefabPage()
        gdm.STAGE.loadStageInfo("UltiStageInfo.json")
        #gdm.STAGE.loadStageInfo("StageInfo.json")


@instance
class GameInitialSetting:
    def __init__(self):
        self.gdataDecoder = GdataDecoder()

        self.initialCharacter()
        self.initialPage()
        self.debugSetting()
    def initialCharacter(self):
        '''
        res={"Slash":0.5,"Pierce":0.5,"Blunt":0.5,"Slash_s":0.25,"Pierce_s":0.25,"Blunt_s":0.25}
        gdm.addAllyCharacter(CharacterData("马库库","Malkuth",200,100,copy.deepcopy(res),4,7,2,10))
        gdm.addAllyCharacter(CharacterData("缪缪","Myo",200,100,copy.deepcopy(res),5,6,2,10))
        gdm.addAllyCharacter(CharacterData("阳","YangN",300,150,copy.deepcopy(res),3,9,2,10))
        gdm.addAllyCharacter(CharacterData("xlpj","Rabbit",200,100,copy.deepcopy(res),1,4,1,10))
        '''
        gdm.addAllyCharacter(genPromotion.genInitialCharData("Malkuth","Malkuth"))
        gdm.addAllyCharacter(genPromotion.genInitialCharData("Netzach","Netzach"))
        gdm.addAllyCharacter(genPromotion.genInitialCharData("Yan","YangN"))
        gdm.addAllyCharacter(genPromotion.genInitialCharData("Hod","Hod"))
        gdm.addAllyCharacter(genPromotion.genInitialCharData("Tiphereth","Tiphereth"))
        
        for ally in gdm.getAllys().values():
            if isinstance(ally,CharacterData):
                ally.addPassive("速战速决",gdm.CUSTOM_PASSIVEPOOL)
        
    def initialPage(self):
        for ally in gdm.getAllys().values():
            if isinstance(ally,CharacterData):
                while len(ally.Page) < 9:
                    _cardNam = random.sample(gdm.CUSTOM_PAGEPOOL,1)[0]["name"]
                    if gdm.PAGE_POOL[_cardNam]["amt"] > 0:
                        ally.Page.append(gdm.getCustomCard(_cardNam))
                        gdm.modifyCustomPageAmt(_cardNam,-1)
                gdm.modifyAllyCards(ally.name,ally.Page)
    def debugSetting(self):
        return
        #gdm.STAGE.stageCur = 4
        #gdm.GAME_DIFFICULTY = 1
        #gdm.FLAG_DEFEAT = True

gameInitialSetting = GameInitialSetting()