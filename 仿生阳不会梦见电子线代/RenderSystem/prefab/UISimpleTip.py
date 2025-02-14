from RenderSystem.Canvas import *
from RenderSystem.MutiLineText import *
from RenderSystem.Sprite import *

import Data.fonts

class UISimpleTip(Canvas):
    def __init__(self, name, screen, priority,txt,width,space=3):
        self._txt = txt
        self._width = width
        self._space = space
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UISimpleTip_Text("txt",self.screen,10,self._txt,self._width,self._space))
        self.addChild(UISimpleTip_BG("BG",self.screen,0))
        self.setScale(Vector2(0.6,0.6))
        self.preventRay(True)

class UISimpleTip_Text(MutiLineText):
    def __init__(self, name, screen, priority,txt,width,space=3):
        super().__init__(name, screen, priority,width,space)
        self.setTexts(txt,Data.fonts.FontRender.Null)
    def init(self):
        self.setFont(Data.fonts.FontSimpleTip)
        self.setColor(Data.fonts.ColorSimpleTip)

class UISimpleTip_BG(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(750,150)
        self.setImage(self.preResize("UI\\simpleTip.png"))

class UISimpleTipLine_800(UISimpleTip):
    def __init__(self, name, screen, priority, txt):
        super().__init__(name, screen, priority, txt, 750, 0)
        _obj = self.findChild("BG")
        _obj.setImage(_obj.preResize(_obj.sprite,Vector2(800/0.6,60)))