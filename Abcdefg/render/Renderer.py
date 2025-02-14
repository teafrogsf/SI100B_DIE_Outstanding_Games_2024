import random
from typing import Tuple

import pygame

ANIMATIONS = []


class Renderer:
    # 更新渲染器状态
    def tick(self):
        pass

    # 渲染到屏幕
    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        pass

    # 获取渲染器的大小
    def get_size(self):
        pass

    # 获取渲染器的矩形区域
    def get_rect(self):
        pass


# 图像渲染器类：渲染一个静态图像
class ImageRenderer(Renderer):

    def __init__(self, image: pygame.Surface):
        self.image = image  # 原始图像
        # 创建镜像图像（水平翻转）
        self.image_mirrored = pygame.transform.flip(self.image, True, False)

    def tick(self):
        pass

    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        # 根据是否需要镜像，选择渲染图像
        screen.blit(self.image_mirrored if mirror else self.image, pos)

    def get_size(self):
        return self.image.get_size()

    def get_rect(self):
        return self.image.get_rect()


# 动画渲染器类：渲染一组图像，构成动画
class AnimationRenderer(Renderer):

    def __init__(self, images: list[pygame.Surface], duration: int, is_random=False, repeat=True, register=True):
        # 注册动画
        if register:
            ANIMATIONS.append(self)
        self.images = images  # 动画的图像列表
        self.images_mirrored = [pygame.transform.flip(image, True, False) for image in images]  # 镜像图像列表
        self.duration = duration  # 每帧的持续时间（ticks）
        self.ticks = 0  # 当前的tick数
        self.index = 0  # 当前的图像索引
        self.is_random = is_random  # 是否随机播放动画
        self.repeat = repeat  # 是否重复播放动画

    def tick(self):
        # 每一帧更新一次
        self.ticks += 1
        if self.ticks >= self.duration:
            self.ticks = 0
            # 如果是随机播放，则随机选择一帧
            if self.is_random:
                self.index = random.randint(0, len(self.images) - 1)
            else:
                # 否则顺序播放动画
                self.index = min(self.index + 1, len(self.images))
                if self.repeat:
                    self.index %= len(self.images)

    def is_end(self):
        # 判断动画是否播放结束（是否到了最后一帧）
        return self.index == len(self.images) - 1

    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        # 渲染当前帧图像，根据是否镜像来决定使用正向图像或镜像图像
        index = 0 if use_default else self.index
        screen.blit(self.images_mirrored[index] if mirror else self.images[index], pos)

    def get_size(self):
        return self.images[0].get_size()

    def get_rect(self):
        return self.images[0].get_rect()


# 实体渲染器类：渲染具有两种状态（默认、移动）图像的实体
class EntityRenderer(Renderer):

    def __init__(self, images: list[pygame.Surface], images_moving: list[pygame.Surface],
                 duration: int, pos_delta=(0, 0), pos_delta_mirrored=(0, 0), register=True):
        if register:
            ANIMATIONS.append(self)
        self.images = images  # 默认状态的图像
        self.images_moving = images_moving  # 移动状态的图像
        self.images_mirrored = [pygame.transform.flip(image, True, False) for image in images]  # 默认状态镜像图像
        self.images_moving_mirrored = [pygame.transform.flip(image, True, False) for image in images_moving]  # 移动状态镜像图像
        self.duration = duration  # 每帧的持续时间（ticks）
        self.ticks = 0  # 当前的tick数
        self.index = 0  # 当前的图像索引
        self.pos_delta = pos_delta  # 默认状态下的位置偏移量
        self.pos_delta_mirrored = pos_delta_mirrored  # 镜像状态下的位置偏移量

    def tick(self):
        self.ticks += 1
        if self.ticks >= self.duration:
            self.ticks = 0
            self.index = (self.index + 1) % len(self.images)  # 顺序播放动画

    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        # 根据是否镜像选择渲染图像，并根据使用默认或移动状态选择渲染图像
        if mirror:
            delta = self.pos_delta_mirrored
            if use_default:
                img = self.images_mirrored
            else:
                img = self.images_moving_mirrored
        else:
            delta = self.pos_delta
            if use_default:
                img = self.images
            else:
                img = self.images_moving
        screen.blit(img[self.index], (pos[0] + delta[0], pos[1] + delta[1]))

    def get_size(self):
        return self.images[0].get_size()

    def get_rect(self):
        return self.images[0].get_rect()


# 辅助函数：生成一个图片渲染器
def image_renderer(file: str, size: Tuple[int, int]):
    return ImageRenderer(pygame.transform.scale(pygame.image.load("./assets/" + file), size))


def load_image(file: str, size: Tuple[int, int]):
    return pygame.transform.scale(pygame.image.load("./assets/" + file), size)


# 辅助函数：从精灵图加载并返回一系列图像
def load_images_from_sprite(file, image_size, resize):
    sprite = pygame.image.load(file)  # 加载精灵图
    sheet_width, sheet_height = sprite.get_size()  # 获取精灵图的宽高
    images = []

    # 按行切割精灵图
    for y in range(0, sheet_height, image_size[1]):
        image = sprite.subsurface((0, y, image_size[0], image_size[1]))  # 从精灵图中提取单个图像
        images.append(pygame.transform.scale(image, resize))  # 缩放并添加到图像列表
    return images


# 辅助函数：加载岩浆的图像并返回图像列表（包含镜像）
def load_lava_images():
    images = load_images_from_sprite("./assets/blocks/lava.png", (16, 16), (60, 60))
    return images + images[::-1]  # 加载镜像图像


# 辅助函数：加载水的图像并返回图像列表（包含镜像）
def load_water_images():
    images = load_images_from_sprite("./assets/blocks/water.png", (16, 16), (60, 60))
    return images + images[::-1]  # 加载镜像图像


FIRE = AnimationRenderer(load_images_from_sprite("./assets/entities/fire.png", (16, 16), (50, 50)), 5)
LAVA = AnimationRenderer(load_lava_images(), 10)
WATER = AnimationRenderer(load_water_images(), 10)
NETHER_PORTAL = AnimationRenderer(load_images_from_sprite("./assets/blocks/nether_portal.png", (16, 16), (60, 60)), 5)
END_PORTAL = AnimationRenderer(load_images_from_sprite("./assets/blocks/end_portal.png", (16, 16), (60, 60)), 5)
PLAYER = EntityRenderer(load_images_from_sprite("./assets/entities/player.png", (34, 26), (67, 50)),
                        load_images_from_sprite("./assets/entities/player_moving.png", (34, 26), (67, 50)),
                        5, pos_delta=(-16, 0), pos_delta_mirrored=(0, 0))
GHAST = EntityRenderer(load_images_from_sprite("./assets/entities/ghast.png", (329, 369), (50, 50)),
                       load_images_from_sprite("./assets/entities/ghast.png", (329, 369), (50, 50)),
                       20, pos_delta=(0, 0), pos_delta_mirrored=(0, 0))
