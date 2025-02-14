#哎 wa sensei的右手

from .UIMapObject import *
from .UICharacter import CharFace
from AnimeSystem.Anime import *

from Data.instance import *

class MapCharMoveAnime(Anime):
    def __init__(self, obj, aniInfo):
        super().__init__(obj, aniInfo, AnimeOp.Keep)
    def Sprite(self):
        return self.Object
    

@instance
class MapCharSD:
    def __init__(self):
        self.idle = LoadImage("mapChar\\idle.png")
        self.move = [LoadImage("mapChar\\SpineFrame_"+str(i)+".png") for i in range(18)]
    def genMoveAnime(self,char):
        _ani = AnimeInfo(36)
        for i in range(18):
            _ani.add(AnimeType.Sprite,i*2,self.move[i])
        _ani.finish()
        return MapCharMoveAnime(char,_ani)
    def getIdle(self):
        return self.idle

mapCharSD = MapCharSD()


class UIMapChar(MapColliderableObject):
    def __init__(self, name, screen, priority, mapPos):
        super().__init__(name, screen, priority, mapPos)
        self.addChild(UIMapCharSprite("sp",self.screen,0))
        self.setBaseRect((lambda x = self.findChild("sp").sprite.get_rect():pygame.Rect(0,0,x.width,x.height//3))())

class UIMapCharSprite(Sprite):
    def __init__(self, name, screen, priority):
        self.face = CharFace.Right
        self.isStill = True 
        super().__init__(name, screen, priority)
        self.setImage(mapCharSD.getIdle())
    def setFace(self,face):
        if face == None:
            return
        self.face = face
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)
    def isMoving(self,keys):
        return keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]
    def isFacing(self,keys):
        return CharFace.Left if keys[pygame.K_a] else CharFace.Right if keys[pygame.K_d] else None
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if self.isMoving(keys):
            self.setFace(self.isFacing(keys))
            if self._anime == None:
                self.AniCreate(mapCharSD.genMoveAnime(self))
                self.AniActivate()
                self.isStill = False
        elif not self.isStill:
            self.isStill = True
            if self._anime != None:
                self._anime.destroy()
            self.setImage(mapCharSD.getIdle())

class MapCannotGoodEnough(MapColliderableObject):
    def __init__(self, name, screen, priority, mapPos):
        super().__init__(name, screen, priority, mapPos)
        self.addChild(CannotGoodEnough("sp",self.screen,0))
        self.addChild(What("what",self.screen,5))
        self.findChild("what").setActive(False)
        self.setBaseRect((lambda x = self.findChild("sp").sprite.get_rect():pygame.Rect(0,0,x.width,x.height//3))())
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("what").setPos(Vector2(180,-200)*self.worldScale())
    def update(self):
        super().update()
        LUCY = self.parent.findChild("Lucy")
        if not isinstance(LUCY,UIMapChar):
            return
        if LUCY.mapPos().x < self.mapPos().x:
            self.findChild("sp").setFace(CharFace.Left)
        else:
            self.findChild("sp").setFace(CharFace.Right)
        if LUCY.mapPos().y > self.mapPos().y:
            if self.priority > LUCY.priority:
                self.setPriority(LUCY.priority-5)
        else:
            if self.priority < LUCY.priority:
                self.setPriority(LUCY.priority+5)
        if (LUCY.mapPos() - self.mapPos()).length() < 350:
            if not self.findChild("what").active:
                from SceneSystem.Scene import Scene
                _scene = self.parent.parent.scene
                if isinstance(_scene,Scene):
                    _scene.rendererTempObject.AddSimpleTip("回忆你的O神键位",450,Vector2(0,-200),45)
            self.findChild("what").setActive(True)
        else:
            self.findChild("what").setActive(False)
    def OnKeyClick(self, event):
        if self.findChild("what").active == False:
            return
        if event.key == pygame.K_f:
            self.parent.delChild(self.name)
            self.parent.parent.scene.EnterGeneratingScene()
        

class CannotGoodEnough(Sprite):
    def __init__(self, name, screen, priority):
        self.face = CharFace.Right
        super().__init__(name, screen, priority)
        self.setImage("mapChar\\goodenough.png")
    def setFace(self,face):
        if face == None:
            return
        self.face = face
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)

class What(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("UI\\what.png",Vector2(120,120)))


class MapMist(MapObject):
    def __init__(self, name, screen, priority, mapPos):
        super().__init__(name, screen, priority, mapPos, False)
        self.addChild(Mist("sp",self.screen,0))
        self.setBaseRect(self.findChild("sp").sprite.get_rect())
    def update(self):
        super().update()
        LUCY = self.parent.findChild("Lucy")
        if (LUCY.mapPos() - self.mapPos()).length() < 250:
            self.parent.delChild("mist")
            self.parent.parent.scene.EnterDeckSelectionScene()

class Mist(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setImage("mapChar\\blackMist.png")
    