from RenderSystem.CanvasAutosort import *
from .UISlowFocusButton import *

import copy
import Data.fonts
from enum import Enum

class UISelectionButton(UISlowFocusButton):
    def __init__(self, name, screen, priority, buttonInfo):
        super().__init__(name, screen, priority, buttonInfo)
    def OnPointHover(self, event):
        self.parent.parent.AtHoverChoice(self.text,Vector2(event.pos[0],event.pos[1]))
    def OnPointExit(self, event):
        super().OnPointExit(event)
        self.parent.parent.AtHoverChoice(None,None)

class UISelectionBar(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),5
        ))
    def init(self):
        pass
    def setValue(self,num,btinfo):
        self.children.clear()
        if isinstance(btinfo,list):
            _p = 0
            for btoi in btinfo:
                if isinstance(btoi,SlowFocusButtonInfo):
                    self.addChild(UISelectionButton(_p,self.screen,0,btoi))
                    _p += 1
        elif isinstance(btinfo,SlowFocusButtonInfo):
            for p in range(num):
                self.addChild(UISelectionButton(p,self.screen,0,btinfo))
    def OnChildClick(self,nam):
        pass

class GenSelectBarType(Enum):
    Upgrade = "upgrade"
    Passive = "passive"

class UIGeneratingSelectionBarArray(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        self.HighlightChoice = None
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),50
        ))
    def setValue(self,lis):
        self.children.clear()
        _p = 0
        for dit in lis:
            if dit["type"] == GenSelectBarType.Upgrade:
                self.addChild(UIUpgradeSelectionBar(dit["type"].value+str(_p),self.screen,0))
            elif dit["type"] == GenSelectBarType.Passive:
                self.addChild(UIPassiveSelectionBar(dit["type"].value+str(_p),self.screen,0))
            self.findChild(dit["type"].value+str(_p)).setValue(dit["list"])
            _p += 1
        self.autosort()
    def AtSelectionBarClick(self,barName,selection):
        self.HighlightChoice = None
        self.parent.AtSelectionBarClick(self.name,barName,selection)
    def AtHoverChoice(self,nam,pos):
        if nam == None:
            self.HighlightChoice = None
        else:
            self.HighlightChoice = {
                "choice":nam,
                "worldPos":pos
            }

class UIGeneratingSelectionBar(UISelectionBar):
    def __init__(self, name, screen, priority):
        self.selectList = []
        self.isSelectEnd = False
        super().__init__(name, screen, priority)
    def setValue(self, num, btinfo):
        self.setBaseRect(pygame.Rect(0,0,240,150))
        super().setValue(num, btinfo)
    def update(self):
        super().update()
        if self.isSelectEnd:
            self.autosort()
            cnt = 0
            for child in self.children:
                if child.active:
                    cnt += 1
            if cnt <= 1:
                self.isSelectEnd = False
    def OnChildClick(self, nam):
        self.parent.AtSelectionBarClick(self.name,self.selectList[nam])
        for child in self.children:
            if child.name != nam:
                child.RequestDisappear()
        self.preventRay(True)
        self.isSelectEnd = True

class UIUpgradeSelectionBar(UIGeneratingSelectionBar):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def setValue(self,lis):
        self.selectList = copy.deepcopy(lis)
        _btLis = []
        for choice in self.selectList:
            _btLis.append(SlowFocusButtonInfo(choice,Data.fonts.ColorSimpleTip,Data.fonts.ColorWhite
                                              ,"UI\\buttonUpgradeBG.png","UI\\buttonUpgradeSP.png",Vector2(240,40)))
        super().setValue(len(_btLis),_btLis)

class UIPassiveSelectionBar(UIGeneratingSelectionBar):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def setValue(self,lis):
        from GameDataManager import gameDataManager
        self.selectList = copy.deepcopy(lis)
        _btLis = []
        for choice in self.selectList:
            _btLis.append(SlowFocusButtonInfo(choice,Data.fonts.ColorSimpleTip,Data.fonts.ColorWhite,
                                            (lambda x = gameDataManager.getCustomPassive(choice):
                                               "UI\\buttonPsvBG1.png" if x == None else 
                                               "UI\\buttonPsvBG1.png" if x["level"] <= 2 else
                                               "UI\\buttonPsvBG2.png" if x["level"] <= 4 else
                                                "UI\\buttonPsvBG3.png"
                                              )(),(lambda x = gameDataManager.getCustomPassive(choice):
                                               "UI\\buttonPsvSP1.png" if x == None else 
                                               "UI\\buttonPsvSP1.png" if x["level"] <= 2 else
                                               "UI\\buttonPsvSP2.png" if x["level"] <= 4 else
                                                "UI\\buttonPsvSP3.png"
                                              )()
                                              ,Vector2(240,40)))
        super().setValue(len(_btLis),_btLis)
    