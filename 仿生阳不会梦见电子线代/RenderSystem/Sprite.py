import pygame,os
from .DrawableObject import *

pathcwd = os.getcwd()
def LoadImage(file):
    path = os.path.join(pathcwd,"Assets","Image",file)
    if os.path.exists(path):
        try:
            return pygame.image.load(path)
        except:
            raise TypeError("Maybe not an legal image file: "+path)
    else:
        raise FileNotFoundError("Not such a file: "+path)
def CheckImageFile(file):
    path = os.path.join(pathcwd,"Assets","Image",file)
    if os.path.exists(path):
        return True
    else:
        pass
        #print("File/Folder not exist:",file,"Try ignore or replace")


class Sprite(Drawableobject):
    def __init__(self,name,screen,priority):
        super().__init__(name,screen,priority)
        self.preSize = Vector2.Zero
        self.RECORD_IMGFILE = None
        self.init()
    def init(self):
        pass
    def preResize(self,sprite,replaceRect=None):
        if isinstance(sprite,str):
            sprite = LoadImage(sprite)
        if not isinstance(sprite,pygame.Surface):
            raise TypeError("Not a surface")
        else:
            rct = sprite.get_rect()
            x = self.preSize().x
            y = self.preSize().y
            if isinstance(replaceRect,Vector2):
                x = replaceRect().x
                y = replaceRect().y
            if x != 0 and y != 0:
                return pygame.transform.scale(sprite,(x,y))
            elif x != 0:
                sc = x/rct.width
                return pygame.transform.scale(sprite,(x,rct.height*sc))
            elif y != 0:
                sc = y/rct.height
                return pygame.transform.scale(sprite,(rct.width*sc,y))
            else:
                return sprite
    def setImage(self,img):
        if isinstance(img,(pygame.Surface)):
            self.sprite = img
            self.setRect()
            return self.sprite
        elif isinstance(img,(str)):
            if self.RECORD_IMGFILE != img:
                self.sprite = LoadImage(img)
                self.RECORD_IMGFILE = img
                self.setRect()
            return self.sprite
        return None 
    def OnClick(self, event):
        pass