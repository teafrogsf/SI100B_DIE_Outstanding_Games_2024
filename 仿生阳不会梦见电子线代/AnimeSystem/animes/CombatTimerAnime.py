from AnimeSystem.Anime import *

class CombatTimerAnime(Anime):
    def __init__(self, obj,lasFrame,process):
        self.process = process
        super().__init__(obj, AnimeInfo(lasFrame).setTimer())
    def destroy(self):
        super().destroy()
        #print(self.process)
        self.Object.ChangeAnimeProcess(self.process)

class CombatSlowTimerAnime(Anime):
    def __init__(self,lasFrame,slowTime):
        self.slowTime = slowTime
        super().__init__(None,AnimeInfo(lasFrame).setTimer())
    def proceed(self):
        animeManager.animeFrameTimer.tempSlow(self.slowTime)
        super().proceed()

class Yang_FloatingTextTimerAnime(Anime):
    def __init__(self, obj, lasFrame):
        super().__init__(obj, AnimeInfo(lasFrame).setTimer())
    def destroy(self):
        super().destroy()
        from SceneSystem.BattleScene import BattleScene
        if isinstance(self.Object,BattleScene):
            self.Object.YanIsCute()