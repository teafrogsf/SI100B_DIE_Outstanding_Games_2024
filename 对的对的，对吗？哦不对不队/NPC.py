import pygame
from Settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale( pygame.image.load(r".\assets_library\characters\NPC商人.png") , (NPCSettings.width, NPCSettings.height) )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def Awake(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP))