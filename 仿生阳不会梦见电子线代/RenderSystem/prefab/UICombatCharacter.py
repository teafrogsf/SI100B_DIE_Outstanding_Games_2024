from .UICharacter import *
from .UICombatCard import *

from AnimeSystem.animes.CombatCharAnime import CombatCharAnime_Death
from AnimeSystem.animes.CombatTimerAnime import CombatSlowTimerAnime

from Data.coder import *
from RenderSystem.sceneRenderer.BattleMainRenderer import BattleTeam

class UICombatCharacter(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UICharSprite("charImg",self.screen,10))
        self.addChild(UILifeBarBlock("infoBar",self.screen,0))
        self.addChild(UICombatCard("combatCard",self.screen,5))
        self.addChild(UIBuffBarBlock("buffBar",self.screen,5))

        self.isHaveCard = False

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("charImg").setPos(Vector2.Zero())
        self.findChild("infoBar").setPos(Vector2(0,150)*self.worldScale())
        self.findChild("infoBar").setScale(Vector2(0.85,0.85))

        self.findChild("buffBar").setScale(Vector2(1.3,1.3))
        self.findChild("buffBar").setPos(Vector2(-120,0)*self.worldScale()
                                         *(Vector2(-1,1) if self.findChild("charImg").face == CharFace.Right else Vector2.One()))
        '''
        self.findChild("combatCard").setPos(
            (Vector2.One() if self.findChild("charImg").face == CharFace.Right else Vector2(-1,1))*self.worldScale()*(
            Vector2(20,-50) if self.findChild("charImg").sprite == None 
            else (lambda rct = (self.findChild("charImg").sprite.get_rect()):Vector2(rct.width-20,-rct.height+50))()
        ))
        '''
        self.findChild("combatCard").setPos(
            (Vector2.One() if self.findChild("charImg").face == CharFace.Right else Vector2(-1,1))*self.worldScale()*(Vector2(170,-100)))
        self.findChild("combatCard").setScale(Vector2(1.25,1.25))
    def setValue(self,dit):
        if "charId" in dit.keys():
            self.charId = dit["charId"]
        if "char" in dit.keys():
            self.findChild("charImg").setValue((None if not ("name" in dit["char"].keys()) else dit["char"]["name"]),
                                                (None if not ("state" in dit["char"].keys()) else dit["char"]["state"]),
                                                ((
                                                    CharFace.Left if decodeCharIdInfo(dit["charId"]) == BattleTeam.Enemy.value else CharFace.Right
                                                ) if not ("face" in dit["char"].keys()) else dit["char"]["face"]))
        if "isHaveCard" in dit.keys():
            self.isHaveCard = dit["isHaveCard"]
            self.findChild("combatCard").setActive(self.isHaveCard)
        if "infoBar" in dit.keys():
            self.findChild("infoBar").setValue(dit["infoBar"])
            if "buff" in dit["infoBar"].keys():
                self.findChild("buffBar").setValue(dit["infoBar"]["buff"])
        if "combatCard" in dit.keys():
            dit["combatCard"]["face"] = self.findChild("charImg").face
            self.findChild("combatCard").setValue(dit["combatCard"])
        self.posSetChildren()
    def setFace(self,face):
        self.findChild("charImg").setFace(face)
        self.findChild("combatCard").setPos(
            (Vector2.One() if self.findChild("charImg").face == CharFace.Right else Vector2(-1,1))*self.worldScale()*(
            Vector2(150,-150) if self.findChild("charImg").sprite == None 
            else (lambda rct = (self.findChild("charImg").sprite.get_rect()):Vector2(rct.width+50,-rct.height-50))()
        ))
    def AniCreate(self,process,dit):
        maxF = 0
        if "sprite" in dit.keys():
            maxF = max(self.findChild("charImg").AniCreate(dit["sprite"]),maxF)
        if "move" in dit.keys():
            maxF = max(super().AniCreate(dit["move"]),maxF)
            #if isinstance(dit["move"],CombatCharAnime_Death):
            #    CombatSlowTimerAnime(15,1/30).start()
        return maxF
    def AniActivate(self,process):
        if process != 2:
            super().AniActivate()
            self.findChild("charImg").AniActivate()
        else:
            if self.isHaveCard:
                self.findChild("combatCard").findChild("rollingDice").AniActivate()

