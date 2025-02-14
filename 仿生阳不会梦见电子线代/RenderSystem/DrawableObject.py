from .RectableObject import *
class Drawableobject(Rectableobject):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)

        self.sprite = None
        self.worldSprite = None
    def setRect(self):
        if self.sprite != None:
            self.rect = self.sprite.get_rect()
            self.rect.height *= self.worldScale().y
            self.rect.width *= self.worldScale().x
            self.rect.centerx = self.worldPosition().x
            self.rect.centery = self.worldPosition().y
            self.worldSprite = pygame.transform.scale(self.sprite,self.rect.size)
    def setSprite(self,sprite):
        if isinstance(sprite,pygame.surface.Surface):
            self.sprite = sprite
            self.setRect()
    def draw(self):
        if super().draw():
            #if self.worldSprite == None:
            #    print(self.name)
            if isinstance(self.worldSprite,pygame.surface.Surface) and isinstance(self.rect, pygame.rect.Rect):
                self.screen.blit(self.worldSprite,self.rect)
                return True
        return False       