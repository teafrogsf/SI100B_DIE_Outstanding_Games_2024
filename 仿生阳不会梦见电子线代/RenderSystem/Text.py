import pygame
from .DrawableObject import *

import Data.fonts

class Text(Drawableobject):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)

        self.text = None

        self.font = None
        self.color = pygame.color.Color(0,0,0)
        self.shadeColor = pygame.color.Color(0,0,0)

        self.outline_offsets = [(0, 0), (4, 0), (4, 4), (0, 4)]

        self.init()
    def setText(self,txt,choice):
        if isinstance(txt,str):
            self.text = txt
            if choice == Data.fonts.FontRender.Null:
                self.renderText()
            elif choice == Data.fonts.FontRender.Outline:
                self.renderOutlineText()
            else:
                self.renderText()
    def setFont(self,font):
        if isinstance(font,pygame.font.Font):
            self.font = font
    def setColor(self,color):
        self.color = color
    def setShadeColor(self,color):
        self.shadeColor = color
    def renderText(self):
        if self.font != None:
            self.setSprite(self.font.render(self.text,True,self.color))
    def renderOutlineText(self):
        if self.font != None:
            ori = self.font.render(self.text,True,self.color)
            res = pygame.surface.Surface((ori.get_width()+4,ori.get_height()+4),pygame.SRCALPHA)
            for sett in self.outline_offsets:
                res.blit(self.font.render(self.text,True,self.shadeColor),sett)
            res.blit(ori,[2,2])
            self.setSprite(res)
