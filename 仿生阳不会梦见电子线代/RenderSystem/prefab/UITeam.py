from .UICharacter import *
from .UIResisBar import *
from RenderSystem.Canvas import *
from RenderSystem.RotationText import *
from RenderSystem.MutiLineText import *
from RenderSystem.prefab.UICombatText import DmgResis

from enum import Enum

class UICharacterCollection(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.teamName = None
        self.maxiChar = 5
        self.charPosBasis = [
            Vector2(120,90),
            Vector2(120,-70),
            Vector2(0,0),
            Vector2(-150,90),
            Vector2(-150,-70)
        ]
        self.charPosXAxisOffset = Vector2(40,0)
        self.teamFace = CharFace.Left
        for i in range(self.maxiChar):
            self.addChild(UICharacter("char"+str(i),self.screen,0))
            self.findChild("char"+str(i)).setScale(Vector2(0.4,0.4))
            if i == 0 or i == 3:
                self.findChild("char"+str(i)).setPriority(10)
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        for i in range(self.maxiChar):
            self.findChild("char"+str(i)).setPos(self.charPosBasis[i]*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Right else Vector2.One()))
        self.findChild("char1").move(self.charPosXAxisOffset*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Right else Vector2.One()))
        self.findChild("char4").move(self.charPosXAxisOffset*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Right else Vector2.One()))
    def setValue(self,dit):
        self.teamName = dit["teamName"]
        self.teamFace = dit["teamFace"]
        _priorChar = []
        _fixedPos = []
        for i in range(min(len(dit["charList"]),self.maxiChar)):
            dit["charList"][i]["char"]["face"] = self.teamFace
            if "pos" in dit["charList"][i].keys():
                _pos = dit["charList"][i]["pos"]-1
                if _pos in _fixedPos:
                    continue
                _fixedPos.append(_pos)
                _priorChar.append(i)
                self.findChild("char"+str(_pos)).setValue(dit["charList"][i])
                if dit["charList"][i]["isDead"]:
                    self.findChild("char"+str(_pos)).setActive(False)
                else: 
                    self.findChild("char"+str(_pos)).setActive(True)
        for i in range(min(len(dit["charList"]),self.maxiChar)):
            if not i in _priorChar:
                for _pos in range(self.maxiChar):
                    if not _pos in _fixedPos:
                        _fixedPos.append(_pos)
                        self.findChild("char"+str(_pos)).setValue(dit["charList"][i])
                        if dit["charList"][i]["isDead"]:
                            self.findChild("char"+str(_pos)).setActive(False)
                        else: 
                            self.findChild("char"+str(_pos)).setActive(True)
                        break
        for pos in range(self.maxiChar):
            if not pos in _fixedPos:
                self.findChild("char"+str(pos)).setActive(False)

        '''
        for i in range(min(len(dit["charList"]),self.maxiChar)):
            dit["charList"][i]["char"]["face"] = self.teamFace
            self.findChild("char"+str(i)).setValue(dit["charList"][i])
            if dit["charList"][i]["isDead"]:
                self.findChild("char"+str(i)).setActive(False)
            else: 
                self.findChild("char"+str(i)).setActive(True)
        for i in range(min(len(dit["charList"]),self.maxiChar),self.maxiChar):
            self.findChild("char"+str(i)).setActive(False)
        '''
        self.posSetChildren()

class UITeamInfoBar(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),0
        ))
        self.preventRay(True)
    def setInitValue(self,teamFace,lis):
        self.children.clear()
        self.teamFace = teamFace
        for dit in lis:
            self.addChild(UITeamCharacterInfoBar(dit["charId"],self.screen,0,self.teamFace))
            self.findChild(dit["charId"]).setValue({
                "charName":dit["char"]["name"],
                "life":(1000 if not "infoBar" in dit.keys() else dit["infoBar"]["life"]["num"]),
                "lifeMax":(514 if not "infoBar" in dit.keys() else dit["infoBar"]["life"]["maxinum"]),
                "emoLevel":(-1 if not "infoBar" in dit.keys() else dit["infoBar"]["emotion"]["emoLevel"]),
                "emoMaxNum":(5 if not "infoBar" in dit.keys() else dit["infoBar"]["emotion"]["emoMaxNum"]),
                "emoList":([] if not "infoBar" in dit.keys() else dit["infoBar"]["emotion"]["emoList"])
            })
    def setValue(self,charId,dit):
        if self.findChild(charId) != None:
            if "infoBar" in dit.keys() and "life" in dit["infoBar"].keys() and "emotion" in dit["infoBar"].keys():
                self.findChild(charId).setValue({
                    "life":dit["infoBar"]["life"]["num"],
                    "lifeMax":dit["infoBar"]["life"]["maxinum"],
                    "emoLevel":dit["infoBar"]["emotion"]["emoLevel"],
                    "emoMaxNum":dit["infoBar"]["emotion"]["emoMaxNum"],
                    "emoList":dit["infoBar"]["emotion"]["emoList"]
                    })

