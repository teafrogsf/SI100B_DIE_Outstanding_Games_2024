from .Scene import Scene
from RenderSystem.sceneRenderer.DeckSelectionSceneRenderer import DeckSelectionSceneRenderer

from Data.types import *

class DeckSelectionScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
    def init(self):
        self.renderer = DeckSelectionSceneRenderer("rd",self.screen,0,self)
    def Activate(self):
        self.renderer.Init()
        super().Activate()
    def TrulyActivate(self):
        from AudioSystem.AudioManager import audioManager
        audioManager.SwitchBGMList("CommonSceneBGM","DeckSelection")
    def AtExitButtonClicked(self):
        if not self.CheckAllyPageFulfill():
            self.rendererTempObject.AddSimpleTip(u"书页未装配完毕",300,Vector2(0,-150),30)
        else:
            self.DisActivate()
    def CheckAllyPageFulfill(self):
        from GameDataManager import gameDataManager,CharacterData
        for ally in gameDataManager.getAllys().values():
            if isinstance(ally,CharacterData):
                if len(ally.Page) < 9:
                    return False
        return True