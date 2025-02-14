from RenderSystem.CanvasAutosort import *
from RenderSystem.MutiLineText import *
from RenderSystem.Sprite import *

import Data.fonts

fontTitle = pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),50)
fontPara = pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),35)

#哦天哪怎么有人到最后才想起来写自动化生成元素的脚本

class UISignBoard(Canvas):
    def __init__(self, name, screen, priority,siz):
        self.size = siz
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UISignBoard_BG("BG",self.screen,-10,self.size()))
        self.addChild(UISignBoard_Content("content",self.screen,0))
    def getContent(self):
        _t = self.findChild("content")
        if isinstance(_t,UISignBoard_Content):
            return _t
        return UISignBoard_Content("_trash",self.screen,-100)
    def getContentLen(self):
        return len(self.getContent().children)
    def addTitle(self,txt):
        _obj = Text(self.getContentLen(),self.screen,-1000)
        _obj.setFont(fontTitle)
        _obj.setColor(Data.fonts.ColorWhite)
        _obj.setText(txt,Data.fonts.FontRender.Null)
        self.getContent().addChild(_obj)
        return self
    def addPara(self,txt):
        _obj = MutiLineText(self.getContentLen(),self.screen,0,int(self.size().x*0.9))
        _obj.setFont(fontPara)
        _obj.setColor(Data.fonts.ColorSimpleTip)
        _obj.setTexts(txt,Data.fonts.FontRender.Null)
        self.getContent().addChild(_obj)
        return self
    def addImage(self,img,siz):
        _obj = Sprite(self.getContentLen(),self.screen,0)
        _obj.setImage(_obj.preResize(img,siz()))
        self.getContent().addChild(_obj)
        return self

class UISignBoard_BG(Sprite):
    def __init__(self, name, screen, priority,siz):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize("UI\\infoBar.png",siz()))

class UISignBoard_Content(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(0,1),5
        ))

class UIBeginningGuide(UISignBoard):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, Vector2(800,600))
        self.addTitle(u"教程是什么？").addImage("UI\\teach.jpg",Vector2(432,432))

class UIBeginningRank(UISignBoard):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, Vector2(800,600))
        self.addTitle(u"这也要卷？").addImage("UI\\rank.png",Vector2(1192,930)*(1/2.5))

class UIBeginningExit(UISignBoard):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, Vector2(800,600))
        self.addPara("There supposed to be an exit here. But the exit went nowhere.")
class UIBeginningDev(UISignBoard):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, Vector2(800,600))
        self.addTitle(u"楼层指定司书").addPara(u"架构层：@NH37").addPara(u"渲染层：@NH37").addPara(u"战斗数据层：@bmwang").addPara(u"LLM层：@2Bpencil").addPara(u"数值层：OpenAI（？）").addPara(u"艺术层：原著AB包（主要？）").addPara(" ").addPara("碎碎念：考虑到项目工程量和开发时间，可能还存有恶性bug没有被发现，果咩呐塞")
