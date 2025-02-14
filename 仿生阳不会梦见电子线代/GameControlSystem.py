from SceneSystem.BattleScene import BattleScene
from SceneSystem.BeginningScene import BeginningScene
from SceneSystem.DeckSelectionScene import DeckSelectionScene
from SceneSystem.GeneratingScene import GeneratingScene
from SceneSystem.MapScene import MapScene
from SceneSystem.EndingScene import EndingScene

from GameDataManager import gameDataManager
from GameInitialSetting import gameInitialSetting

from Data.instance import *
from enum import Enum
import pygame,time

class Scenes(Enum):
    Beginning = "Beginning"
    EndingDefeat = "EndingDefeat"
    EndingVictory = "EndingVictory"
    Battle = "Battle"
    Generating = "Generating"
    DeckSelection = "DeckSelection"
    Map = "Map"

@instance
class GameControlSystem:
    def __init__(self):
        pygame.init()

        self.screen = None

        self.END_GAME = False
        self.CURRENT_SCENE = None
        self.CURRENT_SCENE_INSTANCE = None

        self.NEXT_SCENE = None
        self.NEXT_SCENE_INSTANCE = None

        self.CACHED_SCENE = None
        self.CACHED_SCENE_INSTANCE = None
        self.IS_CACHE = False
    def Init(self):
        self.InitScreen()
        self.InitScenes()
    def InitScreen(self):
        self.screen = pygame.display.set_mode((1440,720))
        pygame.display.set_caption("Library of Redundancy")
        pygame.display.set_icon(pygame.image.load("icon.png"))
    def InitScenes(self):
        self.Scenes = {
            Scenes.Beginning:BeginningScene,
            Scenes.EndingDefeat:EndingScene,
            Scenes.EndingVictory:EndingScene,
            Scenes.Battle:BattleScene,
            Scenes.Generating:GeneratingScene,
            Scenes.DeckSelection:DeckSelectionScene,
            Scenes.Map:MapScene
        }
    def GameStart(self):
        self.CURRENT_SCENE = None
        self.FindNextScene()
    def GameEnd(self):
        pygame.quit()
    def MainLoop(self):
        self.GameStart()
        #_debugTurn = 0
        while not self.END_GAME:
            #_debugTurn += 1
            self.CURRENT_SCENE_INSTANCE = self.NEXT_SCENE_INSTANCE
            self.NEXT_SCENE_INSTANCE = None
            self.CURRENT_SCENE = self.NEXT_SCENE
            if self.IS_CACHE:
                self.CURRENT_SCENE_INSTANCE.CacheActivate()
                self.IS_CACHE = False
            else:
                self.CURRENT_SCENE_INSTANCE.Activate()
            if not self.END_GAME:
                self.FindNextScene()
            #if _debugTurn >= 2:
            #    self.END_GAME = True
        self.GameEnd()
    def Cache(self,scene,sceneName):
        self.CACHED_SCENE = sceneName
        self.CACHED_SCENE_INSTANCE = scene
    def FindNextScene(self):
        '''
        globalDataManager中直接设置胜利和失败的tag
        '''
        if gameDataManager.FLAG_DEFEAT:
            #raise(ValueError("Defeat scene not finished QAQ"))
            self.NEXT_SCENE = Scenes.EndingDefeat
        elif gameDataManager.FLAG_VICTORY:
            #raise(ValueError("Victory scene not finished QWQ"))
            self.NEXT_SCENE = Scenes.EndingVictory
        elif self.IS_CACHE:
            self.NEXT_SCENE_INSTANCE = self.CACHED_SCENE_INSTANCE
            self.NEXT_SCENE = self.CACHED_SCENE
            self.CACHED_SCENE_INSTANCE = None
            self.CACHED_SCENE = None
            return
        elif isinstance(gameDataManager.NEXT_SCENE,Scenes):#检测是否预设至了要跳转到的场景
            self.NEXT_SCENE = gameDataManager.NEXT_SCENE
            gameDataManager.NEXT_SCENE = None
        elif self.CURRENT_SCENE == None:
            self.NEXT_SCENE = Scenes.Beginning
            #self.NEXT_SCENE = Scenes.Generating
        elif self.CURRENT_SCENE == Scenes.Beginning:
            self.NEXT_SCENE = Scenes.Map
            #self.NEXT_SCENE = Scenes.Battle
        elif self.CURRENT_SCENE == Scenes.DeckSelection:
            self.NEXT_SCENE = Scenes.Battle
        elif self.CURRENT_SCENE == Scenes.Battle:
            self.NEXT_SCENE = Scenes.Map
        else:
            raise ValueError("Not a vailable scene type")
        
        print("Start for Creating Scene",self.NEXT_SCENE.value,time.time())
        self.NEXT_SCENE_INSTANCE = self.Scenes[self.NEXT_SCENE](self.screen)
        print("Ending for Creating Scene",self.NEXT_SCENE.value,time.time())

gameControlSystem = GameControlSystem()