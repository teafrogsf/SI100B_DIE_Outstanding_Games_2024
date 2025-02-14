import pygame
import sys
import Map
import random
from openai import OpenAI
from typing import List, Dict
from Settings import *
from Fireworks import FireworkParticle

def load_image(picture, image_size, position):
    image_surf = pygame.image.load(picture).convert_alpha()
    image_surf= pygame.transform.scale(image_surf, image_size)
    image_rect = image_surf.get_rect(center = position)
    return image_surf, image_rect

def load_test(test, test_size, test_color, position):
    test_font = pygame.font.Font(None, test_size)
    test_surf = test_font.render(test, False, test_color).convert_alpha()
    test_rect = test_surf.get_rect(center = position)
    return test_surf, test_rect

def draw_input_box(window, x, y, image, text, font, text_color):
    # 绘制背景图片
    window.blit(image, (x, y))
    # 智能换行逻辑
    lines = []
    words = text.split(' ')
    current_line = []
    line_length = 0
    characters_per_line = 60

    for word in words:
        word_length = len(word)
        # 如果添加当前单词会超出长度限制，则先结束当前行
        if line_length + word_length > characters_per_line and current_line:
            lines.append(' '.join(current_line))
            current_line = []
            line_length = 0
        # 否则，增加单词到当前行
        current_line.append(word)
        line_length += word_length + 1  # +1 为单词之间的空格

    # 不要忘记添加最后一行
    lines.append(' '.join(current_line))

    # 确定文本渲染的起始位置
    text_y = y + 50
    for line in lines:
        # 渲染当前行的文本
        text_surface = font.render(line, True, text_color)
        window.blit(text_surface, (x + 50, text_y))
        # 更新下一行文本的垂直位置
        text_y += text_surface.get_height() + 2  # 可以根据需要调整文本行间距

def draw_output_box(window, x, y, image, reply, font, text_color):
    # 绘制背景图片
    window.blit(image, (x, y))
    
    # 智能换行逻辑
    lines = []
    words = reply.split(' ')
    current_line = []
    line_length = 0
    characters_per_line = 60#

    for word in words:
        word_length = len(word)
        # 如果添加当前单词会超出长度限制，则先结束当前行
        if line_length + word_length > characters_per_line and current_line:
            lines.append(' '.join(current_line))
            current_line = []
            line_length = 0
        # 否则，增加单词到当前行
        current_line.append(word)
        line_length += word_length + 1  # +1 为单词之间的空格

    # 不要忘记添加最后一行
    lines.append(' '.join(current_line))

    # 确定文本渲染的起始位置
    text_y = y + 45
    for line in lines:
        # 渲染当前行的文本
        text_surface = font.render(line, True, text_color)
        window.blit(text_surface, (x + 50, text_y))
        # 更新下一行文本的垂直位置
        text_y += text_surface.get_height() + 2  # 可以根据需要调整文本行间距

