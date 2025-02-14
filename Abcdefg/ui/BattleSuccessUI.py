import pygame

import AIHelper
import Config
import I18n
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton


class BattleSuccessUI(UI):

    def __init__(self, name: I18n.Text, coins=0):
        super().__init__()
        self.name = name
        self.coins = coins
        self.add_button(ClassicButton(I18n.text('continue'),
                                      (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 + 50),
                                      (200, 50), on_click=lambda: Config.CLIENT.close_ui()))
        AIHelper.add_event('player has beaten ' + name.get())

    def tick(self, keys, events):
        super().tick(keys, events)
        return True

    def render(self, screen: pygame.Surface):
        super().render(screen)
        # 绘制击败敌人的提示文本
        txt_surface = Config.LARGE_FONT.render(I18n.text('beat_entity').format(self.name), True, (0, 255, 0))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                  Config.SCREEN_HEIGHT // 2 - 75))  # 将文本居中绘制在屏幕上

        # 绘制获得金币的提示文本
        txt_surface = Config.FONT.render(I18n.text('obtained_coins').format(self.coins), True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                  Config.SCREEN_HEIGHT // 2 - 35))  # 将金币文本居中绘制在屏幕上

        # 绘制金币图标
        screen.blit(Config.COIN_IMAGE, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2 - 22,
                                        Config.SCREEN_HEIGHT // 2 - 37))  # 将金币图标绘制在文本旁边
