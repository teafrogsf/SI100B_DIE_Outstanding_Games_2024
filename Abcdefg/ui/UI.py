import pygame


class UI:

    def __init__(self):
        self.buttons = []  # 存储UI中的按钮
        self.blurred_surface = None  # 存储模糊背景的表面

    def add_button(self, button):
        # 向UI中添加按钮
        self.buttons.append(button)

    def tick(self, keys, events):
        # 处理UI中的每个按钮的事件
        for button in self.buttons:
            button.tick(events)
        return False  # 返回False表示UI保持打开

    def blur_background(self, screen: pygame.Surface):
        # 对背景进行模糊处理
        if self.blurred_surface is None:
            # 创建一个与屏幕大小相同的Surface
            surface = pygame.Surface(screen.get_size())
            surface.blit(screen, (0, 0))  # 将屏幕内容复制到Surface
            for _ in range(5):  # 进行5次模糊处理
                # 缩小并平滑拉伸Surface
                surface = pygame.transform.smoothscale(surface, (surface.get_width() // 2, surface.get_height() // 2))
                surface = pygame.transform.smoothscale(surface, screen.get_size())  # 恢复到原来的大小
            # 创建一个半透明的黑色遮罩层，增加背景暗度
            dark_overlay = pygame.Surface(screen.get_size())
            dark_overlay.fill((0, 0, 0))
            dark_overlay.set_alpha(150)  # 设置透明度
            surface.blit(dark_overlay, (0, 0))  # 将遮罩层叠加到模糊的背景上
            self.blurred_surface = surface  # 保存模糊后的背景
        # 将模糊背景绘制到屏幕上
        screen.blit(self.blurred_surface, (0, 0))

    def render(self, screen: pygame.Surface):
        # 渲染UI界面
        self.blur_background(screen)  # 渲染模糊背景
        # 渲染UI中的所有按钮
        for button in self.buttons:
            button.render(screen)

    def on_close(self):
        pass
