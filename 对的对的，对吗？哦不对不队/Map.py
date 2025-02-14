import pygame
from Settings import *
from LevelMap import *
from random import randint

# 静态场景：Block
class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Machine(Block):
    def __init__(self, image, x, y, dis, dir: str):
        self.image = image[dir]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.tarDis = dis
        self.dir = dir
        self.on = False
        self.returning = False
        self.velocity = 5
        self.moveDis = 0
        self.stayTime = 3
        self.stayTick = 30 * self.stayTime
        
    def update(self, player):
        if self.moveDis == self.tarDis:
            self.on = False
            self.stayTick -= 1
        if self.stayTick <= 0:
            self.on = False
            self.returning = True
        if self.moveDis == 0:
            self.stayTick = 30 * self.stayTime
            self.returning = False
        
        self.move()

    def move(self):
        if self.returning:
            self.moveDis -= self.velocity * 2
            if self.dir == "UP": self.rect = self.rect.move(0, self.velocity * 2)
            if self.dir == "DOWN": self.rect = self.rect.move(0, self.velocity * -2)
            if self.dir == "LEFT": self.rect = self.rect.move(self.velocity * 2, 0)
            if self.dir == "RIGHT": self.rect = self.rect.move(self.velocity * -2, 0)
        if self.on:
            self.moveDis += self.velocity
            if self.dir == "UP": self.rect = self.rect.move(0, -self.velocity)
            if self.dir == "DOWN": self.rect = self.rect.move(0, self.velocit)
            if self.dir == "LEFT": self.rect = self.rect.move(-self.velocity, 0)
            if self.dir == "RIGHT": self.rect = self.rect.move(self.velocity, 0)
                
    def Work(self, player):
        if self.moveDis == 0: self.on = True
        player.rect.bottom = self.rect.top
        if self.on:
            if self.dir == "LEFT": player.rect = player.rect.move(-self.velocity, 0)
            if self.dir == "RIGHT": player.rect = player.rect.move(self.velocity, 0)
        if self.returning:
            if self.dir == "LEFT": player.rect = player.rect.move(2 * self.velocity, 0)
            if self.dir == "RIGHT": player.rect = player.rect.move(-2 * self.velocity, 0)

class Trap(Block):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

class NPC(Block):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.awake = False
        self.uiImage = Images.npcTalk
        self.uiRect = self.uiImage.get_rect()
        self.uiRect.topleft = (x + 25, y - 30)


    def update(self):
        self.rect = self.image.get_rect()

class Portal(Block):
    def __init__(self, image, x, y, name):
        super().__init__(image, x, y)
        self.sceneName = name
    
    def update(self, player):
        if self.rect.colliderect(player.rect):
            if self.sceneName == "Origin":
                pygame.event.post(pygame.event.Event(GameEvent.PLAYER_GOTO_LEVEL_1))
            if self.sceneName == "Level_1":
                pygame.event.post(pygame.event.Event(GameEvent.PLAYER_GOTO_LEVEL_2))
            if self.sceneName == "Level_2":
                pygame.event.post(pygame.event.Event(GameEvent.PLAYER_GOTO_LEVEL_3))
            if self.sceneName == "Level_3":
                pygame.event.post(pygame.event.Event(GameEvent.PLAYER_VICTORY))

#有动画的场景：Anim
class Anim(pygame.sprite.Sprite):
    def __init__(self, images:list, x, y):
        self.images = images
        self.animTimer = 0
        self.animIndex = 0
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.cord = (x, y)
        self.animationTime = 6

    def update(self):
        self.image = self.images[self.animIndex]
        self.rect.topleft = self.cord
        self.animTimer += 1
        if self.animTimer >= self.animationTime:
            self.animIndex += 1
            self.animTimer = 0
        if self.animIndex >= len(self.images): self.Reset()

    def Reset(self):
        self.animIndex = 0
        self.animTimer = 0

class Coin(Anim):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)
        self.value = 4
        self.isGot = False

    def update(self):
        super().update()

