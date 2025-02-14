import pygame

import entity.NetherNPC
import entity.BossNPC
import entity.NPC
import I18n
import Config
import Block
from Config import MAP_WIDTH, MAP_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
from Dimension import Dimension, TheWorldDimension
from render import Renderer, Particle
from ui.ChatUI import ChatUI
from ui.DeathUI import DeathUI
from ui.MainHud import MainHud
from ui.MessageBoxUI import MessageBoxUI


def generate_the_world():
    # 生成世界地图，包含草地、岩浆、石头和水块
    mp = Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [
        Block.GRASS_BLOCK, Block.LAVA, Block.STONE, Block.WATER, Block.JACK_O_LANTERN
    ], [150, 1, 2, 1, 1])

    # 在地图的特定位置添加黑曜石和传送门
    for i in range(3):
        mp[MAP_WIDTH - 10 + i][MAP_HEIGHT - 10] = mp[MAP_WIDTH - 10 + i][MAP_HEIGHT - 8] = Block.OBSIDIAN
    mp[MAP_WIDTH - 10][MAP_HEIGHT - 9] = mp[MAP_WIDTH - 8][MAP_HEIGHT - 9] = Block.OBSIDIAN
    mp[MAP_WIDTH - 9][MAP_HEIGHT - 9] = Block.NETHER_PORTAL

    for i in range(4, 12):
        mp[i][10] = mp[i][19] = Block.OAK_PLANKS
        for j in range(11, 19):
            mp[i][j] = Block.STONE_BRICKS
    for i in range(10, 14):
        mp[3][i] = Block.OAK_PLANKS
        mp[12][i] = Block.OAK_PLANKS
    for i in range(14, 16):
        mp[3][i] = Block.STONE_BRICKS
        mp[12][i] = Block.STONE_BRICKS
    for i in range(16, 20):
        mp[3][i] = Block.OAK_PLANKS
        mp[12][i] = Block.OAK_PLANKS

    return mp


