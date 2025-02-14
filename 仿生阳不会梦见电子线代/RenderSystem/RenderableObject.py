import pygame,os
from Data.types import *
from EventSystem.InteractableInterface import *
from AnimeSystem.IAnime import *

class RenderableObject(InteractableInterface,IAnime):
    def __init__(self,name,screen,priority):
        InteractableInterface.__init__(self)
        IAnime.__init__(self)

        self.name = name

        self.screen = screen

        self.active = True
        
        self.priority = priority
        self.parent = None

        self.localPosition = Vector2.Zero
        self.worldPosition = Vector2.Zero

        self.localScale = Vector2.One
        self.worldScale = Vector2.One
        
        self.dirty = False

        self.preventRay(True)
    def init(self):
        pass
    def markDirty(self):
        self.dirty = True
    def Clean(self):
        if not self.dirty:
            return False
        if self.parent != None:
            self.worldScale = self.localScale() * self.parent.worldScale()
            self.worldPosition = self.localPosition() + self.parent.worldPosition()
        else:
            self.worldScale = self.localScale()
            self.worldPosition = self.localPosition()
        self.dirty = False
        return True
    def DeepClean(self):
        self.Clean()
    def setActive(self,bl):
        self.active = bl
    def setPriority(self,pr):
        self.priority = pr
        if self.parent != None:
            self.parent.sortChildren()
    def setParent(self,parent):
        self.parent = parent
        self.markDirty()
    def setScale(self,scale):
        if Vector2.Is(scale):
            self.Clean()
            self.localScale = Vector2.Copy(scale)
            if self.parent != None:
                self.worldScale = self.localScale() * self.parent.worldScale()
            else:
                self.worldScale = self.localScale()
            return True
        return False
    def setPos(self,vec):
        if Vector2.Is(vec):
            self.Clean()
            self.localPosition = Vector2.Copy(vec)
            if self.parent != None:
                self.worldPosition = self.localPosition() + self.parent.worldPosition()
            else:
                self.worldPosition = self.localPosition()
            return True
        return False
    def move(self,vec):
        if Vector2.Is(vec):
            self.Clean()
            self.localPosition = self.localPosition() + vec()
            if self.parent != None:
                self.worldPosition = self.localPosition() + self.parent.worldPosition()
            else:
                self.worldPosition = self.localPosition()
            return True
        return False
    def draw(self):
        if not self.active:
            return False
        self.Clean()
        return True
    def update(self):
        self.Clean()
        self.EventUpdate()