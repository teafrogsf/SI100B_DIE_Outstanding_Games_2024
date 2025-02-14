from AnimeSystem.Anime import *
from .AoeAnime import *
from RenderSystem.RotationSprite import RotationSprite,Sprite
from Data.types import *
from Data.rotation_linear_sprite_calc import *

from AudioSystem.AudioManager import audioManager

import random

class AoeAnime_FrenziedBloodBlade_Attacker(AoeAttackerAnime):
    def __init__(self,obj,combatRenderer,tempRenderer,info):
        self.tempRender = tempRenderer
        self.combatRenderer = combatRenderer
        self.rcdPos = obj.localPosition()
        _ani = AnimeInfo(len(info["receiver"])*8+3).add(AnimeType.Pos,0,obj.localPosition())
        _kp = -3
        _order = list(range(len(info["receiver"])))
        random.shuffle(_order)
        for index in _order:
            _kp += 8
            (_ani.add(AnimeType.Pos,_kp,self.combatRenderer.findChild(info["receiver"][index]).localPosition())
             .add(AnimeType.Pos,_kp+3,self.combatRenderer.findChild(info["receiver"][index]).localPosition()))
        _ani.add(AnimeType.Pos,_kp+6,obj.localPosition())
        Anime.__init__(self,obj, _ani.disableSprite().finish())
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Pos:
            if self.frame % 8 == 5 or self.frame %5 == 0:
                scale,rotation,mid = getLinearResult(self.rcdPos,self.Object.localPosition(),416)
                self.tempRender.Add(BloodTrace("bt",self.tempRender.screen,10,mid(),rotation),5,
                                    AnimeInfo(20).disableSprite().add(AnimeType.Scale,0,Vector2(scale().x,1.5))
                                    .add(AnimeType.Scale,20,Vector2(scale().x,0)).finish())
                for i in range(3):
                    self.tempRender.Add(Blood("bld",self.tempRender.screen,100,
                                              self.Object.localPosition()+Vector2(random.randint(-70,70),random.randint(-70,70))),5,
                                              AnimeInfo(50).disableSprite().enableAlpha().add(AnimeType.Alpha,0,255).add(AnimeType.Alpha,50,0)
                                              .add(AnimeType.Scale,0,Vector2.One()).add(AnimeType.Scale,50,Vector2(2,2)))
                audioManager.AddEffect("AttackSlash")
            self.rcdPos = self.Object.localPosition()

class BloodTrace(RotationSprite):
    def __init__(self, name, screen, priority,pos,rotation):
        super().__init__(name, screen, priority)
        self.setPos(pos)
        self.setRotation(rotation)
        self.setImage("Texture\\#87921.png")

class Blood(Sprite):
    def __init__(self, name, screen, priority,pos):
        super().__init__(name, screen, priority)
        self.setPos(pos)
        self.setImage(random.sample(["Texture\\blood{0}.png".format(i) for i in range(1,4)],1)[0])