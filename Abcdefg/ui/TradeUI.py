import pygame

import Config
import I18n
from render import Renderer
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton
from ui.widget.TradeButton import TradeButton


class TradeUI(UI):

    def __init__(self, player, npc):
        super().__init__()
        self.player = player
        self.buttons = []
        self.npc = npc
        cnt = 0
        # 遍历NPC的交易列表，创建对应的按钮
        for option in npc.trade_list:
            # 创建每个交易选项的按钮，绑定交易选项
            button = TradeButton(option.name, (Config.SCREEN_WIDTH // 2 - 100, 50 + cnt * 70), (200, 50),
                                 option, on_click=lambda opt=option: self.handle_trade(opt))
            if player.coins < option.price:
                # 如果玩家的金币不足，则禁用按钮
                button.active = False
            self.add_button(button)  # 将按钮添加到界面
            cnt += 1
        # 添加返回按钮
        self.add_button(ClassicButton(I18n.text('go_back'),
                                      (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 + 10),
                                      (200, 50), on_click=Config.CLIENT.close_ui))

    def handle_trade(self, option):
        # 处理交易逻辑
        ret = option.on_trade(self.player, self.npc, option)  # 执行交易
        # 根据玩家金币数量，更新按钮的可用状态
        for button in self.buttons:
            if isinstance(button, TradeButton):
                button.active = self.player.coins >= button.trade_option.price
        return ret  # 返回交易结果

    def render(self, screen: pygame.Surface):
        # 渲染交易界面
        super().render(screen)  # 调用父类的 render 方法
        # 渲染玩家当前金币数量
        txt_surface = Config.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(Config.COIN_IMAGE, (10, 10))  # 绘制金币图标
        screen.blit(txt_surface, (35, 12))  # 绘制金币数量
        # 渲染玩家和NPC的角色图像
        Config.CLIENT.player.render_at_absolute_pos(screen, (20, Config.SCREEN_HEIGHT - 70), False, False)
        self.npc.render_at_absolute_pos(screen, (Config.SCREEN_WIDTH - 70, 20), True, False)

    def tick(self, keys, events):
        # 处理每一帧的键盘和鼠标事件
        super().tick(keys, events)  # 调用父类的 tick 方法
        Renderer.PLAYER.tick()  # 更新玩家的状态
        return True  # 返回True，表示UI仍然有效
