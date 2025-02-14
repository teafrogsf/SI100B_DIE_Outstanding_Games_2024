from .RectableObject import *
from .Sprite import *

class Canvas(Rectableobject):
    def __init__(self,name,screen,priority):
        super().__init__(name,screen,priority)
        
        self.children = []
        self.preventRay(False)

        self.init()
    def init(self):
        pass
    def Clean(self):
        if not super().Clean():
            return False
        for child in self.children:
            child.markDirty()
        return True
    def DeepClean(self):
        self.Clean()
        for child in self.children:
            child.DeepClean()
    def sortChildren(self):
        #developed by NH37
        self.children.sort(key=lambda x:x.priority)
    def posSetChildren(self):
        self.Clean()
        for child in self.children:
            if isinstance(child,Canvas):
                child.markDirty()
                child.posSetChildren()
    def setPos(self,vec):
        if super().setPos(vec):
            for child in self.children:
                child.markDirty()
            return True
        return False
    def setScale(self,scale):
        if super().setScale(scale):
            for child in self.children:
                child.markDirty()
            self.posSetChildren()
            return True
        return False
    def move(self,vec):
        if super().move(vec):
            for child in self.children:
                child.markDirty()
            return True
        return False
    def draw(self):
        if super().draw():
            for child in self.children:
                child.draw()
            return True
        return False
    def update(self):
        super().update()
        for child in self.children:
            child.update()
    
    def rayCast(self, event):
        super().rayCast(event)
        if (not self.prevent) and self.active:
            for child in self.children:
                child.rayCast(event)
    def addChild(self, object):  
        if isinstance(object,Rectableobject):
            self.Clean()
            object.setParent(self)
            self.children.append(object)
            self.sortChildren()
            return True
        return False
    def delChild(self, name):
        for child in self.children:
            if child.name == name:
                del self.children[self.children.index(child)]
                return True
        return False
    def findChild(self,name):
        for child in self.children:
            if child.name == name:
                return child