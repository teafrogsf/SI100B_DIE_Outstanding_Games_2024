import pygame

import I18n
import Config
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton


class MessageBoxUI(UI):

    def __init__(self, message: I18n.Text, father_ui):
        super().__init__()
        self.message = message
        self.father_ui = father_ui
        self.add_button(ClassicButton(I18n.text('go_back'),
                                      (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 + 50),
                                      (200, 50), on_click=lambda: Config.CLIENT.close_ui()))

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.LARGE_FONT.render(self.message.get(), True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                  Config.SCREEN_HEIGHT // 2 - 75))

    def on_close(self):
        Config.CLIENT.open_ui(self.father_ui)

    def tick(self, keys, events):
        super().tick(keys, events)
        return True
