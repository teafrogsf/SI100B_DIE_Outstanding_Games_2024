import pygame, ChatBox
from GenMap import GenMap
from GameSettings import *
from Utility import Scene
from Npc import Npc


class MapPage(Scene):

    def __init__(self, player, id):
        self.maper = GenMap(id)
        self.player = player
        self.SetMap(id)
        self.mapid = id
        self.SetMove()
        self.SetNpc(id)

    # 设置地图
    def SetMap(self, id):
        self.edgeDist = MoveSettings.edgeDist
        self.mapWidth = WindowSettings.width
        self.mapHeight = WindowSettings.height
        self.blockSize = MoveSettings.blockSize
        self.background = pygame.image.load(
            r".\assets\map\background" + str(id) + ".png"
        )
        self.background = pygame.transform.scale(
            self.background, (self.mapWidth, self.mapHeight)
        )
        self.imgMap = [
            [None for j in range(self.maper.col)] for i in range(self.maper.row)
        ]

        self.IsEntity = [
            [None for j in range(self.maper.col)] for i in range(self.maper.row)
        ]

        self.Chestava = [
            [False for j in range(self.maper.col)] for i in range(self.maper.row)
        ]

        self.numMap = self.maper.Map[id]
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if (
                    (self.numMap[i][j] == 1)
                    or (self.numMap[i][j] == 3)
                    or (self.numMap[i][j] == 8)
                ):
                    self.IsEntity[i][j] = True
                else:
                    self.IsEntity[i][j] = False
                    if self.numMap[i][j] == 2:
                        self.Chestava[i][j] = True

        self.mapRect = [
            [None for j in range(self.maper.col)] for i in range(self.maper.row)
        ]

        blocks = [
            r".\assets\map\air.png",
            r".\assets\map\road.png",
            r".\assets\map\chest.png",
            r".\assets\map\trap.png",
            r".\assets\map\benchL.png",
            r".\assets\map\benchR.png",
            r".\assets\map\benchbackL.png",
            r".\assets\map\benchbackR.png",
            r".\assets\map\airwall.png",
        ]
        self.mapDelta = 0  # 地图移动距离
        self.ChestMoney = self.maper.ChestMoney[id]
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                self.imgMap[i][j] = pygame.image.load(blocks[self.numMap[i][j]])
                self.imgMap[i][j] = pygame.transform.scale(
                    self.imgMap[i][j], (self.blockSize, self.blockSize)
                )
                # window.blit(self.imgMap[i][j], (j * self.blockSize, i * self.blockSize))
                self.mapRect[i][j] = self.imgMap[i][j].get_rect()
                self.mapRect[i][j].x = j * self.blockSize
                self.mapRect[i][j].y = i * self.blockSize

    # 刷新 Npc
    def freshnpc(self, id):
        if id == 0:
            if self.isdead[0]:
                for i in range(len(self.npcs)):
                    if self.npcs[i].name == "Enemy5":
                        self.npcs.pop(i)
                        break
            if self.isdead[1]:
                for i in range(len(self.npcs)):
                    if self.npcs[i].name == "Enemy0":
                        self.npcs.pop(i)
                        break

        if id == 1:
            if self.isdead[0]:
                for i in range(len(self.npcs)):
                    if self.npcs[i].name == "Enemy1":
                        self.npcs.pop(i)
                        break
            if self.isdead[1]:
                for i in range(len(self.npcs)):
                    if self.npcs[i].name == "Enemy6":
                        self.npcs.pop(i)
                        break
            if self.isdead[2]:
                for i in range(len(self.npcs)):
                    if self.npcs[i].name == "Enemy2":
                        self.npcs.pop(i)
                        break

        if id == 2:
            if self.isdead[0]:
                for i in range(len(self.npcs)):
                    if self.npcs[i].name == "Enemy3":
                        self.npcs.pop(i)
                        break

        if id == 3:
            if self.isdead[0]:
                for i in range(len(self.npcs)):
                    if self.npcs[i].name == "Boss":
                        self.npcs.pop(i)
                        break

    # 还原地图
    def reborn(self, id):
        blocks = [
            r".\assets\map\air.png",
            r".\assets\map\road.png",
            r".\assets\map\chest.png",
            r".\assets\map\trap.png",
            r".\assets\map\benchL.png",
            r".\assets\map\benchR.png",
            r".\assets\map\benchbackL.png",
            r".\assets\map\benchbackR.png",
            r".\assets\map\airwall.png",
        ]
        self.mapDelta = 0  # 地图移动距离
        self.ChestMoney = self.maper.ChestMoney[id]
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if (self.numMap[i][j] == 2) and (self.Chestava[i][j] == False):
                    self.imgMap[i][j] = pygame.image.load(
                        r".\assets\map\openedchest.png"
                    )
                    self.imgMap[i][j] = pygame.transform.scale(
                        self.imgMap[i][j], (self.blockSize, self.blockSize * 1.289)
                    )
                else:
                    self.imgMap[i][j] = pygame.image.load(blocks[self.numMap[i][j]])
                    self.imgMap[i][j] = pygame.transform.scale(
                        self.imgMap[i][j], (self.blockSize, self.blockSize)
                    )
                # window.blit(self.imgMap[i][j], (j * self.blockSize, i * self.blockSize))
                self.mapRect[i][j] = self.imgMap[i][j].get_rect()
                self.mapRect[i][j].x = j * self.blockSize
                self.mapRect[i][j].y = i * self.blockSize
        # 还原人物
        self.jumpTime = self.fallTime = self.lastDeltaY = self.deltaY = 0
        self.falling = False
        self.player.isDashing = False
        self.player.onJump = False
        self.Dashavailable = True  # 冲刺是否可用
        self.dashTimer = 0  # 用于记录冲刺时间
        self.player.Rect.x = self.player.Rect.y = 0  # 还原坐标，从屏幕左上角降落

        self.npcs = []

        if id == 0:
            if not self.isdead[0]:
                Enemy5 = Npc(
                    "Enemy5",
                    r".\assets\npc\enemy - 1.png",
                    width=56,
                    height=111,
                    posX=14 * MoveSettings.blockSize,
                    posY=self.mapHeight - self.blockSize - 111,
                )
                self.npcs.append(Enemy5)
            if not self.isdead[1]:
                Enemy0 = Npc(
                    "Enemy0",
                    r".\assets\npc\enemy - 0.png",
                    width=93,
                    height=108,
                    posX=6 * MoveSettings.blockSize,
                    posY=self.mapHeight - self.blockSize - 108,
                )
                self.npcs.append(Enemy0)

        if id == 1:
            Cornifer = Npc(
                "Cornifer",
                r".\assets\npc\Cornifer.png",
                width=200,
                height=100,
                posX=0,
                posY=self.mapHeight - self.blockSize - 100,
            )
            self.npcs.append(Cornifer)
            if not self.isdead[0]:
                Enemy1 = Npc(
                    "Enemy1",
                    r".\assets\npc\enemy - 1.png",
                    width=56,
                    height=111,
                    posX=14 * MoveSettings.blockSize,
                    posY=self.mapHeight - self.blockSize - 111,
                )
                self.npcs.append(Enemy1)
            if not self.isdead[1]:
                Enemy6 = Npc(
                    "Enemy6",
                    r".\assets\npc\enemy - 1.png",
                    width=56,
                    height=111,
                    posX=20 * MoveSettings.blockSize,
                    posY=self.mapHeight - self.blockSize - 111,
                )
                self.npcs.append(Enemy6)
            if not self.isdead[2]:
                Enemy2 = Npc(
                    "Enemy2",
                    r".\assets\npc\enemy - 2.png",
                    width=153,
                    height=170,
                    posX=52 * MoveSettings.blockSize,
                    posY=self.mapHeight - self.blockSize * 8 - 170,
                )
                self.npcs.append(Enemy2)

        if id == 2:
            Seer = Npc(
                "Seer",
                r".\assets\npc\Seer.png",
                width=90,
                height=90,
                posX=50 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 90,
            )
            self.npcs.append(Seer)
            if not self.isdead[0]:
                Enemy3 = Npc(
                    "Enemy3",
                    r".\assets\npc\enemy - 1.png",
                    width=56,
                    height=111,
                    posX=9 * MoveSettings.blockSize,
                    posY=self.mapHeight - self.blockSize - 111,
                )
                self.npcs.append(Enemy3)

        if id == 3:
            if not self.isdead[0]:
                Boss = Npc(
                    "Boss",
                    r".\assets\npc\boss.png",
                    width=384,
                    height=408,
                    posX=30 * MoveSettings.blockSize,
                    posY=self.mapHeight - self.blockSize - 408,
                )
                self.npcs.append(Boss)

    # 设置移动
    def SetMove(self):
        self.gravity = MoveSettings.gravity
        self.initialSpeed = MoveSettings.initialSpeed
        self.jumpTime = self.fallTime = self.lastDeltaY = self.deltaY = 0
        self.falling = False
        self.player.isDashing = False
        self.player.onJump = False
        self.Dashavailable = True  # 冲刺是否可用
        self.dashTimer = 0  # 用于记录冲刺时间

    # 设置 NPC
    def SetNpc(self, id):
        self.npcs = []
        self.isdead = []
        if id == 0:
            self.enemyNum = 2
            self.isdead = [False for i in range(self.enemyNum)]
            Enemy5 = Npc(
                "Enemy5",
                r".\assets\npc\enemy - 1.png",
                width=56,
                height=111,
                posX=14 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 111,
            )
            self.npcs.append(Enemy5)

            Enemy0 = Npc(
                "Enemy0",
                r".\assets\npc\enemy - 0.png",
                width=93,
                height=108,
                posX=6 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 108,
            )
            self.npcs.append(Enemy0)

        if id == 1:
            self.enemyNum = 3
            self.isdead = [False for i in range(self.enemyNum)]

            Cornifer = Npc(
                "Cornifer",
                r".\assets\npc\Cornifer.png",
                width=200,
                height=100,
                posX=0,
                posY=self.mapHeight - self.blockSize - 100,
            )
            self.npcs.append(Cornifer)
            Enemy1 = Npc(
                "Enemy1",
                r".\assets\npc\enemy - 1.png",
                width=56,
                height=111,
                posX=14 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 111,
            )
            Enemy6 = Npc(
                "Enemy6",
                r".\assets\npc\enemy - 1.png",
                width=56,
                height=111,
                posX=20 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 111,
            )
            Enemy2 = Npc(
                "Enemy2",
                r".\assets\npc\enemy - 2.png",
                width=153,
                height=170,
                posX=52 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize * 8 - 170,
            )
            self.npcs.append(Enemy1)
            self.npcs.append(Enemy6)
            self.npcs.append(Enemy2)

        if id == 2:
            self.enemyNum = 1
            self.isdead = [False for i in range(self.enemyNum)]
            Seer = Npc(
                "Seer",
                r".\assets\npc\Seer.png",
                width=90,
                height=90,
                posX=50 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 90,
            )
            self.npcs.append(Seer)
            Enemy3 = Npc(
                "Enemy3",
                r".\assets\npc\enemy - 1.png",
                width=56,
                height=111,
                posX=9 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 111,
            )
            self.npcs.append(Enemy3)

        if id == 3:
            self.enemyNum = 1
            self.isdead = [False for i in range(self.enemyNum)]
            Boss = Npc(
                "Boss",
                r".\assets\npc\boss.png",
                width=384,
                height=408,
                posX=30 * MoveSettings.blockSize,
                posY=self.mapHeight - self.blockSize - 408,
            )
            self.npcs.append(Boss)

    # 显示
    def show(self, window):
        window.blit(self.background, (0, 0))
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                # 特殊处理打开的箱子
                if (self.numMap[i][j] == 2) and (self.Chestava[i][j] == False):
                    window.blit(
                        self.imgMap[i][j],
                        (
                            self.mapRect[i][j].x,
                            self.mapRect[i][j].y - 0.289 * self.blockSize,
                        ),
                    )
                else:
                    window.blit(self.imgMap[i][j], self.mapRect[i][j])
        for npc in self.npcs:
            window.blit(npc.image, npc.imageRect)
            # print('blit npc', npc.name, 'at', npc.imageRect.x, npc.imageRect.y)
        self.player.show(window)

    def handle(self, event):
        # bad code
        # keys = pygame.key.get_pressed()
        # if (keys[pygame.K_a]) or (keys[pygame.K_d]) or (keys[pygame.K_w]):
        #     self.move()
        #     return None
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
            return "EnterMenufromMap"

        # 判断是否进入商店
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_b):
            for npc in self.npcs:
                if (self.player.Rect.colliderect(npc.imageRect)) and (
                    npc.name == "Cornifer"
                ):
                    return "EnterShop"

        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_e):
            # 判断是否进入对话
            if (self.touchDown()) and (not self.player.isDashing):
                for npc in self.npcs:
                    if (self.player.Rect.colliderect(npc.imageRect)) and (
                        npc.name == "Seer"
                    ):
                        return ("EnterChat", npc.name)
                    elif (self.player.Rect.colliderect(npc.imageRect)) and (
                        npc.name == "Cornifer"
                    ):
                        return ("EnterChat", npc.name)

            # 判断接触宝箱
            for i in range(self.maper.row):
                for j in range(self.maper.col):
                    if (
                        self.numMap[i][j] == 2
                        and self.Chestava[i][j] == True
                        and self.player.Rect.colliderect(self.mapRect[i][j])
                    ):
                        print("You opened the chest.")
                        self.player.money += self.ChestMoney[i][j]
                        self.Chestava[i][j] = False
                        self.imgMap[i][j] = pygame.image.load(
                            r".\assets\map\openedchest.png"
                        )
                        self.imgMap[i][j] = pygame.transform.scale(
                            self.imgMap[i][j], (self.blockSize, self.blockSize * 1.289)
                        )

            # 判断是否触发战斗
            if (self.touchDown()) and (not self.player.isDashing):
                for npc in self.npcs:
                    if (
                        (self.player.Rect.colliderect(npc.imageRect))
                        and (npc.name == "Enemy1")
                        and (not self.isdead[0])
                        and (self.mapid == 1)
                    ):
                        return ("EnterBattle", npc.name)
                    if (
                        (self.player.Rect.colliderect(npc.imageRect))
                        and (npc.name == "Enemy6")
                        and (not self.isdead[1])
                        and (self.mapid == 1)
                    ):
                        return ("EnterBattle", npc.name)
                    if (
                        (self.player.Rect.colliderect(npc.imageRect))
                        and (npc.name == "Enemy2")
                        and (not self.isdead[2])
                        and (self.mapid == 1)
                    ):
                        return ("EnterBattle", npc.name)
                    if (
                        (self.player.Rect.colliderect(npc.imageRect))
                        and (npc.name == "Enemy3")
                        and (not self.isdead[0])
                        and (self.mapid == 2)
                    ):
                        return ("EnterBattle", npc.name)
                    if (
                        (self.player.Rect.colliderect(npc.imageRect))
                        and (npc.name == "Boss")
                        and (not self.isdead[0])
                        and (self.mapid == 3)
                    ):
                        return ("EnterBattle", npc.name)
                    if (
                        (self.player.Rect.colliderect(npc.imageRect))
                        and (npc.name == "Enemy5")
                        and (not self.isdead[0])
                        and (self.mapid == 0)
                    ):
                        return ("EnterBattle", npc.name)
                    if (
                        (self.player.Rect.colliderect(npc.imageRect))
                        and (npc.name == "Enemy0")
                        and (not self.isdead[1])
                        and (self.mapid == 0)
                    ):
                        return ("EnterBattle", npc.name)

            # 判断是否进入传送门
            if (self.touchDown()) and (not self.player.isDashing):
                for i in range(self.maper.row):
                    for j in range(self.maper.col):
                        if (
                            (self.numMap[i][j] > 3)
                            and (self.numMap[i][j] < 8)
                            and (self.player.Rect.colliderect(self.mapRect[i][j]))
                        ):
                            return ("EnterTeleport", self.numMap[i][j])
        return None

    def move(self):
        keys = pygame.key.get_pressed()
        if self.touchDown():
            self.Dashavailable = True

        if self.player.isDashing:
            if self.player.facing == "left":
                self.tryMoveX(-self.player.dashSpeed)
            else:
                self.tryMoveX(self.player.dashSpeed)
        else:
            if keys[pygame.K_a]:
                self.tryMoveX(-self.player.speed)

                # 处理人物动画
                if self.player.facing != "left":
                    self.player.facing = "left"
                    self.player.frame = 0
                else:
                    self.player.frame = (self.player.frame + 1) % 8

            if keys[pygame.K_d]:
                self.tryMoveX(self.player.speed)

                if self.player.facing != "right":
                    self.player.facing = "right"
                    self.player.frame = 0
                else:
                    self.player.frame = (self.player.frame + 1) % 8

        # 判断是否碰到陷阱
        if (
            (self.player.Rect.y > self.maper.row * self.blockSize)
            or (self.touchDown() == 3)
            or (self.touchUp() == 3)
            or (self.onSide() == 3)
        ):
            print("You fell into trap. Please try again.")
            self.reborn(self.mapid)

        # 判断是否开始冲刺
        if keys[pygame.K_l] and (not self.player.isDashing) and (self.Dashavailable):
            self.player.isDashing = True  # 启动冲刺
            self.dashTimer = pygame.time.get_ticks()  # 记录冲刺开始时间
            self.Dashavailable = False  # 设置冲刺为不可用

        # 判断是否结束冲刺
        if self.player.isDashing:
            elapsed = pygame.time.get_ticks() - self.dashTimer
            if elapsed > MoveSettings.dashDuration:  # 检查冲刺是否结束
                self.player.isDashing = False  # 结束冲刺
                self.player.onJump = False  # 冲刺结束后重置跳跃状态
                self.fallTime = pygame.time.get_ticks()
                self.lastDeltaY = self.deltaY = 0

        # 判断是否起跳
        if keys[pygame.K_SPACE] and self.touchDown():
            self.jumpTime = pygame.time.get_ticks()
            self.tryMoveY(-1)
            self.deltaY = 0
            self.player.onJump = True

        # 处理上升过程
        if (not self.player.isDashing) and (self.player.onJump):
            delta = (pygame.time.get_ticks() - self.jumpTime) / 1000
            self.lastDeltaY = self.deltaY
            self.deltaY = int(
                -self.initialSpeed * delta + 0.5 * self.gravity * delta * delta
            )
            self.tryMoveY(self.deltaY - self.lastDeltaY)
            if self.touchDown():
                self.player.onJump = False

        # 判断是否下落
        if (
            (not self.player.isDashing)
            and (not self.player.onJump)
            and (not self.falling)
            and (not self.touchDown())
        ):
            self.falling = True
            self.fallTime = pygame.time.get_ticks()
            self.deltaY = 0

        # 处理下落过程
        if (self.falling) and (not self.player.isDashing):
            delta = (pygame.time.get_ticks() - self.fallTime) / 1000
            self.lastDeltaY = self.deltaY
            self.deltaY = int(0.5 * self.gravity * delta * delta)
            self.tryMoveY(self.deltaY - self.lastDeltaY)
            if self.touchDown():
                self.falling = False
                self.Dashavailable = True  # 重置冲刺为可用

        # 更新人物显示
        if self.player.facing == "left":
            self.player.img = self.player.leftimg[self.player.frame]
        else:
            self.player.img = self.player.rightimg[self.player.frame]

    def touchDown(self):  # 检测是否接触地面
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if (
                    self.IsEntity[i][j] == True
                    and self.player.Rect.colliderect(self.mapRect[i][j])
                    and self.mapRect[i][j].y
                    >= self.player.Rect.y + self.player.height - 1
                ):
                    return self.numMap[i][j]
        return 0

    def touchUp(self):  # 检测是否接触上面
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if (
                    self.IsEntity[i][j] == True
                    and self.player.Rect.colliderect(self.mapRect[i][j])
                    and self.mapRect[i][j].y + self.blockSize - 1 >= self.player.Rect.y
                ):
                    return self.numMap[i][j]
        return 0

    def touchSide(self):  # 检测是否接触左右面
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                if (
                    self.IsEntity[i][j] == True
                    and self.player.Rect.colliderect(self.mapRect[i][j])
                    and not self.mapRect[i][j].y
                    >= self.player.Rect.y + self.player.height - 1
                ):
                    return self.numMap[i][j]
        return 0

    def onSide(
        self,
    ):  # 判断人旁边是否有墙（当人旁边是墙的时候，由于移动时候的设计，会自动远离1个像素）
        self.player.Rect.x += 1
        res = self.touchSide()
        self.player.Rect.x -= 1
        if res:
            return res

        self.player.Rect.x -= 1
        res = self.touchSide()
        self.player.Rect.x += 1
        if res:
            return res
        return 0

    def moveMap(self, sgnx):
        if self.mapDelta + sgnx > 0:
            return
        self.mapDelta += sgnx
        for i in range(self.maper.row):
            for j in range(self.maper.col):
                self.mapRect[i][j].x += sgnx
        # 移动npc
        for npc in self.npcs:
            npc.imageRect.x += sgnx

    def tryMoveX(self, dx):
        sgnx = 1 if dx > 0 else -1
        for i in range(abs(dx)):
            if (
                self.player.Rect.x + self.player.width >= self.mapWidth - self.edgeDist
                and dx > 0
            ):
                self.moveMap(-1)
                if self.touchSide():
                    self.moveMap(1)
            elif self.player.Rect.x <= self.edgeDist and dx < 0 and self.mapDelta != 0:
                self.moveMap(1)
                if self.touchSide():
                    self.moveMap(-1)
            else:
                self.player.Rect.x += sgnx
                if self.touchSide() or self.player.Rect.x < 0:
                    self.player.Rect.x -= sgnx
                    break

    def tryMoveY(self, dy):
        sgny = 1 if dy > 0 else -1
        for i in range(abs(dy)):
            self.player.Rect.y += sgny
            if self.touchDown():
                break
            elif self.touchUp():
                self.tryMoveY(1)
                self.falling = True
                self.player.onJump = False
                self.fallTime = pygame.time.get_ticks()
                self.deltaY = 0
                break

    def sinkDown(self):
        while not self.touchDown():
            self.player.Rect.y += 1
