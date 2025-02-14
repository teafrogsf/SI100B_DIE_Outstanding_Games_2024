import pygame
from .Text import Text

class RotationText(Text):
    def __init__(self, name, screen, priority):
        self.rotation = 0
        super().__init__(name, screen, priority)
    def init(self):
        pass
    def setRotation(self,rotation):
        if self.rotation != rotation:
            self.rotation = rotation
    def setText(self, txt, choice):
        super().setText(txt, choice)
        if isinstance(txt,str):
            self.setSprite(pygame.transform.rotate(self.sprite,self.rotation))