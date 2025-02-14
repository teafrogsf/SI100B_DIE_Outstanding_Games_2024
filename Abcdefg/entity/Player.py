from typing import Tuple

import AIHelper
import Config
from Config import SCREEN_WIDTH, SCREEN_HEIGHT
from entity.Entity import Entity
from render import Action
from render.Renderer import AnimationRenderer


class Player(Entity):

    def __init__(self, name: str, respawn_pos: Tuple[int, int], pos: Tuple[int, int],
                 renderer: AnimationRenderer, size=None):
        super().__init__(name, pos, renderer, actions=[
            Action.ATTACK_RIGHT, Action.ULTIMATE_RIGHT
        ], crt=0.5, size=size)
        self.dialog_timer = 0
        self.respawn_pos = respawn_pos
        self.energy = 3
        self.souls = 1
        self.skill_unlocked = False
        self.skill = 0
        # 0: NONE, 1: 天谴, 2: 吸血
        self.iron = 0
        self.coins = 0
        Config.CLOCKS.append((90, self.tick_second))

    def get_camera(self):
        return self.x + self.size[0] // 2 - SCREEN_WIDTH // 2, self.y + self.size[1] // 2 - SCREEN_HEIGHT // 2
        # 获得摄像头应该在的位置

    def respawn(self):
        self.reset_energy()
        self.teleport('the_world', self.respawn_pos)
        self.respawn_at_pos(self.respawn_pos)

    def teleport(self, dimension_str, pos: Tuple[int, int]):
        if dimension_str != Config.CLIENT.dimension.name:
            dimension = Config.WORLDS[dimension_str]
            if dimension is None:
                return
            Config.CLIENT.set_dimension(dimension)
        self.x, self.y = pos

    def update_energy(self):
        if self.energy < 3:
            self.energy += 1
            if self.energy == 3:
                AIHelper.add_response('ultimate skill available', (0, 0, 255))

    def reset_energy(self):
        self.energy = 0

    def ultimate_available(self):
        return self.energy == 3

    def tick_second(self):
        if self.fire_tick > 0 and Config.CLIENT.current_ui is None:
            Config.SOUNDS['hit'].play()
