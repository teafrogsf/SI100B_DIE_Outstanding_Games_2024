from AnimeSystem.Anime import *

from RenderSystem.Text import *

class TempObjectAnime(Anime):
    def __init__(self,lasFrame, obj,aniInfo=None):
        super().__init__(obj, AnimeInfo(lasFrame).setTimer() if aniInfo == None else aniInfo)
    def destroy(self):
        super().destroy()
        self.Object.parent.delChild(self.Object.name)
    def Sprite(self):
        return self.Object

class FloatingTextAnime(TempObjectAnime):
    def __init__(self, obj, txt):
        self._txt = txt
        _len = len(txt)*6+30
        _aniInfo = AnimeInfo(_len).disableSprite().enableAlpha().add(AnimeType.Alpha,0,150).add(AnimeType.Alpha,_len-30,150).add(AnimeType.Alpha,_len,0)
        for i in range(len(txt)+1):
            _aniInfo.add(AnimeType.Active,i*6,True)
        super().__init__(_len,obj,_aniInfo.finish())
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Active:
            if isinstance(self.Object,Text):
                self.Object.setText(self._txt[:frame//6],Data.fonts.FontRender.Outline)