from RenderSystem.CanvasAutosort import *
from RenderSystem.Sprite import *
from RenderSystem.MutiLineText import *

from AnimeSystem.animes.ButtonAnime import ButtonClickAnime

from enum import Enum
import Data.fonts

from GameDataManager import gameDataManager as gdm
from AudioSystem.AudioManager import audioManager

class GameDifficulty(Enum):
    BabySitter = 0
    Normal = 1
    Hell = 2

class UIDifficultyArray(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),-20
        ))
    def init(self):
        for e in GameDifficulty:
            self.addChild(UIDifficulty("diff{0}".format(e.value),self.screen,0,e))

class UIDifficulty(Canvas):
    def __init__(self, name, screen, priority,diff):
        self.diff = diff
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UIDifficulty_BG("BG",self.screen,-100,self.diff))
        self.addChild(UIDifficulty_Icon("icon",self.screen,0,self.diff))
        self.addChild(UIDifficulty_Desq("desq",self.screen,5,self.diff))
        self.addChild(UIDifficulty_Title("title",self.screen,10,self.diff))

        self.setBaseRect(self.findChild("BG").sprite.get_rect())
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()

        self.findChild("icon").setPos(Vector2(0,-100)*self.worldScale())
        self.findChild("title").setPos(Vector2(0,0)*self.worldScale())
        self.findChild("desq").setPos(Vector2(0,100)*self.worldScale())
    def OnClick(self, event):
        audioManager.AddEffect("ButtonClick")
        self.AniCreate(ButtonClickAnime(self))
        self.AniActivate()
        gdm.GAME_DIFFICULTY = self.diff.value
        self.parent.parent.scene.AtEnterGame()

class UIDifficulty_BG(Sprite):
    def __init__(self, name, screen, priority,diff):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("UI\\diffBG{0}.png".format(diff.value),Vector2(300,450)))
class UIDifficulty_Icon(Sprite):
    def __init__(self, name, screen, priority,diff):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("UI\\diffIcon{0}.png".format(diff.value),Vector2(100,100)))
class UIDifficulty_Desq(MutiLineText):
    def __init__(self, name, screen, priority,diff):
        super().__init__(name, screen, priority, 200,3)
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),15))
        self.setColor(Data.fonts.ColorWhite)
        self.setTexts("；".join(gdm.Lang["Difficulty"][diff.value]["Desq"]),Data.fonts.FontRender.Null)
class UIDifficulty_Title(Text):
    def __init__(self, name, screen, priority,diff):
        super().__init__(name, screen, priority)
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),30))
        self.setColor(Data.fonts.ColorSimpleTip)
        self.setText(gdm.Lang["Difficulty"][diff.value]["Title"],Data.fonts.FontRender.Null)
