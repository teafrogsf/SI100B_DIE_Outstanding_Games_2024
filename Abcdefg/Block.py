import random
from typing import Tuple

import pygame

import AIHelper
import Config
import I18n
from Config import BLOCK_SIZE
from entity import Player
from render import Renderer, Particle


class Block:
    def __init__(self, name: str, renderer: Renderer, obstacle=False):
        # 初始化方块
        self.name = name  # 方块的名称
        self.renderer = renderer  # 方块的渲染器，用于显示方块的图像
        self.path = obstacle  # 方块是否为障碍物，默认为 False

    @staticmethod
    def get_rect(block_pos: Tuple[int, int]):
        # 获取方块的位置矩形区域
        return pygame.Rect(block_pos, (BLOCK_SIZE, BLOCK_SIZE))

    def on_entity(self, block_pos: Tuple[int, int], mob):
        # 当实体与方块碰撞时触发的方法（可以在子类中实现具体行为）
        pass

    def tick(self, block_pos: Tuple[int, int]):
        pass

    def render(self, screen: pygame.Surface, pos: Tuple[int, int]):
        # 渲染方块
        self.renderer.render(screen, pos, False)


class LavaBlock(Block):

    def tick(self, block_pos: Tuple[int, int]):
        if random.randint(0, 270) == 0:
            x = block_pos[0] * BLOCK_SIZE + BLOCK_SIZE // 4 + random.randint(0, BLOCK_SIZE // 2)
            Particle.ENV_PARTICLES.add(
                Particle.LavaParticle((x, block_pos[1] * BLOCK_SIZE + random.randint(0, BLOCK_SIZE // 2)), 90))

    # 熔岩方块，继承自 Block 类
    def on_entity(self, block_pos: Tuple[int, int], mob):
        # 当实体进入熔岩方块时触发
        mob.fire_tick = 450  # 设置实体的火焰持续时间
        overlap = mob.get_rect().clip(self.get_rect(block_pos))  # 计算实体与熔岩方块的重叠区域
        # 计算重叠区域的面积并给予实体伤害，伤害与重叠面积成正比
        mob.damage((overlap.width * overlap.height) / BLOCK_SIZE ** 2 / 3)


class WaterBlock(Block):
    # 水方块，继承自 Block 类
    def on_entity(self, block_pos: Tuple[int, int], mob):
        # 当实体进入水方块时触发
        mob.fire_tick = 0  # 取消火焰效果
        overlap = mob.get_rect().clip(self.get_rect(block_pos))  # 计算实体与水方块的重叠区域
        # 计算重叠区域的面积并治愈实体，治愈量与重叠面积成正比
        mob.heal((overlap.width * overlap.height) / BLOCK_SIZE ** 2 / 5)


class PortalBlock(Block):
    # 传送门方块，继承自 Block 类
    def __init__(self, name: str, renderer, obstacle=False, target_dimension=None, target_pos=(0, 0)):
        # 初始化传送门方块
        super().__init__(name, renderer, obstacle)  # 调用父类构造函数
        self.target_dimension = target_dimension  # 目标地图维度
        self.target_pos = target_pos  # 目标位置

    def on_entity(self, block_pos: Tuple[int, int], mob):
        # 当实体进入传送门方块时触发
        if isinstance(mob, Player.Player):  # 如果实体是玩家
            if not Config.NETHER_PORTAL_LOCK:  # 如果传送门没有被锁定
                mob.teleport(self.target_dimension, self.target_pos)  # 玩家传送到目标维度和位置
                AIHelper.add_response(f'player has entered portal and been teleported to {self.target_dimension}')
            else:
                Config.CLIENT.current_hud.hint = I18n.text('nether_portal_lock').get()  # 提示传送门被锁定


def image_renderer(file: str):
    # 图片渲染器，根据文件路径加载图片并渲染为方块大小
    return Renderer.image_renderer("blocks/" + file, (BLOCK_SIZE, BLOCK_SIZE))


GRASS_BLOCK = Block("grass_block", image_renderer("grass_block.png"))
STONE = Block("stone", image_renderer("stone.png"), obstacle=True)
LAVA = LavaBlock("lava", Renderer.LAVA)
WATER = WaterBlock("water", Renderer.WATER)
NETHER_PORTAL = PortalBlock("nether_portal", Renderer.NETHER_PORTAL,
                            target_dimension='the_nether', target_pos=(60, 1080))
GRASS_BLOCK_WITH_FLOWER = Block("grass_block_with_flower", image_renderer("grass_block_with_flower.png"))
GRASS_BLOCK_WITH_MUSHROOM = Block("grass_block_with_mushroom", image_renderer("grass_block_with_mushroom.png"))
END_PORTAL = PortalBlock("end_portal", Renderer.END_PORTAL, target_dimension='the_end')
NETHER_BACK_PORTAL = PortalBlock("nether_portal", Renderer.NETHER_PORTAL,
                                 target_dimension='the_world', target_pos=(1080, 1080))
END_STONE = Block("end_stone", image_renderer("end_stone.png"))
WARPED_PLANKS = Block("warped_planks", image_renderer("warped_planks.png"), obstacle=True)
NETHERITE_BLOCK = Block("netherite_block", image_renderer("netherite_block.png"))
OBSIDIAN = Block("obsidian", image_renderer("obsidian.png"))
OAK_TRAPDOOR = Block("oak_trapdoor", image_renderer("oak_trapdoor.png"), obstacle=True)
REDSTONE_BLOCK = Block("redstone_block", image_renderer("redstone_block.png"), obstacle=True)
JACK_O_LANTERN = Block("jack_o_lantern", image_renderer("jack_o_lantern.png"))
OAK_PLANKS = Block("oak_planks", image_renderer("oak_planks.png"), obstacle=True)
STONE_BRICKS = Block("stone_bricks", image_renderer("stone_bricks.png"))
