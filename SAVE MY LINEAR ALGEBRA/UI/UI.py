import pygame
from Statics import *
from TmpTools.tools import *

class StaticState(pygame.sprite.Sprite):
    def __init__(self, importImage, x, y, MULTI, ALPHA):
        super().__init__()
        self.image = importImage
        self.image.set_alpha(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * MULTI), int(self.rect.height * MULTI)))
    def update(self):
        pass

class coin(StaticState):
    def __init__(self):
        super().__init__(
            pygame.image.load(ImportedImages.UI.coin),
            UISettings.coin.x,
            UISettings.coin.y,
            UISettings.coin.MULTI,
            UISettings.coin.ALPHA)
        self.coin_num = 0
    def update(self, screen):
        fonts = pygame.font.Font('Src/fonts/IsaacGame.ttf', 48) #"Src/fonts/prices.psd"
        coin_text = fonts.render(f"{self.coin_num}", True, (225, 225, 225))
        screen.blit(coin_text, (UISettings.coin.x + 45, UISettings.coin.y + 10))


class attack(StaticState):
    def __init__(self):
        super().__init__(
            pygame.image.load(ImportedImages.UI.attack),
            UISettings.attack.x,
            UISettings.attack.y,
            UISettings.attack.MULTI,
            UISettings.attack.ALPHA)
        self.attack_num = 1
        self.shoot_mode = 0
    def update(self, screen):
        fonts = pygame.font.Font('Src/fonts/IsaacGame.ttf', 48) #"Src/fonts/prices.psd"
        attack_text = fonts.render(f"{self.attack_num}", True, (225, 225, 225))
        screen.blit(attack_text, (UISettings.attack.x + 55, UISettings.attack.y + 10))

class Bomb(StaticState):
    def __init__(self):
        Image = get_images(pygame.image.load(ImportedImages.UI.Bomb), 0,0,26,25, (0, 0, 0), 3.0)
        super().__init__(
            Image,
            UISettings.bomb.x,
            UISettings.bomb.y,
            UISettings.bomb.MULTI,
            UISettings.bomb.ALPHA)
        self.bomb_num = 3
    def update(self, screen):
        fonts = pygame.font.Font('Src/fonts/IsaacGame.ttf', 48) #"Src/fonts/prices.psd"
        bomb_text = fonts.render(f"{self.bomb_num}", True, (225, 225, 225))
        screen.blit(bomb_text, (UISettings.bomb.x + 70, UISettings.bomb.y + 15))

class Room_hint(StaticState):
    def __init__(self, bossroom_location, current_location):
        super().__init__(
            pygame.image.load(ImportedImages.UI.attack),
            UISettings.room_hint.x,
            UISettings.room_hint.y,
            UISettings.room_hint.MULTI,
            UISettings.room_hint.ALPHA)
        self.bossroom_num = bossroom_location
        self.current_room = current_location

    def update(self, screen):
        fonts = pygame.font.Font('Src/fonts/IsaacGame.ttf', 48)
        hint_text = fonts.render(f"Boss Room: {self.bossroom_num}", True, (225, 225, 225))
        screen.blit(hint_text, (UISettings.room_hint.x + 10, UISettings.room_hint.y + 10))
        current_room_text = fonts.render(f"Current Room: {self.current_room}", True, (225, 225, 225))
        screen.blit(current_room_text, (UISettings.room_hint.x + 10, UISettings.room_hint.y + 60))