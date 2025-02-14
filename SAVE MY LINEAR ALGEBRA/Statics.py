import pygame
import random
from enum import Enum
import math


class Events:
    # Scene Changes
    MAIN_TO_STARTROOM = pygame.USEREVENT + 1
    TO_CHATBOX = pygame.USEREVENT + 19
    EXIT_CHATBOX = pygame.USEREVENT + 20

    # States
    GAME_OVER = pygame.USEREVENT + 21
    GAME_WIN = pygame.USEREVENT + 24
    RESTART = pygame.USEREVENT + 25
    ROOM_CLEAR = pygame.USEREVENT + 22
    BOMB_EXPLOSION = pygame.USEREVENT + 23

    # Others
    SLICE_ISAAC = pygame.USEREVENT + 26


class Scenes(Enum):
    MAIN_MENU = 0
    START_ROOM = 1
    COMMON_ROOM = 2
    SHOP = 3
    TREASURE = 4
    SECRET = 5
    BLUEWOMB = 6
    CATACOMB = 7
    CHAT_BOX = 11
    GAMEWIN = 100
    GAMEOVER = 101


# Files
class ImportedImages:
    icon = "Src/icons/64x64.ico"
    empty_image = "Src/Textures/Empty.png"

    # Player
    playerImage = "Src/Textures/Play/Issac_sprite.png"
    tearImage = "Src/Textures/Play/Tear.png"
    tear_pop_Image = "data/textures/tears/tears_pop.png"
    BldtearImage = "Src/Textures/Play/Tear_002.png"
    heartImage = "Src/Textures/Play/Heart.png"
    BombImage = "Src/Textures/Play/bomb.png"
    ExplosionImage = "Src/Textures/Play/effect_029_explosion.png"

    # Rooms
    class RoomImages(Enum):
        START_ROOM = "Src/Textures/Map/start_000.png"
        COMMON_ROOM = "Src/Textures/Map/room_000.png"
        SHOP = "Src/Textures/Map/shop.png"
        TREASURE = "Src/Textures/Map/treasure.png"
        SECRET = "Src/Textures/Map/secret.png"
        BLUEWOMB = "Src/Textures/Map/bluewomb.png"
        CATACOMB = "Src/Textures/Map/catacomb.png"  # For Boss Room ?

    class OpenDoorImages(Enum):
        OPEN_WOOD_DOOR = "Src/Textures/Map/OpenWoodDoor.png"
        OPEN_SHOP_DOOR = "Src/Textures/Map/OpenShopDoor.png"
        OPEN_TREASURE_DOOR = "Src/Textures/Map/OpenTreasureDoor.png"
        OPEN_SECRET_DOOR = "Src/Textures/Map/OpenStoneDoor.png"
        OPEN_BLUEWOMB_DOOR = "Src/Textures/Map/OpenBlueWombDoor.png"
        OPEN_CATACOMB_DOOR = "Src/Textures/Map/OpenDevilDoor.png"

    class ClosedDoorImages(Enum):
        CLOSED_WOOD_DOOR = "Src/Textures/Map/ClosedWoodDoor.png"  # to common room
        CLOSED_SHOP_DOOR = "Src/Textures/Map/ClosedShopDoor.png"
        CLOSED_TREASURE_DOOR = "Src/Textures/Map/ClosedTreasureDoor.png"
        CLOSED_SECRET_DOOR = "Src/Textures/Map/ClosedStoneDoor.png"
        CLOSED_BLUEWOMB_DOOR = "Src/Textures/Map/ClosedBlueWombDoor.png"
        CLOSED_CATACOMB_DOOR = "Src/Textures/Map/ClosedDevilDoor.png"

    class ShitImages(Enum):
        TYPE_0 = "Src/Textures/Play/poops/poops (1).png"
        TYPE_1 = "Src/Textures/Play/poops/poops (2).png"
        TYPE_2 = "Src/Textures/Play/poops/poops (3).png"
        TYPE_3 = "Src/Textures/Play/poops/poops (4).png"
        TYPE_4 = "Src/Textures/Play/poops/poops (5).png"

    class BlockImage(Enum):
        Rock = "Data/Textures/Room/altars.png"

    class Web(Enum):
        Web = "Data/Textures/Room/web.png"

    class shop:
        lucky_1 = "Src/Textures/Play/slot_001_machine.png"
        lucky_2 = "Src/Textures/Play/slot_002_machine.png"
        lucky_3 = "Src/Textures/Play/slot_003_machine.png"
        lucky_4 = "Src/Textures/Play/slot_004_machine.png"
        price = "Src/Textures/Play/price.png"

    class UI:
        coin = "Src/Textures/Play/coin.png"
        attack = "Src/Textures/Play/collectibles_705_darkarts.png"
        Bomb = "Src/Textures/Play/pickup_016_bomb.png"

    # MainMenu
    BackGround = "Src/Textures/Title/Title1.png"
    StartButton = "Src/Textures/Title/Draw2.png"
    Options = "Src/Textures/Title/Options.png"
    Continues = "Src/Textures/Title/Continue.png"
    Draw = "Src/Textures/Title/Draw1.png"
    bossHealthBarIcon = "Src/Textures/Play/ui_bosshealthbar_full.png"

    # GAMEWIN
    ReplayButton = "Src/backselectwidget.png"
    deathPortraits = "Src/death portraits.png"

    # GameOver
    GameOver = "Src/gameover.png"

    # Enemies
    Fly = "data/textures/enemies/fly_ok.png"
    Fly_die = "data/textures/enemies/fly_rip.png"
    Fly_blood = "Src/Textures/enemies/fly_ne_ok.png"
    Boss = "Src/Textures/enemies/gurdy.png"
    bug = "Src/Textures/Play/monster_113_charger.png"
    blood = "Src/Textures/Play/effect_032_bloodstains_1.png"

    # Friendly_NPCs
    TrainerImage = "Src/Textures/Trainer.png"
    MerchantImage = "Src/Textures/Merchant.png"
    chatboxImage = "Src/Textures/Play/Issac_Loot.png"


