import pygame
from Data.types import *
import time

class InteractableInterface:
    def __init__(self):
        self.prevent = False
        self.isHalfSelect = False
        self.isMouseOver = False

        self.timeMouseOverStart = 0
        self.timeMouseOver = 0
    def preventRay(self,bl):
        self.prevent = bl
    def rayCast(self,event):
        if self.prevent:
            #print("Ray > Typhoon")
            return
        if hasattr(self,"active") and self.active == False:
            return
        if event.type == pygame.KEYUP:
            self.OnKeyClick(event)
        if hasattr(self,"rect") and self.rect != None:
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos[0],event.pos[1]):
                    if not self.isMouseOver:
                        self._mouseOver("start")
                        self.OnPointEnter(event)
                    self.OnPointHover(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.isHalfSelect = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.isHalfSelect:
                            if event.button == 1:
                                self.OnClick(event)
                            elif event.button == 3:
                                self.OnRightClick(event)
                elif event.type == pygame.MOUSEMOTION and self.isMouseOver == True:
                    self._mouseOver("end")
                    self.OnPointExit(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.isHalfSelect = False
    def EventUpdate(self):
        if self.prevent:
            return
        self._mouseOver()
    def _mouseOver(self,op=None):
        if op == "start":
            self.isMouseOver = True
            self.timeMouseOver = 0
            self.timeMouseOverStart = time.time()
        elif op == "end":
            self.isMouseOver = False
            self.timeMouseOver = 0
            self.timeMouseOverStart = None
        else:
            if self.isMouseOver:
                self.timeMouseOver = time.time()-self.timeMouseOverStart
    def OnPointEnter(self,event):
        pass
    def OnPointHover(self,event):
        pass
    def OnClick(self,event):
        pass
    def OnRightClick(self,event):
        pass
    def OnPointExit(self,event):
        pass
    def OnKeyClick(self,event):
        pass