import pygame


class Hud:

    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def tick(self, keys, events):
        for button in self.buttons:
            button.tick(events)

    def render(self, screen: pygame.Surface):
        for button in self.buttons:
            button.render(screen)
