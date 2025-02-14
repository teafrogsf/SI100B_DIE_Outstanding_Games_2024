from AnimeSystem.Anime import *
from RenderSystem.prefab.UICharacter import CharFace

from Data.types import *

class SlashAnime(AnimeInfo):
    def __init__(self, las,pos,scale,face):
        super().__init__(las)
        slideIn = max(las//7,1)
        fadeOut = max(las//2,1)
        self.enableAlpha().add(AnimeType.Alpha,0,128).add(AnimeType.Alpha,slideIn,255)
        self.add(AnimeType.Scale,0,scale()-Vector2(0.4,0.4)).add(AnimeType.Scale,slideIn,scale())
        self.add(AnimeType.Pos,0,pos()-Vector2(slideIn*40*(-1 if face == CharFace.Right else 1),0)).add(AnimeType.Pos,slideIn,pos())
        self.add(AnimeType.Alpha,las-fadeOut,255).add(AnimeType.Alpha,las,60)