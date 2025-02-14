from RenderSystem.DrawableObject import *

from Data.bezier_curve import *
import math,random

class UIEmotionLine(Drawableobject):
    def __init__(self, name, screen, priority,stPoint,edPoint,color):
        super().__init__(name, screen, priority)
        self.points = bezier_curve(stPoint()+Vector2(random.randint(-50,50),random.randint(-50,50))+Vector2(720,360),edPoint()+Vector2(random.randint(-50,50),random.randint(-50,50))+Vector2(720,360),-500)
        self.frame = 0
        self.color = color
    def proceed(self,frame):
        self.frame = frame
    def draw(self):
        if Rectableobject.draw(self):
            if self.frame <= 20:
                _t = int(math.floor(100*self.frame/20))
                self.safeDraw(self.points[0:_t],3)
                for m in [[4,5],[2,7],[1.5,10],[1.1,15]]:
                    self.safeDraw(self.points[int(_t//m[0]):_t],m[1])
            elif self.frame > 23:
                _t = int(math.ceil(100*(self.frame-23)/7))
                self.safeDraw(self.points[_t:100],3)
                for m in [[2,5],[4,7],[5,10],[8,15]]:
                    self.safeDraw(self.points[int(_t*m[0]):100],m[1])
    def safeDraw(self,points,width):
        if len(points) >= 2:
            pygame.draw.lines(self.screen,self.color,False,points,width)