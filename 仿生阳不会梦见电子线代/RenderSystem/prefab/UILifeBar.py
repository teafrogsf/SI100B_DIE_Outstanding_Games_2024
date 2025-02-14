from RenderSystem.Canvas import *
from RenderSystem.CanvasAutosort import *
from RenderSystem.BarSprite import *
from RenderSystem.Sprite import *
from RenderSystem.Text import *

import Data.fonts

class UILifeBarBlock(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority,AutoSortType(
            Vector2(0,0),Vector2(0,1),-5
        ))
    def init(self):
        self.addChild(UILifeBarLine("Life",self.screen,0,"lifeIcon.png",Data.fonts.ColorRed,"lifeBar.png","lifeBg.png"))
        self.addChild(UILifeBarLine("Stagger",self.screen,0,"staggerIcon.png",Data.fonts.ColorYellow,"staggerBar.png","staggerBg.png"))
    def setValue(self,dit):
        '''
        Dict:
        -life-num
             -maxinum
        -stagger-num
                -maxinum
        '''
        self.findChild("Life").setValue(dit["life"]["num"],dit["life"]["maxinum"])
        self.findChild("Stagger").setValue(dit["stagger"]["num"],dit["stagger"]["maxinum"])
class UILifeBarLine(Canvas):
    def __init__(self, name, screen, priority,img,color,img2,img3):
        super().__init__(name, screen, priority)
        self.addChild(UILifeIcon("icon",self.screen,0,img))
        self.addChild(UILifeText("text",self.screen,5,color))
        self.addChild(UILifeBar("bar",self.screen,0,img2))
        self.addChild(UILifeBar("bg",self.screen,-5,img3))

        self.setBaseRect(pygame.rect.Rect(0,0,240,40))
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("text").setPos(Vector2(-60,0)*self.worldScale())
        self.findChild("icon").setPos(Vector2(-100,0)*self.worldScale())
        self.findChild("bar").setPos(Vector2(40,0)*self.worldScale())
        self.findChild("bg").setPos(Vector2(40,0)*self.worldScale())
    def setValue(self,num,maxinum):
        self.findChild("text").setText(str(int(num)),Data.fonts.FontRender.Outline)
        #why should sb set a maxinum to ZERO ???????????
        if maxinum == 0:
            self.findChild("bar").setPercentage(1.0)
        else:
            self.findChild("bar").setPercentage(num/maxinum)
class UILifeIcon(Sprite):
    def __init__(self, name, screen, priority, img):
        self.tmp_icon = img
        super().__init__(name, screen, priority)
    def init(self):
        self.setImage(self.preResize(self.tmp_icon,Vector2(40,40)))
class UILifeText(Text):
    def __init__(self, name, screen, priority,color):
        super().__init__(name, screen, priority)
        self.setColor(color)
    def init(self):
        self.setFont(Data.fonts.FontLife)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setText("0",Data.fonts.FontRender.Outline)
class UILifeBar(BarSprite):
    def __init__(self, name, screen, priority,img):
        self.tmp_image = img
        super().__init__(name, screen, priority)
    def init(self):
        super().init()
        self.setSlideChoice(BarSlideChoice.Left)
        self.setImage(self.tmp_image)