class Enemy(Anim):
    def __init__(self, image, x, y, actDis: int):
        super().__init__(image, x, y)
        self.actDis = actDis
        self.moveDis = 0
        self.isDead = False
        #move info
        self.velocity = 5
        self.facingRight = True
        self.facingDir = 1
    
    def update(self):
        super().update()
        if self.actDis == 0:
            self.image = Images.enemy[1]
            return
        self.image = pygame.transform.flip( self.image, self.facingRight, False )
        if ( self.moveDis == 0 and not self.facingRight ) or ( self.moveDis == self.actDis and self.facingRight ): self.flip()
        else: self.move()

    def flip(self):
        self.facingRight = not self.facingRight
        self.facingDir = -self.facingDir    
    
    def move(self):
        self.cord = ( self.cord[0] + self.velocity * self.facingDir, self.cord[1] )
        self.moveDis += self.velocity * self.facingDir

class Bullet(Anim):
    def __init__(self, image, x, y, dir):
        super().__init__(image, x, y)
        self.moveDis = 0
        self.lifeDis = 600
        self.animationTime = 2
        #move info
        self.velocity = 15
        self.dir = dir
        if dir == 1: self.facingRight = True
        else: self.facingRight = False
    
    def update(self, scene):
        super().update()
        self.image = pygame.transform.flip( self.image, self.facingRight, False )
        self.cord = ( self.cord[0] + self.dir * self.velocity, self.cord[1] )
        self.moveDis += self.velocity
        #子弹的删除逻辑
        #子弹到达最大飞行距离
        if self.moveDis >= self.lifeDis:
            scene.bullets.remove(self)
            return
        #子弹撞到障碍物
        for obstacle in scene.obstacles:
            if obstacle.rect.colliderect(self.rect):
                scene.bullets.remove(self)
                return
        #子弹打到怪物
        for enemy in scene.enemies:
            if enemy.rect.colliderect(self.rect):
                scene.enemies.remove(enemy)

def scene_map():

    return RandomMap.mapObj

