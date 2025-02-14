from RenderSystem.Canvas import *
from RenderSystem.Text import *
from RenderSystem.Sprite import *

from AnimeSystem.animes.ButtonAnime import ButtonClickAnime,ButtonDisapperAnime

from AudioSystem.AudioManager import audioManager

import Data.fonts

class SlowFocusButtonInfo:
    def __init__(self,text,normalColor,highlightColor,buttonBG,buttonSP,buttonSize):
        self.text = text
        self.normalColor = normalColor
        self.highlightColor = highlightColor
        self.buttonBG = buttonBG
        self.buttonSP = buttonSP
        self.buttonSize = buttonSize

class UISlowFocusButton(Canvas):
    def __init__(self, name, screen, priority,buttonInfo):
        self.text = buttonInfo.text
        self.normalColor = buttonInfo.normalColor
        self.highlightColor = buttonInfo.highlightColor
        self.buttonBG = buttonInfo.buttonBG
        self.buttonSP = buttonInfo.buttonSP
        self.buttonSize = buttonInfo.buttonSize
        super().__init__(name, screen, priority)
    def init(self):
        self.setBaseRect(pygame.Rect(0,0,self.buttonSize().x,self.buttonSize().y))
        self.addChild(UISlowFocusButton_Sprite("buttonBG",self.screen,-10))
        self.addChild(UISlowFocusButton_Sprite("buttonSP",self.screen,0))
        self.addChild(UISlowFocusButton_Text("text",self.screen,10))

        self.findChild("buttonBG").setValue(self.buttonBG,self.buttonSize)
        self.findChild("buttonSP").setValue(self.buttonSP,self.buttonSize)
        self.findChild("text").setValue(self.text,self.normalColor,self.highlightColor)
    def OnPointEnter(self, event):
        self.findChild("text").switchHighlightColor()
        audioManager.AddEffect("ButtonEnter")
    def OnPointExit(self, event):
        self.findChild("text").switchNormalColor()
    def OnClick(self, event):
        audioManager.AddEffect("ButtonClick")
        self.AniCreate(ButtonClickAnime(self))
        self.AniActivate()
        if self.parent != None:
            self.parent.OnChildClick(self.name)
    def RequestDisappear(self):
        self.AniCreate(ButtonDisapperAnime(self))
        self.AniActivate()
    def update(self):
        super().update()
        if self.isMouseOver:
            if self.findChild("buttonSP").localScale().x < 1:
                if self.findChild("buttonSP").localScale().x + 1/20 <= 1:
                    self.findChild("buttonSP").setScale(self.findChild("buttonSP").localScale()+Vector2(1/20,0))
                else:
                    self.findChild("buttonSP").setScale(Vector2.One())
        else:
            if self.findChild("buttonSP").localScale().x > 0:
                if self.findChild("buttonSP").localScale().x - 1/20 >= 0:
                    self.findChild("buttonSP").setScale(self.findChild("buttonSP").localScale()-Vector2(1/20,0))
                else:
                    self.findChild("buttonSP").setScale(Vector2(0,1))

class UISlowFocusButton_Sprite(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def setValue(self,img,siz = Vector2(200,40)):
        self.preSize = siz
        self.setImage(self.preResize(img))

class UISlowFocusButton_Text(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def setValue(self,txt,normalColor = Data.fonts.ColorWhite,highlightColor = Data.fonts.ColorSimpleTip):
        self.normalColor = normalColor
        self.highlightColor = highlightColor
        self.text = txt
        self.setFont(Data.fonts.FontButton1)
        self.switchNormalColor()
    def switchNormalColor(self):
        self.setColor(self.normalColor)
        self.setText(self.text,Data.fonts.FontRender.Outline)
    def switchHighlightColor(self):
        self.setColor(self.highlightColor)
        self.setText(self.text,Data.fonts.FontRender.Outline)