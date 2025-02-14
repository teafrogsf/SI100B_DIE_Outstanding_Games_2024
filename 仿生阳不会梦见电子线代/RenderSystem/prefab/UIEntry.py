from RenderSystem.CanvasAutosort import *
from RenderSystem.Sprite import *
from RenderSystem.Text import *
from RenderSystem.ButtonSprite import *

from AnimeSystem.animes.ButtonAnime import ButtonClickAnime

from AudioSystem.AudioManager import audioManager

class UIEntryLine(CanvasAutoSort):
    def __init__(self, name, screen, priority, scene):
        self.scene = scene
        self.cacheText = None
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),20
        ))
    def init(self):
        self.addChild(UIEntry("entry",self.screen,0))
        self.addChild(UIConfirmIcon("no",self.screen,0,"UI\\confirmNo.png"))
        self.addChild(UIConfirmIcon("yes",self.screen,0,"UI\\confirmYes.png"))
    def OnChildClick(self,nam):
        if nam == "no":
            self.findChild("entry").findChild("txt").setText(" ",Data.fonts.FontRender.Null)
            self.cacheText = None
            audioManager.AddEffect("ButtonClick")
        elif nam == "yes":
            if self.cacheText == None:
                return
            self.findChild("entry").findChild("txt").setText(" ",Data.fonts.FontRender.Null)
            self.scene.AtEntryConfirmed(self.cacheText)
            self.cacheText = None
            audioManager.AddEffect("ButtonClick")
        elif nam == "entry":
            self.cacheText = self.scene.AtEntryTexted()
            return (" " if self.cacheText == None else self.cacheText)

class UIEntry(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setBaseRect(pygame.Rect(0,0,800,30))
        self.addChild(UIEntry_Button("BG",self.screen,-5))
        self.addChild(UIEntry_Text("txt",self.screen,5))
    def OnClick(self, event):
        self.findChild("BG").setState(1)
        self.AniCreate(ButtonClickAnime(self))
        self.AniActivate()
    def AniDestroy(self):
        super().AniDestroy()
        self.findChild("txt").setText(self.parent.OnChildClick(self.name),Data.fonts.FontRender.Null)
        self.findChild("BG").setState(0)


class UIEntry_Button(Sprite):
    def __init__(self, name, screen, priority):
        self.state = None
        super().__init__(name, screen, priority)
        self.preSize = Vector2(800,30)
        self.setState(0)
    def setState(self,state):
        self.state = state
        if self.state == 1:
            self.setImage(self.preResize("UI\\ButtonSP2.png"))
        else:
            self.setImage(self.preResize("UI\\ButtonBG2.png"))
class UIEntry_Text(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontButton1)
        self.setColor(Data.fonts.ColorSimpleTip)
    def setValue(self,txt):
        self.setText(txt,Data.fonts.FontRender.Outline)

class UIConfirmIcon(ButtonSprite):
    def __init__(self, name, screen, priority,img):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize(img,Vector2(40,40)))
    def OnClick(self, event):
        self.AniCreate(ButtonClickAnime(self))
        self.AniActivate()
        self.parent.OnChildClick(self.name)

