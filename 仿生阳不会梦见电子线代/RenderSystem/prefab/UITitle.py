from RenderSystem.Sprite import *
from RenderSystem.Text import *
from RenderSystem.CanvasAutosort import *

import Data.fonts

class UITitleRoundStart_BG(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(1000,0)
        self.setImage(self.preResize("UI\\titleRoundStart.png"))
        self.setPos(Vector2.Zero())

class UITitleRoundStart_Title(Text):
    def __init__(self, name, screen, priority,txt):
        self._txt = txt
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontTitleRoundStart)
        self.setColor(Data.fonts.ColorSimpleTip)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setText(self._txt,Data.fonts.FontRender.Outline)
        self.setPos(Vector2.Zero())

class UITitleVictory(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("UI\\titleVictory.png")

class UITitleDefeat(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("UI\\titleDefeat.png")

class UITitleResultText(Text):
    def __init__(self, name, screen, priority,color,txt):
        self._color = color
        self._txt = txt
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontBattleResult)
        self.setColor(self._color)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setText(self._txt,Data.fonts.FontRender.Outline)
        self.setPos(Vector2.Zero())

class UISceneTransfer(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("background\\starField.png",Vector2(1440,720)))

class UISceneBlurBG(Sprite):
    def __init__(self, name, screen, priority,img):
        super().__init__(name, screen, priority)
        from Data.gaussian_blur import apply_gaussian_blur
        self.setImage(self.preResize(apply_gaussian_blur(LoadImage(img)),Vector2(1440,720)))
class UISceneTitle(CanvasAutoSort):
    def __init__(self, name, screen, priority,index,title):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),10
        ))
        self.addChild(UISceneTitle_operation("op",self.screen,0))
        self.addChild(UISceneTitle_index("id",self.screen,0,index))
        self.addChild(UISceneTitle_title("title",self.screen,0,title))


class UISceneTitle_operation(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Nova),50))
        self.setColor(Data.fonts.ColorWhite)
        self.setText("RECEPTION",Data.fonts.FontRender.Null)
class UISceneTitle_index(Text):
    def __init__(self, name, screen, priority,txt):
        self._txt = txt
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Nova),100))
        self.setColor(Data.fonts.ColorWhite)
        self.setText(self._txt,Data.fonts.FontRender.Null)
class UISceneTitle_title(Text):
    def __init__(self, name, screen, priority,txt):
        self._txt = txt
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),70))
        self.setColor(Data.fonts.ColorWhite)
        self.setText(self._txt,Data.fonts.FontRender.Null)