import pygame

import Config
import I18n
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton


class SelectLanguageUI(UI):

    def __init__(self):
        super().__init__()
        self.add_button(ClassicButton(I18n.literal('简体中文'),
                                      (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 - 150),
                                      (200, 45), (0, 0, 0, 150), (255, 255, 255),
                                      lambda: self.set_language_and_close(0)))
        self.add_button(ClassicButton(I18n.literal('繁體中文'),
                                      (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 - 100),
                                      (200, 45), (0, 0, 0, 150), (255, 255, 255),
                                      lambda: self.set_language_and_close(1)))
        self.add_button(ClassicButton(I18n.literal('English'),
                                      (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 - 50),
                                      (200, 45), (0, 0, 0, 150), (255, 255, 255),
                                      lambda: self.set_language_and_close(2)))
        self.add_button(ClassicButton(I18n.literal('日本語'),
                                      (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2),
                                      (200, 45), (0, 0, 0, 150), (255, 255, 255),
                                      lambda: self.set_language_and_close(3)))

    @staticmethod
    def set_language_and_close(language):
        I18n.set_language(language)
        Config.CLIENT.close_ui()

    def tick(self, keys, events):
        super().tick(keys, events)
        return True

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.FONT.render('Translated by ChatGPT', True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                  Config.SCREEN_HEIGHT // 2 + 100))
