from RenderSystem.Canvas import *
from RenderSystem.CanvasAutosort import *
from RenderSystem.ButtonSprite import *
from RenderSystem.Text import *
from RenderSystem.Sprite import *
from RenderSystem.RotationText import *
from RenderSystem.MutiLineText import *

from AudioSystem.AudioManager import audioManager

import Data.fonts
from enum import Enum

class DiceCategory(Enum):
    Attack = "attack"
    Defense = "defense"
    Counter = "counter"

class DiceType(Enum):
    Slash = "slash"
    Pierce = "pierce"
    Blunt = "blunt"
    Block = "block"
    Evade = "evade"

class CardDisplayType(Enum):
    Small = 1
    Large = 2

class ManaIcon(Enum):
    Blue = "cardFrame\\manaIcon_blue.png"
    Green = "cardFrame\\manaIcon_green.png"
    Purple = "cardFrame\\manaIcon_purple.png"
    Gold = "cardFrame\\manaIcon_gold.png"

class ManaColor(Enum):
    Blue = Data.fonts.ColorBlue

class CardFrame(Enum):
    Blue = "blue.png"
    Green = "green.png"
    Purple = "purple.png"
    Gold = "gold.png"

class CardType(Enum):
    Near = "cardFrame\\cardType_near.png"
    Range = "cardFrame\\cardType_range.png"
    AOE = "cardFrame\\cardType_aoe.png"
'''
TODO add setvalue for each component in uicard
used for dynamic updating value
'''

class UICard(Canvas):
    def __init__(self, name, screen, priority,dit):
        self.valueChanged = False
        self.cardId = None
        self.displayType = CardDisplayType.Small
        self.setValue(dit)
        super().__init__(name, screen, priority)
    def setValue(self,dit,requireInit = False):
        if dit == None:
            return
        if self.cardId == dit["cardId"]:
            if hasattr(self,"mana") and self.mana == dit["mana"]:
                return
            else:
                requireInit = True
        self.valueChanged = True
        self.cardId = dit["cardId"]
        self.mana = dit["mana"]#int
        self.manaIcon = dit["manaIcon"]#enum
        self.manaColor = dit["manaColor"]
        self.cardImg = dit["cardImg"]#string
        self.cardFrame = dit["cardFrame"]#enum
        self.pageDesq = dit["pageDesq"]#dit for uicard_pagedesq

        self.cardTitle = u"精神鞭笞" if not "cardTitle" in dit.keys() else dit["cardTitle"]
        self.cardType = CardType.Near if not "cardType" in dit.keys() else dit["cardType"]

        if requireInit:
            self.init()
    def init(self):
        if not self.valueChanged:
            return
        self.valueChanged = False
        self.children.clear()
        self.addChild(UICard_ManaIcon("manaIcon",self.screen,-5,self.manaIcon.value))
        self.addChild(UICard_ManaText("mana",self.screen,5,self.mana,(Data.fonts.ColorEmotionGreen if self.manaColor == "Green" else
                                                                      Data.fonts.ColorRed if self.manaColor == "Red" else
                                                                      Data.fonts.ColorWhite)))
        self.addChild(UICard_CardFrame_Small("cardFrame_small",self.screen,-10,self.cardFrame.value))
        self.addChild(UICard_CardFrame_Large("cardFrame_large",self.screen,-10,self.cardFrame.value))
        self.addChild(UICard_CardImg("cardImg",self.screen,-20,self.cardImg))
        self.addChild(UICard_PageDesq("pageDesq",self.screen,0,self.pageDesq))

        self.addChild(UICard_CardTitle("cardTitle",self.screen,5,self.cardTitle))
        self.addChild(UICard_DiceView("diceView",self.screen,5,self.pageDesq["list"]))
        self.addChild(UICard_TypeIcon("cardType",self.screen,5,self.cardType))
        
        self.addChild(UICard_SelectedCardPin("pin",self.screen,50))
        self.findChild("pin").setActive(False)

        self.controlSys = {
            "Selected":False
        }

        self.posSetChildren()
    def posSetChildren(self):
        if len(self.children) == 0:
            return
        super().posSetChildren()
        self.findChild("pin").setPos(Vector2(0,-175)*self.worldScale())
        if self.displayType == CardDisplayType.Small:
            self.findChild("manaIcon").setPos(Vector2(-85,-135)*self.worldScale())
            self.findChild("mana").setPos(Vector2(-85,-135)*self.worldScale())
            self.findChild("cardFrame_small").setPos(Vector2(0,0))
            self.findChild("cardImg").setPos(Vector2(0,-10)*self.worldScale())

            self.findChild("cardTitle").setPos(Vector2(-5,-110)*self.worldScale())
            self.findChild("diceView").setPos(Vector2(-5,110)*self.worldScale())
            self.findChild("cardType").setPos(Vector2(80,-135)*self.worldScale())

            self.findChild("cardFrame_small").setActive(True)
            self.findChild("cardFrame_large").setActive(False)
            self.findChild("pageDesq").setActive(False)

            self.setBaseRect(self.findChild("cardFrame_small").sprite.get_rect())
        else:
            self.findChild("manaIcon").setPos(Vector2(-85-110,-135)*self.worldScale())
            self.findChild("mana").setPos(Vector2(-85-110,-135)*self.worldScale())
            self.findChild("cardFrame_large").setPos(Vector2(0,0))
            self.findChild("cardImg").setPos(Vector2(-110,-10)*self.worldScale())
            self.findChild("pageDesq").setPos(Vector2(110,0)*self.worldScale())

            self.findChild("cardTitle").setPos(Vector2(-5-110,-110)*self.worldScale())
            self.findChild("diceView").setPos(Vector2(-5-110,110)*self.worldScale())
            self.findChild("cardType").setPos(Vector2(80-110,-135)*self.worldScale())

            self.findChild("cardFrame_small").setActive(False)
            self.findChild("cardFrame_large").setActive(True)
            self.findChild("pageDesq").setActive(True)

            self.setBaseRect(self.findChild("cardFrame_large").sprite.get_rect())
    def setDisplayType(self,typpe):
        if typpe != self.displayType:
            self.displayType = typpe
            self.posSetChildren()
    def OnPointEnter(self, event):
        audioManager.AddEffect("ButtonEnter")
    def OnPointHover(self, event):
        self.parent.AtSetDisplayType(self.cardId,CardDisplayType.Large)
    def OnPointExit(self, event):
        if self.displayType == CardDisplayType.Large:
            self.parent.AtSetDisplayType(self.cardId,CardDisplayType.Small)
    def OnClick(self, event):
        audioManager.AddEffect("CardClick")
        self.parent.AtSelectedCard(self.cardId)
    def RequestSelectedState(self,bl):
        if bl == True:
            self.findChild("pin").setActive(True)
        else:
            self.findChild("pin").setActive(False)

