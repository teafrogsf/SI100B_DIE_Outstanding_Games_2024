import pygame,os
from enum import Enum
pygame.init()

pathcwd = os.getcwd()
def LoadFont(file):
    path = os.path.join(pathcwd,"Assets","Font",file)
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError("Not such a file: "+path)

ttf_Brlnsdb = "BRLNSDB.ttf"
ttf_Maturasc = "MATURASC.ttf"
ttf_Arlrdbd = "ARLRDBD.ttf"
ttf_Liti = "STLITI.ttf"
ttf_P22 = "P22.ttf"
ttf_Hp = "HP.ttf"
ttf_stz = "STZHONGS.TTF"
ttf_alger = "ALGER.ttf"
ttf_Nova = "Nova.otf"
ttf_Siyf = "SerifHeavy.otf"

FontSpeedDice = pygame.font.Font(LoadFont(ttf_P22),60)
FontSpeedDice_Alter = pygame.font.Font(LoadFont(ttf_Hp),100)
FontLife = pygame.font.Font(LoadFont(ttf_Brlnsdb),40)

FontMana = pygame.font.Font(LoadFont(ttf_P22),40)
FontDiceNum = pygame.font.Font(LoadFont(ttf_P22),25)
FontDmg = pygame.font.Font(LoadFont(ttf_P22),60)
FontDmgText = pygame.font.Font(LoadFont(ttf_Hp),40)
FontEmotion = pygame.font.Font(LoadFont(ttf_Brlnsdb),40)
FontBuffNum = pygame.font.Font(LoadFont(ttf_P22),25)

FontCardTitle = pygame.font.Font(LoadFont(ttf_Hp),20)
FontUICardTitle = pygame.font.Font(LoadFont(ttf_stz),25)
FontUICardDesq = pygame.font.Font(LoadFont(ttf_Hp),18)
FontUICharAbility = pygame.font.Font(LoadFont(ttf_Hp),16)
FontUICharAbility2 = pygame.font.Font(LoadFont(ttf_Hp),12)

FontSimpleTip = pygame.font.Font(LoadFont(ttf_Hp),30)
FontTitleRoundStart = pygame.font.Font(LoadFont(ttf_Hp),80)
FontButton1 = pygame.font.Font(LoadFont(ttf_Hp),23)
FontBattleResult = pygame.font.Font(LoadFont(ttf_alger),100)
FontButton2 = pygame.font.Font(LoadFont(ttf_P22),60)
FontButton3 = pygame.font.Font(LoadFont(ttf_Hp),20)


class FontRender(Enum):
    Null = 0,
    Shade = 1,
    Outline = 2


ColorBlack = pygame.color.Color(0,0,0),
ColorWhite = pygame.color.Color(255,255,255),
ColorRed = pygame.color.Color(255,10,10)
ColorYellow = pygame.color.Color(255,255,10)
ColorBlue = pygame.color.Color(37,189,253)


ColorEmotionPurple = pygame.color.Color(255,51,255)
ColorEmotionRed = pygame.color.Color(245,24,76)
ColorEmotionGreen = pygame.color.Color(24,245,149)
ColorBrightRed = pygame.color.Color(255,120,120)
ColorBrightBlue = pygame.color.Color(120,120,255)
ColorDarkRed = pygame.color.Color(120,0,0)
ColorClashingYellow = pygame.color.Color(255,204,51)
ColorLight = pygame.Color(254,255,193)
ColorStaggerGain = pygame.Color(0,255,240)
ColorLifeGain = pygame.Color(0,255,114)

ColorSimpleTip = pygame.color.Color(209,201,168)
ColorVictory = pygame.color.Color(219,187,127)
ColorDefeat = pygame.color.Color(237,5,0)