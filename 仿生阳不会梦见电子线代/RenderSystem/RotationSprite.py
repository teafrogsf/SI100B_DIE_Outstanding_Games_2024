import pygame
from .Sprite import *

class RotationSprite(Sprite):
    def __init__(self, name, screen, priority):
        self.rotation = 0
        self.oriSprite = None
        super().__init__(name, screen, priority)
    def setRotation(self,rotation):
        rotation *= -1
        if self.rotation != rotation:
            self.rotation = rotation
            self.setRect()
    def setImage(self, img):
        self.oriSprite = (super().setImage(img)).copy()
    def setRect(self):
        super().setRect()
        if self.sprite != None:
            self.worldSprite = pygame.transform.rotate(self.worldSprite,self.rotation)
            self.rect = self.worldSprite.get_rect()
            self.rect.centerx = self.worldPosition().x
            self.rect.centery = self.worldPosition().y
            

