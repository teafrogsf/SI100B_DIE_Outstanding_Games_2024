import pygame
from Statics import *

class bossheart:
    @staticmethod
    def update(surface, x, y, width, height, health, max_health):
        '''
        绘制血条函数
        :param surface: 绘制血条的表面（屏幕等）
        :param x: 血条左上角x坐标
        :param y: 血条左上角y坐标
        :param width: 血条总宽度
        :param height: 血条高度
        :param health: 当前血量
        :param max_health: 最大血量
        '''
        fill = (health / max_health) * width
        outline_rect = pygame.Rect(x, y, width, height)
        fill_rect = pygame.Rect(x, y, fill, height)
        background_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (0, 0, 0), background_rect)
        pygame.draw.rect(surface, (255, 0, 0), fill_rect)
        pygame.draw.rect(surface, (0, 0, 0), outline_rect, 2)

