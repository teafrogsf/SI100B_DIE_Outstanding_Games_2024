from RenderSystem.CanvasAutosort import *
from RenderSystem.Text import *
from RenderSystem.MutiLineText import *

import copy,random

class UIGenProcess(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority,AutoSortType(
            Vector2.Zero(),Vector2(0,1),5
        ))
        self.rcdDit = None
        self.ranTxt = [
            u"司书正在翻找书页",
            u"司书正在烧书（？）",
            u"司书正在被掉落的书本砸中脑袋",
            u"司书正在往书页里塞闪避骰",
            u"司书正在用“精神鞭笞”替换书页的标题",
            u"司书正在污染关键词列表"
        ]
    def init(self):
        self.addChild(UIGenProcess_Dialog("dialog",self.screen,0))
        self.addChild(UIGenProcess_Text("mainTxt",self.screen,0))
        self.addChild(UIGenProcess_Text("desqTxt",self.screen,0))
    def setValue(self,dit):
        if self.rcdDit == None or dit["pageCnt"] != self.rcdDit["pageCnt"]:
            dit["mainTxt"] = random.sample(self.ranTxt,1)[0]
        else:
            dit["mainTxt"] = self.rcdDit["mainTxt"]
        self.rcdDit = copy.deepcopy(dit)
        self.findChild("mainTxt").setText(self.rcdDit["mainTxt"],Data.fonts.FontRender.Null)
        self.findChild("desqTxt").setText("当前收集第 "+str(self.rcdDit["pageCnt"])+" 张（"
                                          +str(self.rcdDit["pcs"])+"/"+str(self.rcdDit["pcsMax"])+"）",Data.fonts.FontRender.Null)
        self.autosort()
    def setDialog(self,txt):
        self.findChild("dialog").setTexts(txt,Data.fonts.FontRender.Null)
class UIGenProcess_Dialog(MutiLineText):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, 500, 5)
    def init(self):
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),25))
        self.setColor(Data.fonts.ColorWhite)
class UIGenProcess_Text(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(pygame.font.Font(Data.fonts.LoadFont(Data.fonts.ttf_Hp),40))
        self.setColor(Data.fonts.ColorSimpleTip)