class UICard_SelectedCardPin(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.preSize = Vector2(100,100)
        self.setImage(self.preResize("selectedCardPin.png"))

class UICard_ManaIcon(Sprite):
    def __init__(self, name, screen, priority,img):
        self.tmp_img = img
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(50,50)
        self.setImage(self.tmp_img)
        self.setImage(self.preResize(self.sprite))
class UICard_ManaText(RotationText):
    def __init__(self, name, screen, priority,amt,color=Data.fonts.ColorWhite):
        self.manaAmt = amt
        super().__init__(name, screen, priority)
        self.setColor(color)
        self.setText(str(self.manaAmt),Data.fonts.FontRender.Outline)
    def init(self):
        self.setFont(Data.fonts.FontMana)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setRotation(11.3)
        
class UICard_TypeIcon(Sprite):
    def __init__(self, name, screen, priority,typ):
        self._typ = typ
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(50,50)
        self.setImage(self.preResize(self._typ.value))
class UICard_CardImg(Sprite):
    def __init__(self, name, screen, priority,img):
        self.tmp_img = "cardImg/"+img
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(220,220)
        self.setImage(self.tmp_img)
        self.setImage(self.preResize(self.sprite))

class UICard_CardTitle(RotationText):
    def __init__(self, name, screen, priority,title):
        self.cardTitle = title
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontUICardTitle)
        self.setColor(Data.fonts.ColorBlack)
        #self.setShadeColor(Data.fonts.ColorBlack)
        self.setRotation(11.3)
        self.setText(self.cardTitle,Data.fonts.FontRender.Null)

class UICard_DiceView(CanvasAutoSort):
    def __init__(self, name, screen, priority,lis):
        self._dicelis = lis
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,-2),-8
        ))
    def init(self):
        for i in range(len(self._dicelis)):
            dice = self._dicelis[i]
            self.addChild(UICard_Dice("viewDice"+str(i),self.screen,0,dice["diceType"],dice["isCounter"]))
            self.findChild("viewDice"+str(i)).setScale(Vector2(1.3,1.3))

