import Config
import I18n
from Dialog import Dialog
from entity.NPC import NPC
from render import Renderer, Action
from ui.BattleUI import BattleUI
from ui.BossBattleUI import BossBattleUI
from entity import Entity
from ui.DialogUI import DialogUI
from ui.TheEndUI import TheEndUI


class HerobrineNPC(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('yourself'), pos, Renderer.image_renderer('entities/herobrine.png', (50, 50)))
        self.battle = True
        self.actions = [Action.ATTACK_LEFT, Action.LASER_CANNON_LEFT, Action.LASER_CANNON_LEFT]
        self.hp = 500
        self.max_hp = 500
        self.atk = 10

    def on_battle(self, player):
        Config.CLIENT.open_ui(BossBattleUI(player, self, self.open_stage2_battle_ui))

    def open_stage2_battle_ui(self, win: bool):
        if win:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss_true'),
                                           lambda msg: self.process_choice(Config.CLIENT.player, msg)))
            return False
        else:
            return True

    def process_choice(self, player, choice):
        if choice == '1':
            self.hp = 1500  # 脚填数值
            self.max_hp = 1500
            self.atk = 15
            Config.CLIENT.open_ui(BossBattleUI(player, self, self.open_finale_dialog))
        return "!#"

    def open_finale_dialog(self, win):
        if win:
            Config.CLIENT.change_music('./assets/sounds/music_finale.mp3')
            Config.CLIENT.open_ui(DialogUI(
                self, Dialog('last'), lambda msg_2: self.process_choice_2(Config.CLIENT.player, msg_2)))
            return False
        return True

    def process_choice_2(self, player, choice):
        e_npc = Entity.Entity(I18n.text('programmer'), self.get_right_bottom_pos(),
                              Renderer.image_renderer('entities/programmer.png', (50, 50)), atk=0, sp=0)
        if choice == '1':
            Config.CLIENT.open_ui(DialogUI(e_npc, Dialog('end'),
                                           lambda msg: self.process_choice_3(Config.CLIENT.player, msg)))

    @staticmethod
    def process_choice_3(player, choice):
        if choice == '1':
            Config.CLIENT.open_ui(TheEndUI())


class BossNPC6(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.GHAST)

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss1'),
                                           lambda msg: self.process_choice(player, msg)))

    @staticmethod
    def process_choice(player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '3':
            h_npc = HerobrineNPC((500, 500))
            Config.CLIENT.open_ui(BattleUI(player, h_npc, h_npc.open_stage2_battle_ui))
            return "!"
        return "!#"


class BossNPC2(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('entities/dragon.png', (50, 50)))
        self.max_hp = 11111111
        self.hp = 11111111
        self.atk = 114541

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss2'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.open_ui(BattleUI(player, self))
            if Config.CLIENT.player.hp > Config.CLIENT.player.max_hp / 2:
                Config.CLIENT.player.damage(Config.CLIENT.player.hp - Config.CLIENT.player.max_hp / 2)
            Config.CLIENT.player.max_hp /= 2
        elif choice == '3':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        return "!#"


class BossNPC3(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('entities/electro_dragon.png', (50, 50)))
        self.max_hp = 1
        self.hp = 1
        self.atk = 0.1

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss3'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.open_ui(BattleUI(player, self))
        elif choice == '3':
            Config.CLIENT.player.crt_damage *= 2
            self.interact = False
        elif choice == '4':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        return "!#"


class BossNPC4(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('entities/inferno_dragon.png', (50, 50)))
        self.max_hp = 11111111
        self.hp = 11111111
        self.atk = 114541

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss4'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        elif choice == '3':
            Config.CLIENT.open_ui(BattleUI(player, self))
            Config.CLIENT.player.atk /= 2
        elif choice == '4':
            Config.CLIENT.player.crt *= 2
            self.interact = False

        return "!#"


class BossNPC5(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('entities/lava_hound.png', (50, 50)))
        self.max_hp = 1
        self.hp = 1
        self.atk = 0.1

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss5'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.open_ui(BattleUI(player, self))
            Config.CLIENT.player.coins += 100
            self.interact = False
        elif choice == '3':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        elif choice == '4':
            Config.CLIENT.player.atk *= 2
            self.interact = False

        return "!#"


class BossNPC1(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('entities/super_dragon.png', (50, 50)))
        self.max_hp = 1
        self.hp = 1
        self.atk = 0.1



    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss6'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.open_ui(BattleUI(player, self))
            Config.CLIENT.player.coins += 100
            self.interact = False
        elif choice == '3':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        elif choice == '4':
            Config.CLIENT.player.hp *= 2
            Config.CLIENT.player.max_hp *= 2
            self.interact = False

        return "!#"
