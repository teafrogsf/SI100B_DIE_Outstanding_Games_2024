from .AnimeManager import animeManager

from enum import Enum

class AnimeType(Enum):
    Pos = 0
    Scale = 1
    Sprite = 2
    Active = 3
    Alpha = 4
class AnimeOp(Enum):
    Reset = 1
    Keep = 2

class Anime:
    def __init__(self,obj,aniInfo,aniOp=AnimeOp.Keep):
        self.id = None

        self.Object = obj
        self.aniOp = aniOp

        self.spChange = aniInfo.spriteChange
        self.spCommon = aniInfo.commonSprite

        self.timer = aniInfo.timer

        self.ableAlpha = aniInfo.ableAlpha
        self.rcdAlpha = None

        self.lasFrame = aniInfo.lasTime
        self.frame = 0
        self.pin = [0,0,0,0,0]
        self.frameDelta = [[],[],[],[],[]]

        if not self.timer:
            self.calc(aniInfo)
        #print(self.frameDelta)
    def calc(self,aniInfo):
        if len(aniInfo.posKFrame) == 0 or aniInfo.posKFrame[0][0] != 0:
            aniInfo.posKFrame.insert(0,(0,self.Object.localPosition()))
        if len(aniInfo.scaleKFrame) == 0 or aniInfo.scaleKFrame[0][0] != 0:
            aniInfo.scaleKFrame.insert(0,(0,self.Object.localScale()))
        
        if self.spChange and self.spCommon:
            if len(aniInfo.spriteKFrame) == 0 or aniInfo.spriteKFrame[0][0] != 0:
                aniInfo.spriteKFrame.insert(0,(0,self.Sprite().sprite))
        
        if len(aniInfo.activeKFrame) == 0 or aniInfo.activeKFrame[0][0] != 0:
            aniInfo.activeKFrame.insert(0,(0,self.Object.active))
        
        if self.ableAlpha:
            if len(aniInfo.alphaKFrame) == 0 or aniInfo.alphaKFrame[0][0] != 0:
                aniInfo.alphaKFrame.insert(0,(0,255))

        self.frameDelta[0].append(aniInfo.posKFrame[0])
        for i in range(0,len(aniInfo.posKFrame)-1):
            self.frameDelta[0].append((aniInfo.posKFrame[i+1][0],
                (aniInfo.posKFrame[i+1][1]-aniInfo.posKFrame[i][1])/(aniInfo.posKFrame[i+1][0]-aniInfo.posKFrame[i][0])))
        self.frameDelta[1].append(aniInfo.scaleKFrame[0])
        for i in range(0,len(aniInfo.scaleKFrame)-1):
            self.frameDelta[1].append((aniInfo.scaleKFrame[i+1][0],
                (aniInfo.scaleKFrame[i+1][1]-aniInfo.scaleKFrame[i][1])/(aniInfo.scaleKFrame[i+1][0]-aniInfo.scaleKFrame[i][0])))
        
        for i in range(0,len(aniInfo.spriteKFrame)):
            self.frameDelta[2].append((aniInfo.spriteKFrame[i][0],
                                      aniInfo.spriteKFrame[i][1]))
        for i in range(0,len(aniInfo.activeKFrame)):
            self.frameDelta[3].append((aniInfo.activeKFrame[i][0],
                                      aniInfo.activeKFrame[i][1]))
        
        if self.ableAlpha:
            self.frameDelta[4].append(aniInfo.alphaKFrame[0])
            for i in range(0,len(aniInfo.alphaKFrame)-1):
                self.frameDelta[4].append((aniInfo.alphaKFrame[i+1][0],
                    (aniInfo.alphaKFrame[i+1][1]-aniInfo.alphaKFrame[i][1])/(aniInfo.alphaKFrame[i+1][0]-aniInfo.alphaKFrame[i][0])))
    def Sprite(self):#put the pin where .sprite is the sprite
        return None
    def OnKFrame(self,typ,frame):
        pass
    def start(self):
        if not self.timer:
            self.proceedPos(True)
            self.proceedScale(True)
            self.proceedSprite(True)
            self.proceedActive(True)
            self.proceedAlpha(True)
        return (animeManager.safeAddAnime(self),self)
    def proceed(self):
        if not self.timer:
            self.proceedPos()
            self.proceedScale()
            self.proceedSprite()
            self.proceedActive()
            self.proceedAlpha()
        
        self.frame += 1
        if self.frame > self.lasFrame:
            self.destroy()
    def proceedPos(self,st=False):
        if st:
            self.Object.setPos(self.frameDelta[0][0][1]())
            return
        if self.pin[0] < len(self.frameDelta[0]):
            if self.frameDelta[0][self.pin[0]][0] == self.frame:
                self.pin[0] += 1
                self.OnKFrame(AnimeType.Pos,self.frame)
            if self.pin[0] < len(self.frameDelta[0]):
                self.Object.move(self.frameDelta[0][self.pin[0]][1]())
    def proceedScale(self,st=False):
        if st:
            self.Object.setScale(self.frameDelta[1][0][1]())
            return
        if self.pin[1] < len(self.frameDelta[1]):
            if self.frameDelta[1][self.pin[1]][0] == self.frame:
                self.pin[1] += 1
                self.OnKFrame(AnimeType.Scale,self.frame)
            if self.pin[1] < len(self.frameDelta[1]):
                self.Object.setScale(self.Object.localScale() + self.frameDelta[1][self.pin[1]][1]())
    def proceedSprite(self,st=False):
        if not self.spChange or not self.spCommon:
            return
        if st:
            self.Sprite().setImage(self.frameDelta[2][0][1])
            return
        if self.pin[2] < len(self.frameDelta[2]):
            if self.frameDelta[2][self.pin[2]][0] == self.frame:
                self.Sprite().setImage(self.frameDelta[2][self.pin[2]][1])
                self.pin[2] += 1
                self.OnKFrame(AnimeType.Sprite,self.frame)
    def proceedActive(self,st=False):
        if st:
            self.Object.setActive(self.frameDelta[3][0][1])
            return
        if self.pin[3] < len(self.frameDelta[3]):
            if self.frameDelta[3][self.pin[3]][0] == self.frame:
                self.Object.setActive(self.frameDelta[3][self.pin[3]][1])
                self.pin[3] += 1
                self.OnKFrame(AnimeType.Active,self.frame)
    def proceedAlpha(self,st=False):
        if not self.ableAlpha:
            return
        if st:
            _sp = self.Sprite().sprite
            _sp.set_alpha(self.frameDelta[4][0][1])
            self.Sprite().setSprite(_sp)
            self.rcdAlpha = self.frameDelta[4][0][1]
        if self.pin[4] < len(self.frameDelta[4]):
            if self.frameDelta[4][self.pin[4]][0] == self.frame:
                self.pin[4] += 1
                self.OnKFrame(AnimeType.Alpha,self.frame)
            if self.pin[4] < len(self.frameDelta[4]):
                self.rcdAlpha += self.frameDelta[4][self.pin[4]][1]
                _sp = self.Sprite().sprite
                _sp.set_alpha(max(0,min(int(self.rcdAlpha),255)))
                self.Sprite().setSprite(_sp)
                #print(max(0,min(int(self.rcdAlpha),255)))
    def destroy(self):
        if not self.timer and self.aniOp == AnimeOp.Reset:
            self.proceedPos(True)
            self.proceedScale(True)
            self.proceedSprite(True)
            self.proceedActive(True)
            self.proceedAlpha(True)
        animeManager.safeDelAnime(self.id)
        from .IAnime import IAnime
        if isinstance(self.Object,IAnime):
            self.Object.AniDestroy()

