import random
from typing import Tuple

import pygame
from pygame import Rect

from render import Action, Renderer, Particle
import Config
from Config import BLOCK_SIZE, INTERACTION_DISTANCE
from ui.BattleUI import BattleUI


def render_dialog_at_absolute_pos(text, screen, pos, font: pygame.font):
    # 渲染对话框文本，并且添加背景和边框
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (pos[0] - text_rect.width // 2, pos[1])

    # 绘制边框
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(17, 17), border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(15, 15), border_radius=8)
    screen.blit(text_surface, text_rect.topleft)


class Entity:
    def __init__(self, name: str, pos: Tuple[int, int], renderer: Renderer, actions: list[Action] = None,
                 atk: float = 1.0, crt: float = 0.0, coins: int = 0, max_hp: float = 100, size: Tuple[int, int] = None,
                 sp: int = 0):
        # 初始化实体
        self.name = name
        self.x, self.y = pos
        self.renderer = renderer
        self.size = size or renderer.get_size()
        self.mirror = False  # 是否镜像（用于角色朝向）
        self.hp = self.max_hp = max_hp  # 生命值和最大生命值
        self.fire_tick = 0  # 火焰持续时间，用于持续伤害
        self.sp = sp
        self.atk = atk  # 攻击力
        self.crt = crt  # 暴击率
        self.moving = False  # 是否在移动
        self.crt_damage = 2.0  # 暴击伤害
        self.coins = coins  # 拥有的金币数量
        self.interact = False  # 是否可以与玩家互动
        self.battle = True  # 是否参与战斗
        self.actions = actions if actions is not None else [Action.ATTACK_LEFT]  # 实体可以执行的动作

    def damage(self, damage: float):
        # 扣除生命值，确保不低于0
        self.hp = max(0.0, self.hp - damage)

    def heal(self, cure: float):
        # 恢复生命值，确保不超过最大生命值
        self.hp = min(self.max_hp, self.hp + cure)

    def move(self, direction: int, dimension, speed: int = 4):
        # 根据方向移动实体，考虑地图边界和障碍物
        if not (1 <= direction <= 4):
            return

        self.moving = True
        # 获取当前方块位置，并检查是否有障碍物
        block_x, block_y = dimension.get_block_index((self.x, self.y))
        block2_x, block2_y = block_x, block_y

        if direction == 1:
            self.x += speed  # 向右移动
            self.mirror = False  # 不镜像
            block_x += 1
            block2_x, block2_y = block_x, block_y + 1
        elif direction == 2:
            self.x -= speed  # 向左移动
            self.mirror = True  # 镜像
            block_x -= 1
            block2_x, block2_y = block_x, block_y + 1
        elif direction == 3:
            self.y += speed  # 向下移动
            block_y += 1
            block2_x, block2_y = block_x + 1, block_y
        elif direction == 4:
            self.y -= speed  # 向上移动
            block_y -= 1
            block2_x, block2_y = block_x + 1, block_y

        # 地图边界限制
        limit_x, limit_y = dimension.get_render_size()
        self.x = max(0, min(limit_x - self.size[0], self.x))
        self.y = max(0, min(limit_y - self.size[1], self.y))

        # 障碍物处理，检查是否与障碍物相撞
        rect = self.get_rect()
        if ((rect.colliderect(Rect(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) and
             dimension.get_block_from_index((block_x, block_y)).path) or
                (rect.colliderect(Rect(block2_x * BLOCK_SIZE, block2_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) and
                 dimension.get_block_from_index((block2_x, block2_y)).path)):
            # 根据方向调整位置，防止穿越障碍物
            if direction == 1:
                self.x -= self.x + self.size[0] - block_x * BLOCK_SIZE
            elif direction == 2:
                self.x += block_x * BLOCK_SIZE - self.x + BLOCK_SIZE
            elif direction == 3:
                self.y -= self.y + self.size[1] - block_y * BLOCK_SIZE
            elif direction == 4:
                self.y += block_y * BLOCK_SIZE - self.y + BLOCK_SIZE

        if random.randint(0, 5) == 0:
            pos = self.get_left_bottom_pos()
            Particle.ENV_PARTICLES.add(Particle.WalkParticle((pos[0] + random.randint(0, self.size[0]),
                                                              pos[1] + random.randint(-5, 5)), 30))

    def tick(self, dimension, player=None):
        # 每帧更新实体状态，处理持续伤害等
        self.moving = False
        for i in {dimension.get_block_index(self.get_left_top_pos()),
                  dimension.get_block_index(self.get_left_bottom_pos()),
                  dimension.get_block_index(self.get_right_top_pos()),
                  dimension.get_block_index(self.get_right_bottom_pos())}:
            blk = dimension.get_block_from_index(i)
            if blk is not None:
                blk.on_entity(dimension.get_pos_from_index(i), self)
        if self.fire_tick > 0:
            self.fire_tick -= 1
            self.damage(1 / 12)  # 火焰伤害

    def respawn_at_pos(self, pos: Tuple[int, int]):
        # 重生，恢复生命值并重置火焰持续时间
        self.x, self.y = pos
        self.hp = self.max_hp
        self.fire_tick = 0

    def get_pos(self):
        # 返回实体的位置
        return self.x, self.y

    def get_rect(self):
        # 返回实体的矩形区域
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def get_left_top_pos(self):
        # 返回实体的左上角位置
        return self.x, self.y

    def get_left_bottom_pos(self):
        # 返回实体的左下角位置
        return self.x, self.y + self.size[1] - 1

    def get_right_top_pos(self):
        # 返回实体的右上角位置
        return self.x + self.size[0] - 1, self.y

    def get_right_bottom_pos(self):
        # 返回实体的右下角位置
        return self.x + self.size[0] - 1, self.y + self.size[1] - 1

    def is_nearby(self, entity, distance=INTERACTION_DISTANCE):
        # 检查另一个实体是否在交互范围内
        return abs(self.x - entity.x) + abs(self.y - entity.y) < distance * BLOCK_SIZE

    def render(self, layers: list[pygame.Surface], camera: Tuple[int, int]):
        # 渲染实体及其生命条
        self.renderer.render(layers[0], (self.x - camera[0], self.y - camera[1]), self.mirror, not self.moving)
        if self.fire_tick > 0:
            Renderer.FIRE.render(layers[0], (self.x - camera[0], self.y - camera[1]))
        self.render_hp_bar(layers[0], (self.x - camera[0], self.y - camera[1] - 10), Config.FONT)

    def render_at_absolute_pos(self, screen: pygame.Surface, pos: Tuple[int, int], use_mirror=False, hp_bar=True):
        # 在绝对位置渲染实体
        self.renderer.render(screen, pos, use_mirror, True)
        if hp_bar:
            self.render_hp_bar(screen, (pos[0], pos[1] - 10), Config.FONT)

    def render_hp_bar(self, screen: pygame.Surface, pos: Tuple[int, int], font=None):
        # 渲染实体的生命条
        bar_width, bar_height = self.size[0], 5
        hp_rect = pygame.Rect(pos[0], pos[1], bar_width * min(1.0, self.hp / self.max_hp), bar_height)
        border_rect = pygame.Rect(pos[0], pos[1], bar_width, bar_height)
        color = (0, 255, 0)
        if self.hp <= 2 * self.max_hp // 3:
            color = (255, 255, 0)
            if self.hp <= self.max_hp // 3:
                color = (255, 0, 0)
        pygame.draw.rect(screen, color, hp_rect)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 1)

    def on_interact(self, player):
        # 互动逻辑（可以在子类中实现具体行为）
        pass

    def on_battle(self, player):
        # 开始战斗
        Config.CLIENT.open_ui(BattleUI(player, self))

    def can_interact(self):
        # 是否可以与该实体互动
        return self.interact

    def can_battle(self):
        # 是否可以与该实体战斗
        return self.battle


class Monster(Entity):

    def __init__(self, name: str, pos: Tuple[int, int], renderer: Renderer, actions: list[Action] = None,
                 atk: float = 1.0, crt: float = 0.0, coins: int = 0, max_hp: float = 100, size: Tuple[int, int] = None,
                 sp: int = 0):
        # 初始化怪物
        super().__init__(name, pos, renderer, actions, atk, crt, coins, max_hp, size, sp)
        self.direction = 0

    def tick(self, dimension, player=None):
        # 怪物的行为更新
        super().tick(dimension, player)
        self.move(self.direction, dimension, 1)  # 按方向移动
        if random.randint(0, 450) == 0:
            if random.randint(0, 5) == 0:
                self.direction = random.randint(1, 4)  # 随机选择一个新方向
            else:
                self.direction = 0  # 停止移动
