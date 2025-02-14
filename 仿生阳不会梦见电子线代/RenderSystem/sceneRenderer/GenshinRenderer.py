from RenderSystem.Canvas import *
from RenderSystem.prefab.UIMap import *
from RenderSystem.prefab.UIMapObject import *

from GameDataManager import gameDataManager

class GenshinRenderer(Canvas):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        self.rcdTime = None
        self.smoothScale = Vector2.One()

        super().__init__(name, screen, priority)
    def init(self):
        self.setPos(Vector2(720,360))
        self.addChild(ChronoArkMap("map",self.screen,0))
        self.findChild("map").addMapTile(gameDataManager.getMapTile(gameDataManager.STAGE.getStageInfo()["map"]))
    def Render(self):
        self.screen.fill([0,0,0])
        self.draw()
    def rayCast(self, event):
        return super().rayCast(event)
    def update(self):
        _t = time.time()
        if self.rcdTime == None:
            self.smoothScale = Vector2.One()
        else:
            _v = (_t-self.rcdTime)/(1/60)
            self.smoothScale = Vector2(_v,_v)
        self.rcdTime = _t
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.moveCamera(Vector2(0,-12)*self.smoothScale)
        if keys[pygame.K_s]:
            self.moveCamera(Vector2(0,12)*self.smoothScale)
        if keys[pygame.K_a]:
            self.moveCamera(Vector2(-12,0)*self.smoothScale)
        if keys[pygame.K_d]:
            self.moveCamera(Vector2(12,0)*self.smoothScale)
        super().update()
    def moveCamera(self,vec):
        pos = self.findChild("map").moveCamera(vec())
        if isinstance(pos,Vector2):
            if Vector2(abs(pos.x),abs(pos.y)) >= Vector2(4500,3000):
                self.scene.EnterNowhere()
            if Vector2(abs(pos.x),abs(pos.y)) >= Vector2(3000,1500):
                self.scene.AtOutsideTheMap()