class Scene:
    def __init__(self, window, Initial_X, Initial_Y):
        self.state = None
        self.map = None
        self.walls = []
        self.machines = []
        self.obstacles = []
        self.traps = []
        self.coins = []
        self.enemies = []
        self.npcs = []
        self.bullets = []
        self.portals = []
        self.background = None

        self.window = window

        self.cameraX = Initial_X
        self.cameraY = Initial_Y

    def Check_Draw(self, Obj):
        if Obj is not None:
            for sprite in Obj:
                drawRect = sprite.rect.move(-self.cameraX, -self.cameraY)
                self.window.blit( sprite.image, drawRect )

    #获取过的金币不能再次获取， 单独写一个函数
    def Draw_Coin(self, player):
        for i in range( len( self.coins ) ):
            if not player.coinsGet[self.name][i]:
                drawRect = self.coins[i].rect.move(-self.cameraX, -self.cameraY)
                self.window.blit( self.coins[i].image, drawRect )

    #NPC头顶有对话标识， 单独画
    def Draw_NPC(self):
        for npc in self.npcs:
            drawRect = npc.rect.move(-self.cameraX, -self.cameraY)
            self.window.blit( npc.image, drawRect )
            if npc.awake: 
                drawRect = npc.uiRect.move(-self.cameraX, -self.cameraY)
                self.window.blit( npc.uiImage, drawRect )

    # render for every scene
    def render(self, player):
        if self.state == GameState.GAME_PLAY_ORIGIN:
            for i in range(SceneSettings.scene_tileXnum):
                for j in range(SceneSettings.scene_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        
        if self.state == GameState.GAME_PLAY_LEVEL_1:
            for i in range(SceneSettings.scene_tileXnum):
                for j in range(SceneSettings.scene_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        
        if self.state == GameState.GAME_PLAY_LEVEL_2:
            for i in range(SceneSettings.scene_tileXnum):
                for j in range(SceneSettings.scene_tileYnum):
                    self.window.blit(self.map[i][j], (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))

        self.Check_Draw(self.background)
        self.Check_Draw(self.obstacles)
        self.Check_Draw(self.machines)
        self.Check_Draw(self.traps)
        self.Check_Draw(self.enemies)
        self.Check_Draw(self.bullets)
        self.Check_Draw(self.portals)
        self.Draw_NPC()
        self.Draw_Coin(player)
    
    def CAMERA_spawn(self, x, y):
        self.cameraX = x
        self.cameraY = y

class MainMenuScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.MAIN_MENU
        self.bg = pygame.image.load('assets_library\scenes\WelcomeBg.gif').convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))
        #这是Welcome的文字
        self.Welcome_font = pygame.font.Font(None, 150)
        self.Welcome_surf = self.Welcome_font.render('Welcome!', False, 'Black').convert_alpha()
        self.Welcome_rect = self.Welcome_surf.get_rect(center = (500, 300))
        #这是Press Here To Start的文字
        self.PressHere_font = pygame.font.Font(None, 100)
        self.PressHere_surf = self.PressHere_font.render('Press Enter To Start! :)', False, 'Black').convert_alpha()
        self.PressHere_rect = self.PressHere_surf.get_rect(center = (500, 600))
        #这是Press Here To Start下面的图案
        self.bgPress_suef = pygame.image.load('assets_library\objects\\bg_for_PressHere.png').convert_alpha()
        self.bgPress_suef= pygame.transform.scale(self.bgPress_suef, (880, 200))
        self.bgPress_rect = self.bgPress_suef.get_rect(center = (500, 600))

    def render(self):
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.Welcome_surf, self.Welcome_rect)
        self.window.blit(self.bgPress_suef, self.bgPress_rect)
        self.window.blit(self.PressHere_surf, self.PressHere_rect)

class PauseMenuScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y, playerX, playerY, preScene):
        super().__init__(window, Initial_X, Initial_Y)
        self.state = GameState.GAME_PLAY_PAUSE
        
        self.playerX = playerX
        self.playerY = playerY
        self.preScene = preScene

        self.test_color = 'Pink'   #字体颜色统一，我先搞成粉色
        #这是Pause文字
        self.Pause_font = pygame.font.Font(None, 100)
        self.Pause_surf = self.Pause_font.render('PAUSE', False, self.test_color).convert_alpha()
        self.Pause_rect = self.Pause_surf.get_rect(center = (500, 150))

        #这是Continue图像和文字
        self.continue_surf = pygame.image.load('assets_library\特殊符号\continue.png').convert_alpha()
        self.continue_surf= pygame.transform.scale(self.continue_surf, (150, 150))
        self.continue_rect = self.continue_surf.get_rect(center = (500, 350))

        self.Continue_font = pygame.font.Font(None, 50)
        self.Continue_surf = self.Continue_font.render('Continue [C]', False, self.test_color).convert_alpha()
        self.Continue_rect = self.Continue_surf.get_rect(center = (500, 450))

        #这是Replay的图像和文字
        self.replay_surf = pygame.image.load('assets_library\特殊符号\\replay.png').convert_alpha()
        self.replay_surf = pygame.transform.scale(self.replay_surf, (80, 80))
        self.replay_rect = self.replay_surf.get_rect(center = (200, 575))

        self.Restart_font = pygame.font.Font(None, 50)
        self.Restart_surf = self.Restart_font.render('Restart [R]', False, self.test_color).convert_alpha()
        self.Restart_rect = self.Restart_surf.get_rect(center = (200, 650))

        #这是Question的图像和文字
        self.question_surf = pygame.image.load('assets_library\特殊符号\\question.png').convert_alpha()
        self.question_surf= pygame.transform.scale(self.question_surf, (80, 80))
        self.question_rect = self.replay_surf.get_rect(center = (500, 575))

        self.Question_font = pygame.font.Font(None, 50)
        self.Question_surf = self.Question_font.render('Help [E]', False, self.test_color).convert_alpha()
        self.Question_rect = self.Question_surf.get_rect(center = (500, 650))

        #这是Home的图像和文字
        self.home_surf = pygame.image.load('assets_library\特殊符号\\Home.png').convert_alpha()
        self.home_surf= pygame.transform.scale(self.home_surf, (80, 80))
        self.home_rect = self.replay_surf.get_rect(center = (800, 575))

        self.Home_font = pygame.font.Font(None, 50)
        self.Home_surf = self.Home_font.render('Quit [Q]', False, self.test_color).convert_alpha()
        self.Home_rect = self.Home_surf.get_rect(center = (800, 650))

    def render(self):
        self.window.blit(self.Pause_surf, self.Pause_rect)
        self.window.blit(self.continue_surf, self.continue_rect)
        self.window.blit(self.Continue_surf, self.Continue_rect)
        self.window.blit(self.replay_surf, self.replay_rect)
        self.window.blit(self.Restart_surf, self.Restart_rect)
        self.window.blit(self.question_surf, self.question_rect)
        self.window.blit(self.Question_surf, self.Question_rect)
        self.window.blit(self.home_surf, self.home_rect)
        self.window.blit(self.Home_surf, self.Home_rect)

class DeadMenuScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y, preScene):
        super().__init__(window, Initial_X, Initial_Y)
        self.preScene = preScene
        self.screen = window
        #绘画变量
        self.bg_color = 'Black'
        self.test_color = 'White'
        self.littleCounter = 0
        #最后一个页面用到的东西
        self.again_surf, self.again_rect = load_image('assets_library\特殊符号\\replay.png', (200, 200), (500, 400))
        self.Again_surf, self.Again_rect = load_test('TRY  AGAIN [R]', 100, self.test_color, (500, 560))
        self.quit_surf, self.quit_rect = load_image('assets_library\特殊符号\Home.png', (50, 50), (900, 700))
        self.Quit_surf, self.Quit_rect = load_test('QUIT [Q]', 50, self.test_color, (900, 750))
        self.question_surf, self.question_rect = load_image('assets_library\特殊符号\question.png', (50, 50), (100, 700))
        self.Question_surf, self.Question_rect = load_test('Questions', 50, self.test_color, (100, 750))
        self.Motivation_surf, self.Motivation_rect = load_test('You Can Make It !!!', 100, self.test_color, (500, 180))
        #动画中用到的东西
        self.You_surf, self.You_rect = load_test('YOU', 100, self.test_color, (500, 400))
        self.Are_surf, self.Are_rect = load_test('ARE', 100, self.test_color, (500, 400))
        self.Dead_surf, self.Dead_rect = load_test('DEAD !', 100, self.test_color, (500, 400))

    def render(self):
        self.littleCounter += 1
        '''这里做了个小动画'''
        self.screen.fill(self.bg_color)
        if 0 <= self.littleCounter <=30:  # 0.5秒
            self.screen.blit(self.You_surf, self.You_rect)
        elif 30 < self.littleCounter <= 60:  # 0.5秒
            self.screen.blit(self.Are_surf, self.Are_rect)
        elif 60 < self.littleCounter <= 120:  # 1秒
            self.screen.blit(self.Dead_surf, self.Dead_rect)
        else:
            self.screen.blit(self.Motivation_surf, self.Motivation_rect)
            self.screen.blit(self.again_surf, self.again_rect)
            self.screen.blit(self.Again_surf, self.Again_rect)
            self.screen.blit(self.quit_surf, self.quit_rect)
            self.screen.blit(self.Quit_surf, self.Quit_rect)
            self.screen.blit(self.question_surf, self.question_rect)
            self.screen.blit(self.Question_surf, self.Question_rect)
        '''正片结束'''

class VictoryMenuScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y, preScene):
        super().__init__(window, Initial_X, Initial_Y)
        self.preScene = preScene
        self.screen = window
        self.bg_color = 'Black'
        self.test_color = 'White'
        self.littleCounter = 0
        self.particles = []
        self.particles_eachtime = 50  # 我先设置成每次生成50个粒子
        self.COLORS = [(random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)) for _ in range(10)]

        self.Congratulations_surf, self.Congratulations_rect = load_test('Congratulations !!!', 100, self.test_color, (500, 400))
        self.Click_surf, self.Click_rect = load_test('Click your mouse and enjoy :)', 50, self.test_color, (500, 750))
        self.You_surf, self.You_rect = load_test('YOU', 100, self.test_color, (500, 400))
        self.Have_surf, self.Have_rect = load_test('Have', 100, self.test_color, (500, 400))
        self.Made_surf, self.Made_rect = load_test('Made It !!', 100, self.test_color, (500, 400))

        self.again_surf, self.again_rect = load_image('assets_library\特殊符号\\replay.png', (50, 50), (100, 50))
        self.Again_surf, self.Again_rect = load_test('Play again', 50, self.test_color, (100, 100))
        self.quit_surf, self.quit_rect = load_image('assets_library\特殊符号\Home.png', (50, 50), (900, 50))
        self.Quit_surf, self.Quit_rect = load_test('Quit [Q]', 50, self.test_color, (900, 100))

    def render(self):
        self.littleCounter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for _ in range(self.particles_eachtime):
                    color = random.choice(self.COLORS)
                    self.particles.append(FireworkParticle(mouse_x, mouse_y, color, self.screen))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.particles = [p for p in self.particles if p.alive]
        for particle in self.particles:
            particle.update()

        self.screen.fill(self.bg_color)
        if 0 <= self.littleCounter <=30:  # 0.5秒
            self.screen.blit(self.You_surf, self.You_rect)
        elif 30 < self.littleCounter <= 60:  # 0.5秒
            self.screen.blit(self.Have_surf, self.Have_rect)
        elif 60 < self.littleCounter <= 120:  # 1秒
            self.screen.blit(self.Made_surf, self.Made_rect)
        else:
            self.screen.fill((0, 0, 0))
            for particle in self.particles:
                particle.draw()
            self.screen.blit(self.Congratulations_surf, self.Congratulations_rect)
            self.screen.blit(self.Click_surf, self.Click_rect)
            self.screen.blit(self.again_surf, self.again_rect)
            self.screen.blit(self.Again_surf, self.Again_rect)
            self.screen.blit(self.quit_surf, self.quit_rect)
            self.screen.blit(self.Quit_surf, self.Quit_rect)

class OriginScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.name = "Origin"
        self.state = GameState.GAME_PLAY_ORIGIN
        self.map = Map.scene_map()
        self.walls = Map.scene_walls()
        self.machines = Map.scene_machines()
        self.coins = Map.scene_coins()
        self.enemies = Map.scene_enemies()
        self.portals = Map.scene_portals()

        self.obstacles = self.walls + self.machines

class Level_1_Scene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.name = "Level_1"
        self.state = GameState.GAME_PLAY_LEVEL_1
        self.map = Map.scene_map()
        self.walls = Map.level_1_walls()
        self.machines = Map.level_1_machines()
        self.traps = Map.level_1_traps()
        self.coins = Map.level_1_coins()
        self.portals = Map.level_1_portals()

        self.obstacles = self.walls + self.machines

class Level_2_Scene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.name = "Level_2"
        self.state = GameState.GAME_PLAY_LEVEL_2
        self.map = Map.scene_map()
        self.walls = Map.level_2_walls()
        self.machines = Map.level_2_machines()
        self.traps = Map.level_2_traps()
        self.coins = Map.level_2_coins()
        self.enemies = Map.level_2_enemies()
        self.npcs = Map.level_2_NPCs()
        self.portals = Map.level_2_portals()

        self.obstacles = self.walls + self.machines

