from RenderSystem.CanvasAutosort import *
from .UICard import *
from .UICardArray import UIDisplayCard
from GameDataManager import gameDataManager

import copy

class UICardSelectionBar(CanvasAutoSort):
    def __init__(self, name, screen, priority,row,column):
        self.row = row
        self.column = column
        self.cardLis = None
        self.HighlightCard = None
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),0
        ))
    def init(self):
        for i in range(self.row):
            self.addChild(UICardSelectionLine("cardLine"+str(i),self.screen,0,self.column))
            self.findChild("cardLine"+str(i)).setActive(False)
    def setValue(self,lis):
        self.cardLis = copy.deepcopy(lis)
        lis = [lis[i:i+self.column] for i in range(0,len(lis),self.column)]
        for child in self.children:
            child.setActive(False)
        for i in range(len(lis)):
            self.findChild("cardLine"+str(i)).setActive(True)
            self.findChild("cardLine"+str(i)).setValue(lis[i])
        self.autosort(True)
    def AtSelectedCard(self,cardName):
        pass
    def AtHoverCard(self,cardDit,pos):
        if cardDit == None:
            self.HighlightCard = None
        else:
            self.HighlightCard = {
                "cardDit":cardDit,
                "worldPos":pos
            }

class UICardSelectionLine(CanvasAutoSort):
    def __init__(self, name, screen, priority,amiya):
        self.amiya = amiya
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),40
        ))
    def init(self):
        for i in range(self.amiya):
            self.addChild(UISelectionCard("card"+str(i),self.screen,0))
            self.findChild("card"+str(i)).setActive(False)
            self.findChild("card"+str(i)).setScale(Vector2(0.5,0.5))
        self.setBaseRect(pygame.Rect(0,0,450,200))
    def setValue(self,lis):
        for child in self.children:
            child.setActive(False)
        for i in range(len(lis)):
            self.findChild("card"+str(i)).setActive(True)
            self.findChild("card"+str(i)).resetValue(lis[i])
        self.autosort(True)

class UISelectionCard(UICard):
    def __init__(self, name, screen, priority):
        self.isInCardPool = False
        self.rcdCardDit = None
        super().__init__(name, screen, priority, None)
        self.setBaseRect(pygame.Rect(0,0,220,320))
    def resetValue(self, dit):
        self.cardName = dit["name"]
        self.cardAmiya = dit["amt"]
        self.rcdCardDit = dit
        super().setValue(dit["card"], True)
        if self.isInCardPool:
            self.addChild(UISelectionCardAmt("cardAmiya",self.screen,100000,self.cardAmiya))
        self.displayType = CardDisplayType.Large
        #print(self.findChild("cardFrame_small").rect)
        self.setDisplayType(CardDisplayType.Small)
    def posSetChildren(self):
        super().posSetChildren()
        if self.findChild("cardAmiya") != None:
            if self.displayType == CardDisplayType.Small:
                self.findChild("cardAmiya").setActive(True)
                self.findChild("cardAmiya").setPos(Vector2(-105,150)*self.worldScale())
            else:
                self.findChild("cardAmiya").setActive(False)
    def OnPointHover(self, event):
        self.parent.parent.AtHoverCard(self.rcdCardDit,Vector2(event.pos[0],event.pos[1]))
    def OnPointExit(self, event):
        self.parent.parent.AtHoverCard(None,None)
    def OnClick(self, event):
        if self.isInCardPool and self.cardAmiya > 0:
            self.parent.parent.AtSelectedCard(self.cardName)
        elif not self.isInCardPool:
            self.parent.parent.AtSelectedCard(self.cardName)
    def RequestSelectedState(self,bl):
        pass

class UISelectionCardAmt(Canvas):
    def __init__(self, name, screen, priority,val):
        super().__init__(name, screen, priority)
        self.setValue(val)
    def init(self):
        self.addChild(UISelectionCard_Icon("icon",self.screen,-5))
        self.addChild(UISelectionCard_Txt("txt",self.screen,0))
    def setValue(self,val):
        self.findChild("txt").setValue(str(val))

