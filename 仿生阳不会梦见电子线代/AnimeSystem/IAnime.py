from .Anime import Anime
class IAnime:
    def __init__(self):
        self._anime = None
        #print("Kisara is CUUUUUUUTE!")
    def AniCreate(self,ani):
        if self._anime != None:
            return None
        self._anime = ani
        if isinstance(self._anime,Anime):
            return self._anime.lasFrame
    def AniActivate(self):
        if isinstance(self._anime,Anime):
            self._anime.start()
    def AniDestroy(self):#should be called by the anime
        self._anime = None