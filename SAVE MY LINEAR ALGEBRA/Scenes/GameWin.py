import pygame
import pygame.event
from Statics import *


class GameWin(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.add(ReplayButton(), deathPortraits())


class deathPortraits(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ImportedImages.deathPortraits)

        self.rect = self.image.get_rect()
        self.rect.x = GameWinSettings.death.x
        self.rect.y = GameWinSettings.death.y
        m = GameWinSettings.death.MULTI
        self.image = pygame.transform.scale(
            self.image, (int(self.rect.width * m), int(self.rect.height * m))
        )

    def update(self):
        pass


class ReplayButton(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(ImportedImages.ReplayButton)
        self.rect = self.image.get_rect()

        self.rect.centerx = GameWinSettings.ReplayButton.x
        self.rect.centery = GameWinSettings.ReplayButton.y

        self.scaled_images = {
            1: pygame.transform.smoothscale(
                self.image, (self.rect.width * 2, self.rect.height * 2)
            ),
            1.2: pygame.transform.smoothscale(
                self.image, (self.rect.width * 2.4, self.rect.height * 2.4)
            ),
        }

    def update(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
            self.rect.left <= mouse_x <= self.rect.right
            and self.rect.top <= mouse_y <= self.rect.bottom
        ):
            self.image = self.scaled_images[1.2]
            self.rect = self.image.get_rect()
            self.rect.centerx = GameWinSettings.ReplayButton.x
            self.rect.centery = GameWinSettings.ReplayButton.y

            if pygame.mouse.get_pressed()[0]:
                pygame.event.post(pygame.event.Event(Events.RESTART))
        else:
            self.image = self.scaled_images[1]
            self.rect = self.image.get_rect()
            self.rect.centerx = GameWinSettings.ReplayButton.x
            self.rect.centery = GameWinSettings.ReplayButton.y
