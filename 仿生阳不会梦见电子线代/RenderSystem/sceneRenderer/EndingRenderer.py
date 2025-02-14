from RenderSystem.prefab.UIEnding import *

from GameDataManager import gameDataManager as gdm

class EndingRenderer(Canvas):
    def __init__(self, name, screen, priority):
        self.endingType = None
        super().__init__(name, screen, priority)
    def init(self):
        self.endingType = EndingType.Victory if gdm.FLAG_VICTORY else EndingType.Defeat if gdm.FLAG_DEFEAT else None
        if self.endingType == None:
            return
        self.addChild(UIEndingBG("BG",self.screen,-100,self.endingType))
        self.addChild(UIEndingTitle("title",self.screen,0,self.endingType))
        self.addChild(UIEndingDesq("desq",self.screen,10,self.endingType))
        self.addChild(UIEndingSentence("sen",self.screen,100,self.endingType))

        self.findChild("desq").setActive(False)
        self.findChild("sen").setActive(False)

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.setPos(Vector2(720,360))

        if self.endingType == None:
            return
        
        self.findChild("title").setPos(Vector2(0,-300))
        self.findChild("desq").setPos(Vector2(0,-100))
        self.findChild("sen").setPos(Vector2(0,100))
    def AtDesqFinish(self):
        self.findChild("sen").AniActivate()
    def PlaySceneAnime(self):
        if self.findChild("desq") != None:
            self.findChild("desq").AniCreate()
            self.findChild("sen").AniCreate()
            self.findChild("desq").AniActivate()
    def Render(self):
        self.draw()