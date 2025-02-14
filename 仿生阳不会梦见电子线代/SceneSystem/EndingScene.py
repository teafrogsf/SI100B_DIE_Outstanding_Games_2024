from .Scene import Scene
from RenderSystem.sceneRenderer.EndingRenderer import EndingRenderer

class EndingScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
    def init(self):
        self.renderer = EndingRenderer("rd",self.screen,0)
    def TrulyActivate(self):
        from AudioSystem.AudioManager import audioManager
        audioManager.SwitchBGMList("CommonSceneBGM","Ending")
        self.renderer.PlaySceneAnime()