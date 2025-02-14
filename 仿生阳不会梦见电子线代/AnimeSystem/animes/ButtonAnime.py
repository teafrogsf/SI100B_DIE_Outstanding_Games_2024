from AnimeSystem.Anime import *

from Data.types import *

class ButtonClickAnime(Anime):
    def __init__(self, obj):
        super().__init__(obj, AnimeInfo(4).disableSprite().add(AnimeType.Scale,0,Vector2(0.8,0.8))
                         .add(AnimeType.Scale,4,Vector2.One()).finish())

class ButtonDisapperAnime(Anime):
    def __init__(self, obj):
        super().__init__(obj, AnimeInfo(10).disableSprite().add(AnimeType.Scale,0,obj.localScale())
                         .add(AnimeType.Scale,10,Vector2(0.05,0.05)).add(AnimeType.Active,10,False).finish())