import pygame
from GameSettings import *


class Npc:
    def __init__(self, name, imgpath, width, height, posX, posY):

        self.image = pygame.image.load(imgpath)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.imageRect = pygame.Rect(posX, posY, width, height)
        self.name = name
