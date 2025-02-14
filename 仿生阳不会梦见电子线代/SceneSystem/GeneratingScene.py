from .Scene import Scene
from RenderSystem.sceneRenderer.GeneratingSceneRenderer import GeneratingSceneRenderer
from LLMSystem.InteractionWithGPT import LLMSystem

from .Timer import *
from LLMStorage import llmStorage
from GameDataManager import gameDataManager
from Data.types import *

class GeneratingScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
    def init(self):
        from GameDataManager import gameDataManager
        self.renderer = GeneratingSceneRenderer("rd",self.screen,0,self)
        self.controlSys.update({
            "inGenerating":False,
            "genTime":None,
            "genThread":None
        })
    def Activate(self):
        self.renderer.Init()
        super().Activate()
    def TrulyActivate(self):
        from AudioSystem.AudioManager import audioManager
        audioManager.SwitchBGMList("CommonSceneBGM","Generating")
    def SceneUpdate(self):
        if llmStorage.inGenerating:
            from GameDataManager import gameDataManager
            if llmStorage.genTime.tick():
                print("Time limit apporoached when gen llm page. Backup plan activated")
                llmStorage.shutDown()
            llmStorage.gather()
            if llmStorage.inGenerating:
                self.renderer.RequestOnGenCard(True)
            else:
                self.renderer.RequestOnGenCard(False)

                gameDataManager.loadGenPage()
                self.renderer.LoadGenCardBar()

                llmStorage.refresh()
    def AtEntryTexted(self):
        if llmStorage.inGenerating:
            return None
        from EventSystem.TkinterManager import tkManager
        return tkManager.createSimpleDialog()
    def AtEntryConfirmed(self,text):
        if llmStorage.inGenerating:
            return
        #print(text)
        '''
        here connect llm
        '''
        self.renderer.RequestGenProcessDialog(u"司书说：")
        llmStorage.register(125,self.ThreadPool.submit(llmStorage.LLM_SYSTEM.create_page0,text,3))
        self.ThreadPool.submit(self.Thread_GenCardDialog,text)
        #print("submit")
    def Thread_GenCardDialog(self,text):
        self.renderer.RequestGenProcessDialog(llmStorage.genCardDialog(text))  
    def AtExitButtonClicked(self):
        if self.renderer.RequestCanExitScene():
            gameDataManager.injectGenPage(None)
            self.DisActivate()
        else:
            self.rendererTempObject.AddSimpleTip(u"司书正在收集书页ing",400,Vector2(0,-150),30)
    def DisActivate(self):
        from GameControlSystem import gameControlSystem
        gameControlSystem.IS_CACHE = True
        super().DisActivate()