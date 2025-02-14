import pygame
from Statics import *

class lucky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [
            pygame.transform.scale(pygame.image.load(ImportedImages.shop.lucky_1), (48 * 2.0, 48 * 2.0)),
            pygame.transform.scale(pygame.image.load(ImportedImages.shop.lucky_2), (48 * 2.0, 48 * 2.0)),
            pygame.transform.scale(pygame.image.load(ImportedImages.shop.lucky_3), (48 * 2.0, 48 * 2.0)),
            pygame.transform.scale(pygame.image.load(ImportedImages.shop.lucky_4), (48 * 2.0, 48 * 2.0))]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = ShopSettings.lucky.x
        self.rect.y = ShopSettings.lucky.y
        self.state = 'normal'
        self.timer = 0
        self.countdown = 0

    def update(self):

        if self.state == 'open':
            current_time = pygame.time.get_ticks()
            if self.timer == 0:
                self.timer = current_time
            elif current_time - self.timer > 125:
                self.timer = current_time
                self.countdown += 1
                self.frame_index += 1
                self.frame_index %= 2
            if self.countdown >= 9:
                self.state = 'destroy'
                self.countdown = 0

        self.image = self.frames[self.frame_index]


class StaticState(pygame.sprite.Sprite):
    def __init__(self, importImage, x, y, MULTI, ALPHA):
        super().__init__()
        self.image = pygame.image.load(importImage)
        self.image.set_alpha(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(
            self.image, (int(self.rect.width * MULTI), int(self.rect.height * MULTI)))
    def update(self):
        pass

class price(StaticState):
    def __init__(self):
        super().__init__(
            ImportedImages.shop.price,
            ShopSettings.price.x,
            ShopSettings.price.y,
            ShopSettings.price.MULTI,
            ShopSettings.price.ALPHA,
        )
