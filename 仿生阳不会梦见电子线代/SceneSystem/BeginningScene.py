from .Scene import Scene
from RenderSystem.sceneRenderer.BeginningSceneRenderer import BeginningSceneRenderer

from GameDataManager import gameDataManager as gdm
from GameDataManager import CharacterData

from Data.types import *

class BeginningScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
    def init(self):
        self.renderer = BeginningSceneRenderer("rd",self.screen,0,self)
    def TrulyActivate(self):
        from AudioSystem.AudioManager import audioManager
        audioManager.SwitchBGMList("CommonSceneBGM","Beginning")
    def AtEnterGame(self):
        if gdm.GAME_DIFFICULTY == 0:
            for ally in gdm.getAllys().values():
                if isinstance(ally,CharacterData):
                    ally.healthOri *= 1.3
                    ally.staggerOri *= 1.3
                    ally.calcHealth()
                    ally.calcStagger()
                    for typ in ["Stagger"]:
                        for cate in ["Slash","Pierce","Blunt"]:
                            ally.modifyAttribute("resis",{
                                "type":typ,"category":cate,"val":1
                            })
                    ally.modifyAttribute("light",1)
                    ally.modifyAttribute("speed",Vector2(1,2))
        elif gdm.GAME_DIFFICULTY == 2:
            for ally in gdm.getAllys().values():
                if isinstance(ally,CharacterData):
                    ally.healthOri *= 0.85
                    ally.staggerOri *= 0.85
                    ally.calcHealth()
                    ally.calcStagger()
                    for typ in ["Life"]:
                        for cate in ["Slash","Pierce","Blunt"]:
                            ally.modifyAttribute("resis",{
                                "type":typ,"category":cate,"val":-1
                            })
                    ally.modifyAttribute("speed",Vector2(-2,-1))
        self.DisActivate()