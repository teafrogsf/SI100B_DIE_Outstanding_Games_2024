from AnimeSystem.Anime import *
from Data.types import Vector2

from AudioSystem.AudioManager import audioManager

class CardDiceRollingAnime_DiceImg(Anime):
    def __init__(self, obj,rolled_img):
        super().__init__(obj, AnimeInfo(20).add(AnimeType.Sprite,10,rolled_img).finish(), AnimeOp.Keep)
    def Sprite(self):
        return self.Object
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Sprite and frame == 10:
            audioManager.AddEffect("DiceRolling")

class CardDiceRollingAnime_DiceText(Anime):
    def __init__(self, obj):
        super().__init__(obj, 
                         AnimeInfo(20).add(AnimeType.Scale,0,Vector2(1,1))
                         .add(AnimeType.Active,10,True).add(AnimeType.Scale,10,Vector2(0.6,0.6))
                         .add(AnimeType.Scale,15,Vector2(1.5,1.5)).add(AnimeType.Scale,18,Vector2.One())
                         .disableSprite().finish(), AnimeOp.Keep)