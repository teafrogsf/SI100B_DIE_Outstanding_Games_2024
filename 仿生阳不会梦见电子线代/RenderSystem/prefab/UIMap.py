#哎 wa sensei的大手）））

from RenderSystem.Canvas import *
from RenderSystem.Sprite import *

from .UIMapObject import MapObject,MapTile,MapColliderableObject
from .UIMapChar import UIMapChar,MapCannotGoodEnough,MapMist

import random

class UIMap(Canvas):
    def __init__(self, name, screen, priority):
        self.mapSize = None
        self.mapTileSiz = None
        self.Camera = None

        self.mapTile = None

        self.CoillidorObject = set()

        self.EventTilePos = {
            "startPoint":Vector2.Zero()
        }
        self.EventMapPos = {

        }

        super().__init__(name, screen, priority)
    def init(self):
        pass
    def addChild(self, object):
        if isinstance(object,MapObject):
            if isinstance(object,MapColliderableObject):
                self.CoillidorObject.add(object.name)
            return super().addChild(object)
        return False
    def delChild(self, name):
        if name in self.CoillidorObject:
            self.CoillidorObject.discard(name)
        return super().delChild(name)
    def draw(self):
        if self.active:
            for child in self.children:
                child.draw(self.Camera())
            return True
        return False
    def moveCamera(self,vec):
        if isinstance(vec,Vector2):
            self.Camera += vec
    def genMapTile(self):
        pass
    def genEvent(self):
        pass
    def addMapTile(self,dit):
        self.genMapTile()
        vst = Vector2(-(self.mapTileSiz.x//2)*(self.mapSize.x//2),-self.mapTileSiz.y*(self.mapSize.y//2))
        for x in range(self.mapSize.x):
            for y in range(self.mapSize.y):
                dv = Vector2((self.mapTileSiz.x//2)*x,self.mapTileSiz.y*y)+Vector2(0,(0 if x%2==0 else self.mapTileSiz.y//2))
                if Vector2(x,y) in self.EventTilePos.keys() and self.EventTilePos[Vector2(x,y)] == "startPoint":
                    self.moveCamera(vst+dv)
                if Vector2(x,y) in self.EventTilePos.keys():
                    self.EventMapPos[self.EventTilePos[Vector2(x,y)]] = vst+dv
                if self.mapTile[x][y] in dit.keys():
                    #print(vst+dv)
                    #print(dit[self.mapTile[x][y]])
                    self.addChild(MapTile("tile_"+str(x)+"_"+str(y),self.screen,vst+dv,random.sample(dit[self.mapTile[x][y]],1)[0],self.mapTileSiz()))
        self.genEvent()


class ChronoArkMap(UIMap):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.mapSize = Vector2(60,30)
        self.mapTileSiz = Vector2(208,108)
        self.Camera = Vector2.Zero()

        self.addChild(UIMapChar("Lucy",self.screen,0,Vector2.Zero()))
        self.findChild("Lucy").setScale(Vector2(0.5,0.5))
    def genMapTile(self):
        p1 = Vector2(10,random.randint(10,20))
        p2 = Vector2(30,random.randint(10,20))
        p3 = Vector2(50,random.randint(10,20))
        self.EventTilePos[p1()] = "startPoint"
        self.EventTilePos[p2()] = "cannotgoodenough"
        self.EventTilePos[p3()] = "mist"
        self.mapTile = [["Background" for i in range(self.mapSize.y)] for j in range(self.mapSize.x)]
        for p in [p1,p2,p3]:
            for dx in range(-4,4+1):
                d = 4 - abs(dx)
                for dy in range(-d,d+1):
                    _dp = p+Vector2(dx,dy)
                    self.mapTile[_dp.x][_dp.y] = "Road"
        r1 = random.sample([i for i in range(p1.x+1+3,p2.x-3)],abs(p2.y-p1.y))
        r2 = random.sample([i for i in range(p2.x+1+3,p3.x-3)],abs(p3.y-p2.y))
        #print(r1)
        #print(r2)
        _cy = p1.y
        for x in range(self.mapSize.x):
            if p1.x < x and x < p2.x:
                if x in r1:
                    _cy += 1 if p2.y > p1.y else -1
                self.mapTile[x][_cy] = self.mapTile[x][_cy+1]  = self.mapTile[x][_cy-1] = "Road"
            elif p2.x < x and x < p3.x:
                if x in r2:
                    _cy += 1 if p3.y > p2.y else -1
                self.mapTile[x][_cy] = self.mapTile[x][_cy+1]  = self.mapTile[x][_cy-1] = "Road"
        '''
        _p = 0
        for lis in self.mapTile:
            if _p%2 == 0:
                print("",end=" ")
            for i in lis:
                if i == "Background":
                    print("-",end=" ")
                else:
                    print("#",end=" ")
            _p += 1
            print(" ")
        '''
    def genEvent(self):
        self.addChild(MapCannotGoodEnough("cannotgoodenough",self.screen,5,self.EventMapPos["cannotgoodenough"]))
        self.findChild("cannotgoodenough").setScale(Vector2(0.75,0.75))
        self.addChild(MapMist("mist",self.screen,100,self.EventMapPos["mist"]))
        self.findChild("mist").setScale(Vector2(1.5,2.5))
    def moveCamera(self, vec):
        if isinstance(vec,Vector2):
            super().moveCamera(vec)
            self.findChild("Lucy").alterMapPos(vec(),self.Camera)
            _success = True
            for nam in self.CoillidorObject:
                if nam != "Lucy":
                    if self.findChild(nam).Collider(self.findChild("Lucy").genMapRect()):
                        _success = False
                        break
            if not _success:
                super().moveCamera(vec()*(-1))
                self.findChild("Lucy").alterMapPos(vec()*(-1),self.Camera)
            return self.Camera()
                