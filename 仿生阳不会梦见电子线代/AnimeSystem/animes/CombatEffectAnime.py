from AnimeSystem.Anime import *

class CombatEffectAnime(Anime):
    def __init__(self,lasFrame, obj,genPos,deltaPos,delay=0):
        if delay == 0:
            super().__init__(obj, AnimeInfo(lasFrame).add(AnimeType.Pos,0,genPos())
                            .add(AnimeType.Pos,lasFrame,genPos()+deltaPos()).disableSprite().finish())
        else:
            super().__init__(obj, AnimeInfo(lasFrame+delay).add(AnimeType.Active,0,False).add(AnimeType.Active,delay,True)
                             .add(AnimeType.Pos,0,genPos()).add(AnimeType.Pos,delay,genPos())
                             .add(AnimeType.Pos,lasFrame+delay,genPos()+deltaPos()).disableSprite().finish())
    def proceed(self):
        super().proceed()
        #print(self.frame)
    def destroy(self):
        super().destroy()
        self.Object.parent.delCombatEffect(self.id)

class CombatEmotionAnime(CombatEffectAnime):
    def __init__(self, obj):
        Anime.__init__(self,obj,AnimeInfo(30).setTimer())
    def proceed(self):
        from RenderSystem.prefab.UIEmotionLine import UIEmotionLine
        if isinstance(self.Object,UIEmotionLine):
            self.Object.proceed(self.frame)
        super().proceed()