class ImportedBGM:
    main_theme = "Src/sounds/main_theme.mp3"
    common_bgm = "Src/sounds/Sacrificial.mp3"
    walk = "data/sounds/squish1.mp3"
    shoot = "Src/sounds/pop1.wav"
    hurt = "data/sounds/isaac_hurt1.mp3"
    explosion = "data/sounds/explosion1.mp3"
    tear_impact = "data/sounds/tear_impact1.mp3"
    door_open = "data/sounds/door_open.wav"


# Settings
class BasicSettings:
    screenWidth = 1280
    screenHeight = 720

    # distance between screen frame and room frame
    marginWidth = 150
    marginHeight = 50

    roomWidth = screenWidth - marginWidth
    roomHeight = screenHeight - marginHeight

    caption = "The Binding of Issac"
    fps = 60
    Hardship_coefficient = 0


class UpdateEnemiesSettings:
    flyNumber = 5
    bossNumber = 1


class UISettings:
    class coin:
        x = 50
        y = 100
        MULTI = 2.5
        ALPHA = 256

    class heart:
        x = 50
        y = 30

    class attack:
        x = 40
        y = 150
        MULTI = 2.3
        ALPHA = 256

    class bomb:
        x = 30
        y = 200
        MULTI = 0.88
        ALPHA = 256

    class room_hint:
        x = 850
        y = 50
        MULTI = 1
        ALPHA = 256


class BossSettings:
    class health_bar:
        max = 100 + BasicSettings.Hardship_coefficient * 15
        width = 600
        height = 30
        x = 1280 / 2 - 600 / 2 + 50
        y = 50

    class Body:
        frame_rects = [(9, 17, 133, 116), (167, 20, 136, 113), (5, 168, 140, 109)]

    class attack:
        frame_rects = [
            (7, 344, 32, 28),
            (49, 345, 40, 33),
            (98, 344, 44, 29),
            (160, 342, 46, 29),
            (209, 344, 44, 28),
            (160, 342, 46, 29),
            (209, 344, 44, 28),
            (257, 345, 41, 27),
            (0, 0, 1, 1),
        ]


class HeartSettings:
    heartWidth = 48 * 3
    heartHeight = 48
    heart_frame_rects = [
        (0, 0, 74, 24),
        (0, 24, 74, 24),
        (0, 48, 74, 24),
        (0, 72, 74, 24),
        (0, 96, 74, 24),
        (0, 120, 74, 24),
        (0, 144, 74, 24),
    ]


