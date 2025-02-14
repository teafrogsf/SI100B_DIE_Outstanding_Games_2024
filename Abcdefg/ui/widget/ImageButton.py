import pygame

from ui.widget.Button import Button


class ImageButton(Button):

    def __init__(self, image: pygame.Surface, pos, on_click=lambda: None):
        super().__init__(pos, image.get_size(), on_click)
        self.image = image

    def render(self, screen):
        if self.hovered or self.mouse_down:
            bg_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 100))
            screen.blit(bg_surface, self.pos)
        screen.blit(self.image, self.pos)

