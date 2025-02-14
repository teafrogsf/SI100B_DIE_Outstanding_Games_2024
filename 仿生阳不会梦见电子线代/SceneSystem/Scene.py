from .Timer import Timer
from AnimeSystem.AnimeManager import animeManager
from AudioSystem.AudioManager import audioManager
from EventSystem.EventManager import GatherEvent
from RenderSystem.sceneRenderer.TempObjectRenderer import TempObjectRenderer

from AnimeSystem.animes.SceneTimer import SceneTrulyDisactivateTimer,SceneTrulyActivateTimer

import pygame,time
from concurrent.futures import ThreadPoolExecutor

class Scene:
    def __init__(self,screen):
        self.screen = screen

        self.renderer = None
        self.rendererTempObject = TempObjectRenderer("tempRenderer",self.screen,114514)

        self.dataFrameTimer = Timer(1/60)
        self.renderFrameTimer = Timer(1/30)

        self.controlSys = {
            "ForceStop":False,
            "BlockSelfEventInput":False
        }
        self.ThreadPool = ThreadPoolExecutor(max_workers=4)

        self.init()
        #self.RunningThread = threading.Thread(target = self.run)
    def init(self):
        pass
    def Activate(self):
        self.rendererTempObject.AddSceneTansfer(1)
        SceneTrulyActivateTimer(self,10).start()
        self.run()
    def TrulyActivate(self):
        pass
    def DisActivate(self):
        self.rendererTempObject.AddSceneTansfer(-1)
        SceneTrulyDisactivateTimer(self,10).start()
    def TrulyDisactivate(self):
        self.controlSys["ForceStop"] = True
        print("Scene End",time.time())
    def CacheActivate(self):
        GatherEvent()
        print("Scene CacheActivate",time.time())
        self.controlSys["ForceStop"] = False
        self.rendererTempObject.AddSceneTansfer(1)
        self.run()
    def CacheDisactivate(self,sceneName):
        from GameControlSystem import gameControlSystem
        gameControlSystem.Cache(self,sceneName)
        print("Scene CacheDisactivate",time.time())
        self.rendererTempObject.AddSceneTansfer(-1)
        SceneTrulyDisactivateTimer(self,10).start()
    def SceneUpdate(self):
        pass
    def BlockSelfEventInput(self,bl):
        self.controlSys["BlockSelfEventInput"] = bl
    def TickingDataFrame(self):
        if self.dataFrameTimer.tick():
            if self.renderer != None:
                self.renderer.update()
            self.SceneUpdate()
    def TickingRenderFrame(self):
        if self.renderFrameTimer.tick():
            self.screen.fill((0,0,0))
            if self.renderer != None:
                self.renderer.Render()
            if self.rendererTempObject != None:
                self.rendererTempObject.Render()
            pygame.display.flip()
            audioManager.TickingAudioFrame()
    def EventReceive(self,event):
        self.handleEvent(event)
        if self.renderer != None:
            self.renderer.rayCast(event)
    def run(self):
        animeManager.ResetTimer()
        self.dataFrameTimer.reset()
        self.renderFrameTimer.reset()
        while not self.controlSys["ForceStop"]:
            for event in GatherEvent():
                #print(event)
                if event.type == pygame.QUIT:
                    from GameControlSystem import gameControlSystem
                    gameControlSystem.END_GAME = True
                    self.DisActivate()
                self.EventReceive(event)
            self.TickingDataFrame()
            self.TickingRenderFrame()
            animeManager.TickingAnimeFrame()
        self.safeGuardSave()
    def safeGuardSave(self):
        pass
    def handleEvent(self,event):
        pass