class AnimeInfo:
    def __init__(self,las):
        self.lasTime = las
        self.spriteChange = True
        self.commonSprite = True
        self.timer = False
        self.ableAlpha = False

        self.posKFrame = []
        self.scaleKFrame = []
        self.spriteKFrame = []
        self.activeKFrame = []
        self.alphaKFrame = []
    def add(self,typ,keyF,val):
        if typ == AnimeType.Pos:
            self.posKFrame.append((keyF,val))
        elif typ == AnimeType.Scale:
            self.scaleKFrame.append((keyF,val))
        elif typ == AnimeType.Sprite:
            self.spriteKFrame.append((keyF,val))
        elif typ == AnimeType.Active:
            self.activeKFrame.append((keyF,val))
        elif typ == AnimeType.Alpha:
            self.alphaKFrame.append((keyF,val))
        return self
    def addDelay(self,delay):
        return self.add(AnimeType.Active,0,False).add(AnimeType.Active,delay,True)
    def disableSprite(self):
        self.spriteChange = False
        return self
    def uncommonSprite(self):
        self.commonSprite = False
        return self
    def setTimer(self):
        self.timer = True
        return self
    def enableAlpha(self):
        self.ableAlpha = True
        return self
    def finish(self):
        self.posKFrame.sort(key=lambda x:x[0])
        self.scaleKFrame.sort(key=lambda x:x[0])
        self.spriteKFrame.sort(key=lambda x:x[0])
        self.activeKFrame.sort(key=lambda x:x[0])
        self.alphaKFrame.sort(key=lambda x:x[0])
        return self
