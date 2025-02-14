import random
import time

import pygame

import AIHelper
import Config
from entity import Entity
from render import Particle, Action, Renderer
import I18n
from ui.UI import UI
from ui.BattleSuccessUI import BattleSuccessUI
from ui.widget.ClassicButton import ClassicButton


class BattleUI(UI):

    def __init__(self, player, enemy, after_battle=None):
        super().__init__()
        # 初始化所有动作
        for i in Action.ACTIONS:
            i.reset()
        self.after_battle = after_battle  # lambda bool
        self.player = player
        self.enemy = enemy
        self.player_pos = (150, 200)
        self.enemy_pos = (Config.SCREEN_WIDTH - 200, 200)
        self.round = 0  # 当前回合数
        self.half_round = 0  # 半回合数（用来分开玩家和敌人的攻击阶段）
        self.playing_action = False  # 是否正在进行攻击
        self.action = None  # 当前执行的动作
        self.use_crt = False  # 是否触发暴击
        self.escaping_stage = 0  # 逃跑阶段
        # 记录玩家和敌人进入战斗
        AIHelper.add_event('player has entered battle with ' + enemy.name.get())
        self.clock_heart_particle = [10, lambda: Particle.UI_PARTICLES.add(Particle.LifeStealingParticle(
            (600, 215), 90)), 10]
        self.ultimate_button = None
        self.init_buttons()

    def init_buttons(self):
        # 普通攻击按钮
        attack_button = ClassicButton(I18n.text('common_attack'),
                                      (Config.SCREEN_WIDTH // 2 - 200, Config.SCREEN_HEIGHT // 2 + 50),
                                      (95, 50), on_click=lambda: self.round_start(Action.ATTACK_RIGHT))
        self.add_button(attack_button)
        tnt_button = ClassicButton(I18n.text('tnt'),
                                   (Config.SCREEN_WIDTH // 2 - 100, Config.SCREEN_HEIGHT // 2 + 50),
                                   (95, 50), on_click=lambda: self.round_start(Action.TNT_RIGHT))
        self.add_button(tnt_button)
        # 终极攻击按钮
        self.ultimate_button = ClassicButton(I18n.text('ultimate_attack'),
                                             (Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2 + 50),
                                             (95, 50), on_click=lambda: self.round_start(Action.ULTIMATE_RIGHT))
        self.add_button(self.ultimate_button)
        # 判断玩家是否可以使用终极攻击
        self.ultimate_button.set_active(self.player.ultimate_available())
        # 逃跑按钮
        escape_button = ClassicButton(I18n.text('escape'),
                                      (Config.SCREEN_WIDTH // 2 + 100, Config.SCREEN_HEIGHT // 2 + 50),
                                      (95, 50), on_click=self.on_click_escape_button)
        self.add_button(escape_button)

    # 点击逃跑按钮的操作
    def on_click_escape_button(self):
        self.escaping_stage = 1
        self.round_start(Action.EMPTY)
        AIHelper.add_event('player has tried to escape from ' + self.enemy.name.get())

    # 设置所有按钮的激活状态
    def set_buttons_active(self, active):
        for button in self.buttons:
            button.set_active(active)

    # 回合开始，选择使用的攻击方式
    def round_start(self, use_action=Action.ATTACK_RIGHT):
        self.round += 1  # 回合数增加
        self.half_round += 1  # 半回合增加
        self.set_buttons_active(False)  # 禁用所有按钮
        self.playing_action = True  # 标记为正在进行攻击
        self.action = use_action  # 设置当前使用的攻击
        # 根据选择的攻击类型，更新能量或重置能量
        if use_action == Action.ATTACK_RIGHT:
            self.player.update_energy()
        elif use_action == Action.ULTIMATE_RIGHT:
            self.player.reset_energy()
        elif use_action == Action.LIFE_STEAL_RIGHT:
            Config.CLOCKS.append(self.clock_heart_particle)
            self.player.skill_unlocked = False
        elif self.action == Action.TNT_RIGHT:
            Particle.UI_PARTICLES.add(Particle.TntParticle(
                (self.player_pos[0] + self.player.size[0] // 2, self.player_pos[1]), 100))
        # 判断是否触发暴击
        self.use_crt = random.randint(0, 100) < self.player.crt * 100

    # 渲染UI
    def render(self, screen: pygame.Surface):
        super().render(screen)
        if self.playing_action:
            # 获取当前攻击目标、伤害、文本和音效
            target_poses, damage, heal, text, sounds = self.action.get_current_pos()
            damage = max(1, random.randint(damage - 2, damage + 2)) if damage > 0 else damage
            for sound in sounds:
                Config.SOUNDS[sound].play()
            if self.half_round < self.round * 2:  # 玩家攻击阶段
                # 计算真实伤害并应用到敌人
                real_dmg = damage * self.player.atk * (self.player.crt_damage if self.use_crt else 1)
                self.enemy.damage(real_dmg)
                if real_dmg != 0:
                    # 播放伤害粒子效果
                    Particle.UI_PARTICLES.add(Particle.DamageParticle(real_dmg, self.enemy_pos, 180, self.use_crt))
                    center = (self.enemy_pos[0] + self.enemy.size[0] // 2, self.enemy_pos[1] + self.enemy.size[1] // 2)
                    for _ in range(min(1000, int(real_dmg // 3))):
                        Particle.UI_PARTICLES.add(Particle.CriticalHitParticle(center, 50))
                    if self.action == Action.ULTIMATE_RIGHT or self.action == Action.TNT_RIGHT:
                        self.generate_explosion(self.enemy_pos)
                    if self.enemy.hp < self.enemy.max_hp // 3:
                        AIHelper.add_response(f'enemy {self.enemy.name} is now low hp {self.enemy.hp}', (0, 255, 0))
                if heal != 0:
                    self.player.heal(heal)
                    Particle.UI_PARTICLES.add(Particle.DamageParticle(-heal, self.player_pos, 180,
                                                                      False, (0, 255, 0)))
                self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
                if target_poses is None:
                    self.player.render_at_absolute_pos(screen, self.player_pos)
                else:
                    if text != '':
                        text = I18n.text(text).get() or ''
                    for i in target_poses:
                        self.player.render_at_absolute_pos(screen, i)
                        if text != '':
                            Entity.render_dialog_at_absolute_pos(text, screen, (i[0] + self.player.size[0] // 2,
                                                                                i[1] - 40), Config.FONT)
            else:  # 敌人攻击阶段
                real_dmg = damage * self.enemy.atk * (self.enemy.crt_damage if self.use_crt else 1)
                self.player.damage(real_dmg)
                if real_dmg != 0:
                    Particle.UI_PARTICLES.add(Particle.DamageParticle(real_dmg, self.player_pos, 180, self.use_crt))
                    center = (self.player_pos[0] + self.player.size[0] // 2,
                              self.player_pos[1] + self.player.size[1] // 2)
                    for _ in range(min(1000, int(real_dmg // 3))):
                        Particle.UI_PARTICLES.add(Particle.CriticalHitParticle(center, 50))
                    if self.player.hp <= 0:
                        Config.SOUNDS['player_death'].play()
                    elif self.player.hp < self.player.max_hp // 3:
                        AIHelper.add_response(f'player is now in a low hp {self.player.hp}', (255, 0, 0))
                    if heal != 0:
                        self.enemy.heal(heal)
                        Particle.UI_PARTICLES.add(Particle.DamageParticle(-heal, self.player_pos, 180,
                                                                          False, (0, 255, 0)))
                self.player.render_at_absolute_pos(screen, self.player_pos)
                if target_poses is None:
                    self.enemy.render_at_absolute_pos(screen, self.enemy_pos)
                else:
                    for i in target_poses:
                        self.enemy.render_at_absolute_pos(screen, i)
        else:
            self.player.render_at_absolute_pos(screen, self.player_pos)
            self.enemy.render_at_absolute_pos(screen, self.enemy_pos)

        # 渲染当前回合数
        txt_surface = Config.FONT.render(I18n.text('rounds').format(self.round), True, (255, 255, 255))
        screen.blit(txt_surface, (30, 30))

        # 显示最近的聊天消息
        current_time = time.time()
        y_offset = Config.SCREEN_HEIGHT - 50
        lines_cnt = 0
        for message, color, timestamp in Config.CLIENT.current_hud.messages:
            if timestamp > current_time - 20:  # 只显示最近20秒的消息
                if len(message.get().strip()) > 0:
                    txt_surface = Config.FONT.render(message.get().strip(), True, color)
                    screen.blit(txt_surface, (10, y_offset))
                    y_offset -= 20
                    lines_cnt += 1
            if lines_cnt > 6:
                break

    @staticmethod
    def generate_explosion(pos):
        for _ in range(10):
            pos1 = (pos[0] + random.randint(-80, 80), pos[1] + random.randint(-80, 80))
            Particle.UI_PARTICLES.add(Particle.ExplosionParticle(pos1, 40))

    # 处理每一帧的事件
    def tick(self, keys, events):
        super().tick(keys, events)
        Renderer.PLAYER.tick()
        if self.playing_action is None or (self.action is not None and self.action.is_end()):
            if self.player.hp <= 0:
                if self.after_battle is None or self.after_battle(False):
                    Config.CLIENT.close_ui()
                    Config.CLIENT.open_death_ui()
            elif self.enemy.hp <= 0:
                # 玩家战胜敌人，增加金币
                self.player.coins += self.enemy.coins
                self.player.sp += self.enemy.sp
                if self.enemy.name.get() == I18n.text('iron_golem').get():
                    self.player.iron += 1
                if self.after_battle is None or self.after_battle(True):
                    Config.CLIENT.close_ui()
                    Config.CLIENT.open_ui(BattleSuccessUI(self.enemy.name, self.enemy.coins))
                    Config.SOUNDS['victory'].play()
        if self.playing_action:
            if self.action.is_end():
                if self.half_round < self.round * 2:
                    self.action.reset()
                    self.action = random.choice(self.enemy.actions)
                    if self.enemy.hp > 0:
                        if self.action == Action.ARROW_LEFT:
                            Particle.UI_PARTICLES.add(Particle.ArrowParticle(
                                (self.enemy_pos[0], self.enemy_pos[1] + 10), 50))
                        if self.action == Action.LASER_CANNON_LEFT:
                            Particle.UI_PARTICLES.add(Particle.LaserCannonParticle((200, 170), 10))
                    self.half_round += 1
                    self.use_crt = random.randint(0, 100) < self.enemy.crt * 100
                    if self.escaping_stage == 2:
                        Config.CLIENT.close_ui()
                else:
                    self.action.reset()
                    self.playing_action = False
                    self.set_buttons_active(True)
                    self.ultimate_button.set_active(self.player.ultimate_available())
                    if self.escaping_stage == 1:
                        self.escaping_stage = 2
                        self.round_start(Action.ESCAPE_LEFT)
            self.action.tick()
        return True

    # 关闭UI时清除所有粒子
    def on_close(self):
        Particle.UI_PARTICLES.clear()
