from AnimeSystem.Anime import *
from RenderSystem.prefab.UICombatCharacter import CharSD,CharFace
from RenderSystem.prefab.UICharacter import UICharSprite
from RenderSystem.Sprite import *

from Data.types import *
from enum import Enum
import random

from AudioSystem.AudioManager import audioManager

class CharActionType(Enum):
    Remain = 0
    EnterStage = 1
    LeaveStage = 2
    Stay = 3

class CombatCharAnime_CharSprite(Anime): 
    def proceedSprite(self, st=False):
        if st:
            self.Object.setState(self.frameDelta[2][0][1])
            return
        if self.pin[2] < len(self.frameDelta[2]):
            if self.frameDelta[2][self.pin[2]][0] == self.frame:
                self.Object.setState(self.frameDelta[2][self.pin[2]][1])
                self.pin[2] += 1
                self.OnKFrame(AnimeType.Sprite,self.frame)
    def OnKFrame(self, typ, frame):
        if typ == AnimeType.Sprite:
            if isinstance(self.Object,UICharSprite):
                _scene = self.Object.getCombatScene()
                if _scene == None:
                    return
                if self.Object.SD == CharSD.Slash:
                    _scene.rendererTempObject.Add(CombatAttackFlash("fh",self.Object.screen,1000,self.Object.worldPosition(),
                                                                    self.Object.face,AttackFlashType.Slash),15)
                    audioManager.AddEffect("AttackSlash")
                elif self.Object.SD == CharSD.Pierce:
                    _scene.rendererTempObject.Add(CombatAttackFlash("fh",self.Object.screen,1000,self.Object.worldPosition(),
                                                                    self.Object.face,AttackFlashType.Pierce),15)
                    audioManager.AddEffect("AttackPierce")
                elif self.Object.SD == CharSD.Blunt:
                    _scene.rendererTempObject.Add(CombatAttackFlash("fh",self.Object.screen,1000,self.Object.worldPosition(),
                                                                    self.Object.face,AttackFlashType.Blunt),15)
                    audioManager.AddEffect("AttackBlunt")
                elif self.Object.SD == CharSD.Block:
                    _scene.rendererTempObject.Add(CombatAttackFlash("fh",self.Object.screen,1000,self.Object.worldPosition(),
                                                                    self.Object.face,AttackFlashType.Blunt),15)
                    audioManager.AddEffect("DefenseBlock",3)
                elif self.Object.SD == CharSD.Evade:
                    audioManager.AddEffect("DefenseEvade",3)

class CombatCharAnime_SimpleAct(CombatCharAnime_CharSprite):
    def __init__(self, obj, lasFrame,actionState):
        super().__init__(obj, AnimeInfo(lasFrame).add(AnimeType.Sprite,0,actionState).uncommonSprite().finish(), AnimeOp.Keep)

class CombatCharAnime_CharMove(Anime):
    def __init__(self, obj, lasFrame,Pstart,Pend,charType = CharActionType.Remain):
        ani = AnimeInfo(lasFrame).add(AnimeType.Pos,0,Pstart).add(AnimeType.Pos,lasFrame,Pend)
        if charType == CharActionType.EnterStage:
            ani.add(AnimeType.Active,0,True)
        elif charType == CharActionType.LeaveStage:
            ani.add(AnimeType.Active,lasFrame,False)
        super().__init__(obj, ani.disableSprite().finish())

class CombatCharAnime_Death(Anime):
    def __init__(self, obj,delay=0):
        _curScale = obj.localScale()
        if delay == 0:
            super().__init__(obj, AnimeInfo(5).add(AnimeType.Scale,0,_curScale()).add(AnimeType.Scale,5,Vector2(0,_curScale.y))
                         .disableSprite().add(AnimeType.Active,5,False).finish())
        else:
            super().__init__(obj, AnimeInfo(5+delay).add(AnimeType.Scale,delay,_curScale()).add(AnimeType.Scale,5+delay,Vector2(0,_curScale.y))
                         .disableSprite().add(AnimeType.Active,5+delay,False).add(AnimeType.Scale,0,_curScale()).finish())

class AnimeSprite_DeathBook(Sprite):
    def __init__(self, name, screen, priority,pos,scale = Vector2.One()):
        super().__init__(name, screen, priority)
        self.preSize = Vector2(150,225)
        self.setImage(self.preResize("deathBook.png"))
        self.setPos(pos)
        self.setScale(scale)

class CombatCharAnime_DeathBook(Anime):
    def __init__(self, obj,delay=0):
        _curScale = obj.localScale()
        if delay == 0:
            super().__init__(obj, AnimeInfo(30).enableAlpha().add(AnimeType.Alpha,0,255).add(AnimeType.Alpha,15,255)
                         .add(AnimeType.Alpha,25,0).add(AnimeType.Scale,0,Vector2(0,1)).add(AnimeType.Scale,5,Vector2(0,_curScale.y))
                         .add(AnimeType.Scale,15,_curScale()).add(AnimeType.Scale,30,_curScale()+Vector2(2,2)))
        else:
            super().__init__(obj, AnimeInfo(30+delay).enableAlpha().add(AnimeType.Alpha,delay,255).add(AnimeType.Alpha,15+delay,255)
                         .add(AnimeType.Alpha,25+delay,0).add(AnimeType.Scale,delay,Vector2(0,_curScale.y)).add(AnimeType.Scale,5+delay,Vector2(0,_curScale.y))
                         .add(AnimeType.Scale,15+delay,_curScale).add(AnimeType.Scale,30+delay,_curScale()+Vector2(2,2))
                         .add(AnimeType.Active,0,False).add(AnimeType.Active,delay,True).finish())
    def Sprite(self):
        return self.Object

class AttackFlashType(Enum):
    Slash = ("slash",30)
    Pierce = ("pierce",16)
    Blunt = ("blunt",18)

class CombatAttackFlash(Sprite):
    def __init__(self, name, screen, priority,pos,face,typ):
        self.face = face
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("Texture\\attackTexture\\{0} ({1}).png".format(typ.value[0],random.randint(1,typ.value[1])),Vector2(0,300)))
        #print(pos()-Vector2(720,360))
        self.setPos(pos()-Vector2(720,360)+(Vector2(100,0) if face == CharFace.Left else Vector2(-100,0)))
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)