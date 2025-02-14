from RenderSystem.Canvas import *
from RenderSystem.CanvasAutosort import *
from RenderSystem.ButtonSprite import *
from RenderSystem.Text import *

from enum import Enum

from AudioSystem.AudioManager import audioManager

import Data.fonts

class StateSpeedDice(Enum):
    Unrolled = 1,
    Rolled = 2,
    Highlighted = 3
    Broken = 4
    Paged = 5
    Broken_Highlighted = 6

class UISpeedDiceArray(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2(0,0),Vector2(1,0),-3
        ))

        self.charId = None
        self.amt = None
    def elcsort(self, elm):
        new_elm = sorted(elm,key= lambda e : 100 if e.speed == None else e.speed,reverse=True)
        return new_elm
    def setValue(self,dit):
        '''
        Dict:
        -charId
        -amount
        -list-diceId
             -spd
             -state
             -cardDit
        '''
        self.charId = dit["charId"]
        self.amt = dit["amt"]
        while len(self.children) > self.amt:
            self.delChild(self.children[0].name,False)
        while len(self.children) < self.amt:
            self.addChild(UISpeedDice("dice",self.screen,0),False)
        for i in range(self.amt):
            self.children[i].setValue(self.charId,dit["list"][i])
        self.autosort()
        for i in range(len(self.children)):
            self.children[i].name = "dice"+str(i+1)

class UISpeedDice(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UISpeedDice_ImgDice("ImgDice",self.screen,-5))
        self.addChild(UISpeedDice_Text("Text",self.screen,5))

        self.setBaseRect(self.findChild("ImgDice").sprite.get_rect())

        self.characterId = None
        self.diceId = None
        self.speed = None
        self.diceState = None
        
        self.cardDit = None
        self.targets = None
        self.isClashing = None

        self.controlSys = {
            "Highlighted":False,
        }
    def setValue(self,charId,dit):
        self.characterId = charId
        self.diceId = dit["diceId"]
        self.speed = dit["spd"]
        self.diceState = dit["state"]
        self.speedRange = (dit["speedL"],dit["speedR"])

        if "cardDit" in dit.keys():
            self.cardDit = dit["cardDit"]
        if "target" in dit.keys():
            self.targets = dit["target"]
        else:
            self.targets = None
        if "isClashing" in dit.keys():
            self.isClashing = dit["isClashing"]
        else:
            self.isClashing = None

        self.findChild("ImgDice").setState(self.diceState,self.controlSys["Highlighted"],self.cardDit != None)
        self.findChild("Text").setText((
            "∞" if (self.diceState == StateSpeedDice.Rolled and self.speed >= 99) else
                                        str(self.speed) if self.diceState == StateSpeedDice.Rolled else 
                                        " " if (self.diceState == StateSpeedDice.Broken or self.diceState == StateSpeedDice.Broken_Highlighted) else
                                        str(dit["speedL"])+"-"+str(dit["speedR"]))
                                       ,Data.fonts.FontRender.Outline)
    def OnPointHover(self, event):
        self.parent.parent.parent.parent.AtHoverDice(self.diceId)
        self.findChild("ImgDice").setState(self.diceState,(self.controlSys["Highlighted"] or self.isMouseOver),self.cardDit != None)
    def OnPointExit(self, event):
        self.parent.parent.parent.parent.AtHoverDice(None)
        self.findChild("ImgDice").setState(self.diceState,(self.controlSys["Highlighted"] or self.isMouseOver),self.cardDit != None)
    def OnClick(self, event):
        #print("clicked")
        audioManager.AddEffect("ButtonClick")
        self.parent.parent.parent.parent.AtSelectedDice(self.diceId)
    def OnRightClick(self, event):
        #print("rightClicked")
        audioManager.AddEffect("ButtonClick")
        if self.cardDit != None:
            self.parent.parent.parent.parent.AtDeselectedDice(self.diceId)
    def RequestSelectedState(self,bl):
        self.controlSys["Highlighted"] = bl
        self.findChild("ImgDice").setState(self.diceState,(self.controlSys["Highlighted"] or self.isMouseOver),self.cardDit != None)
    def RequestPageState(self):
        return self.cardDit != None
    def RequestDiceStateNormal(self):
        return self.diceState != StateSpeedDice.Broken and self.diceState != StateSpeedDice.Broken_Highlighted

class UISpeedDice_ImgDice(ButtonSprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        super().init()
        self.state = None
        self.setState(StateSpeedDice.Unrolled,False,False)
    def setImage(self, img):
        super().setImage(self.preResize(img,Vector2(100,100)))
    def setState(self,state,isHighlight,isPaged):
        if isHighlight:
            if state == StateSpeedDice.Broken:
                state = StateSpeedDice.Broken_Highlighted
            else:
                state = StateSpeedDice.Highlighted
        elif isPaged:
            state = StateSpeedDice.Paged
        if self.state == state:
            return
        self.state = state
        if state == StateSpeedDice.Paged:
            self.setImage("speedDice_paged.png")
        elif state == StateSpeedDice.Highlighted:
            self.setImage("speedDice_highlighted.png")
        elif state == StateSpeedDice.Broken:
            self.setImage("speedDice_broken.png")
        elif state == StateSpeedDice.Broken_Highlighted:
            self.setImage("speedDice_broken_highlighted.png")
        else:
            self.setImage("speedDice_rolled.png")
        

class UISpeedDice_Text(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontSpeedDice)
        self.setColor(Data.fonts.ColorWhite)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setText(" ",Data.fonts.FontRender.Outline)
    def setText(self, txt, choice):
        if txt == "∞":
            self.setFont(Data.fonts.FontSpeedDice_Alter)
        else:
            self.setFont(Data.fonts.FontSpeedDice)
        super().setText(txt, choice)