class UITeamCharacterInfoBar(Canvas):
    def __init__(self, name, screen, priority,teamFace):
        self.teamFace = teamFace
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UITeamCharacterInfoBack("BG",self.screen,-100,self.teamFace))
        self.addChild(UITeamCharacterHeadImage("charImg",self.screen,0,self.teamFace))
        self.addChild(UITeamLifeBarLine("life",self.screen,10,self.teamFace))
        self.addChild(UITeamEmotionBarLine("emotion",self.screen,5,self.teamFace))

        self.findChild("life").setScale(Vector2(0.5,0.5))
        self.findChild("emotion").setScale(Vector2(0.5,0.5))

        self.setBaseRect(self.findChild("BG").sprite.get_rect())

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("charImg").setPos(Vector2(-70,-10)*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Left else Vector2.One()))
        self.findChild("life").setPos(Vector2(5,5)*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Left else Vector2.One()))
        self.findChild("emotion").setPos(Vector2(-15,17)*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Left else Vector2.One()))
    def setValue(self,dit):
        if "charName" in dit.keys():
            self.findChild("charImg").setValue(dit["charName"],HeadImage.Small)
        self.findChild("life").setValue(dit["life"],dit["lifeMax"])
        self.findChild("emotion").setValue(dit["emoLevel"],dit["emoMaxNum"],dit["emoList"])

class HeadImage(Enum):
    Small = Vector2(40,40)
    Large = Vector2(100,100)
    Team = Vector2(60,60)

class UITeamCharacterInfoBack(Sprite):
    def __init__(self, name, screen, priority,teamFace):
        self.face = teamFace
        super().__init__(name, screen, priority)
    def init(self):
        self.setImage("teamCharInfoBar.png")
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)

class UITeamCharacterHeadImage(Sprite):
    def __init__(self, name, screen, priority,teamFace):
        self.face = teamFace
        self.rcdName = None
        super().__init__(name, screen, priority)
    def setValue(self,charName,typ):
        if self.rcdName != charName:
            self.rcdName = charName
            path = "character\\"+charName+"\\"+charName+"_head.png"
            if CheckImageFile(path):
                self.setImage(self.preResize(self.setImage(path),typ.value))
            #self.setImage(self.preResize(self.setImage("character\\"+"Malkuth"+"\\"+"Malkuth"+"_head.png"),typ.value))
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)

class UITeamLifeBarLine(Canvas):
    def __init__(self, name, screen, priority,teamFace):
        self.teamFace = teamFace
        super().__init__(name, screen, priority)
        self.addChild(UITeamLifeText("text",self.screen,5))
        self.addChild(UITeamLifeBar("bar",self.screen,0,self.teamFace))

        self.setBaseRect(pygame.rect.Rect(0,0,240,40))
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("text").setPos(Vector2(60,0)*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Left else Vector2.One()))
        self.findChild("bar").setPos(Vector2(-40,0)*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Left else Vector2.One()))
    def setValue(self,num,maxinum):
        self.findChild("text").setText(str(int(num)),Data.fonts.FontRender.Outline)
        self.findChild("bar").setPercentage(num/maxinum)
class UITeamLifeText(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontLife)
        self.setColor(Data.fonts.ColorRed)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setText(" ",Data.fonts.FontRender.Outline)
class UITeamLifeBar(BarSprite):
    def __init__(self, name, screen, priority,face):
        self.face = face
        super().__init__(name, screen, priority)
    def init(self):
        super().init()
        if self.face == CharFace.Right:
            self.setSlideChoice(BarSlideChoice.Right)
        else:
            self.setSlideChoice(BarSlideChoice.Left)
        self.setImage("teamLifeBar.png")
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)

EmotionLevel = {
    0:"0",1:"I",2:"II",3:"III",4:"IV",5:"V"
}
class EmotionType(Enum):
    Red = Data.fonts.ColorEmotionRed
    Green = Data.fonts.ColorEmotionGreen

class UITeamEmotionBarLine(Canvas):
    def __init__(self, name, screen, priority,teamFace):
        self.teamFace = teamFace
        super().__init__(name, screen, priority)
        self.addChild(UITeamEmotionText("text",self.screen,5))
        self.addChild(UITeamEmotionBar("bar",self.screen,0,self.teamFace))

        self.setBaseRect(pygame.rect.Rect(0,0,240,40))
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("text").setPos(Vector2(-80,-10)*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Left else Vector2.One()))
        self.findChild("bar").setPos(Vector2(40,0)*self.worldScale()*(Vector2(-1,1) if self.teamFace == CharFace.Left else Vector2.One()))
    def setValue(self,level,maxEmoNum,emoList):
        self.findChild("text").setText("x" if level<0 or level > 5 else EmotionLevel[level],Data.fonts.FontRender.Outline)
        self.findChild("bar").setValue(maxEmoNum,emoList)
