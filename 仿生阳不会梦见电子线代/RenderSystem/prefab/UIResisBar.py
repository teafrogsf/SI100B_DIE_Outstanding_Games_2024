from RenderSystem.CanvasAutosort import *
from RenderSystem.Sprite import *
from RenderSystem.Text import *

from RenderSystem.prefab.UICard import DiceType
from RenderSystem.prefab.UICombatText import DmgType

from enum import Enum

class ResisDisplayType(Enum):
    Brief = 1
    Detailed = 2

class UIResisBar(CanvasAutoSort):
    def __init__(self, name, screen, priority,displayType = ResisDisplayType.Brief):
        self.displayType = displayType
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),0
        ))
    def init(self):
        self.addChild(UIResisLine("life",self.screen,0,DmgType.Life,self.displayType))
        self.addChild(UIResisLine("stagger",self.screen,0,DmgType.Stagger,self.displayType))
    def setValue(self,dit):
        self.findChild("life").setValue(dit["life"])
        self.findChild("stagger").setValue(dit["stagger"])

class UIResisLine(CanvasAutoSort):
    def __init__(self, name, screen, priority,typ,displayType = ResisDisplayType.Brief):
        self.displayType = displayType
        self.dmgTyp = typ
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),0
        ))
    def init(self):
        self.addChild(UIResisUnit("icon1",self.screen,0,self.displayType))
        self.addChild(UIResisUnit("icon2",self.screen,0,self.displayType))
        self.addChild(UIResisUnit("icon3",self.screen,0,self.displayType))
        if self.displayType == ResisDisplayType.Brief:
            self.setBaseRect(pygame.Rect(0,0,60,180))
        else:
            self.setBaseRect(pygame.Rect(0,0,180,180))
    def setValue(self,dit):
        self.findChild("icon1").setValue(self.dmgTyp,DiceType.Slash,dit["slash"])
        self.findChild("icon2").setValue(self.dmgTyp,DiceType.Pierce,dit["pierce"])
        self.findChild("icon3").setValue(self.dmgTyp,DiceType.Blunt,dit["blunt"])
        self.autosort()

class UIResisUnit(CanvasAutoSort):
    def __init__(self, name, screen, priority,displayType = ResisDisplayType.Brief):
        self.displayType = displayType
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),5
        ))
    def init(self):
        self.addChild(UIResisIcon("icon",self.screen,0))
        self.setBaseRect(pygame.Rect(0,0,60,60))
        if self.displayType == ResisDisplayType.Detailed:
            self.addChild(UIResisText("txt",self.screen,0))
            self.setBaseRect(pygame.Rect(0,0,180,60))
    def setValue(self,typ,cat,resis):
        self.findChild("icon").setValue(typ,cat,resis)
        if isinstance(self.findChild("txt"),UIResisText):
            self.findChild("txt").setValue(typ,resis)
        self.autosort()

class UIResisIcon(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def setValue(self,typ,cat,resis):
        from GameDataManager import gameDataManager
        self.setImage(gameDataManager.getResisIcon(typ,cat,resis))

class UIResisText(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontDmgText)
    def setValue(self,typ,resis):
        if typ == DmgType.Life:
            self.setColor(Data.fonts.ColorRed)
        else:
            self.setColor(Data.fonts.ColorYellow)
        self.setText(resis.value,Data.fonts.FontRender.Outline)