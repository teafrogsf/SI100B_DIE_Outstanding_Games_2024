import pygame
import sys
from GameSettings import *

class Listener:
    def __init__(self):
        pass

    def handle(self, event):
        pass

    def post(self):
        pass

class Entity(Listener):
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

    def handle(self, event):
        pass

    def render(self):
        pygame.windows.blit(self.image, self.rect)

class Scene(Listener):
    def __init__(self):
        pass

    def handle(self, event):
        pass

    def render(self):
        pass

class BgmPlayer():
    def __init__(self):
        pygame.mixer.init()
        bgm = pygame.mixer.music.load('./assets/bgm/Menu - Hollow Knight.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(BgmSettings.defaultvolume)
    
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def switch(self, scene):
        if (scene == 'Menu'):
            bgm = pygame.mixer.music.load('./assets/bgm/Menu - Hollow Knight.mp3')
        elif (scene == 'Map0'):
            bgm = pygame.mixer.music.load('./assets/bgm/Map - Greenpath.mp3')
        elif (scene == 'Map1'):
            bgm = pygame.mixer.music.load('./assets/bgm/Map - City of Tears.mp3')
        elif (scene == 'Map2'):
            bgm = pygame.mixer.music.load('./assets/bgm/Map - Crossroads.mp3')
        elif (scene == 'Map3'):
            bgm = pygame.mixer.music.load('./assets/bgm/Map - Final.mp3')
        elif (scene == 'Fight'):
            bgm = pygame.mixer.music.load('./assets/bgm/Battle - enemies.mp3')
        elif (scene == 'BossFight'):
            bgm = pygame.mixer.music.load('./assets/bgm/Battle - Radiance.mp3')
        pygame.mixer.music.play(-1)

    def post(self):
        pass