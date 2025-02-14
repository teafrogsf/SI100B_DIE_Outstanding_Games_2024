from typing import Tuple

import pygame

import Block
import random

import Config
from Config import BLOCK_SIZE, MAP_WIDTH, MAP_HEIGHT
from render import Particle


class Dimension:

    def __init__(self, name: str, width: int, height: int, blocks: list[list[Block.Block]], music: str = None):
        self.name = name
        self.width = width
        self.height = height
        self.blocks = blocks
        self.entities = []
        self.music = music

    def set_block(self, pos: Tuple[int, int], replace_block: Block.Block):
        self.blocks[pos[0]][pos[1]] = replace_block

    def spawn_entity(self, entity):
        self.entities.append(entity)

    def get_render_size(self):
        return self.width * BLOCK_SIZE, self.height * BLOCK_SIZE

    @staticmethod
    def generate_map(width: int, height: int, blocks: list[Block.Block], weights: list[int]):
        return [random.choices(blocks, weights, k=height) for _ in range(width)]
        # 最简单的地图生成器，可自定义权重

    def foreach_block_in_camera(self, camera: Tuple[int, int], func):
        st_x = max(0, camera[0] // BLOCK_SIZE - 1)
        st_y = max(0, camera[1] // BLOCK_SIZE - 1)
        ed_x = min(st_x + Config.SCREEN_WIDTH // BLOCK_SIZE + 3, MAP_WIDTH)
        ed_y = min(st_y + Config.SCREEN_HEIGHT // BLOCK_SIZE + 3, MAP_HEIGHT)
        for x in range(st_x, ed_x):
            for y in range(st_y, ed_y):
                func(self.blocks[x][y], (x, y))

    def tick(self, camera: Tuple[int, int]):
        self.foreach_block_in_camera(camera, lambda block, pos: block.tick(pos))

    def render(self, screen: pygame.Surface, camera: Tuple[int, int]):
        self.foreach_block_in_camera(camera, lambda block, pos: block.render(screen, (pos[0] * BLOCK_SIZE - camera[0],
                                                                                      pos[1] * BLOCK_SIZE - camera[1])))

    @staticmethod
    def get_block_index(pos: Tuple[int, int]):
        return pos[0] // BLOCK_SIZE, pos[1] // BLOCK_SIZE
        # 取整，根据实际位置获得方块坐标

    @staticmethod
    def get_pos_from_index(i: Tuple[int, int]):
        return i[0] * BLOCK_SIZE, i[1] * BLOCK_SIZE

    def get_block_from_pos(self, pos: Tuple[int, int]):
        x, y = self.get_block_index(pos)
        return self.blocks[x][y]
        # 根据实际位置获得方块

    def get_block_from_index(self, xy: Tuple[int, int]):
        if 0 <= xy[0] < self.width and 0 <= xy[1] < self.height:
            return self.blocks[xy[0]][xy[1]]
        else:
            return None
        # 根据方块坐标获得方块

    def nearest_entity(self, pos: Tuple[int, int]):
        if len(self.entities) == 0:
            return None
        return min(self.entities, key=lambda e: abs(e.x - pos[0]) + abs(e.y - pos[1]))


class TheWorldDimension(Dimension):

    def __init__(self, name: str, width: int, height: int, blocks: list[list[Block.Block]], music: str = None):
        super().__init__(name, width, height, blocks, music)
        rain_image = pygame.image.load("./assets/maps/rain.png").convert_alpha()
        self.rain_surface = pygame.Surface((1600, 1200), pygame.SRCALPHA)
        for i in range(0, self.rain_surface.get_height(), rain_image.get_height()):
            for j in range(0, self.rain_surface.get_width(), rain_image.get_width()):
                self.rain_surface.blit(rain_image, (j, i))
        self.rain_scroll_y = 0

    def render(self, screen: pygame.Surface, camera: Tuple[int, int]):
        super().render(screen, camera)
        if Config.CLIENT.current_ui is None:
            self.rain_scroll_y += 6
            if self.rain_scroll_y >= 600:  # 当滚动到屏幕底部时，重置
                self.rain_scroll_y = 0
            screen.blit(self.rain_surface, (-(camera[0] % 800), -600 + self.rain_scroll_y))
            x, y = (camera[0] + random.randint(0, Config.SCREEN_WIDTH),
                    camera[1] + random.randint(0, Config.SCREEN_HEIGHT))
            if random.randint(0, 9) == 0:
                Particle.ENV_PARTICLES.add(Particle.SplashParticle((x, y), 30))
