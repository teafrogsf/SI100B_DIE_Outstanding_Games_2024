import pygame
from GameSettings import *
from Utility import Scene


class HelpPage(Scene):
    def __init__(self):
        pass

    def show(self, window):
        font = pygame.font.Font(FontSettings.FontPath, 36)
        window.fill(BLACK)
        self.text = font.render("请阅读 README.md", True, WHITE)
        self.QuitButton = font.render("返回", True, WHITE)
        self.textRect = self.text.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2)
        )
        self.QuitRect = self.QuitButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 + 100)
        )
        window.blit(self.text, self.textRect)
        window.blit(self.QuitButton, self.QuitRect)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.QuitRect.collidepoint(mouse_x, mouse_y):
                return "EnterMenufromHelp"
