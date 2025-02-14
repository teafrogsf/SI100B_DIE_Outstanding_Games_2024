#哎 wa sensei的左手）））

from RenderSystem.Sprite import *
from RenderSystem.Canvas import *

class MapObject(Canvas):
    def __init__(self, name, screen, priority,mapPos,isCollider=False):
        self.mapPos = mapPos()
        self.isCollider = isCollider
        self.isOnMap = True

        self.preventRay(True)

        super().__init__(name, screen, priority)
    def loadChild(self):
        pass
    def setCollider(self,bl):
        self.isCollider = bl
    def genMapRect(self):
        if isinstance(self.rect,pygame.Rect):
            return pygame.Rect(self.mapPos.x-self.rect.width/2,self.mapPos.y-self.rect.height/2,self.rect.width,self.rect.height)
    def Collider(self,rct):
        if not self.isCollider:
            return False
        if not self.isOnMap:
            return False
        _rct = self.genMapRect()
        return False if not isinstance(_rct,pygame.Rect) else _rct.colliderect(rct)
    def alterMapPos(self,vec,Camera):
        if isinstance(vec,Vector2):
            self.mapPos += vec
    def draw(self,Camera):
        if not self.active:
            return False
        #self.Clean()
        Camera = Camera()
        if isinstance(self.rect,pygame.Rect) and isinstance(Camera,Vector2) and isinstance(self.mapPos,Vector2):
            if pygame.Rect(Camera.x-720,Camera.y-360,1440,720).colliderect(
                pygame.Rect(self.mapPos.x-self.rect.width/2,self.mapPos.y-self.rect.height/2,self.rect.width,self.rect.height)):
                self.isOnMap = True
                self.setPos(Vector2(self.mapPos.x-Camera.x,self.mapPos.y-Camera.y))
                if len(self.children) == 0:
                    self.loadChild()
                return super().draw()
            else:
                self.isOnMap = False

class MapTile(MapObject):
    def __init__(self, name, screen,mapPos,tile,presize):
        self._tile = tile
        self._presize = presize
        super().__init__(name, screen, -114514,mapPos,False)
        self.setBaseRect(pygame.Rect(0,0,presize().x,presize().y))
    def loadChild(self):
        self.addChild(MapTile_Sprite("tile",self.screen,0,self._tile,self._presize))
        
class MapTile_Sprite(Sprite):
    def __init__(self, name, screen, priority,tile,presize):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize(tile,presize()))

class MapColliderableObject(MapObject):
    def __init__(self, name, screen, priority, mapPos):
        super().__init__(name, screen, priority, mapPos, True)