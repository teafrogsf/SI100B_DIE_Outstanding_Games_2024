import Data.fonts
from RenderSystem.Canvas import *
from RenderSystem.Text import *
from RenderSystem.MutiLineText import *
from RenderSystem.Sprite import *

from AnimeSystem.animes.PrintingTextAnime import PrintingTextAnime,AppearingTextAnime

from enum import Enum
import random,time
from datetime import datetime

import Data.deltaTime
from GameDataManager import gameDataManager as gdm

class EndingType(Enum):
    Victory = {
        "Tag":"Victory",
        "BG":"background\\endingVictoryBG.png",
        "Color":pygame.Color(40,40,255)
    }
    Defeat = {
        "Tag":"Defeat",
        "BG":"background\\endingDefeatBG.png",
        "Color":pygame.Color(255,30,30)
    }

class UIEndingBG(Sprite):
    def __init__(self, name, screen, priority,typ):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize(typ.value["BG"],Vector2(1440,720)))

class UIEndingTitle(Text):
    def __init__(self, name, screen, priority,typ):
        self._txt = gdm.Lang["Ending"][typ.value["Tag"]]["Title"]
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Siyf),80))
        self.setColor(Data.fonts.ColorWhite)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setText(self._txt,Data.fonts.FontRender.Outline)

class UIEndingSentence(MutiLineText):
    def __init__(self, name, screen, priority, typ):
        super().__init__(name, screen, priority, 720, 10)
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),30))
        self.setColor(typ.value["Color"])
        if typ == EndingType.Victory:
            _txt = gdm.Lang["Ending"][typ.value["Tag"]]["Sentence"][0]
        else:
            _txt = random.sample(gdm.Lang["Ending"][typ.value["Tag"]]["Sentence"][gdm.STAGE.getStageIndex()],1)[0]
        self.setTexts(_txt,Data.fonts.FontRender.Null)
    def AniCreate(self):
        super().AniCreate(AppearingTextAnime(self,60))

class UIEndingDesq(MutiLineText):
    def __init__(self, name, screen, priority,typ):
        self.typ = typ
        super().__init__(name, screen, priority, 600,5)
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),25))
        self.setColor(Data.fonts.ColorWhite)
    def AniCreate(self):
        _desq = gdm.Lang["Ending"]["Desq"]
        _txt = (_desq[0]+_desq[1][gdm.GAME_DIFFICULTY]+_desq[2]+Data.deltaTime.format_time(time.time()-gdm.TIME_START)+_desq[3]
                +datetime.now().strftime("%Y/%m/%d %H时%M分%S秒")+_desq[4][0 if self.typ == EndingType.Defeat else 1]+
                gdm.STAGE.getStageBattleInfo()["receptionIndex"]+" "+gdm.STAGE.getStageBattleInfo()["receptionName"])
        super().AniCreate(PrintingTextAnime(self,_txt))
    def AniDestroy(self):
        super().AniDestroy()
        self.parent.AtDesqFinish()
