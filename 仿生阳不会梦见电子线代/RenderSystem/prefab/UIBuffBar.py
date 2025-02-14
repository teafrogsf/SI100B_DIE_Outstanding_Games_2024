from RenderSystem.Canvas import *
from RenderSystem.CanvasAutosort import *
from RenderSystem.Sprite import *
from RenderSystem.Text import *

from enum import Enum
    
class UIBuffBarBlock(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),5
        ))
    def init(self):
        self.maxiLineBuff = 3
    def setValue(self,bufList):
        _lineCnt = len(bufList)//self.maxiLineBuff + (1 if len(bufList)%self.maxiLineBuff != 0 else 0)
        while len(self.children) > _lineCnt:
            self.delChild(self.children[0].name,False)
        while len(self.children) < _lineCnt:
            self.addChild(UIBuffBarLine("buffLine",self.screen,0),False)
        for i in range(_lineCnt):
            self.children[_lineCnt-i-1].setValue(bufList[i*self.maxiLineBuff:min(len(bufList),(i+1)*self.maxiLineBuff)])
        self.autosort()
        for i in range(len(self.children)):
            self.children[i].name = "buffLine"+str(_lineCnt-i)
        
class UIBuffBarLine(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),5
        ))
    def init(self):
        self.maxiBuff = 3
        self.setBaseRect(pygame.Rect(0,0,40,200))
    def setValue(self,lis):
        while len(self.children) > len(lis):
            self.delChild(self.children[0].name,False)
        while len(self.children) < len(lis):
            self.addChild(UIBuff("buf",self.screen,0),False)
        for i in range(len(lis)):
            self.children[i].setValue(lis[i])
        self.autosort()
        for i in range(len(self.children)):
            self.children[i].name = "buff"+str(i+1)
    

class UIBuff(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UIBuff_Sprite("img",self.screen,0))
        self.addChild(UIBuff_Level("txt",self.screen,5))
        self.setBaseRect(pygame.rect.Rect(0,0,40,40))

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("txt").setPos(Vector2(15,15)*self.worldScale())
    def setValue(self,dit):
        from GameDataManager import gameDataManager
        _bf = gameDataManager.getBuff(dit["buffName"])
        self.findChild("img").setValue(_bf["Icon"])
        self.findChild("txt").setValue(dit["buffLevel"])
        if "isNext" in dit.keys() and dit["isNext"] == True:
            self.findChild("img").setAlpha(120)

class UIBuff_Sprite(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(40,40)
    def setValue(self,copiedBufIcon):
        self.setImage(self.preResize(copiedBufIcon))
    def setAlpha(self,alpha):
        if self.sprite != None:
            _sp = self.sprite.copy()
            _sp.set_alpha(alpha)
            self.setImage(_sp)

class UIBuff_Level(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontBuffNum)
        self.setColor(Data.fonts.ColorWhite)
        self.setShadeColor(Data.fonts.ColorBlack)
    def setValue(self,num):
        self.setText(str(num),Data.fonts.FontRender.Outline)
    