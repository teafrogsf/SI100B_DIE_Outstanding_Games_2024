from RenderSystem.Canvas import *
from RenderSystem.ButtonSprite import *
from RenderSystem.MutiLineText import *
from RenderSystem.prefab.UICharacterInfo import UICharacterArray,UICharacterInfo
from RenderSystem.prefab.UISelectionBar import UIGeneratingSelectionBarArray

from RenderSystem.prefab.UIEntry import UIEntryLine
from RenderSystem.prefab.UICardSelection import UIGenCardBar
from RenderSystem.prefab.UICardArray import UIDisplayCard
from RenderSystem.prefab.UIGenProcess import UIGenProcess

from RenderSystem.prefab.UISimpleTip import UISimpleTipLine_800

from RenderSystem.prefab.UIDoubleCheckButton import UIExitSceneButton

from GameDataManager import gameDataManager
from RogueSystem.GenPromotion import genPromotion
from RogueSystem.DealPromotion import dealPromotion

import Data.fonts
from enum import Enum

class GenMode(Enum):
    Promotion = "promotion"
    Card = "card"

class GeneratingSceneRenderer(Canvas):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        super().__init__(name, screen, priority)
    def init(self):
        self.controlSys = {
            "Mode":None,
            "SelectedChar":None,
            "InGenerating":False
        }
        self.addChild(UIExitSceneButton("EXIT",self.screen,1000,self.scene))

        self.addChild(UICharacterArray("charArray",self.screen,0))
        self.addChild(UICharacterInfo("charInfo",self.screen,0))
        self.addChild(UIModeSelectionIcon("modePromotion",self.screen,10,"UI\\modePromotion"))
        self.addChild(UIModeSelectionIcon("modeGencard",self.screen,10,"UI\\modeGencard"))

        self.addChild(UIEntryLine("entryLine",self.screen,100,self.scene))
        self.addChild(UIGenCardBar("genCardBar",self.screen,50,self.scene))
        self.addChild(UIDisplayCard("displayCard",self.screen,250))
        self.addChild(UIGenProcess("genProcess",self.screen,200))

        self.addChild(UISimpleTipLine_800("tip_first",self.screen,10,u"前面需要左（键）"))
        self.addChild(UISimpleTipLine_800("tip_promotion",self.screen,10,u"接下来，选择会很有用"))
        self.addChild(UISimpleTipLine_800("tip_card",self.screen,10,u"献上文字吧！"))

        self.addChild(UIChoiceDetail("choiceDetail",self.screen,250))

        self.findChild("tip_first").setActive(True)
        self.findChild("tip_promotion").setActive(False)
        self.findChild("tip_card").setActive(False)

        self.findChild("choiceDetail").setActive(False)
        self.findChild("displayCard").setActive(False)
        self.findChild("displayCard").setScale(Vector2(0.9,0.9))
        self.findChild("genCardBar").setScale(Vector2(1.75,1.75))

        self.refreshModeDisplay()
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()

        self.setPos(Vector2(720,360))

        self.findChild("EXIT").setPos(Vector2(-480,-300))

        self.findChild("charArray").setPos(Vector2(-480,-200))
        self.findChild("charInfo").setPos(Vector2(-480,90))

        self.findChild("modePromotion").setPos(Vector2(60,-270))
        self.findChild("modeGencard").setPos(Vector2(370,-270))

        self.findChild("entryLine").setPos(Vector2(200,-120))
        self.findChild("genCardBar").setPos(Vector2(200,120))
        self.findChild("genProcess").setPos(Vector2(200,100))

        self.findChild("tip_promotion").setPos(Vector2(200,-180))
        self.findChild("tip_card").setPos(Vector2(200,-180))
        self.findChild("tip_first").setPos(Vector2(200,-180))

        for child in self.children:
            if child.name.find("SelectionBar") != -1:
                child.setPos(Vector2(200,0))
                child.setActive(False)
    def update(self):
        super().update()
        hcard = self.findChild("genCardBar").HighlightCard
        if hcard == None:
            self.findChild("displayCard").setActive(False)
        elif self.controlSys["Mode"] != GenMode.Card:
            self.findChild("displayCard").setActive(False)
        else:
            self.findChild("displayCard").setActive(True)
            self.findChild("displayCard").resetValue(hcard["cardDit"]["card"])
            self.findChild("displayCard").setPos(hcard["worldPos"]()-Vector2(720,360)+Vector2(0,-300))
        
        if self.controlSys["Mode"] == GenMode.Promotion:
            info = None
            for child in self.children:
                if child.name.find("SelectionBar") != -1 and child.active:
                    info = child.HighlightChoice
            if info == None:
                self.findChild("choiceDetail").setActive(False)
            else:
                self.findChild("choiceDetail").setActive(True) 
                self.findChild("choiceDetail").setValue(info["choice"])
                self.findChild("choiceDetail").setPos(info["worldPos"]()-Vector2(720,360)+Vector2(0,-80))
        else:
            self.findChild("choiceDetail").setActive(False)

        if self.controlSys["Mode"] == GenMode.Card:
            if self.controlSys["InGenerating"]:
                self.findChild("genProcess").setActive(True)
                self.findChild("genCardBar").setActive(False)
            else:
                self.findChild("genProcess").setActive(False)
                self.findChild("genCardBar").setActive(True)
        else:
            self.findChild("genProcess").setActive(False)
            self.findChild("genCardBar").setActive(False)
    def refreshModeDisplay(self):
        self.displayModeGencard()
        self.displayModePromotion()
    def displayModePromotion(self):
        if self.controlSys["Mode"] != GenMode.Promotion:
            for child in self.children:
                if child.name.find("SelectionBar") != -1:
                        child.setActive(False)
            self.findChild("tip_promotion").setActive(False)
            return
        for child in self.children:
            if child.name.find("SelectionBar") != -1:
                if child.name[13:] == self.controlSys["SelectedChar"]:
                    child.setActive(True)
                else:
                    child.setActive(False)
        self.findChild("tip_promotion").setActive(True)
    def displayModeGencard(self):
        if self.controlSys["Mode"] != GenMode.Card:
            self.findChild("entryLine").setActive(False)
            self.findChild("genCardBar").setActive(False)
            self.findChild("genProcess").setActive(False)
            self.findChild("tip_card").setActive(False)
            return
        self.findChild("entryLine").setActive(True)
        self.findChild("genCardBar").setActive(True)
        self.findChild("tip_card").setActive(True)
        if self.controlSys["InGenerating"]:
            self.findChild("genProcess").setActive(True)
    def RequestOnGenCard(self,bl):
        from LLMStorage import llmStorage
        self.controlSys["InGenerating"] = bl
        _dit = {
            "pcs":llmStorage.GENPAGE_PROCESS,
            "pcsMax":llmStorage.GENPAGE_PROCESS_MAX,
            "pageCnt":llmStorage.GENPAGE_PROCESS_PAGE
        }
        #print(_dit)
        self.findChild("genProcess").setValue(_dit)
    def Render(self):
        self.draw()
    def Init(self):
        self.findChild("charArray").setValue(gameDataManager.getAllys())
        self.findChild("charInfo").setActive(False)
        self.Init_SelectionBar()
    def Init_SelectionBar(self):
        dit1 = genPromotion.genUpgrade()
        dit2 = genPromotion.genPassive()
        for charName in gameDataManager.getAllys().keys():
            list = []
            list.extend([] if not charName in dit1.keys() else dit1[charName])
            list.extend([] if not charName in dit2.keys() else dit2[charName])
            self.addChild(UIGeneratingSelectionBarArray("SelectionBar_"+charName,self.screen,0))
            self.findChild("SelectionBar_"+charName).setValue(list)
        self.posSetChildren()
    def LoadGenCardBar(self):
        self.findChild("genCardBar").setValue()
    def RequestExitButtonReset(self):
        self.findChild("EXIT").setState(0)
    def RequestCanExitScene(self):
        from LLMStorage import llmStorage
        return not llmStorage.inGenerating
    def RequestGenProcessDialog(self,txt):
        self.findChild("genProcess").setDialog(txt)
    def AtModeClicked(self,modeName):
        self.RequestExitButtonReset()
        self.findChild("modePromotion").RequestState(0)
        self.findChild("modeGencard").RequestState(0)
        if modeName == "modePromotion":
            self.controlSys["Mode"] = GenMode.Promotion
            self.findChild("modePromotion").RequestState(1)
        elif modeName == "modeGencard":
            self.controlSys["Mode"] = GenMode.Card
            self.findChild("modeGencard").RequestState(1)
        else:
            self.controlSys["Mode"] = None
        self.refreshModeDisplay()
    def AtCharClicked(self,charName):
        self.RequestExitButtonReset()
        self.findChild("charInfo").setValue(gameDataManager.getAlly(charName))
        self.findChild("charInfo").setActive(True)
        self.controlSys["SelectedChar"] = charName
        self.refreshModeDisplay()
    def AtSelectionBarClick(self,charBarName,barName,selectChoice):
        self.RequestExitButtonReset()
        from RenderSystem.prefab.UISelectionBar import GenSelectBarType
        print(charBarName,barName,selectChoice)
        _charName = charBarName[13:]
        if barName.find(GenSelectBarType.Upgrade.value) != -1:
            dealPromotion.gainUpgrade(_charName,selectChoice)
        elif barName.find(GenSelectBarType.Passive.value) != -1:
            dealPromotion.gainPassive(_charName,selectChoice)
        self.findChild("charInfo").setValue(gameDataManager.getAlly(_charName))