def generate_the_end():
    # 生成末地地图，只有末地石
    mp = Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [Block.END_STONE, Block.REDSTONE_BLOCK], [150, 1])
    # 设置末地中的传送门
    mp[MAP_WIDTH // 2][MAP_HEIGHT // 2] = Block.NETHER_BACK_PORTAL
    return mp


def generate_the_nether():
    # 读取并生成地狱地图
    mp = [[Block.WARPED_PLANKS] * 17 + [Block.NETHERITE_BLOCK] * 3 + [Block.WARPED_PLANKS] * 40]
    with open('assets/maps/nether.txt', 'r') as f:
        for line in f.readlines():
            mp.append([Block.WARPED_PLANKS if i == 'B' else Block.NETHERITE_BLOCK
                       for i in line.strip()] + [Block.WARPED_PLANKS] * 39)
    # 生成陷阱门和其他特殊地形
    for i in range(38):
        mp.append([Block.WARPED_PLANKS] * MAP_WIDTH)
    mp[2][17] = mp[3][19] = Block.OAK_TRAPDOOR
    mp[7][11] = mp[8][10] = Block.OAK_TRAPDOOR
    mp[0][18] = Block.LAVA

    return mp


def load_sound(name, path, volume=0.5):
    # 加载音效文件并设置音量
    Config.SOUNDS[name] = pygame.mixer.Sound(path)
    Config.SOUNDS[name].set_volume(volume)


class Client:
    def __init__(self, screen: pygame.Surface, clock, player, dimension):
        # 初始化游戏世界
        Config.WORLDS['the_world'] = TheWorldDimension('the_world', MAP_WIDTH, MAP_HEIGHT, generate_the_world(),
                                                       './assets/sounds/music_minecraft.mp3')
        Config.WORLDS['the_nether'] = Dimension('the_nether', MAP_WIDTH, MAP_HEIGHT, generate_the_nether(),
                                                './assets/sounds/music_mario.mp3')
        Config.WORLDS['the_end'] = Dimension('the_end', MAP_WIDTH, MAP_HEIGHT, generate_the_end(),
                                             './assets/sounds/music_terribly.mp3')

        # 设置字体
        Config.FONT = pygame.font.Font("./assets/lang/simhei.ttf", 16)
        Config.FONT_BOLD = pygame.font.Font("./assets/lang/simhei.ttf", 16)
        Config.FONT_BOLD.set_bold(True)
        Config.MIDDLE_FONT = pygame.font.Font("./assets/lang/simhei.ttf", 24)
        Config.MIDDLE_FONT_BOLD = pygame.font.Font("./assets/lang/simhei.ttf", 24)
        Config.MIDDLE_FONT_BOLD.set_bold(True)
        Config.LARGE_FONT = pygame.font.Font("./assets/lang/simhei.ttf", 32)
        Config.HUGE_FONT = pygame.font.Font("./assets/lang/simhei.ttf", 48)

        world_npc1 = entity.NPC.MasterstrokeTradeNPC(((MAP_WIDTH - 11) * Config.BLOCK_SIZE + 5,
                                                      (MAP_WIDTH - 11) * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_world'].spawn_entity(world_npc1)
        world_npc2 = entity.NPC.VillagerNPC((5 * Config.BLOCK_SIZE + 5, 17 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_world'].spawn_entity(world_npc2)
        world_npc3 = entity.NPC.MedicineTraderNPC((5 * Config.BLOCK_SIZE + 5, 12 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_world'].spawn_entity(world_npc3)
        world_npc4 = entity.NPC.WeaponTraderNPC((10 * Config.BLOCK_SIZE + 5, 17 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_world'].spawn_entity(world_npc4)

        nether_npc1 = entity.NetherNPC.NetherNPC1((2 * Config.BLOCK_SIZE + 5, 18 * Config.BLOCK_SIZE + 5))
        nether_npc1.mirror = True
        Config.WORLDS['the_nether'].spawn_entity(nether_npc1)
        nether_npc2 = entity.NetherNPC.NetherNPC2((8 * Config.BLOCK_SIZE + 5, 11 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_nether'].spawn_entity(nether_npc2)
        nether_npc3 = entity.NetherNPC.NetherNPC3((2 * Config.BLOCK_SIZE + 5, 1 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_nether'].spawn_entity(nether_npc3)
        nether_npc4 = entity.NetherNPC.NetherNPC4((12 * Config.BLOCK_SIZE + 5, 2 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_nether'].spawn_entity(nether_npc4)
        nether_npc5 = entity.NetherNPC.NetherNPC5((20 * Config.BLOCK_SIZE + 5, 1 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_nether'].spawn_entity(nether_npc5)

        boss_npc1 = entity.BossNPC.BossNPC1((2 * Config.BLOCK_SIZE + 5, 10 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_end'].spawn_entity(boss_npc1)
        boss_npc2 = entity.BossNPC.BossNPC2((2 * Config.BLOCK_SIZE + 5, 12 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_end'].spawn_entity(boss_npc2)
        boss_npc3 = entity.BossNPC.BossNPC3((2 * Config.BLOCK_SIZE + 5, 14 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_end'].spawn_entity(boss_npc3)
        boss_npc4 = entity.BossNPC.BossNPC4((2 * Config.BLOCK_SIZE + 5, 16 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_end'].spawn_entity(boss_npc4)
        boss_npc5 = entity.BossNPC.BossNPC5((2 * Config.BLOCK_SIZE + 5, 18 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_end'].spawn_entity(boss_npc5)
        boss_npc6 = entity.BossNPC.BossNPC6((2 * Config.BLOCK_SIZE + 5, 20 * Config.BLOCK_SIZE + 5))
        Config.WORLDS['the_end'].spawn_entity(boss_npc6)

        # 加载音效
        load_sound('hit', './assets/sounds/hit.mp3', 0.5)
        load_sound('player_death', './assets/sounds/player_death.mp3', 0.5)
        load_sound('zeus', './assets/sounds/zeus.mp3', 0.25)
        load_sound('button1', './assets/sounds/button1.mp3', 0.75)
        load_sound('button2', './assets/sounds/button2.mp3', 0.75)
        load_sound('victory', './assets/sounds/victory.mp3', 0.75)
        load_sound('heart', './assets/sounds/heart.mp3', 1)
        load_sound('arrow', './assets/sounds/arrow.mp3', 0.75)
        load_sound('tnt', './assets/sounds/tnt.mp3', 0.75)
        load_sound('explosion', './assets/sounds/explosion.mp3', 0.5)

        # 加载图像资源
        Config.COIN_IMAGE = pygame.transform.scale(pygame.image.load('./assets/ui/coin.png'), (20, 20))
        Config.SPIRIT_POWER_IMAGE = pygame.transform.scale(pygame.image.load('./assets/ui/spirit_power.png'), (20, 20))
        Config.LANGUAGE_IMAGE = pygame.transform.scale(pygame.image.load('./assets/ui/language.png'), (20, 20))
        Config.MESSAGE_IMAGE = pygame.transform.scale(pygame.image.load('./assets/ui/message.png'), (20, 20))

        # 初始化客户端界面
        self.screen = screen
        self.clock = clock
        self.tick_counter = 0
        self.player = player
        self.current_ui = None
        self.current_hud = MainHud(player)
        self.dimension = Config.WORLDS[dimension]
        self.set_dimension(Config.WORLDS[dimension])
        self.camera = self.player.get_camera()

        # 注册定时任务
        Config.CLOCKS.append((15, self.update_hint))

    def update_hint(self):
        # 更新显示提示信息
        nearest = self.dimension.nearest_entity(self.player.get_pos())
        if nearest is not None and nearest.is_nearby(self.player):
            self.current_hud.display_hint = True
            self.current_hud.target_entity = nearest
        else:
            self.current_hud.display_hint = False
            self.current_hud.target_entity = None

    @staticmethod
    def change_music(music):
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    @staticmethod
    def pause_music():
        pygame.mixer.music.pause()

    def spawn_entity(self, entity_to_spawn):
        self.dimension.spawn_entity(entity_to_spawn)

    def set_dimension(self, dimension):
        self.dimension = dimension
        if dimension.music is not None:
            self.change_music(dimension.music)

    def open_ui(self, ui):
        self.current_ui = ui

    def open_message_box(self, text: I18n.Text, father_ui):
        self.open_ui(MessageBoxUI(text, father_ui))

    def close_ui(self):
        ui = self.current_ui
        self.current_ui = None
        if ui is not None:
            ui.on_close()
        del ui

    def open_death_ui(self):
        self.player.coins //= 2
        self.current_ui = DeathUI()

    def player_respawn(self):
        self.player.respawn()
        self.close_ui()

    def render_entities(self, layers):
        for i in self.dimension.entities:
            if (self.camera[0] - i.size[0] <= i.x <= self.camera[0] + SCREEN_WIDTH and
                    self.camera[1] - i.size[1] <= i.y <= self.camera[1] + SCREEN_HEIGHT):
                i.render(layers, self.camera)
        self.player.render(layers, self.camera)

    def tick(self, events):
        # 务必先渲染背景
        self.screen.fill((50, 50, 50))

        self.dimension.render(self.screen, self.camera)

        if self.current_ui is None:
            layers = [self.screen, pygame.Surface(self.screen.get_size(), pygame.SRCALPHA),
                      pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)]

            self.dimension.tick(self.camera)
            for i in Renderer.ANIMATIONS:
                i.tick()
            self.player.tick(self.dimension)
            for i in self.dimension.entities:
                if i.hp <= 0:
                    self.dimension.entities.remove(i)
                    del i
                else:
                    i.tick(self.dimension, self.player)

            # 玩家移动
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SLASH]:
                self.open_ui(ChatUI())
            if keys[pygame.K_w]:  # 向上移动
                self.player.move(4, self.dimension)
            if keys[pygame.K_s]:  # 向下移动
                self.player.move(3, self.dimension)
            if keys[pygame.K_a]:  # 向左移动
                self.player.move(2, self.dimension)
            if keys[pygame.K_d]:  # 向右移动
                self.player.move(1, self.dimension)
            if keys[pygame.K_f] or keys[pygame.K_b]:
                nearest = self.dimension.nearest_entity(self.player.get_pos())
                if nearest is not None and nearest.is_nearby(self.player):
                    if keys[pygame.K_f]:
                        nearest.on_interact(self.player)
                    if keys[pygame.K_b]:
                        nearest.on_battle(self.player)

            # 踩岩浆扣血
            # for k in range(50):
            #     if (dimension.get_block_from_pos((player.x + k, player.y + k)) == Block.LAVA or
            #             dimension.get_block_from_pos((player.x + 50 - k, player.y + k)) == Block.LAVA):
            #         player.hp -= 1 / 90
            # player.hp = max(0, player.hp)

            # 更新摄像机位置
            self.camera = self.player.get_camera()

            if self.player.hp <= 0:
                Config.SOUNDS['player_death'].play()
                self.open_death_ui()

            self.render_entities(layers)

            Particle.ENV_PARTICLES.tick()
            Particle.ENV_PARTICLES.render(self.screen, Config.FONT, self.camera)

            self.screen.blit(layers[1], (0, 0))
            self.screen.blit(layers[2], (0, 0))

            self.current_hud.tick(keys, events)
            self.current_hud.render(self.screen)
        else:
            self.render_entities([self.screen, self.screen, self.screen])
            self.current_ui.render(self.screen)
            if not self.current_ui.tick(pygame.key.get_pressed(), events):
                self.close_ui()

        Particle.UI_PARTICLES.tick()
        Particle.UI_PARTICLES.render(self.screen, Config.MIDDLE_FONT)

        self.tick_counter += 1
        for clock in Config.CLOCKS:
            if isinstance(clock, list):
                ticks, method, times = clock
                if self.tick_counter % ticks == 0:
                    method()
                    clock[2] -= 1
                    if clock[2] == 0:
                        Config.CLOCKS.remove(clock)
            else:
                ticks, method = clock
                if self.tick_counter % ticks == 0:
                    method()
