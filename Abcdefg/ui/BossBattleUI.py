import Config
import I18n
from render import Action
from ui.BattleUI import BattleUI
from ui.widget.ClassicButton import ClassicButton


class BossBattleUI(BattleUI):

    def __init__(self, player, enemy, after_battle=None):
        self.life_steal_button = None
        super().__init__(player, enemy, after_battle)
        Config.CLIENT.change_music('./assets/sounds/music_battle.mp3')

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
        self.life_steal_button = ClassicButton(I18n.text('live_steal')
                                               if self.player.skill_unlocked and self.player.skill == 1
                                               else I18n.text('live_steal_lock'),
                                               (Config.SCREEN_WIDTH // 2 + 100, Config.SCREEN_HEIGHT // 2 + 50),
                                               (95, 50),
                                               on_click=lambda: self.round_start(Action.LIFE_STEAL_RIGHT))
        self.life_steal_button.set_active(self.player.skill_unlocked and self.player.skill == 1)
        self.add_button(self.life_steal_button)

    # 设置所有按钮的激活状态
    def set_buttons_active(self, active):
        super().set_buttons_active(active)
        self.life_steal_button.set_active(self.player.skill_unlocked and self.player.skill == 1)

    def round_start(self, action=None):
        super().round_start(action)
        self.enemy.atk -= 0.5