class PlayerSettings:
    playerWidth = 65
    playerHeight = 90
    playerSpeed = 3
    PlayerAttackSpeed = 0.5
    PlayerHP = 6
    PlayerBuff = 0
    MULTI = 1.8
    head_frame_rects = [
        (4, 20, 29, 26),  # down
        (83, 21, 29, 26),  # right
        (243, 20, 29, 26),  # left
        (202, 21, 29, 26),  # up
    ]
    body_down_frame_rects = [
        (9, 75, 19, 14),
        (41, 75, 19, 14),
        (74, 75, 19, 14),
        (105, 75, 19, 14),
        (137, 75, 19, 14),
        (169, 75, 19, 14),
        (201, 75, 19, 14),
        (232, 75, 19, 14),
        (265, 75, 19, 14),
        (297, 75, 19, 14),
    ]
    body_left_frame_rects = [
        (9, 118, 19, 14),
        (41, 118, 19, 14),
        (74, 118, 19, 14),
        (105, 118, 19, 14),
        (137, 118, 19, 14),
        (169, 118, 19, 14),
        (201, 118, 19, 14),
        (232, 118, 19, 14),
        (265, 118, 19, 14),
        (297, 118, 19, 14),
    ]
    body_up_frame_rects = [
        (9, 405, 19, 14),
        (41, 405, 19, 14),
        (74, 405, 19, 14),
        (105, 405, 19, 14),
        (137, 405, 19, 14),
        (169, 405, 19, 14),
        (201, 405, 19, 14),
        (232, 405, 19, 14),
        (265, 405, 19, 14),
        (297, 405, 19, 14),
    ]
    body_right_frame_rects = [
        (9, 448, 19, 14),
        (41, 448, 19, 14),
        (74, 448, 19, 14),
        (105, 448, 19, 14),
        (137, 448, 19, 14),
        (169, 448, 19, 14),
        (201, 448, 19, 14),
        (232, 448, 19, 14),
        (265, 448, 19, 14),
        (297, 448, 19, 14),
    ]


class TearSettings:
    tearWidth = 100
    tearHeight = 100
    tearSpeed = 6
    tear_frame_rects = [
        (0, 0, 64, 64),
        (64, 0, 64, 64),
        (128, 0, 64, 64),
        (192, 0, 64, 64),
        (256, 0, 64, 64),
        (320, 0, 64, 64),
        (384, 0, 64, 64),
        (448, 0, 64, 64),
        (512, 0, 64, 64),
        (576, 0, 64, 64),
        (640, 0, 64, 64),
        (704, 0, 64, 64),
        (768, 0, 64, 64),
        (832, 0, 64, 64),
        (896, 0, 64, 64),
        (0, 64, 64, 64),
        (64, 64, 64, 64),
        (128, 64, 64, 64),
        (192, 64, 64, 64),
        (256, 64, 64, 64),
        (320, 64, 64, 64),
        (384, 64, 64, 64),
        (448, 64, 64, 64),
        (512, 64, 64, 64),
        (576, 64, 64, 64),
        (640, 64, 64, 64),
        (704, 64, 64, 64),
        (768, 64, 64, 64),
        (832, 64, 64, 64),
        (896, 64, 64, 64),
    ]


class BombSettings:
    bombWidth = 40
    bombHeight = 42
    bomb_frame_rects = [
        (0, 0, 40, 42),
        (40, 0, 40, 42),
        (80, 0, 40, 42),
    ]
    affect_radius = 100
    power = 3


class ExplosionSettings:
    explosionWidth = 96
    explosionHeight = 96
    explosion_frame_rects = []
    for i in range(4):
        for j in range(4):
            explosion_frame_rects.append((96 * j, 96 * i, 96, 96))


class ShopSettings:
    class price:
        MULTI = 1.5
        ALPHA = 256
        x = 0.5 * BasicSettings.screenWidth
        y = 0.5 * BasicSettings.screenHeight - 30

    class lucky:
        x = 0.5 * BasicSettings.screenWidth
        y = 0.5 * BasicSettings.screenHeight


class GameWinSettings:
    class death:
        x = 1280 * 0.2
        y = 5
        MULTI = 3.0

    class ReplayButton:
        x = 1280 * 0.5 + 350
        y = 720 * 0.6 + 30


