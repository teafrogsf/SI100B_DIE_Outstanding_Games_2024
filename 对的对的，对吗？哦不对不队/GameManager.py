import pygame
import sys

import Scene
import Player
from Settings import *

class Gamemanager():
    def __init__(self, window, player):
        self.window = window
        self.player = player
        self.scene = Scene.MainMenuScene(window, 0, 0)
        self.state = GameState.MAIN_MENU
        self.clock = pygame.time.Clock()

    def tick(self, fps):    # ticks
        self.clock.tick(fps)

    def event_queue(self, player:Player.Player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #主菜单的操作
                if self.state == GameState.MAIN_MENU:
                    if event.key == pygame.K_RETURN:
                        self.flush_scene(GameState.GAME_PLAY_ORIGIN, player, PosSettings.originX, PosSettings.originY)
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

                #Origin的操作
                if self.state == GameState.GAME_PLAY_ORIGIN:
                    if event.key == pygame.K_ESCAPE:
                        self.flush_scene(GameState.GAME_PLAY_PAUSE, player, 0, 0)

                #Level-1的操作
                if self.state == GameState.GAME_PLAY_LEVEL_1:
                    if event.key == pygame.K_ESCAPE:
                        self.flush_scene(GameState.GAME_PLAY_PAUSE, player, 0, 0)

                #Level-2的操作
                if self.state == GameState.GAME_PLAY_LEVEL_2:
                    if event.key == pygame.K_ESCAPE:
                        self.flush_scene(GameState.GAME_PLAY_PAUSE, player, 0, 0)
                    if event.key == pygame.K_t and self.scene.npcs[0].awake:
                        self.flush_scene(GameState.GAME_PLAY_SHOP, player, 0, 0)
                
                #level-3的操作
                if self.state == GameState.GAME_PLAY_LEVEL_3:
                    if event.key == pygame.K_ESCAPE:
                        self.flush_scene(GameState.GAME_PLAY_PAUSE, player, 0, 0)

                #Pause的操作
                if self.state == GameState.GAME_PLAY_PAUSE:
                    if event.key == pygame.K_c:
                        self.flush_scene(self.scene.preScene, player, self.scene.playerX, self.scene.playerY)
                    if event.key == pygame.K_r:
                        if self.scene.preScene == GameState.GAME_PLAY_ORIGIN:
                            self.flush_scene(self.scene.preScene, player, PosSettings.originX, PosSettings.originY)
                        elif self.scene.preScene == GameState.GAME_PLAY_LEVEL_1:
                            self.flush_scene(self.scene.preScene, player, PosSettings.level_1_X, PosSettings.level_1_Y)
                        elif self.scene.preScene == GameState.GAME_PLAY_LEVEL_2:
                            self.flush_scene(self.scene.preScene, player, PosSettings.level_2_X, PosSettings.level_2_Y)
                        elif self.scene.preScene == GameState.GAME_PLAY_LEVEL_3:
                            self.flush_scene(self.scene.preScene, player, PosSettings.level_3_X, PosSettings.level_3_Y) 
                    if event.key == pygame.K_q:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                
                #Dead的操作
                if self.state == GameState.GAME_PLAY_DEAD:
                    if event.key == pygame.K_r:
                        player.isDead = False
                        if self.scene.preScene == GameState.GAME_PLAY_ORIGIN:
                            self.flush_scene(self.scene.preScene, player, PosSettings.originX, PosSettings.originY)
                        elif self.scene.preScene == GameState.GAME_PLAY_LEVEL_1:
                            self.flush_scene(self.scene.preScene, player, PosSettings.level_1_X, PosSettings.level_1_Y)
                        elif self.scene.preScene == GameState.GAME_PLAY_LEVEL_2:
                            self.flush_scene(self.scene.preScene, player, PosSettings.level_2_X, PosSettings.level_2_Y)
                        elif self.scene.preScene == GameState.GAME_PLAY_LEVEL_3:
                            self.flush_scene(self.scene.preScene, player, PosSettings.level_3_X, PosSettings.level_3_Y) 
                    if event.key == pygame.K_q:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            
            if event.type == GameEvent.PLAYER_GOTO_LEVEL_1:
                pygame.event.get(GameEvent.PLAYER_GOTO_LEVEL_1)
                self.flush_scene(GameState.GAME_PLAY_LEVEL_1, player, PosSettings.level_1_X, PosSettings.level_1_Y)
            
            if event.type == GameEvent.PLAYER_GOTO_LEVEL_2:
                pygame.event.get(GameEvent.PLAYER_GOTO_LEVEL_2)
                self.flush_scene(GameState.GAME_PLAY_LEVEL_2, player, PosSettings.level_2_X, PosSettings.level_2_Y)

            if event.type == GameEvent.PLAYER_GOTO_LEVEL_3:
                pygame.event.get(GameEvent.PLAYER_GOTO_LEVEL_3)
                self.flush_scene(GameState.GAME_PLAY_LEVEL_3, player, PosSettings.level_3_X, PosSettings.level_3_Y)
            
            if event.type == GameEvent.PLAYER_VICTORY:
                self.flush_scene(GameState.VICTORY, player, 0, 0)

            if event.type == GameEvent.EVENT_PLAYER_DEAD:
                pygame.event.get(GameEvent.EVENT_PLAYER_DEAD)
                self.flush_scene(GameState.GAME_PLAY_DEAD, player, 0, 0)

            if event.type == GameEvent.EVENT_QUIT_SHOP:
                pygame.event.get(GameEvent.EVENT_QUIT_SHOP)
                self.flush_scene(GameState.GAME_PLAY_LEVEL_2, player, self.scene.playerX, self.scene.playerY)

    def flush_scene(self, GOTO:GameState, player:Player.Player, Initial_X, Initial_Y):  # switch scene
        if GOTO == GameState.GAME_PLAY_PAUSE:
            self.scene = Scene.PauseMenuScene(self.window, Initial_X, Initial_Y, player.rect.left, player.rect.top, self.state)
        if GOTO == GameState.GAME_PLAY_DEAD:
            self.scene = Scene.DeadMenuScene(self.window, Initial_X, Initial_Y, self.state)
        if GOTO == GameState.VICTORY:
            self.scene = Scene.VictoryMenuScene(self.window, Initial_X, Initial_Y, self.state)
        if GOTO == GameState.GAME_PLAY_SHOP:
            self.scene = Scene.ShopScene(self.window, Initial_X, Initial_Y, player, player.rect.left, player.rect.top)
        if GOTO == GameState.GAME_PLAY_ORIGIN:
            self.scene = Scene.OriginScene(self.window, Initial_X, Initial_Y)
        if GOTO == GameState.GAME_PLAY_LEVEL_1:
            self.scene = Scene.Level_1_Scene(self.window, Initial_X, Initial_Y)
        if GOTO == GameState.GAME_PLAY_LEVEL_2:
            self.scene = Scene.Level_2_Scene(self.window, Initial_X, Initial_Y)
        if GOTO == GameState.GAME_PLAY_LEVEL_3:
            self.scene = Scene.Level_3_Scene(self.window, Initial_X, Initial_Y)
        player.rect.topleft = ( Initial_X, Initial_Y )
        #player.colliSys = Attributes.Collidable(self.scene)
        self.state = GOTO

    def update_camera(self, player:Player.Player):
        playerCenter = ( player.rect.center )  # 获取玩家当前的位置

        self.scene.cameraX = playerCenter[0] - WindowSettings.width // 2
        self.scene.cameraY = playerCenter[1] - WindowSettings.height // 2

        self.scene.cameraX = max(self.scene.cameraX, 0)
        self.scene.cameraX = min(self.scene.cameraX, SceneSettings.sceneWidth)

        self.scene.cameraY = max(self.scene.cameraY, 0)
        self.scene.cameraY = min(self.scene.cameraY, SceneSettings.sceneHeight)

    def update_machine(self, player):
        for machine in self.scene.machines:
            machine.update(player)

    def update_coin(self):
        for coin in self.scene.coins:
            coin.update()

    def update_enemy(self):
        for enemy in self.scene.enemies:
            enemy.update()

    def update_bullet(self):
        for bullet in self.scene.bullets:
            bullet.update(self.scene)
    
    def update_portal(self, player):
        for portal in self.scene.portals:
            portal.update(player)

    def update(self, player:Player.Player):
        if self.state != GameState.GAME_PLAY_PAUSE:
            self.update_camera(player)
            self.update_machine(player)
            self.update_portal(player)
            self.update_coin()
            self.update_enemy()
            self.update_bullet()


    def render(self):
        if self.state == GameState.GAME_PLAY_LEVEL_1 or self.state == GameState.GAME_PLAY_LEVEL_2 or self.state == GameState.GAME_PLAY_LEVEL_3 or self.state == GameState.GAME_PLAY_ORIGIN:
            self.scene.render(self.player)
            ui = Scene.GamingUI(self.window, 0, 0, self.player)
            ui.render()
        else:
            self.scene.render()