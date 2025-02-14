from RenderSystem.Canvas import *
from RenderSystem.CanvasAutosort import *
from RenderSystem.ButtonSprite import *
from RenderSystem.Text import *
from RenderSystem.prefab.UICardSelection import UIPlayerCardBar,UICardPoolBar
from RenderSystem.prefab.UICharacterInfo import UICharacterArray,UICharacterInfo
from RenderSystem.prefab.UICardArray import UIDisplayCard

from RenderSystem.prefab.UIDoubleCheckButton import UIExitSceneButton

from GameDataManager import gameDataManager

class DeckSelectionSceneRenderer(Canvas):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UIPlayerCardBar("playerCardBar",self.screen,0))
        self.addChild(UICardPoolBar("cardPoolBar",self.screen,0))
        self.addChild(UICharacterArray("charArray",self.screen,0))
        self.addChild(UICharacterInfo("charInfo",self.screen,0))
        self.addChild(UICardPoolIndexModifier("indexModifier",self.screen,10))
        self.addChild(UIDisplayCard("displayCard",self.screen,30))

        self.addChild(UIExitSceneButton("EXIT",self.screen,1000,self.scene))

        self.findChild("displayCard").setActive(False)
        self.findChild("displayCard").setScale(Vector2(0.9,0.9))

        self.findChild("playerCardBar").LinkCardPoolBar(self.findChild("cardPoolBar"))
        self.findChild("cardPoolBar").LinkPlayerCardBar(self.findChild("playerCardBar"))
        self.findChild("indexModifier").LinkCardPoolBar(self.findChild("cardPoolBar"))
        self.findChild("cardPoolBar").LinkPageModifier(self.findChild("indexModifier"))

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()

        self.setPos(Vector2(720,360))

        self.findChild("EXIT").setPos(Vector2(480,-300))

        self.findChild("playerCardBar").setPos(Vector2(-480,0))
        self.findChild("cardPoolBar").setPos(Vector2(0,20))
        self.findChild("charArray").setPos(Vector2(480,-200))
        self.findChild("charInfo").setPos(Vector2(480,90))
        self.findChild("indexModifier").setPos(Vector2(0,-320))

        self.findChild("indexModifier").setScale(Vector2(0.5,0.5))
    def Render(self):
        self.draw()
    def update(self):
        super().update()
        hcard1 = self.findChild("playerCardBar").HighlightCard
        hcard2 = self.findChild("cardPoolBar").HighlightCard
        if hcard1 == None and hcard2 == None:
            self.findChild("displayCard").setActive(False)
        else:
            hcard = hcard1 if hcard2 == None else hcard2
            self.findChild("displayCard").setActive(True)
            self.findChild("displayCard").resetValue(hcard["cardDit"]["card"])
            self.findChild("displayCard").setPos(hcard["worldPos"]()-Vector2(720,360)+Vector2(300,0))
    def Init(self):
        self.findChild("cardPoolBar").setIndex(0)
        self.findChild("charArray").setValue(gameDataManager.getAllys())
        self.findChild("charInfo").setActive(False)
    def RequestExitButtonReset(self):
        self.findChild("EXIT").setState(0)
    def AtCharClicked(self,charName):
        self.RequestExitButtonReset()
        self.findChild("playerCardBar").setValue(gameDataManager.getAllyCards(charName))
        self.findChild("charInfo").setValue(gameDataManager.getAlly(charName))
        self.findChild("charInfo").setActive(True)
'''
class UISelectionDisplayCard(UIDisplayCard):
    def __init__(self, name, screen, priority):
        self.rcdCardName = None
        super().__init__(name, screen, priority)
    def resetValue(self,nam,pos):
        if nam != self.rcdCardName:
            self.rcdCardName = nam
            super().resetValue(gameDataManager.getCustomCard(nam)["card"])
'''

class UICardPoolIndexModifier(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        self.cardPoolPage = None
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),30
        ))
    def init(self):
        self.addChild(UIArrow("left1",self.screen,0,"UI\\leftArrow.png"))
        self.addChild(UIPageIndex("pageindex",self.screen,0))
        self.addChild(UIArrow("right1",self.screen,0,"UI\\rightArrow.png"))
    def LinkCardPoolBar(self,cardPoolBar):
        self.cardPoolBar = cardPoolBar
    def setValue(self,num):
        self.cardPoolPage = num
        self.findChild("pageindex").setValue(str(num+1))
    def OnChildClick(self,nam):
        rg = gameDataManager.getCustomCardsPageRange()
        if nam == "left1":
            if self.cardPoolPage - 1 >= rg[0]:
                self.cardPoolBar.setIndex(self.cardPoolPage - 1)
        elif nam == "right1":
            if self.cardPoolPage + 1 <= rg[1]:
                self.cardPoolBar.setIndex(self.cardPoolPage + 1)


class UIArrow(ButtonSprite):
    def __init__(self, name, screen, priority,img):
        super().__init__(name, screen, priority)
        self.setImage(img)
    def OnClick(self, event):
        from AnimeSystem.animes.ButtonAnime import ButtonClickAnime
        if self.AniCreate(ButtonClickAnime(self)) != None:
            self.AniActivate()
        if self.parent != None:
            self.parent.OnChildClick(self.name)
class UIPageIndex(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontButton2)
        self.setColor(Data.fonts.ColorSimpleTip)
        self.setText("0",Data.fonts.FontRender.Outline)
    def setValue(self,txt):
        self.setText(txt,Data.fonts.FontRender.Outline)