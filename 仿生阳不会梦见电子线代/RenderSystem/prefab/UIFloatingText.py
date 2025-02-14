from RenderSystem.RotationText import *
from AnimeSystem.animes.TempObjectAnime import FloatingTextAnime

from Data.types import *
import Data.fonts
import random

class UIFloatingText(RotationText):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
        self.setColor(Data.fonts.ColorBrightBlue)
        self.setShadeColor(Data.fonts.ColorDarkRed)
        self.setFont(Data.fonts.FontSimpleTip)
        self.setPos(Vector2(random.randint(-500,500),random.randint(-200,200)))
        self.setRotation(random.randint(-60,60))
        self.setText(" ",Data.fonts.FontRender.Outline)
