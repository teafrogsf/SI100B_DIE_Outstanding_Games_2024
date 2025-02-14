import time

import pygame

import AIHelper
import Config
import I18n
from ui.TheEndUI import TheEndUI
from ui.UI import UI


class ChatUI(UI):

    def __init__(self):
        super().__init__()
        self.input_rect = pygame.Rect(10, Config.SCREEN_HEIGHT - 40, Config.SCREEN_WIDTH - 20, 30)
        self.text = ''
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.input_rect)

    def on_close(self):
        pygame.key.stop_text_input()
        super().on_close()

    @staticmethod
    def send_message(text):
        # 发送消息的静态方法
        if text.startswith('/'):
            args = text[1:].split(' ')
            if args[0] == 'tp' and len(args) == 3:
                Config.CLIENT.player.x = int(args[1])
                Config.CLIENT.player.y = int(args[2])
            elif args[0] == 'kill':
                Config.CLIENT.player.hp = 0
            elif args[0] == 'flag':
                Config.CLIENT.current_hud.messages.insert(0, (I18n.text('flag_leaked'), (255, 0, 0), time.time()))
                Config.NETHER_PORTAL_LOCK = False  # 解锁传送门
            elif args[0] == 'end':
                Config.CLIENT.open_ui(TheEndUI())
                return
            elif args[0] == 'undead':
                Config.CLIENT.player.hp = 114514
                Config.CLIENT.player.skill_unlocked = True
                Config.CLIENT.player.skill = 1
                Config.CLIENT.current_hud.messages.insert(0, (I18n.text('flag_leaked'), (255, 0, 0), time.time()))
                Config.NETHER_PORTAL_LOCK = False  # 解锁传送门
            elif args[0] == 'cheat':
                Config.CLIENT.player.atk = 1000
                Config.CLIENT.player.crt = 1000
                Config.CLIENT.player.hp = 114514
                Config.CLIENT.player.sp = 114514
                Config.CLIENT.player.coins = 114514
                Config.CLIENT.player.skill_unlocked = True
                Config.CLIENT.player.skill = 1
                Config.CLIENT.current_hud.messages.insert(0, (I18n.text('flag_leaked'), (255, 0, 0), time.time()))
                Config.NETHER_PORTAL_LOCK = False  # 解锁传送门
            Config.CLIENT.close_ui()  # 关闭聊天UI
            return

        # 普通消息发送
        s = I18n.text('player_name').get() + ': ' + text  # 将玩家名字和消息拼接
        while s:
            i = 0
            # 将消息按屏幕宽度分割，避免文字溢出
            for i in range(len(s)):
                if Config.FONT.size(s[:i + 1])[0] > Config.SCREEN_WIDTH // 2:
                    break
            Config.CLIENT.current_hud.add_message(I18n.text(s[:i + 1]), (255, 255, 255))  # 添加消息到HUD
            s = s[i + 1:]  # 处理剩余的消息

        AIHelper.add_response(text)  # 记录响应
        Config.CLIENT.close_ui()  # 关闭聊天UI

    def paste_text(self):
        # 从剪贴板粘贴文本
        if pygame.scrap.get(pygame.SCRAP_TEXT):
            try:
                self.text += pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8').replace('\0', '')  # 尝试使用UTF-8解码
            except UnicodeDecodeError:
                try:
                    self.text += pygame.scrap.get(pygame.SCRAP_TEXT).decode('gbk').replace('\0', '')  # 如果解码失败，尝试GBK
                except UnicodeDecodeError:
                    pass  # 如果仍然无法解码，则不做处理

    def tick(self, keys, events):
        # 处理每一帧的键盘和鼠标事件
        super().tick(keys, events)  # 调用父类的 tick 方法
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (not Config.AI_INPUT_LOCK) and event.key == pygame.K_RETURN:
                    # 如果没有锁定AI输入且按下回车键，发送消息
                    self.send_message(self.text)
                    self.text = ''  # 清空输入框
                elif event.key == pygame.K_BACKSPACE:
                    # 如果按下退格键，删除最后一个字符
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    # 如果按下Esc键，关闭聊天窗口
                    return False
                elif event.key == pygame.K_v and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    # 如果按下Ctrl+V，粘贴剪贴板内容
                    self.paste_text()
            if event.type == pygame.TEXTINPUT:
                # 处理文本输入事件
                self.text += event.text  # 将输入的字符添加到文本中
        return True  # 返回True，表示UI仍然有效

    def render(self, screen: pygame.Surface):
        # 渲染聊天UI界面
        super().render(screen)  # 调用父类的 render 方法
        pygame.draw.rect(screen, self.bg_color, self.input_rect)  # 绘制输入框的背景
        txt_surface = Config.FONT.render(self.text, True, self.text_color)  # 渲染输入框中的文本
        screen.blit(txt_surface, (self.input_rect.x + 5, self.input_rect.y + 5))  # 将文本绘制到输入框内

        # 渲染聊天消息
        y_offset = Config.SCREEN_HEIGHT - 60  # 初始位置从屏幕底部向上
        lines_cnt = 0  # 计数器，限制最多显示25行消息
        for message, color, timestamp in Config.CLIENT.current_hud.messages:
            if len(message.get().strip()) > 0:  # 如果消息不为空
                txt_surface = Config.FONT.render(message.get().strip(), True, color)  # 渲染消息文本
                screen.blit(txt_surface, (10, y_offset))  # 将消息绘制到屏幕上
                y_offset -= 20  # 每条消息之间的间隔
                lines_cnt += 1
            if lines_cnt > 25:  # 限制最多显示25条消息
                break

