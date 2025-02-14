from RenderSystem.CanvasAutosort import *
from RenderSystem.Text import *
from .UITeam import UITeamCharacterHeadImage,HeadImage,UICharacterTitle,UICharacterBriefInfo_DesqBar
from .UICharacter import UICharSprite,CharFace
from .UIResisBar import UIResisBar,ResisDisplayType

from AudioSystem.AudioManager import audioManager

from enum import Enum
import Data.fonts

class UICharacterArray(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),5
        ))
    def setValue(self,dit):
        self.children.clear()
        _p = 0
        for cls in dit.values():
            self.addChild(UICharcaterUnit("char"+str(_p),self.screen,0))
            self.findChild('char'+str(_p)).setValue(cls)
            _p += 1
    def AtChildClick(self,cname,charName):
        for child in self.children:
            if child.name == cname:
                child.findChild("BG").Switch(0)
            else:
                child.findChild("BG").Switch(1)
        self.parent.AtCharClicked(charName)

class UICharcaterUnit(Canvas):
    def __init__(self, name, screen, priority):
        self.charName = None
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UITeamCharacterHeadImage("icon",self.screen,0,CharFace.Right))
        self.addChild(UICharacterTitle("title",self.screen,5))
        self.addChild(UICharacterUnit_BG("BG",self.screen,-5))
        self.setBaseRect(pygame.Rect(0,0,75,105))
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("icon").setPos(Vector2(0,-10)*self.worldScale())
        self.findChild("title").setPos(Vector2(0,35)*self.worldScale())
        self.findChild("title").setScale(Vector2(0.5,0.5))
    def setValue(self,cls):
        from GameDataManager import CharacterData
        #print(cls)
        if isinstance(cls,CharacterData):
            self.charName = cls.name
            self.findChild("icon").setValue(cls.SDname,HeadImage.Team)
            self.findChild("title").setValue(cls.name)
    def OnClick(self, event):
        audioManager.AddEffect("ButtonClick")
        self.parent.AtChildClick(self.name,self.charName)

class UICharacterUnit_BG(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.preSize = Vector2(75,105)
        self.Switch(1)
    def Switch(self,state):
        self.state = state
        if self.state == 1:
            self.setImage(self.preResize("UI\\ButtonBG2.png"))
        else:
            self.setImage(self.preResize("UI\\ButtonSP2.png"))

class UICharacterInfo(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UICharSprite("head",self.screen,0))
        #self.addChild(UICharacterTitle("title",self.screen,5))
        self.addChild(UIResisBar("resisBar",self.screen,5,ResisDisplayType.Detailed))
        self.addChild(UICharacterBriefInfo_DesqBar("desqBar",self.screen,5,330))
        self.addChild(UICharacterBaseInfoLine("baseInfo",self.screen,10))

        self.posSetChildren()
    def setValue(self,dit):
        from GameDataManager import CharacterData,gameDataManager
        if not isinstance(dit,CharacterData):
            return
        self.findChild("head").setValue(dit.SDname,None,None)
        #self.findChild("title").setValue(dit.name)
        self.findChild("resisBar").setValue(dit.mapResistance(gameDataManager.resdit))
        self.findChild("baseInfo").setValue(dit)
        self.findChild("desqBar").setValue({
            "charId":dit.name,
            "abilityDesq":dit.mapAbility(gameDataManager.psvdit)
        },True)
        #print(dit.mapAbility(gameDataManager.psvdit))
    def posSetChildren(self):
        super().posSetChildren()

        self.findChild("head").setPos(Vector2(-125,-110)*self.worldScale())
        self.findChild("resisBar").setPos(Vector2(80,-90)*self.worldScale())
        self.findChild("resisBar").setScale(Vector2(0.6,0.6)*self.worldScale())
        #self.findChild("title").setPos(Vector2(-75,-80)*self.worldScale())
        self.findChild("baseInfo").setPos(Vector2(80,-180)*self.worldScale())
        self.findChild("baseInfo").setScale(Vector2(0.6,0.6)*self.worldScale())

class CharBaseInfo(Enum):
    Life = {
        "icon":"lifeIcon.png",
        "color":Data.fonts.ColorRed
    }
    Stagger = {
        "icon":"staggerIcon.png",
        "color":Data.fonts.ColorYellow
    }
    Dice = {
        "icon":"diceIcon.png",
        "color":Data.fonts.ColorSimpleTip
    }
    Light = {
        "icon":"lightIcon.png",
        "color":Data.fonts.ColorLight
    }

class UICharacterBaseInfoLine(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),5
        ))
    def init(self):
        self.addChild(UICharacterBaseInfo("life",self.screen,0,CharBaseInfo.Life))
        self.addChild(UICharacterBaseInfo("stagger",self.screen,0,CharBaseInfo.Stagger))
        self.addChild(UICharacterBaseInfo("light",self.screen,0,CharBaseInfo.Light))
        self.addChild(UICharacterBaseInfo("dice",self.screen,0,CharBaseInfo.Dice))
    def setValue(self,cls):
        from GameDataManager import CharacterData
        if not isinstance(cls,CharacterData):
            return
        self.findChild("life").findChild("txt").setValue(str(cls.healthMax))
        self.findChild("stagger").findChild("txt").setValue(str(cls.staggerMax))
        self.findChild("light").findChild("txt").setValue(str(cls.lightMax))
        self.findChild("dice").findChild("txt").setValue(str(cls.speedL)+"-"+str(cls.speedR))
        self.autosort()

class UICharacterBaseInfo(CanvasAutoSort):
    def __init__(self, name, screen, priority,typ):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),2
        ))
        self.addChild(UICharacterBaseInfo_Icon("icon",self.screen,0,typ))
        self.addChild(UICharacterBaseInfo_Text("txt",self.screen,5,typ))
        self.setBaseRect(pygame.Rect(0,0,90,40))

class UICharacterBaseInfo_Icon(Sprite):
    def __init__(self, name, screen, priority,typ):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize(typ.value["icon"],Vector2(40,40)))

class UICharacterBaseInfo_Text(Text):
    def __init__(self, name, screen, priority,typ):
        super().__init__(name, screen, priority)
        self.setColor(typ.value["color"])
    def init(self):
        self.setFont(Data.fonts.FontMana)
    def setValue(self,txt):
        self.setText(txt,Data.fonts.FontRender.Null)
        self.parent.autosort()
