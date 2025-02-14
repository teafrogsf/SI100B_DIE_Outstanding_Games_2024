from SceneSystem.Timer import Timer

from Data.instance import *

@instance
class AnimeManager:
    def __init__(self):
        self.animeFrameTimer = Timer(1/30)

        self.animeIDcounter = 0
        self.ID_MOD = 9931110261

        self.animes = {}
        self.end_anime = []
        self.start_anime = []
       
    def genID(self):
        self.animeIDcounter += 1
        self.animeIDcounter %= self.ID_MOD
        return self.animeIDcounter
    def addAnime(self,anime):
        self.animes[anime.id] = anime
    def safeAddAnime(self,anime):
        anime.id = self.genID()
        self.start_anime.append(anime)
        return anime.id
    def delAnime(self,id):
        if id in self.animes.keys():
            self.animes.pop(id)
    def safeDelAnime(self,id):
        self.end_anime.append(id)
    def TickingAnimeFrame(self):
        if self.animeFrameTimer.tick():
            for anime in self.animes.values():
                if not anime.id in self.end_anime:
                    anime.proceed()
            for idd in self.end_anime:
                self.delAnime(idd)
            for animme in self.start_anime:
                self.addAnime(animme)
            self.end_anime.clear()
            self.start_anime.clear()
    def ResetTimer(self):
        self.animeFrameTimer.reset()

animeManager = AnimeManager()