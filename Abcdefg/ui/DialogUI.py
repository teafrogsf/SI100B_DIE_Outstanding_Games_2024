import pygame

import I18n
import Config
from Dialog import Dialog
from render import Renderer
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton


class DialogUI(UI):

    def __init__(self, npc, dialogs: Dialog, choose):
        super().__init__()
        # 初始化对话UI，设置NPC、对话内容和选择函数
        self.npc = npc
        self.dialogs = dialogs
        self.choose = choose
        # 获取NPC当前的对话内容
        self.npc_text = I18n.text(self.dialogs.current['npc']).get()
        self.lines = []
        self.achieved_length = 0
        # 获取玩家可选择的选项
        self.options = self.dialogs.current['player']
        self.typing_index = 1  # 打字动画的索引
        # 启动定时器，每5帧触发一次打字动画
        Config.CLOCKS.append((5, self.typer_animate))

    # 关闭对话UI时，移除定时器
    def on_close(self):
        Config.CLOCKS.remove((5, self.typer_animate))
        super().on_close()

    # 打字动画效果，每次增加一个字符
    def typer_animate(self):
        self.typing_index = min(len(self.npc_text) + 1, self.typing_index + 1)
        # 如果打字动画结束，更新按钮选项
        if self.typing_index == len(self.npc_text):
            self.update_buttons(self.options)

    # 更新按钮选项
    def update_buttons(self, options):
        height = len(options) * 50
        for i, option in enumerate(options):
            # 为每个选项创建一个按钮
            self.add_button(ClassicButton(
                I18n.text(option['str']),
                (Config.SCREEN_WIDTH // 2 - 250, Config.SCREEN_HEIGHT // 2 + 115 - height // 2 + i * 50),
                (500, 45), on_click=lambda index=i: self.next_dialog(index), border_radius=1))

    # 处理玩家选择的选项
    def next_dialog(self, choice: int):
        nxt = self.dialogs.next(choice)  # 获取下一个对话
        if isinstance(nxt, str):  # 如果下一个是字符串，表示跳转到另一个对话
            s = self.choose(nxt) or '!#'  # 调用选择函数获取新的对话
            if s[0] == '!':  # 如果是以!开头，关闭对话UI
                if Config.CLIENT.current_ui == self:
                    Config.CLIENT.close_ui()
                return
            else:
                # 如果是有效的对话键，更新当前对话
                nxt = self.dialogs.current = self.dialogs.dialogs[s]
        # 获取下一个对话的玩家选项
        self.options = nxt['player']
        self.lines.clear()  # 清除对话文本
        self.buttons.clear()  # 清除旧的按钮
        self.npc_text = I18n.text(self.dialogs.current['npc']).get()  # 更新NPC文本
        self.typing_index = 1  # 重置打字动画的索引
        self.achieved_length = 0  # 重置已经打印的文本长度

    # 渲染UI
    def render(self, screen: pygame.Surface):
        # 绘制一个半透明的黑色遮罩层
        dark_overlay = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT - 140), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, 200), (0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT - 140))
        screen.blit(dark_overlay, (0, 70))

        # 渲染所有按钮
        for button in self.buttons:
            button.render(screen)

        # 渲染NPC的对话文本，限制为当前的打字索引
        if Config.FONT.size(self.npc_text[self.achieved_length:self.typing_index])[0] > 350:
            self.lines.append(self.npc_text[self.achieved_length:self.typing_index])
            self.achieved_length = self.typing_index
        for i, line in enumerate(self.lines):
            txt_surface = Config.FONT.render(line, True, (255, 255, 255))
            screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                      Config.SCREEN_HEIGHT // 2 - 75 - (len(self.lines) - i * 2) * 12.5))
        txt_surface = Config.FONT.render(self.npc_text[self.achieved_length:self.typing_index], True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                  Config.SCREEN_HEIGHT // 2 - 75 + len(self.lines) * 12.5))

        # 渲染玩家和NPC的形象
        Config.CLIENT.player.render_at_absolute_pos(screen, (20, Config.SCREEN_HEIGHT - 140), False, False)
        self.npc.render_at_absolute_pos(screen, (Config.SCREEN_WIDTH - 70, 90), True, False)

        # 如果当前对话有图片，加载并显示图片
        if 'image' in self.dialogs.current:
            img = pygame.image.load(self.dialogs.current['image'])
            img = pygame.transform.scale(img, (Config.SCREEN_WIDTH // 4, Config.SCREEN_HEIGHT // 2))
            screen.blit(img, (10, 150))

    # 处理每一帧的事件
    def tick(self, keys, events):
        super().tick(keys, events)
        Renderer.PLAYER.tick()
        return True