class Level_3_Scene(Scene):
    def __init__(self, window, Initial_X, Initial_Y):
        super().__init__(window, Initial_X, Initial_Y)
        self.name = "Level_3"
        self.state = GameState.GAME_PLAY_LEVEL_2
        self.map = Map.scene_map()
        self.walls = Map.level_3_walls()
        self.machines = Map.level_3_machines()
        self.traps = Map.level_3_traps()
        self.enemies = Map.level_3_enemies()
        self.portals = Map.level_3_portals()

        self.obstacles = self.walls + self.machines

class GamingUI(Scene):
    def __init__(self, window, Initial_X, Initial_Y, player):
        super().__init__(window, Initial_X, Initial_Y)
        self.test_color = 'White'   #字体颜色统一

        #这是Coin图像和文字，还有冒号和数字
        self.coin_surf = pygame.image.load('assets_library\coins\Gold-1.png').convert_alpha()
        self.coin_surf= pygame.transform.scale(self.coin_surf, (40, 40))
        self.coin_rect = self.coin_surf.get_rect(center = (45, 45))

        self.Coin_font = pygame.font.Font(None, 30)
        self.Coin_surf = self.Coin_font.render('Coins', False, self.test_color).convert_alpha()
        self.Coin_rect = self.Coin_surf.get_rect(center = (45, 80))

        self.coin_amount_font = pygame.font.Font(None, 50)
        self.coin_amount_surf = self.coin_amount_font.render(f": {player.coins}", False, self.test_color).convert_alpha()
        self.coin_amount_rect = self.coin_amount_surf.get_rect(center = (90, 45))
    
    def render(self):
        self.window.blit(self.coin_surf, self.coin_rect)
        self.window.blit(self.Coin_surf, self.Coin_rect)
        self.window.blit(self.coin_amount_surf, self.coin_amount_rect)

