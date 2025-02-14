import random

import AIHelper
import Block
import Config
import I18n
from Dialog import Dialog
from entity.NPC import TraderNPC, NPC
from render import Renderer
from ui.DialogUI import DialogUI


class NetherNPC1(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc1'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def dialog(self):
        return I18n.text('nether_npc1_dialog')

    def on_interact(self, player):
        # 玩家与NPC交互时触发
        if self.interact:
            # 打开对话框UI，调用process_choice方法处理玩家选择
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc1'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        Config.CLIENT.dimension.set_block((0, 19), Block.NETHERITE_BLOCK)
        if choice == '1':
            Config.CLIENT.dimension.set_block((2, 17), Block.NETHERITE_BLOCK)
            self.generate_the_end_portal()
            AIHelper.add_response('player has interacted with nether npc1')
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((3, 19), Block.NETHERITE_BLOCK)
            self.generate_the_end_portal()
            AIHelper.add_response('player has interacted with nether npc1')
            return 'b2'
        else:
            return '!#'

    @staticmethod
    def generate_the_end_portal():
        # 在草地上随机生成花朵或蘑菇
        mp = Config.WORLDS['the_world'].blocks
        for i in range(3):
            mp[Config.MAP_WIDTH - 10 + i][8] = mp[Config.MAP_WIDTH - 10 + i][10] = (
                random.choice([Block.GRASS_BLOCK_WITH_FLOWER, Block.GRASS_BLOCK_WITH_MUSHROOM]))
        mp[Config.MAP_WIDTH - 10][9] = mp[Config.MAP_WIDTH - 8][9] = random.choice([Block.GRASS_BLOCK_WITH_FLOWER,
                                                                                    Block.GRASS_BLOCK_WITH_MUSHROOM])
        mp[Config.MAP_WIDTH - 9][9] = Block.END_PORTAL


class NetherNPC2(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc2'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def dialog(self):
        return I18n.text('nether_npc2_dialog')

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc2'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            player.skill_unlocked = True
            Config.CLIENT.dimension.set_block((7, 11), Block.NETHERITE_BLOCK)
            AIHelper.add_response('player has interacted with nether npc2')
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((8, 10), Block.NETHERITE_BLOCK)
            AIHelper.add_response('player has interacted with nether npc2')
            return 'b2'
        else:
            return '!#'


class NetherNPC3(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc3'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def dialog(self):
        return I18n.text('nether_npc3_dialog')

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc3'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '#':
            return '!#'
        elif player.sp < 2:
            return 'b2'
        elif choice == '1':
            self.interact = False
            Config.CLIENT.dimension.set_block((9, 17), Block.NETHERITE_BLOCK)
            Config.CLIENT.dimension.set_block((19, 19), Block.OAK_TRAPDOOR)
            player.sp -= 2
            player.atk += 0.2
            player.crt += 0.1  # 获得狂暴战刃
            AIHelper.add_response('player has interacted with nether npc3')
            return 'b1'
        else:
            return '!#'


class NetherNPC4(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc4'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def dialog(self):
        return I18n.text('nether_npc4_dialog')

    def on_interact(self, player):
        # 玩家与交易NPC交互时触发，打开对话框UI并显示交易界面
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc4'),
                                           lambda msg: self.process_choice(player, msg)))
    
    def process_choice(self, player, choice):
        self.interact = False
        if choice == '#':
            return '!#'
        elif player.sp < 2:
            return 'b3'
        elif choice == '1':
            # 以5点灵力换取冰霜冲击
            player.sp -= 2
            player.atk += 0.15
            player.crt += 0.15
            AIHelper.add_response('player has interacted with nether npc4')
            return 'b1'
        elif choice == '2':
            player.sp = 0
            # 清空你所有的灵力，换取50点攻击力，并直接离开这个世界
            AIHelper.add_response('player has interacted with nether npc4')
            return 'b2'
        else:
            return '!#'


class NetherNPC5(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc5'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def dialog(self):
        return I18n.text('nether_npc5_dialog')

    def on_interact(self, player):
        # 玩家与交易NPC交互时触发，打开对话框UI并显示交易界面
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc5'),
                                           lambda msg: self.process_choice(player, msg)))
            
    def process_choice(self, player, choice):
        self.interact = False
        if choice == '#':
            return '!#'
        elif player.sp < 2:
            return 'b2'
        elif choice == '1':
            # 获得回响之杖
            player.sp -= 2
            player.crt += 0.3
            AIHelper.add_response('player has interacted with nether npc5')
            return 'b1'
        else:
            return '!#'