class UITeamEmotionText(RotationText):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontEmotion)
        self.setColor(Data.fonts.ColorEmotionPurple)
        self.setShadeColor(Data.fonts.ColorWhite)
        self.setRotation(30)
        self.setText(" ",Data.fonts.FontRender.Outline)
class UITeamEmotionBar(Drawableobject):
    def __init__(self, name, screen, priority,face):
        self.face = face
        self.init()
        super().__init__(name, screen, priority)
    def init(self):
        self.emotionLine = pygame.surface.Surface((180,15), pygame.SRCALPHA)
    def setValue(self,maxEmoNum,emoList):
        self.emotionLine.fill([0,0,0,0])
        if maxEmoNum == 0:
            _width = 1
        else:
            _width = 180/maxEmoNum
        for i in range(len(emoList)):
            self.emotionLine.fill(emoList[i].value,rect = (_width*i+1,0,_width-1,15))
        self.sprite = self.emotionLine
        self.setRect()
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)


class UICharacterBriefInfo(Canvas):
    def __init__(self, name, screen, priority,teamFace):
        self.face = teamFace
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UICharacterBriefInfo_BG("BG",self.screen,-5,self.face))
        self.addChild(UITeamCharacterHeadImage("head",self.screen,0,self.face))
        self.addChild(UICharacterTitle("title",self.screen,5))
        self.addChild(UIResisBar("resisBar",self.screen,5))
        self.addChild(UICharacterBriefInfo_DesqBar("desqBar",self.screen,5))

        self.posSetChildren()
    def setValue(self,dit):
        self.findChild("head").setValue(dit["name"],HeadImage.Large)
        self.findChild("title").setValue(dit["charTitle"])
        if dit["resis"] != None:
            self.findChild("resisBar").setValue(dit["resis"])
        else:
            self.findChild("resisBar").setValue({
                "life":{
                    "slash":DmgResis.Fatal,
                    "pierce":DmgResis.Ineffective,
                    "blunt":DmgResis.Normal
                },
                "stagger":{
                    "slash":DmgResis.Weak,
                    "pierce":DmgResis.Endured,
                    "blunt":DmgResis.Immerse
                }
            })
        self.findChild("desqBar").setValue(dit)
    def posSetChildren(self):
        super().posSetChildren()

        self.findChild("head").setPos(Vector2(-75,-170)*self.worldScale()*(Vector2(-1,1) if self.face == CharFace.Right else Vector2.One()))
        self.findChild("resisBar").setPos(Vector2(60,-150)*self.worldScale()*(Vector2(-1,1) if self.face == CharFace.Right else Vector2.One()))
        self.findChild("resisBar").setScale(Vector2(1,1)*self.worldScale())
        self.findChild("title").setPos(Vector2(-75,-80)*self.worldScale()*(Vector2(-1,1) if self.face == CharFace.Right else Vector2.One()))

class UICharacterTitle(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontSimpleTip)
        self.setColor(Data.fonts.ColorSimpleTip)
    def setValue(self,txt):
        self.setText(txt,Data.fonts.FontRender.Outline)

class UICharacterBriefInfo_BG(Sprite):
    def __init__(self, name, screen, priority,face):
        self.face = face
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("teamCharBriefInfoBar.png",Vector2(300,480)))
    def setRect(self):
        super().setRect()
        if self.worldSprite != None:
            if self.face == CharFace.Right:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)

class UICharacterBriefInfo_DesqBar(CanvasAutoSort):
    def __init__(self, name, screen, priority,width = 240):
        self.lineWidth = width
        self.rcdChar = None
        super().__init__(name, screen, priority,AutoSortType(
            Vector2.Zero(),Vector2(0,1),3
        ))
    def setValue(self,dit,ForceUpdate = False):
        if dit["charId"] == self.rcdChar and not ForceUpdate:
            return
        self.rcdChar = dit["charId"]
        self.children.clear()
        if dit["abilityDesq"] == None:
            dit["abilityDesq"] = []
            #return
        _p = 0
        _height = 0
        for desq in dit["abilityDesq"]:
            self.addChild(UICharacterBriefInfo_Desq("ab"+str(_p),self.screen,0,desq,self.lineWidth))
            _height += self.findChild("ab"+str(_p)).rect.height
            _p += 1
        self.setPos(Vector2(0,10+_height/2)*self.worldScale())

class UICharacterBriefInfo_Desq(MutiLineText):
    def __init__(self, name, screen, priority,txt,width=240):
        self._txt = txt
        super().__init__(name, screen, priority,width,1)
    def init(self):
        self.setFont(Data.fonts.FontUICharAbility)
        self.setColor(Data.fonts.ColorSimpleTip)
        self.setTexts(self._txt,Data.fonts.FontRender.Null)