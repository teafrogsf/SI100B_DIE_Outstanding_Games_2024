from .Scene import Scene
from RenderSystem.sceneRenderer.BattleMainRenderer import BattleMainRenderer
from RenderSystem.sceneRenderer.BattleCombatRenderer import BattleCombatRenderer
from ReceptionSystem.CombatSystem import BattleSystem
from AnimeSystem.AnimeManager import animeManager
from AudioSystem.AudioManager import audioManager
import ReceptionSystem.GenerateDict

from AnimeSystem.animes.SceneTimer import SceneTrulyActivateTimer,SceneTrulyDisactivateTimer

from enum import Enum
from Data.types import *
import threading,pygame,time,random

class SceneBattle(Enum):
    BattleMainScene = 1
    CombatingScene = 2
class RoundPeriod(Enum):
    RoundStart = 1
    Operating = 2
    Combating = 3
class BattleResult(Enum):
    Win = 1
    Defeat = 2

class BattleScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
    def init(self):
        self.controlSys.update({
            "CurrentRenderer":None,
            "RoundPeriod":None
        })
        self.battleMainRenderer = BattleMainRenderer("battleMainRenderer",self.screen,0,self)
        self.combatRenderer = BattleCombatRenderer("battleCombatRenderer",self.screen,0,self)

        self.battleSystem = BattleSystem("None")
        self.combatDict = None

        self.LoadMainRendererThread = None
        self.LoadCombatRendererThread = None
    def Activate(self):
        self.BlockSelfEventInput(True)
        self.BattleInitialize()
        
        self.rendererTempObject.AddBattleSceneEnter()
        SceneTrulyActivateTimer(self,105).start()
        self.run()
    def TrulyActivate(self):
        from AudioSystem.AudioManager import audioManager
        from GameDataManager import gameDataManager
        audioManager.SwitchBGMList("BattleSceneBGM",gameDataManager.STAGE.getStageBattleInfo()["receptionMusic"])

        self.rendererTempObject.AddTitleRoundStart(self.battleSystem.round)
        if gameDataManager.STAGE.getStageBattleInfo()["Reception"] == "rnfmabj":
            self.YanIsCute()
        #self.OnRoundChange()
        self.BlockSelfEventInput(False)
    def DisActivate(self):
        #Not Ugly code anyway
        self.rendererTempObject.AddSceneTansfer(-1,90)
        SceneTrulyDisactivateTimer(self,100).start()
    def BattleInitialize(self):#call by globalController
        from GameDataManager import gameDataManager
        #print("Here")
        self.battleSystem.Init({
            "Ally":gameDataManager.genBattleAllys(),
            "Enemy":gameDataManager.STAGE.getStageBattleInfo()["Enemy"],
            "Reception":gameDataManager.STAGE.getStageBattleInfo()["Reception"]
        })
        self.OnRoundChange()
    def BattleEnd(self,res):#call by combatRenderer
        pass
    def BattlePlayAnime(self):
        if self.controlSys["CurrentRenderer"] == SceneBattle.CombatingScene:
            self.combatRenderer.PlayBattleAnime()
    def SwitchRenderer(self,newRender):
        print("SwitchRenderer",newRender,time.time())
        self.controlSys["CurrentRenderer"] = newRender
        if newRender == SceneBattle.BattleMainScene:
            self.renderer = self.battleMainRenderer
            self.LoadMainRendererThread = self.ThreadPool.submit(self.OnMainRendererActivate)
            self.LoadMainRendererThread.result()
        elif newRender == SceneBattle.CombatingScene:
            self.renderer = self.combatRenderer
            self.LoadCombatRendererThread = self.ThreadPool.submit(self.OnCombatRendererActivate)
            self.LoadCombatRendererThread.result()
            self.BattlePlayAnime()
        animeManager.ResetTimer()
    def OnMainRendererActivate(self):
        #print(self.GetBattleMainDict())
        print("start for main combat",time.time())
        self.battleMainRenderer.setValue(self.GetBattleMainDict())
        print("main renderer ready",time.time())
    def OnCombatRendererActivate(self):
        print("start for anime",time.time())
        self.battleSystem.SecondSpace()
        print("second space finished",time.time())
        self.OnRoundEnd()
        print("round end",time.time())
        #print(self.combatDict)
        self.combatRenderer.setValue(self.GetCombatDict())
        print("renderer ready",time.time())
    def handleEvent(self, event):
        if self.controlSys["BlockSelfEventInput"]:
            return
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.controlSys["RoundPeriod"] == RoundPeriod.RoundStart:
                    self.OnFirstSpacePress()
                elif self.controlSys["RoundPeriod"] == RoundPeriod.Operating:
                    self.OnSecondSpacePress()
            elif event.key == pygame.K_p:
                if self.controlSys["RoundPeriod"] == RoundPeriod.Operating:
                    self.OnTheP()
    def OnFirstSpacePress(self):
        #self.rendererTempObject.AddSimpleTip(u"前面需要空格",250,Vector2(0,-250))
        self.controlSys["RoundPeriod"] = RoundPeriod.Operating
        audioManager.AddEffect("Snap")
        print("recieve space",time.time())
        self.battleSystem.FirstSpace()
        #print(self.GetBattleMainDict())
        print("data first space",time.time())
        self.battleMainRenderer.setValue(self.GetBattleMainDict())
        self.renderer.preventRay(False)
    def OnSecondSpacePress(self):
        self.controlSys["RoundPeriod"] = RoundPeriod.Combating
        audioManager.AddEffect("Snap")
        self.SwitchRenderer(SceneBattle.CombatingScene)
    def OnRoundChange(self):
        self.controlSys["RoundPeriod"] = RoundPeriod.RoundStart
        self.battleSystem.RoundStart()
        self.SwitchRenderer(SceneBattle.BattleMainScene)
        if self.battleSystem.round != 1:
            self.rendererTempObject.AddTitleRoundStart(self.battleSystem.round)
        #self.AtBattleEnd({"result":BattleResult.Defeat})
        self.renderer.preventRay(True)
    def OnRoundEnd(self):
        self.combatDict = self.battleSystem.RoundEnd()
    def OnTheP(self):
        self.rendererTempObject.AddSimpleTip("the P！",200,Vector2(0,-200),10)
        self.battleSystem.AutoBattle()
        self.AtValueChanged()
    def AtValueChanged(self):#call by children
        if self.controlSys["CurrentRenderer"] == SceneBattle.BattleMainScene:
            self.battleMainRenderer.setValue(self.GetBattleMainDict())
    def AtBattleEnd(self,info):
        from GameDataManager import gameDataManager
        if info["result"] == BattleResult.Win:
            self.rendererTempObject.AddTitleVictory()
            if not gameDataManager.STAGE.nextStage():
                gameDataManager.FLAG_VICTORY = True
        else:
            self.rendererTempObject.AddTitleDefeat()
            gameDataManager.FLAG_DEFEAT = True
        self.DisActivate()
        #self.ThreadPool.submit(self.DisActivate)
    def GetBattleMainDict(self):
        from GameDataManager import gameDataManager
        _dict = ReceptionSystem.GenerateDict.GenerateDict(self.battleSystem)
        _dict["BG"] = gameDataManager.getBackground("Battle",gameDataManager.STAGE.getStageBattleInfo()["receptionBG"])[0]
        return _dict
    def GetCombatDict(self):
        from GameDataManager import gameDataManager
        _dict = self.combatDict
        _dict["BG"] = gameDataManager.getBackground("Battle",gameDataManager.STAGE.getStageBattleInfo()["receptionBG"])
        return _dict
    def YanIsCute(self):
        from GameDataManager import gameDataManager as gdm
        from AnimeSystem.animes.CombatTimerAnime import Yang_FloatingTextTimerAnime
        self.rendererTempObject.AddFloatingText(random.sample(gdm.Lang["ReceptionBackWord"]["rnfmabj"],1)[0])
        Yang_FloatingTextTimerAnime(self,105).start()