def scene_walls():
    obstacles = []

    for i in range(2 * WindowSettings.width // 40 + 1):
        obstacles.append(Block(Images.wall, SceneSettings.tileWidth * i, 760))
    
    for i in range(WindowSettings.width // 40 + 1, 2 * WindowSettings.width // 40 + 1):
        obstacles.append(Block(Images.wall, SceneSettings.tileWidth * i, 640))
    
    for i in range(2 * WindowSettings.height // 40 + 1):
        obstacles.append(Block(Images.wall, 1640, SceneSettings.tileWidth * i))

    return obstacles

def scene_machines():
    machines = []

    machines.append(Machine(Images.machine, 400, 720, 400, "UP"))

    return machines

def scene_coins():
    coins = []
    coinsGot = []

    coins.append(Coin(Images.coin, 1000, 720))
    coins.append(Coin(Images.coin, 400, 160))
    coinsGot.append(True)

    return coins

def scene_enemies():
    enemies = []

    enemies.append(Enemy(Images.enemy, 1040, 600, 560))

    return enemies

def scene_portals():
    portals = []

    portals.append(Portal(Images.portal, 1520, 520, "Origin"))

    return portals

def level_1_walls():
    walls = []
    for cord in level_1.Walls:
        walls.append(Block(Images.wall, cord[0] * 40, cord[1] * 40))
    return walls

def level_1_traps():
    traps = []
    for cord in level_1.Traps:
        traps.append(Trap(Images.trap, cord[0] * 40, cord[1] * 40 + 15))
    return traps

def level_1_machines():
    machines = []
    machines.append(Machine(Images.machine, 22 * SceneSettings.tileWidth, 15 * SceneSettings.tileHeight, 480, "LEFT"))
    return machines

def level_1_coins():
    coins = []
    coinsGot = []
    for cord in level_1.Coins:
        coins.append(Coin(Images.coin, SceneSettings.tileWidth * cord[0], SceneSettings.tileHeight * cord[1]))
    coinsGot.append(True)
    return coins

def level_1_portals():
    portals = []

    portals.append(Portal(Images.portal, 69 * SceneSettings.tileWidth, 3 * SceneSettings.tileHeight, "Level_1"))

    return portals

def level_2_walls():
    walls = []
    for cord in level_2.Walls:
        walls.append(Block(Images.wall, cord[0] * 40, cord[1] * 40))
    return walls

def level_2_traps():
    traps = []
    for cord in level_2.Traps:
        traps.append(Trap(Images.trap, cord[0] * 40, cord[1] * 40 + 15))
    return traps

def level_2_enemies():
    enemies = []
    enemies.append(Enemy(Images.enemy, 40 * SceneSettings.tileWidth, 30 * SceneSettings.tileHeight, 320))
    enemies.append(Enemy(Images.enemy, 40 * SceneSettings.tileWidth, 27 * SceneSettings.tileHeight, 80))
    enemies.append(Enemy(Images.enemy, 28 * SceneSettings.tileWidth, 26 * SceneSettings.tileHeight, 240))
    enemies.append(Enemy(Images.enemy, 25 * SceneSettings.tileWidth, 23 * SceneSettings.tileHeight, 200))
    enemies.append(Enemy(Images.enemy, 28 * SceneSettings.tileWidth, 20 * SceneSettings.tileHeight, 240))
    return enemies

def level_2_machines():
    machines = []
    machines.append(Machine(Images.machine, 7 * SceneSettings.tileWidth, 10 * SceneSettings.tileHeight, 280, "UP"))
    machines.append(Machine(Images.machine, 73 * SceneSettings.tileWidth, 17 * SceneSettings.tileHeight, 120, "UP"))
    machines.append(Machine(Images.machine, 78 * SceneSettings.tileWidth, 34 * SceneSettings.tileWidth, 400, "LEFT"))
    machines.append(Machine(Images.machine, 88 * SceneSettings.tileWidth, 30 * SceneSettings.tileHeight, 920, "UP"))
    return machines

def level_2_coins():
    coins = []
    coinsGot = []
    for cord in level_2.Coins:
        coins.append(Coin(Images.coin, SceneSettings.tileWidth * cord[0], SceneSettings.tileHeight * cord[1]))
    coinsGot.append(True)

    return coins

def level_2_NPCs():
    NPCs = []
    NPCs.append(NPC(Images.npc, 82 * SceneSettings.tileWidth, 3 * SceneSettings.tileHeight))
    return NPCs

def level_2_portals():
    portals = []

    portals.append(Portal(Images.portal, 14 * SceneSettings.tileWidth, 17 * SceneSettings.tileHeight, "Level_2"))

    return portals

def level_3_walls():
    walls = []
    for cord in level_3.Walls:
        walls.append(Block(Images.wall, cord[0] * 40, cord[1] * 40))
    return walls

def level_3_traps():
    traps = []
    for cord in level_3.Traps:
        traps.append(Trap(Images.trap, cord[0] * 40, cord[1] * 40 + 15))
    return traps

def level_3_enemies():
    enemies = []
    enemies.append(Enemy(Images.enemy, 4 * SceneSettings.tileWidth, 8 * SceneSettings.tileHeight, 160))
    enemies.append(Enemy(Images.enemy, 4 * SceneSettings.tileWidth, 11 * SceneSettings.tileHeight, 160))
    for cord in level_3.E:
        enemies.append(Enemy(Images.enemy, cord[0] * SceneSettings.tileWidth, cord[1] * SceneSettings.tileHeight, 0))
    return enemies

def level_3_machines():
    machines = []
    machines.append(Machine(Images.machine, 68 * SceneSettings.tileWidth, 13 * SceneSettings.tileHeight, 800, "RIGHT"))
    machines.append(Machine(Images.machine, 90 * SceneSettings.tileWidth, 13 * SceneSettings.tileHeight, 200, "UP"))
    return machines

def level_3_portals():
    portals = []

    portals.append(Portal(Images.portal, 95 * SceneSettings.tileWidth, 3 * SceneSettings.tileHeight, "Level_3"))

    return portals