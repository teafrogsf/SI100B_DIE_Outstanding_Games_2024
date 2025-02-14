from AnimeSystem.Anime import *
from RenderSystem.prefab.UICharacter import UICharSprite

#AoeAttackerAnime attackerObj combatRender tempRender info
#AoeEffectAnime centerPos combatRender tempRender info

class AoeEffectAnime(Anime):
    def __init__(self,centerPos,combatRender,tempRender,info):
        pass
    def Sprite(self):
        return self.Object
    def destroy(self):
        super().destroy()
        self.Object.parent.delCombatEffect(self.id)

class AoeAttackerAnime(Anime):
    def __init__(self,obj,combatRenderer,tempRenderer,info):
        pass
    def getAttackerCharSprite(self):
        _element = self.Object.findChild("charImg")
        if isinstance(_element,UICharSprite):
            return _element
        return None