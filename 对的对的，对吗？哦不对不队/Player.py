import pygame
from Settings import *
from Map import Bullet

class Player(pygame.sprite.Sprite):  # 玩家类
    def __init__(self):
        super().__init__()
        #initialize
        self.image = pygame.transform.scale( pygame.image.load(r".\assets_library\PlayerBasic\PlayerIdle.png") , (PlayerSettings.width, PlayerSettings.height) )
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        #collision info
        self.groundCheckDis = 1
        self.isGrounded = False
        self.headCheckDis = 1
        self.headCollide = False
        #move info
        self.moveSpeed = 10
        self.velocity_x = 0
        self.velocity_y = 0
        self.facingRight = True
        self.facingDir = 1
        #jump info
        self.gravity = 3
        self.jumpForce = 30
        #states
        self.states = ["Idle", "Move", "Jump", "Fall"]
        self.state = "Idle"
        #animation info
        self.animTimer = 0
        self.animIndex = 0
        self.currentAnim = None
        self.idleAnim = [pygame.transform.scale( pygame.image.load(r".\assets_library\PlayerBasic\PlayerIdle.png") , (PlayerSettings.width, PlayerSettings.height) )]
        self.moveAnim = [pygame.transform.scale( pygame.image.load(rf".\assets_library\PlayerBasic\PlayerMove-{i}.png") , (PlayerSettings.width, PlayerSettings.height) ) for i in range(1,5)]
        self.jumpAnim = [pygame.transform.scale( pygame.image.load(rf".\assets_library\PlayerBasic\PlayerJump.png") , (PlayerSettings.width, PlayerSettings.height) )]
        self.fallAnim = [pygame.transform.scale( pygame.image.load(rf".\assets_library\PlayerBasic\PlayerFall.png") , (PlayerSettings.width, PlayerSettings.height) )]
        #dead info
        self.isDead = False
        #shop info
        self.coins = 0
        self.coinsGet = { 
            "Origin": [False for i in range(CoinNum.Origin)], 
            "Level_1": [False for i in range(CoinNum.Level_1)],
            "Level_2": [False for i in range(CoinNum.Level_2)] 
            }
        #shoot ability
        self.canShoot = False
        self.shootCD = 0.5 * 30
        self.shootTimer = 0

    def StateControl(self):
        if self.velocity_y != 0 :
            if self.velocity_y < 0:
                if self.state != "Jump":
                    self.state = "Jump"
                self.currentAnim = self.jumpAnim
                self.Reset()
            else:
                if self.state != "Fall":
                    self.state = "Fall"
                self.currentAnim = self.fallAnim
                self.Reset()
        elif self.velocity_x != 0 :
            if self.state != "Move":
                self.Reset()
            self.state = "Move"
            self.currentAnim = self.moveAnim
        else:
            if self.state != "Idle":
                self.Reset()
            self.state = "Idle"
            self.currentAnim = self.idleAnim

    def Detect(self, scene):
        attackCheck = pygame.Rect(self.rect.left + 5, self.rect.bottom, PlayerSettings.width - 10, self.groundCheckDis)
        groundCheck = pygame.Rect(self.rect.left, self.rect.bottom, PlayerSettings.width, self.groundCheckDis)
        headCheck = pygame.Rect(self.rect.left, self.rect.top, PlayerSettings.width, self.headCheckDis)
        self.isGrounded = False
        self.headCollide = False
        #检测与墙体
        for obstacle in scene.obstacles:
            if obstacle.rect.colliderect(groundCheck): self.isGrounded = True
            if obstacle.rect.colliderect(headCheck): self.headCollide = True
        #检测与移动平台
        for machine in scene.machines:
            #踩到平台上，平台开始移动
            if machine.rect.colliderect(groundCheck):
                self.isGrounded = True
                machine.Work(self)
            if machine.rect.colliderect(headCheck): self.headCollide = True
        #检测与陷阱
        for trap in scene.traps:
            if trap.rect.colliderect(self.rect) and not self.isDead:
                self.isDead = True
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_PLAYER_DEAD))
                break
        #检测与金币
        for i in range( len( scene.coins ) ):
            coin = scene.coins[i]
            if coin.rect.colliderect(self.rect) and not self.coinsGet[scene.name][i] :
                self.coins += coin.value
                self.coinsGet[scene.name][i] = True
                break
        #检测与敌人
        for enemy in scene.enemies:
            if enemy.rect.colliderect(attackCheck):
                scene.enemies.remove(enemy)
                self.velocity_y = -25
                break
            elif enemy.rect.colliderect(self.rect) and not self.isDead:
                self.isDead = True
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_PLAYER_DEAD))
                break
        #检测与NPC商人
        for npc in scene.npcs:
            if npc.rect.colliderect(self.rect): npc.awake = True
            else: npc.awake = False

    def PositionFix(self, scene, moveY, yRect):
        if not self.isGrounded and not moveY and self.velocity_y > 0:
            for obstacle in scene.obstacles:
                if obstacle.rect.colliderect(yRect):
                    self.rect.bottom = obstacle.rect.top
                    break
        
        if not self.headCollide and not moveY and self.velocity_y < 0:
            for obstacle in scene.obstacles:
                if obstacle.rect.colliderect(yRect):
                    self.rect.top = obstacle.rect.bottom
                    break
    
    def update(self, keys, scene):
        #Shoot:
        self.shootTimer -= 1
        #Detect:
        self.Detect(scene)
        #Animation:
        self.StateControl()
        self.image = self.currentAnim[ self.animIndex ]
        self.image = pygame.transform.flip( self.image, not self.facingRight, False )

        self.animTimer += 1
        if self.animTimer >= PlayerSettings.animationTime:
            self.animIndex += 1
            self.animTimer = 0
        if self.animIndex >= len(self.currentAnim): self.Reset()

        #Input + VelocitySet
        if  keys[pygame.K_f]and self.canShoot and self.shootTimer < 0 :
            self.shootTimer = self.shootCD
            if self.facingRight:
                scene.bullets.append(Bullet(Images.bullet, self.rect.centerx, self.rect.centery - 10, self.facingDir))
            else:
                scene.bullets.append(Bullet(Images.bullet, self.rect.centerx - 40, self.rect.centery - 10, self.facingDir))
        if keys[pygame.K_SPACE] and self.isGrounded:  # Jump key
            self.velocity_y = -self.jumpForce  # Jump strength
            self.isGrounded = False
        if keys[pygame.K_a]:
            self.velocity_x = -self.moveSpeed
            if self.facingRight: self.flip()
        elif keys[pygame.K_d]:
            self.velocity_x = self.moveSpeed
            if not self.facingRight: self.flip()
        else:
            self.velocity_x = 0
    
        self.velocity_y = min( self.velocity_y + self.gravity, self.jumpForce )

        if self.isGrounded: self.velocity_y = 0

        #Move    
        moveX = moveY = True
        xRect = self.rect.move(self.velocity_x, 0)
        yRect = self.rect.move(0, self.velocity_y)

        #普通墙体的互动
        for obstacle in scene.walls:
            if obstacle.rect.colliderect(xRect): moveX = False
            if obstacle.rect.colliderect(yRect): moveY = False
        #移动平台的互动
        for machine in scene.machines:
            if machine.rect.colliderect(xRect): moveX = False
            if machine.rect.colliderect(yRect): moveY = False


        if moveX: self.rect = self.rect.move(self.velocity_x, 0)
        if moveY: self.rect = self.rect.move(0, self.velocity_y)

        self.PositionFix(scene, moveY, yRect)
        
    def Reset(self):
        self.animIndex = 0
        self.animTimer = 0 

    def flip(self):
        self.facingRight = not self.facingRight
        self.facingDir = -self.facingDir

    def draw(self, window, dx, dy):
        drawRect = self.rect.move(-dx, -dy)
        window.blit(self.image, drawRect)