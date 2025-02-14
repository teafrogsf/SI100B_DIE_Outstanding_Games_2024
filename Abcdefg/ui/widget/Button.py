import pygame

import Config


class Button:

    def __init__(self, pos, size, on_click=lambda: None):
        self.on_click = on_click
        self.active = True
        self.hovered = False
        self.mouse_down = False
        self.mouse_timer = 15
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)

    def tick(self, events):
        if not self.active:
            return
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.mouse_down:
            self.mouse_timer = max(0, self.mouse_timer - 1)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    Config.SOUNDS['button1'].play()
                    self.mouse_down = True
            elif self.mouse_down and event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_timer == 0:
                    Config.SOUNDS['button2'].play()
                self.on_toggle_click()
                self.mouse_down = False
                self.mouse_timer = 15

    def on_toggle_click(self):
        self.on_click()

    def set_active(self, active):
        self.active = active