class ShopScene(Scene):
    def __init__(self, window, Initial_X, Initial_Y, player, playerX, playerY):
        super().__init__(window, Initial_X, Initial_Y)
        self.playerX = playerX
        self.playerY = playerY
        self.player = player
        self.quit = False
        # 初始化 mixer 模块
        pygame.mixer.init()
        # 加载音乐
        pygame.mixer.music.load(r'.\assets_library\mickey.mp3')
        # 播放音乐
        pygame.mixer.music.play(-1)  # 参数 -1 使音乐循环播放
        self.background_image = pygame.image.load('assets_library\scenes\罪恶工具.gif')
        # 将背景图像缩放到窗口大小
        self.background_image = pygame.transform.scale(self.background_image, (WindowSettings.width, WindowSettings.height))
        self.main_player = pygame.image.load(r".\assets_library\PlayerBasic\PlayerIdle.png").convert_alpha()
        self.main_player = pygame.transform.scale(self.main_player, (PlayerSettings.width, PlayerSettings.height))
        self.main_npc = pygame.image.load(r".\assets_library\characters\NPC商人.png").convert_alpha()
        self.main_npc = pygame.transform.scale(self.main_npc, (PlayerSettings.width + 20, PlayerSettings.height + 20))
        # 文本的字体和颜色
        self.font = pygame.font.Font(None,25)
        self.text_color= 'Black'
        #文本内容
        self.You_surf, self.You_rect = load_test('You', 80, self.text_color, (50, 630))
        self.Magician_surf, self.Magician_rect = load_test('Magician', 80, 'Orange', (850, 420))
        self.Buy_surf, self.Buy_rect = load_test('Magical House', 100, 'Purple', (500, 80))
        self.Reminder_surf, self.Reminder_rect = load_test('Type in your chat box. ', 50, self.text_color, (420, 700))
        # 文本框的位置和大小
        self.input_box_x = 100
        self.input_box_y = 550
        self.input_box_width = 600
        self.input_box_height = 200
        self.input_box_background = pygame.image.load(r".\assets_library\objects\PlayerBox.png").convert_alpha()
        self.output_box_background = pygame.image.load(r".\assets_library\objects\bg_for_PressHere.png").convert_alpha()
        # 调整图片大小（如果需要）
        self.input_box_background = pygame.transform.scale(self.input_box_background, (600, 200))
        self.output_box_background = pygame.transform.scale(self.output_box_background, (600, 200))
        # 初始化文本内容
        self.text = ''
        self.reply = ''
        # 文本框是否被激活
        self.active = False
        #语言模型的初始化
        self.client = OpenAI(
            base_url='http://10.15.88.73:5033/v1',
            api_key='ollama',  # required but ignored
        )
        #根据玩家收集到的金币数量，店主会有不同的态度，也决定能否买到物品
        self.playerCoins = player.coins

        if self.playerCoins >= 100:
            self.messages : List[Dict] = [
                {"role": "system", "content": f"I have a wand. Its price is 100 coins.The buyer only have {self.playerCoins} coins.I only have one wand,so when you buy it,I don't have anything else to sell.I am taciturn.Don't give any hint."}
            ]
        elif self.playerCoins >= 80:
            self.messages : List[Dict] = [
                {"role": "system", "content": f"I have a wand. Its price is 100 coins.The buyer only have {self.playerCoins} coins.If I hear the key word 'shanghaitech',I will lower the price to 80 coins,otherwise i will never lower the price.But I cannot tell anyone my key word.I only have one wand,so when you buy it,I don't have anything else to sell.I am taciturn.Don't give any hint."}
            ]
        else:
            self.messages : List[Dict] = [
                {"role": "system", "content": "I have a wand whose price is 100 coins but I will never  sell it.And I am rude and mean and I am taciturn.If someone want to buy my wand,I will be angry and say'Leave me alone'."}
            ]

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检查鼠标点击位置是否在文本框内
                if self.input_box_x <= event.pos[0] <= self.input_box_x + self.input_box_width and \
                self.input_box_y <= event.pos[1] <= self.input_box_y + self.input_box_height:
                    self.active = not self.active
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        print(self.text)  # 处理输入的文本
                        
                        self.messages.append({"role": "user", "content": self.text})

                        self.response = self.client.chat.completions.create(
                            model = "llama3.2",      
                            messages = self.messages,    # a list of dictionary contains all chat dictionary
                        )
                        self.reply=''
                        self.text=''
                        # 提取模型回复
                        self.reply = self.response.choices[0].message.content
                        print(f"Llama: {self.reply}")
                        self.messages.append({"role": "assistant", "content": self.text})
                        print(self.messages)
                    else:
                        self.text += event.unicode
                elif event.key == pygame.K_q:
                    self.messages.append({"role": "user", "content": "Did you sell out your wand?Answer 'Yes' or 'No' only."})
                    response = self.client.chat.completions.create(
                        model = "llama3.2",      
                        messages = self.messages,    # a list of dictionary contains all chat dictionary
                    )
                    self.reply=''
                    self.text=''
                    # 提取模型回复
                    self.reply = response.choices[0].message.content
                    if self.reply == 'Yes':
                        self.player.canShoot = True
                        if self.player.coins >= 100: self.player.coins -= 100
                        else: self.player.coins -= 80
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_QUIT_SHOP))
                    pygame.mixer.music.stop()
                    self.quit = True

            
            # 填充背景
            self.window.fill((200, 200, 200))
            
            # 绘制背景图像和NPC
            self.window.blit(self.background_image, (0, 0))
            
            self.window.blit(self.main_player, (40, 670))
            self.window.blit(self.main_npc, (895, 250))

            # 绘制文本框
            draw_input_box(self.window, self.input_box_x, self.input_box_y, self.input_box_background, self.text, self.font, self.text_color)
            draw_output_box(self.window, 300, 200, self.output_box_background, self.reply, self.font, self.text_color)
            
            self.window.blit(self.You_surf, self.You_rect)
            self.window.blit(self.Magician_surf, self.Magician_rect)
            self.window.blit(self.Buy_surf, self.Buy_rect)
            self.window.blit(self.Reminder_surf, self.Reminder_rect)






