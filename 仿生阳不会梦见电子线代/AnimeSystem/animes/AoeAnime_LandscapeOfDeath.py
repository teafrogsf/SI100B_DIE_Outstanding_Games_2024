from AnimeSystem.Anime import *
from .AoeAnime import *
from RenderSystem.prefab.UICharacter import CharFace,CharSD
from RenderSystem.Sprite import Sprite,LoadImage

from AudioSystem.AudioManager import audioManager

from Data.types import *
import pygame

var_animeDelta = 45
var_enterDelay = 5
var_lightDelay = 25

img_red = Sprite("sp",None,0).preResize("Texture\\bloodmist_red.png",Vector2(1440,720))
img_light = Sprite("sp",None,0).preResize("Texture\\bloodmist_light.png",Vector2(1440,720))

class AoeAnime_LandscapeOfDeath_Attacker(AoeAttackerAnime):
    def __init__(self,obj,combatRenderer,tempRenderer,info):
        self.tempRender = tempRenderer
        self.combatRenderer = combatRenderer
        self.rcdPos = obj.localPosition()
        Anime.__init__(self,obj,AnimeInfo(50+var_animeDelta).disableSprite().add(AnimeType.Pos,5,Vector2.Zero()).add(AnimeType.Pos,5+var_animeDelta,Vector2.Zero())
                         .add(AnimeType.Pos,45+var_animeDelta,Vector2.Zero()).add(AnimeType.Pos,var_animeDelta+50,self.rcdPos).finish())
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Pos:
            _sp = self.getAttackerCharSprite()
            if _sp != None:
                if (frame == 0 or frame == 20+var_animeDelta):
                    _sp.setState(CharSD.Move)
                elif frame == 5+var_animeDelta:
                    _sp.setState(CharSD.Slash)
                    audioManager.AddEffect("AttackSlash")
                    self.tempRender.Add(BloodMistSlash("bms",self.tempRender.screen,100,Vector2.Zero(),_sp.face),45)

class BloodMistSlash(Sprite):
    def __init__(self, name, screen, priority,pos,face):
        self.face = face
        super().__init__(name, screen, priority)
        self.setPos(pos)
        self.setScale(Vector2(0.6,0.6))
        self.setImage("Texture\\bloodmist_slash.png")
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)

class AoeAnime_LandscapeOfDeath_Mimic(AoeEffectAnime):
    def __init__(self, centerPos, combatRender, tempRender, info):
        _ani = AnimeInfo(var_enterDelay+30).addDelay(var_enterDelay).add(AnimeType.Pos,0,Vector2.Zero())
        for i in range(1,6):
            _ani.add(AnimeType.Sprite,var_enterDelay+5*(i-1),LoadImage("Texture\mimic{0}.png".format(i)))
            _ani.add(AnimeType.Scale,var_enterDelay+5*(i-1),Vector2.One()+Vector2((i-1)*0.1,-(i-1)*0.05))
        Anime.__init__(self,Mimic("mimic",combatRender.screen,10000),_ani)

class Mimic(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("Texture\mimic1.png")

class AoeAnime_LandscapeOfDeath_BG(AoeEffectAnime):
    def __init__(self, centerPos, combatRender, tempRender, info):
        _obj = Mask("msk",combatRender.screen,5000)
        _obj.setImage(_obj.preResize("Texture\\bloodmist_bg.png",Vector2(1440,720)))
        _ani = (AnimeInfo(var_enterDelay+30).enableAlpha().addDelay(var_enterDelay).add(AnimeType.Pos,0,Vector2.Zero())
                .add(AnimeType.Alpha,var_enterDelay,0).add(AnimeType.Alpha,var_enterDelay+5,255))
        Anime.__init__(self,_obj,_ani)
class AoeAnime_LandscapeOfDeath_Light(AoeEffectAnime):
    def __init__(self, centerPos, combatRender, tempRender, info):
        _ani = (AnimeInfo(var_lightDelay+20).enableAlpha().addDelay(var_lightDelay).add(AnimeType.Pos,0,Vector2.Zero())
                .add(AnimeType.Alpha,var_lightDelay,0).add(AnimeType.Alpha,var_lightDelay+5,255)
                .add(AnimeType.Sprite,var_lightDelay,img_red.copy())
                .add(AnimeType.Sprite,var_lightDelay+10,img_light.copy()))
        Anime.__init__(self,Mask("msk",combatRender.screen,20000),_ani)
class AoeAnime_LandscapeOfDeath_Mask(AoeEffectAnime):
    def __init__(self, centerPos, combatRender, tempRender, info):
        _ani = (AnimeInfo(var_lightDelay+16).addDelay(var_lightDelay+10).add(AnimeType.Pos,0,Vector2.Zero())
                .add(AnimeType.Pos,var_lightDelay+12,Vector2.Zero()).add(AnimeType.Pos,var_lightDelay+16,Vector2(1440,0)))
        Anime.__init__(self,Mask("msk",combatRender.screen,30000),_ani)
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Pos and frame == var_lightDelay+12:
            audioManager.AddEffect("AttackPierce")


class Mask(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("Texture\\bloodmist_black.png",Vector2(1440,720)))