import pygame
import sys
from GameSettings import *
from Utility import Scene


class Menu(Scene):

    def __init__(self, window):
        pass

    def show(self, window):
        window.fill(BLACK)
        font = pygame.font.Font(FontSettings.FontPath, 36)

        self.title = pygame.image.load("./assets/Title.png")
        self.title = pygame.transform.scale(self.title, (600, 200))
        window.blit(
            self.title,
            (WindowSettings.width // 2 - 300, WindowSettings.height // 2 - 260),
        )

        self.StartButton = font.render("开始游戏", True, WHITE)
        self.SettingButton = font.render("设置", True, WHITE)
        self.HelpButton = font.render("帮助", True, WHITE)
        self.QuitButton = font.render("退出游戏", True, WHITE)

        StartRect = self.StartButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 - 40)
        )
        SettingRect = self.SettingButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 + 40)
        )
        HelpRect = self.HelpButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 + 120)
        )
        QuitRect = self.QuitButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 + 200)
        )

        window.blit(self.StartButton, StartRect)
        window.blit(self.SettingButton, SettingRect)
        window.blit(self.HelpButton, HelpRect)
        window.blit(self.QuitButton, QuitRect)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            return self.check_mouse_click(mouse_x, mouse_y)

    # 检查鼠标点击
    def check_mouse_click(self, x, y):
        StartRect = self.StartButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 - 40)
        )
        SettingRect = self.SettingButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 + 40)
        )
        HelpRect = self.HelpButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 + 120)
        )
        QuitRect = self.QuitButton.get_rect(
            center=(WindowSettings.width // 2, WindowSettings.height // 2 + 200)
        )

        if StartRect.collidepoint(x, y):
            return "EnterMap"
        elif SettingRect.collidepoint(x, y):
            return "EnterSetting"
        elif HelpRect.collidepoint(x, y):
            return "EnterHelp"
        elif QuitRect.collidepoint(x, y):
            print("See you next time!")
            pygame.quit()
            sys.exit()
