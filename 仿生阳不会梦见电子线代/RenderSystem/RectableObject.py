from .RenderableObject import *
class Rectableobject(RenderableObject):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)

        self.baseRect = None
        self.rect = None
    def Clean(self):
        if not super().Clean():
            return False
        self.setRect()
        return True
    def DeepClean(self):
        self.Clean()
    def setBaseRect(self,rect):
        if isinstance(rect,pygame.rect.Rect):
            self.baseRect = rect.copy()
            self.setRect()
    def setRect(self):
        if self.baseRect != None:
            self.rect = self.baseRect.copy()
            self.rect.height *= self.worldScale().y
            self.rect.width *= self.worldScale().x
            self.rect.centerx = self.worldPosition().x
            self.rect.centery = self.worldPosition().y
    def setPos(self,vec):
        if super().setPos(vec):
            self.setRect()
            return True
        return False
    def setScale(self,scale):
        if super().setScale(scale):
            self.setRect()
            return True
        return False
    def move(self,vec):
        if super().move(vec):
            self.setRect()
            return True
        return False
    def draw(self):
        return super().draw()