from AnimeSystem.Anime import *
from RenderSystem.MutiLineText import MutiLineText,Text

from AudioSystem.AudioManager import audioManager

import Data.fonts

class PrintingTextAnime(Anime):
    def __init__(self, obj, txt):
        self._txt = txt
        _aniInfo = AnimeInfo(len(txt)*6+10).disableSprite()
        for i in range(len(txt)+1):
            _aniInfo.add(AnimeType.Active,i*6,True)
        super().__init__(obj,_aniInfo.finish())
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Active:
            if isinstance(self.Object,MutiLineText):
                self.Object.setTexts(self._txt[:frame//6],Data.fonts.FontRender.Null)
            if frame%180 == 0:
                audioManager.AddEffect("Typing")

class AppearingTextAnime(Anime):
    def __init__(self, obj, fr):
        super().__init__(obj, AnimeInfo(fr).disableSprite().enableAlpha().add(AnimeType.Active,0,True).add(AnimeType.Alpha,0,0).add(AnimeType.Alpha,fr,255).finish())
    def Sprite(self):
        return self.Object