class MainMenuSettings:
    class StartButton:
        x = 1280 * 0.5 + 20
        y = 720 * 0.6 + 30

    class Options:
        MULTI = 1.5
        ALPHA = 180
        x = 420
        y = 500

    class bossHealthBarIcon:
        MULTI = 2.5
        ALPHA = 180
        x = 1280 / 2 - 600 / 2 + 15
        y = 40

    class Continue:
        MULTI = 1.5
        ALPHA = 180
        x = 680
        y = 550

    class Bomb:
        MULTI = 3.0
        ALPHA = 100
        x = 900
        y = 200
        frames_duration = 125
        frame_rects = [
            (69, 127, 21, 30),
            (101, 127, 21, 30),
            (133, 127, 21, 30),
            (69, 63, 21, 30),
            (133, 0, 21, 30),
        ]

    class Draw:
        MULTI = 3.0
        ALPHA = 0
        x = 400
        y = 100
        frames_duration = 125
        frame_rects = [(0, 0, 165, 156), (160, 0, 154, 156)]


class EnemiesSettings:

    class blood:
        frames_rects = [
            (0, 0, 48, 32),
            (0, 32, 48, 32),
            (0, 64, 48, 32),
            (0, 96, 48, 32),
            (0, 128, 48, 32),
            (0, 160, 48, 32),
        ]

    class bug:
        HP = 3 + BasicSettings.Hardship_coefficient
        speed = 1 + BasicSettings.Hardship_coefficient // 2
        frames_rects_right_or_left = [
            (0, 0, 32, 32),
            (32, 0, 32, 32),
            (64, 0, 32, 32),
            (96, 0, 32, 32),
        ]
        frames_rects_up = [
            (0, 32, 32, 32),
            (32, 32, 32, 32),
            (64, 32, 32, 32),
            (96, 32, 32, 32),
        ]
        frames_rects_down = [
            (0, 64, 32, 32),
            (32, 64, 32, 32),
            (64, 64, 32, 32),
            (96, 64, 32, 32),
        ]
        frames_rects_run = [(0, 96, 32, 32), (32, 96, 32, 32), (64, 96, 32, 32)]

    class Fly:
        MULTI = 1.0
        ALPHA = 256
        x = random.randint(350, 550)
        y = random.randint(350, 550)
        frames_duration = 125
        frame_rects = [
            (7, 8, 42, 33),
            (71, 8, 42, 33),
            (134, 8, 42, 33),
            (197, 8, 42, 33),
        ]
        frame_rects_blood = [
            (0, 0, 40, 35),
            (41, 0, 30, 35),
            (72, 0, 40, 35),
            (112, 0, 30, 35),
        ]
        HP = 1 + BasicSettings.Hardship_coefficient // 2
        speed = [0.5, 0.8, 1, 1.2, 3, -0.5, -0.8, -1, -1.2, -3]
        frame_rects_die = [
            (0, 0, 64, 63),
            (64, 0, 64, 63),
            (128, 0, 64, 63),
            (192, 0, 64, 63),
            (0, 63, 64, 63),
            (64, 63, 64, 63),
            (128, 63, 64, 63),
            (192, 63, 64, 63),
            (0, 126, 64, 63),
            (64, 126, 64, 63),
            (128, 126, 64, 63),
        ]


class NPC_Original_messages:
    npc_message = [
        [
            {
                "role": "system",
                "content": (
                    "\nYou are a guardian for the castle. Your mission is to test whether the player is clever enough. "
                    "\nYou should ask the player three math questions."
                    "\nIf the player answers correctly for at least two of them, the player will get a reward. "
                    "\nOtherwise, the player will be punished. The first and second questions are very simple. "
                    "\nThe third one should be about calculus or linear algebra."
                    "\nBefore giving the reward, check whether the player's HP is 6, which is full."
                    "\nIf it's full, strengthen him to be able to use more powerful bullets."
                    "\nIf the player get the HP+2, print HEAL!!!."
                    "\nIf the player get the more powerful bullets, print MORE BULLETS!!!."
                    "\nIf the player get the punishment, print PUNISHMENT!!!."
                    f"\nCurrent Hardship coefficient is {BasicSettings.Hardship_coefficient}."
                    "\nBelow is the player's current state."
                ),
            }
        ],
        [
            {
                "role": "system",
                "content": (
                    "You are an evil demon merchant thirsty for gold and blood. You can sell at most 4 items to the player."
                    "\nDon't sell if the player can't afford."
                    "\nYou should judge what the player is eager to buy depending on his current state."
                    "\nYou have 3 healers, 3 ATK boosters, 3 tear boosters and 3 bombs"
                    "\nHealer heals 1 HP, ATK booster boosts 1 ATK, and tear booster shortens shoot delay by 25."
                    "\nEach healer costs 3 coins, each bomb costs 2 coins."
                    "\nEach ATK booster or tear booster costs 1 HP."
                    "\nTo the player, 6 HP is full, lowest ATK is 1, 5 ATK is very high, longest delay is 200, 150 delay is very short."
                    "\nEach time the player buys 1 healer, print HEAL!!!."
                    "\nEach time the player buys 1 ATK booster, print BATTLE!!!."
                    "\nEach time the player buys 1 tear booster, print FIERCE TEAR!!!."
                    "\nEach time the player buys 1 bomb, print BOMB!!!."
                    f"\nCurrent Hardship coefficient is {BasicSettings.Hardship_coefficient}."
                    "\nBelow is the player's current state."
                ),
            }
        ],
    ]


