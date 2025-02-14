from .Sprite import *
from enum import Enum
class BarSlideChoice(Enum):
    Left = 1
    Right = 2
    Top = 3
    Bottom = 4
    MiddleColumn = 5
    MiddleRow = 6
class BarSprite(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.percentage = 1.0
        self.slideChoice = BarSlideChoice.Left
        self.cutRect = None
    def setPercentage(self,per):
        if isinstance(per,float):
            self.percentage = max(min(per,1.0),0)
            self.setRect()
    def setSlideChoice(self,choice):
        self.slideChoice = choice     
    def setRect(self):
        super().setRect()
        if self.rect != None:
            if self.slideChoice == BarSlideChoice.Left:
                self.cutRect = pygame.rect.Rect((0,0),(self.rect.width*self.percentage,self.rect.height))
            elif self.slideChoice == BarSlideChoice.Right:
                self.cutRect = pygame.rect.Rect(self.rect.width*(1-self.percentage),0,self.rect.width*self.percentage,self.rect.height)
            elif self.slideChoice == BarSlideChoice.Top:
                self.cutRect = pygame.rect.Rect((0,0),(self.rect.width,self.rect.height*self.percentage))
            elif self.slideChoice == BarSlideChoice.Bottom:
                self.cutRect = pygame.rect.Rect(self.rect.height*(1-self.percentage),0 ,self.rect.width,self.rect.height*self.percentage)
    def draw(self):
        if self.active:
            if self.cutRect != None:
                self.Clean()
                self.screen.blit(self.worldSprite,self.rect,self.cutRect)
                return True
            else:
                return super().draw()
        return False  