class UICard_CardFrame_Small(ButtonSprite):
    def __init__(self, name, screen, priority,img):
        self.tmp_img = "cardFrame\\cardFrame_small_"+img
        super().__init__(name, screen, priority)
    def init(self):
        super().init()
        self.preSize = Vector2(220,320)
        self.setImage(self.tmp_img)
        self.setImage(self.preResize(self.sprite))
    def OnPointHover(self, event):
        pass
    def OnClick(self, event):
        pass

class UICard_CardFrame_Large(ButtonSprite):
    def __init__(self, name, screen, priority,img):
        self.tmp_img = "cardFrame\\cardFrame_large_"+img
        super().__init__(name, screen, priority)
    def init(self):
        super().init()
        self.preSize = Vector2(440,320)
        self.setImage(self.tmp_img)
        self.setImage(self.preResize(self.sprite))
    def OnPointHover(self, event):
        pass
    def OnClick(self, event):
        pass

class UICard_PageDesq(CanvasAutoSort):
    def __init__(self, name, screen, priority,dit):
        self.setValue(dit)
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),10
        ))
    def setValue(self,dit):
        '''
        Dice
        overall_desq
        list{
            dice
        }
        '''
        self.overall_desq = " " if( not "overall_desq" in dit.keys() or dit["overall_desq"] == None) else dit["overall_desq"]
        #self.overall_desq = "使用时 恢复1点光芒，抽取2张书页"
        self.diceList = dit["list"]
    def init(self):
        self.addChild(UICard_FullTextDesq("diceDesq",self.screen,-1,200,self.overall_desq))
        idx = 0
        for dice in self.diceList:
            self.addChild(UICard_DiceDesqLine("dice"+str(idx),self.screen,0,dice))
            idx += 1
        


class UICard_FullTextDesq(MutiLineText):
    def __init__(self, name, screen, priority,width,txt):
        self._txt = txt
        super().__init__(name, screen, priority,width,1)
    def init(self):
        self.setFont(Data.fonts.FontUICardDesq)
        self.setColor(Data.fonts.ColorWhite)
        self.setTexts(self._txt,Data.fonts.FontRender.Null)
    

class UICard_DiceDesqLine(Canvas):
    def __init__(self, name, screen, priority,dit):
        self.setValue(dit)
        super().__init__(name, screen, priority)
    def setValue(self,dit):
        '''
        Dict
        diceType
        isCounter
        minDice'
        maxDice
        desq
        '''
        self.diceType = dit["diceType"]
        self.isCounter = dit["isCounter"]
        self.minDice = dit["minDice"]
        self.maxDice = dit["maxDice"]
        self.desq = " " if( not "desq" in dit.keys() or dit["desq"] == None) else dit["desq"]
        #self.desq = "命中时 追加8点混乱伤害"
    def init(self):
        self.addChild(UICard_Dice("dice",self.screen,0,self.diceType,self.isCounter))
        self.addChild(UICard_DiceNum("diceNum",self.screen,3,self.diceType,self.minDice,self.maxDice,self.isCounter))
        self.addChild(UICard_FullTextDesq("diceDesq",self.screen,4,120,self.desq))

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("dice").setPos(Vector2(-90,0)*self.worldScale())
        self.findChild("diceNum").setPos(Vector2(-50,0)*self.worldScale())
        self.findChild("diceDesq").setPos(Vector2(40,0)*self.worldScale())
        self.setBaseRect(pygame.rect.Rect(0,0,220*self.worldScale().x,60*self.worldScale().y))
class UICard_Dice(Sprite):
    def __init__(self, name, screen, priority,dicetype,counter):
        self.diceType = dicetype
        self.counter = counter
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(40,40)
        self.setDice()
    def setDice(self):
        for e in DiceType:
            if e == self.diceType:
                file = "dice_"+e.value+("_counter" if self.counter else "")+".png"
                self.setImage(file)
                break
        self.setImage(self.preResize(self.sprite))
class UICard_DiceNum(Text):
    def __init__(self, name, screen, priority,dicetype,minn,maxx,iscounter):
        self.diceType = dicetype
        self.isCounter = iscounter
        self.minDice = minn
        self.maxDice = maxx
        self.diceText = str(self.minDice)+"-"+str(self.maxDice)
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontDiceNum)
        self.diceColor()
        self.setText(self.diceText,Data.fonts.FontRender.Outline)
    def diceColor(self):
        if self.isCounter:
            self.setColor(Data.fonts.ColorYellow)
        elif self.diceType == DiceType.Block or self.diceType == DiceType.Evade:
            self.setColor(Data.fonts.ColorBlue)
        else:
            self.setColor(Data.fonts.ColorRed)
    
    