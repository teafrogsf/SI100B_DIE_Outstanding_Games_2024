import pygame
from .Text import Text

class MutiLineText(Text):
    def __init__(self, name, screen, priority,width=100,space=3):
        self.lineWidth = width
        self.lineSpace = space
        super().__init__(name, screen, priority)
    def calcSpace(self):
        if self.font != None and self.text != None:
            if len(self.text) == 0:
                self.text = " "
            lis = [""]
            lis_height = []
            _acWidth = 0;_sumHeight = 0;_sumDigit = 0
            for char in self.text:
                _sumHeight += self.font.size(char)[1]
                _sumDigit += 1
                if _acWidth + self.font.size(char)[0] >= self.lineWidth:
                    lis[len(lis)-1] += str(char)
                    lis.append("")
                    lis_height.append(_sumHeight/_sumDigit)
                    _acWidth = 0;_sumHeight = 0;_sumDigit = 0
                else:
                    lis[len(lis)-1] += str(char)
                    _acWidth += self.font.size(char)[0]
            if lis[len(lis)-1] == "":
                del(lis[len(lis)-1])
            if _sumDigit != 0:
                lis_height.append(_sumHeight/_sumDigit)
            lis_y = [self.lineSpace]
            for i in range(1,len(lis_height)):
                lis_y.append(lis_y[i-1]+lis_height[i-1]+self.lineSpace*2)
            #print(self.text)
            #print(lis)
            #print(lis_y)
            #print(lis_height)
            return (lis,lis_y,lis_y[len(lis_y)-1]+lis_height[len(lis_y)-1]+self.lineSpace)
    def setTexts(self,txt,choice):
        self.text = txt
        #print(txt)
        lis,lis_y,height = self.calcSpace()
        _surface = pygame.surface.Surface((self.lineWidth+30,height),pygame.SRCALPHA)
        _surface.fill([255,255,255,0])
        for i in range(len(lis)):
            self.setText(lis[i],choice)
            _surface.blit(self.sprite,(max(0,(self.lineWidth+30-self.sprite.get_rect().width)/2),lis_y[i]))
        self.setSprite(_surface)
        self.text = txt
    def setLineWidth(self,width):
        self.lineWidth = width
    def setLineSpace(self,space):
        self.lineSpace = space

