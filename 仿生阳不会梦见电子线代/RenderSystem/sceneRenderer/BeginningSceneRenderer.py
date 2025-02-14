from RenderSystem.Canvas import *
from RenderSystem.CanvasAutosort import *
from RenderSystem.prefab.UISlowFocusButton import UISlowFocusButton,SlowFocusButtonInfo
from .BattleMainRenderer import UIBattleBackground

from RenderSystem.prefab.UIDifficulty import UIDifficultyArray
from RenderSystem.prefab.UISignBoard import *

from GameDataManager import gameDataManager

import Data.fonts

buttonArray = [{"name":"gameStart","title":"新游戏"},{"name":"guide","title":"教程"},{"name":"rank","title":"排行榜"},
               {"name":"dev","title":"制作组名单"},{"name":"exit","title":"退出游戏"}]

class BeginningSceneRenderer(Canvas):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UIBattleBackground("BG",self.screen,-100))
        self.addChild(BeginningSceneButtonArray("buttonArray",self.screen,0))
        self.addChild(BeginningSceneButtonArea("area",self.screen,-10))
        
        self.addChild(UIDifficultyArray("gameStart",self.screen,10))
        self.addChild(UIBeginningGuide("guide",self.screen,10))
        self.addChild(UIBeginningRank("rank",self.screen,10))
        self.addChild(UIBeginningExit("exit",self.screen,10))
        self.addChild(UIBeginningDev("dev",self.screen,10))

        self.findChild("BG").setValue(gameDataManager.getBackground("Beginning"))

        self.AtButtonArrayClick(None)
        self.posSetChildren() 
    def posSetChildren(self):
        super().posSetChildren()

        self.setPos(Vector2(720,360))
        self.findChild("area").setPos(Vector2(-400,0))
        self.findChild("buttonArray").setPos(Vector2(-400,0))

        self.findChild("gameStart").setPos(Vector2(250,0))
        for child in ["guide","rank","exit","dev"]:
            self.findChild(child).setPos(Vector2(250,0))
    def Render(self):
        self.draw()
    def AtButtonArrayClick(self,nam):
        for bt in buttonArray:
            _obj = self.findChild(bt["name"])
            if _obj != None:
                if bt["name"] == nam:
                    _obj.setActive(True)
                else:
                    _obj.setActive(False)


class BeginningSceneButtonInfo(SlowFocusButtonInfo):
    def __init__(self,text):
        self.text = text
        self.normalColor = Data.fonts.ColorSimpleTip
        self.highlightColor = Data.fonts.ColorWhite
        self.buttonBG = "UI\\buttonBG1.png"
        self.buttonSP = "UI\\buttonSP1.png"
        self.buttonSize = Vector2(250,50)

class BeginningSceneButtonArray(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority,AutoSortType(
            Vector2.Zero(),Vector2(0,1),50
        ))
    def init(self):
        for bt in buttonArray:
            self.addChild(UISlowFocusButton(bt["name"],self.screen,0,BeginningSceneButtonInfo(bt["title"])))
    def OnChildClick(self,buttonName):
        self.parent.AtButtonArrayClick(buttonName)

class BeginningSceneButtonArea(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("UI\\beginning.png")