class UIModeSelectionIcon(ButtonSprite):
    def __init__(self, name, screen, priority,img):
        self.raw_img = img
        super().__init__(name, screen, priority)
        self.RequestState(0)
    def OnClick(self, event):
        self.parent.AtModeClicked(self.name)
    def RequestState(self,state):
        if state == 1:
            self.setImage(self.preResize(self.raw_img+"_active.png",Vector2(90,90)))
        else:
            self.setImage(self.preResize(self.raw_img+"_inactive.png",Vector2(70,70)))

class UIChoiceDetail(Canvas):
    def __init__(self, name, screen, priority):
        self.rcdName = None
        super().__init__(name, screen, priority)
        self.preventRay(True)
    def init(self):
        self.addChild(UIChoiceDetail_BG("BG",self.screen,-5))
        self.addChild(UIChoiceDetail_Text("txt",self.screen,0))
    def setValue(self,nam):
        if nam == self.rcdName:
            return
        self.rcdName = nam
        self.findChild("txt").setValue(nam)

class UIChoiceDetail_BG(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("UI\\buttonBG4.png",Vector2(400,120)))

class UIChoiceDetail_Text(MutiLineText):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, 300,0)
    def init(self):
        self.setFont(Data.fonts.FontUICharAbility)
        self.setColor(Data.fonts.ColorSimpleTip)
    def setValue(self,nam):
        if nam in gameDataManager.CUSTOM_CHARUPGRADEPOOL.keys():
            self.setTexts(gameDataManager.CUSTOM_CHARUPGRADEPOOL[nam]["Desq"],Data.fonts.FontRender.Outline)
        elif nam in gameDataManager.CUSTOM_PASSIVEPOOL.keys():
            self.setTexts(gameDataManager.CUSTOM_PASSIVEPOOL[nam]["Desq"],Data.fonts.FontRender.Outline)
        
