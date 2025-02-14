from AnimeSystem.Anime import *
from .AoeAnime import *
from .CombatAttackAnime import *

from RenderSystem.Sprite import Sprite,LoadImage
from RenderSystem.prefab.UICharacter import CharFace,CharSD

from AudioSystem.AudioManager import audioManager

from Data.types import *
import pygame

class AoeAnime_RangingInferno_Attacker(AoeAttackerAnime):
    def __init__(self,obj,combatRenderer,tempRenderer,info):
        self.tempRender = tempRenderer
        self.combatRenderer = combatRenderer
        self.rcdPos = obj.localPosition()
        Anime.__init__(self,obj, (AnimeInfo(45).disableSprite().add(AnimeType.Pos,5,Vector2.Zero())
                                  .add(AnimeType.Pos,15,Vector2.Zero()).add(AnimeType.Pos,30,Vector2.Zero())
                                  .add(AnimeType.Pos,40,Vector2.Zero()).add(AnimeType.Pos,45,Vector2.Zero()).finish()))
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Pos:
            _sp = self.getAttackerCharSprite()
            if _sp != None:
                if (frame == 0 or frame == 40):
                    _sp.setState(CharSD.Move)
                    if frame == 40:
                        audioManager.AddEffect("AttackSlash")    
                elif frame == 15 or frame == 30:
                    _sp.setState(CharSD.Slash)
                    audioManager.AddEffect("AttackSlash")
                    if frame == 15:
                        self.tempRender.Add(LowellSlash("bms15",self.tempRender.screen,1000,_sp.face,False),40,
                                            SlashAnime(40,Vector2(-100 if _sp.face == CharFace.Right else 100,90),Vector2(1,1),_sp.face))                      
                    else:
                        self.tempRender.Add(LowellSlash("bms30",self.tempRender.screen,1000,_sp.face,True),25,
                                            SlashAnime(25,Vector2(-250 if _sp.face == CharFace.Right else 250,-40),Vector2(1.5,1.5),_sp.face)) 
                        
class LowellSlash(Sprite):
    def __init__(self, name, screen, priority,face,yFilp):
        self.face = face
        self.yFilp = yFilp
        super().__init__(name, screen, priority)
        self.setImage("Texture\\lowell_slash.png")
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            self.worldSprite = pygame.transform.flip(self.worldSprite,(True if self.face == CharFace.Left else False),self.yFilp)

