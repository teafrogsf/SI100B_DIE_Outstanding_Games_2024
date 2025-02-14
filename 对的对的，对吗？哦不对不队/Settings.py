import pygame
import random
from enum import Enum

class PlayerSettings:
    width = 48
    height = 54
    animationTime = 6

class NPCSettings:
    width = 80
    height = 80

class WindowSettings:
    width = 1000
    height = 800

class GameState(Enum):
    MAIN_MENU = 1
    GAME_PLAY_ORIGIN = 2
    GAME_PLAY_LEVEL_1 = 3
    GAME_PLAY_LEVEL_2 = 4
    GAME_PLAY_LEVEL_3 = 5
    GAME_PLAY_PAUSE = 6
    GAME_PLAY_DEAD = 7
    VICTORY = 8
    GAME_PLAY_SHOP = 9

class GameEvent:
    EVENT_PLAYER_DEAD = pygame.USEREVENT + 1
    EVENT_QUIT_SHOP = pygame.USEREVENT + 2
    PLAYER_GOTO_LEVEL_1 = pygame.USEREVENT + 3
    PLAYER_GOTO_LEVEL_2 = pygame.USEREVENT + 4
    PLAYER_GOTO_LEVEL_3 = pygame.USEREVENT + 5
    PLAYER_VICTORY = pygame.USEREVENT + 6

class SceneSettings:
    tileWidth = tileHeight = 40

    scene_tileXnum = 120
    scene_tileYnum = 120
    sceneWidth = scene_tileXnum * tileWidth
    sceneHeight = scene_tileYnum * tileHeight


class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxAlpha = 150
    boxStartX = WindowSettings.width // 4           # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20 # Coordinate Y of the box

    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 + 10         # Coordinate X of the first line of dialog
    textStartY = WindowSettings.height // 3 * 2 + 30    # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3                # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20

    flashCD = 15

class PosSettings:
    originX = 0
    originY = 16 * 40

    level_1_X = 10 * 40
    level_1_Y = 3 * 40

    level_2_X = 3 * 40
    level_2_Y = 10 * 40

    level_3_X = 4 * 40
    level_3_Y = 4 * 40

class Images:
    wall = pygame.transform.scale( pygame.image.load(r".\assets_library\tiles\12.jpg"), (40, 40) )
    trap = pygame.transform.scale( pygame.image.load(r".\assets_library\Trap.png"), (40, 25) )
    machine = {
        "UP": pygame.transform.scale( pygame.image.load(r".\assets_library\tiles\Machine-UP.jpg"), (40, 40) ),
        "DOWN": pygame.transform.scale( pygame.image.load(r".\assets_library\tiles\Machine-DOWN.jpg"), (40, 40) ),
        "LEFT": pygame.transform.scale( pygame.image.load(r".\assets_library\tiles\Machine-LEFT.jpg"), (40, 40) ),
        "RIGHT": pygame.transform.scale( pygame.image.load(r".\assets_library\tiles\Machine-RIGHT.jpg"), (40, 40) )
    }
    coin = [pygame.transform.scale( pygame.image.load(rf".\assets_library\Coins\Gold-{i}.png") , (40, 40) ) for i in range(1,5)]
    enemy = [pygame.transform.scale( pygame.image.load(rf".\assets_library\Enemy\Enemy-{i}.png") , (40, 40) ) for i in range(1,5)]
    npc = pygame.transform.scale( pygame.image.load(r".\assets_library\characters\NPC商人.png") , (NPCSettings.width, NPCSettings.height) )
    npcTalk = pygame.transform.scale( pygame.image.load(r".\assets_library\特殊符号\test.png") , (30, 30) )
    bullet = [pygame.transform.scale( pygame.image.load(rf".\assets_library\子弹\子弹{i}.png") , (40, 30) ) for i in range(1,5)]
    portal = pygame.transform.scale( pygame.image.load(r".\assets_library\objects\传送门.png") , (120, 120) )



class CoinNum:
    Origin = 2
    Level_1 = 32
    Level_2 = 28

class RandomMap:
    images = [ pygame.transform.scale( pygame.image.load(rf".\assets_library\tiles\{type}.jpg"), (40, 40), ) for type in range(1,7) ]
    images = [pygame.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    mapObj = []
    for i in range(SceneSettings.scene_tileXnum):
        tmp = []
        for j in range(SceneSettings.scene_tileYnum):
            tmp.append(images[random.randint(0, len(images) - 1)])
        mapObj.append(tmp)