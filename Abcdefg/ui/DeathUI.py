import pygame

import AIHelper
import Config
import I18n
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton
from Config import SCREEN_WIDTH, SCREEN_HEIGHT


class DeathUI(UI):

    def __init__(self):
        super().__init__()
        # 添加复活按钮
        self.add_button(ClassicButton(I18n.text('respawn'), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50),
                                      (200, 50), on_click=lambda: Config.CLIENT.player_respawn()))
        # 记录玩家死亡并复活的事件
        AIHelper.add_event('player has died and respawned')
        # 玩家死亡后，AI系统会给出一些简短的建议
        AIHelper.add_response(f'player died, lost half of coins and all energy, please give some brief advices', (255, 0, 0))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True  # 确保UI继续保持打开

    def render(self, screen: pygame.Surface):
        super().render(screen)
        # 渲染死亡提示文本
        txt_surface = Config.LARGE_FONT.render(I18n.text('you_died').get(), True, (255, 255, 255))
        # 将白色的死亡提示文本绘制到屏幕
        screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2 + 1, SCREEN_HEIGHT // 2 - 74))
        # 渲染红色的死亡提示文本
        txt_surface = Config.LARGE_FONT.render(I18n.text('you_died').get(), True, (255, 0, 0))
        # 将红色的死亡提示文本绘制到屏幕
        screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 75))