class UISelectionCard_Icon(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("UI\\cardAmt.png",Vector2(60,60)))
class UISelectionCard_Txt(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontButton2)
        self.setColor(Data.fonts.ColorSimpleTip)
        self.setText("×0",Data.fonts.FontRender.Outline)
    def setValue(self,txt):
        self.setText("×"+txt,Data.fonts.FontRender.Outline)

class UIPlayerCardBar(UICardSelectionBar):
    def __init__(self, name, screen, priority):
        self.charName = None
        super().__init__(name, screen, priority,3,3)
    def LinkCardPoolBar(self,cardPoolBar):
        self.cardPoolBar = cardPoolBar
    def setValue(self, tupl):
        self.charName = tupl[0]
        super().setValue(tupl[1])
    def AtSelectedCard(self, cardName):
        _dit = None
        for dit in self.cardLis:
            if dit["name"] == cardName:
                _dit = dit
                break
        if _dit != None:
            self.cardLis.remove(_dit)
            self.setValue(gameDataManager.modifyAllyCards(self.charName,self.cardLis))
            gameDataManager.modifyCustomPageAmt(cardName,1)
            self.cardPoolBar.Refresh()
    def AddHandCard(self,dit):
        if self.cardLis == None or self.charName == None:
            return False
        if isinstance(self.cardLis,list) and len(self.cardLis) >= 9:
            return False
        self.cardLis.append(dit)
        self.setValue(gameDataManager.modifyAllyCards(self.charName,self.cardLis))
        return True

class UICardPoolBar(UICardSelectionBar):
    def __init__(self, name, screen, priority):
        self.index = 0
        super().__init__(name, screen, priority,3,3)
        self.setInCardPool()
    def LinkPlayerCardBar(self,playerCardBar):
        self.playerCardBar = playerCardBar
    def LinkPageModifier(self,pageModifier):
        self.pageModifier = pageModifier
    def AtSelectedCard(self, cardName):
        if self.playerCardBar.AddHandCard(gameDataManager.getCustomCard(cardName)):
            gameDataManager.modifyCustomPageAmt(cardName,-1)
            self.Refresh()
    def Refresh(self):
        self.setValue(gameDataManager.getCustomCardsOnPage(self.index))
    def setIndex(self, ind):
        self.index = ind
        self.setValue(gameDataManager.getCustomCardsOnPage(self.index))
        self.pageModifier.setValue(self.index)
    def setInCardPool(self):
        for child in self.children:
            for grandson in child.children:
                if isinstance(grandson,UISelectionCard):
                    grandson.isInCardPool = True

class UIGenCardBar(UICardSelectionBar):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        super().__init__(name, screen, priority,1,3)
        self.setInCardPool()
    def setValue(self):
        lis = gameDataManager.getGenPage()
        if len(lis) < 3:
            return
        super().setValue(lis[0:3])
        self.preventRay(False)
    def AtSelectedCard(self, cardName):
        from RenderSystem.sceneRenderer.TempObjectRenderer import TempObjectRenderer
        _dit = None
        for dit in self.cardLis:
            if dit["name"] == cardName:
                _dit = dit
                break
        if _dit != None:
            gameDataManager.injectGenPage(cardName)
            #print(gameDataManager.PAGE_POOL)
            self.HighlightCard = None
            self.preventRay(True)
            for child in self.children:
                for grandson in child.children:
                    if isinstance(grandson,UISelectionCard):
                        if grandson.cardName != cardName:
                            grandson.setActive(False)
                child.autosort()
            if isinstance(self.scene.rendererTempObject, TempObjectRenderer):
                self.scene.rendererTempObject.AddSimpleTip(u"书页 "+cardName+" ×"+str(dit["amt"])+u"已收入藏书",400,Vector2(0,-220),75)
    def setInCardPool(self):
        for child in self.children:
            for grandson in child.children:
                if isinstance(grandson,UISelectionCard):
                    grandson.isInCardPool = True