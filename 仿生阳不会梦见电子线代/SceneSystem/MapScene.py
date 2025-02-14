from .Scene import Scene
from RenderSystem.sceneRenderer.GenshinRenderer import GenshinRenderer

import pygame
from Data.types import *

class MapScene(Scene):
    def __init__(self, screen):
        self.GUIDE = {
            "wasd":False,
            "F":False,
            "out":False,
            "trueOut":False
        }
        super().__init__(screen)
    def init(self):
        self.renderer = GenshinRenderer("rd",self.screen,0,self)
    def Activate(self):
        super().Activate()
    def TrulyActivate(self):
        from GameDataManager import gameDataManager
        from AudioSystem.AudioManager import audioManager
        audioManager.SwitchBGMList("CommonSceneBGM","Map")
        mapping = {1:"I 歧途",2:"II 残躯",3:"III 迷城",4:"IV 噩梦",5:"Ω 无终"}
        self.rendererTempObject.AddTitleRoundStart(-1,mapping[gameDataManager.STAGE.getStageIndex()])
        if not self.GUIDE["wasd"]:
            self.GUIDE["wasd"] = True
            self.rendererTempObject.AddSimpleTip(u"轻推WASD",400,Vector2(0,-250),90)
    def CacheActivate(self):
        from AudioSystem.AudioManager import audioManager
        audioManager.SwitchBGMList("CommonSceneBGM","Map")
        self.renderer.rcdTime = None
        super().CacheActivate()
    def CacheDisactivate(self):
        from GameControlSystem import Scenes
        return super().CacheDisactivate(Scenes.Map)
    def EnterGeneratingScene(self):
        from GameControlSystem import Scenes
        from GameDataManager import gameDataManager
        gameDataManager.NEXT_SCENE = Scenes.Generating
        self.CacheDisactivate()
    def EnterDeckSelectionScene(self):
        from GameControlSystem import Scenes
        from GameDataManager import gameDataManager
        gameDataManager.NEXT_SCENE = Scenes.DeckSelection
        self.DisActivate()
    def EnterNowhere(self):
        if self.GUIDE["trueOut"]:
            return
        self.GUIDE["trueOut"] = True
        from GameDataManager import gameDataManager
        gameDataManager.STAGE.stageCur = 0
        gameDataManager.FLAG_DEFEAT = True
        self.DisActivate()
    def handleEvent(self, event):
        if event.type == pygame.TEXTEDITING:
            self.rendererTempObject.AddSimpleTip("啊哈！猜你在使用：中文输入法",400,Vector2(0,-200),20)
    def AtOutsideTheMap(self):
        if not self.GUIDE["out"]:
            self.GUIDE["out"] = True
            self.rendererTempObject.AddSimpleTip(u"往外走会发生什么呢？",400,Vector2(0,-250),150)
            