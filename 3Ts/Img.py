import pygame as pg


class Img:
    def __init__(
        self,
        img: pg.Surface,
        size: tuple = (-1, -1),
        pos: tuple = (0, 0),
        alpha: int = 255,
    ):
        self.img = img
        if size != (-1, -1):
            self.img = pg.transform.scale(self.img, size)
        self.img.set_alpha(alpha)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.size = (self.width, self.height)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.alpha = alpha

    def setPos(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos

    def setAlpha(self, alpha: int):
        self.img.set_alpha(alpha)
        self.alpha = alpha
