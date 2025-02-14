from AnimeSystem.Anime import *

class SceneTrulyActivateTimer(Anime):
    def __init__(self, scene,lasFrame):
        self.scene = scene
        super().__init__(None, AnimeInfo(lasFrame).setTimer())
    def destroy(self):
        super().destroy()
        from SceneSystem.Scene import Scene
        if isinstance(self.scene,Scene):
            self.scene.TrulyActivate()

class SceneTrulyDisactivateTimer(Anime):
    def __init__(self, scene,lasFrame):
        self.scene = scene
        super().__init__(None, AnimeInfo(lasFrame).setTimer())
    def destroy(self):
        super().destroy()
        from SceneSystem.Scene import Scene
        if isinstance(self.scene,Scene):
            self.scene.TrulyDisactivate()