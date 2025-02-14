from AnimeSystem.Anime import *
from .AoeAnime import *
from RenderSystem.Sprite import Sprite,LoadImage

from Data.types import *
from AudioSystem.AudioManager import audioManager

class AoeAnime_WarpedBlade_SpellCircle(AoeEffectAnime):
    def __init__(self, centerPos, combatRender, tempRender, info):
        _ani = (AnimeInfo(50).disableSprite().enableAlpha().add(AnimeType.Scale,0,Vector2(0.1,0.1))
                .add(AnimeType.Scale,30,Vector2.One()).add(AnimeType.Alpha,0,128).add(AnimeType.Alpha,10,255)
                .add(AnimeType.Pos,0,centerPos()+Vector2(0,0)).add(AnimeType.Scale,45,Vector2.One()).add(AnimeType.Scale,50,Vector2(5,5)).finish())
        Anime.__init__(self,SpellCircle("sc",combatRender.screen,100),_ani)

class SpellCircle(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("Texture\\warpedBlade_circle.png")

class AoeAnime_WarpedBlade_Blade(AoeEffectAnime):
    def __init__(self, centerPos, combatRender, tempRender, info):
        self.centerPos = centerPos
        self.tempRender = tempRender
        _ani = (AnimeInfo(56).add(AnimeType.Active,0,False).add(AnimeType.Active,10,True).add(AnimeType.Pos,0,centerPos()+Vector2(0,-600))
                .add(AnimeType.Pos,30,centerPos()+Vector2(0,-700)).add(AnimeType.Pos,50,centerPos()+Vector2(0,-700)).add(AnimeType.Pos,53,centerPos()+Vector2(0,-100))
                .add(AnimeType.Sprite,50,LoadImage("Texture\\warpedBlade_drop.png")).add(AnimeType.Sprite,53,LoadImage("Texture\\warpedBlade_wait.png")).finish())
        Anime.__init__(self,Blade("bld",combatRender.screen,100),_ani)
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Sprite and frame == 53:
            self.tempRender.Add(Explode("ex",self.tempRender.screen,1000),5,
                                    AnimeInfo(25).enableAlpha().disableSprite().add(AnimeType.Pos,0,self.centerPos()-Vector2(0,90))
                                    .add(AnimeType.Scale,20,Vector2(1,1)).add(AnimeType.Scale,25,Vector2(1.5,1.5))
                                    .add(AnimeType.Alpha,0,255).add(AnimeType.Alpha,20,128).add(AnimeType.Alpha,25,0).finish())
            audioManager.AddEffect("Explosion")
            audioManager.AddEffect("Explosion",2)
            audioManager.AddEffect("Explosion",4)
            audioManager.AddEffect("Explosion",6)
            #WOW!

class Blade(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("Texture\\warpedBlade_wait.png")
class Explode(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("Texture\\warpedBlade_explode.png")