class StaticMethods:

    @staticmethod
    def get_images(sheet, x, y, width, height, colorkey, scale):
        image = pygame.Surface((width, height))
        image.blit(sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(colorkey)
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        return image

    @staticmethod
    def get_direction_vector(sprite1, x, y):
        """
        获取一个sprite实例相对另一个sprite实例的方向向量(单位向量形式)

        参数:
        sprite1 (pygame.sprite.Sprite): 第一个精灵实例
        sprite2 (pygame.sprite.Sprite): 第二个精灵实例

        返回:
        tuple: 包含x方向和y方向分量的方向向量(单位向量)，例如 (dx, dy)
        """
        # 获取两个精灵中心的x坐标差值
        dx = x - sprite1.rect.centerx
        # 获取两个精灵中心的y坐标差值
        dy = y - sprite1.rect.centery
        # 计算两个精灵之间的距离
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:  # 避免除0错误，当两个精灵重合时距离为0
            # 将坐标差值转换为单位向量，即向量的长度归一化为1
            dx /= distance
            dy /= distance
        return dx, dy

    # Custom spritecollide using mask collision
    @staticmethod
    def mask_spritecollide(
        sprite: pygame.sprite.Sprite, group: pygame.sprite.Group, dokill: bool
    ) -> list:
        collided_sprites = []

        # Get the mask and rect for the main sprite
        mask1 = pygame.mask.from_surface(sprite.image)
        rect1 = sprite.rect

        for group_sprite in group:
            # Get the mask and rect for the group sprite
            mask2 = pygame.mask.from_surface(group_sprite.image)
            rect2 = group_sprite.rect

            # Calculate the offset for collision checking
            offset = (rect2.x - rect1.x, rect2.y - rect1.y)

            # Check for a pixel-perfect collision using masks
            if mask1.overlap(mask2, offset):
                collided_sprites.append(group_sprite)

                if dokill:
                    group.remove(group_sprite)

        return collided_sprites

    @staticmethod
    def mask_groupcollide(
        group1: pygame.sprite.Group,
        group2: pygame.sprite.Group,
        dokill1: bool,
        dokill2: bool,
    ) -> dict:
        collided = {}

        for sprite1 in group1:
            mask1 = pygame.mask.from_surface(sprite1.image)
            rect1 = sprite1.rect

            for sprite2 in group2:
                mask2 = pygame.mask.from_surface(sprite2.image)
                rect2 = sprite2.rect

                offset = (rect2.x - rect1.x, rect2.y - rect1.y)

                if mask1.overlap(mask2, offset):
                    if sprite1 not in collided:
                        collided[sprite1] = []
                    collided[sprite1].append(sprite2)

                    if dokill1:
                        group1.remove(sprite1)
                    if dokill2:
                        group2.remove(sprite2)

        return collided

    sound_played = False
    timer = 0

    @staticmethod
    def play_sound_effect_once_with_interval(
        bgm_player, sound_effect: str, interval: int
    ):
        if not StaticMethods.sound_played:
            bgm_player.play_sound_effect(sound_effect)
            StaticMethods.sound_played = True
            StaticMethods.timer = pygame.time.get_ticks()
        if pygame.time.get_ticks() - StaticMethods.timer > interval:
            StaticMethods.sound_played = False
