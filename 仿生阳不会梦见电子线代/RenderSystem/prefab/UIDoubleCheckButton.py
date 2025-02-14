from RenderSystem.Canvas import *
from RenderSystem.Sprite import *
from RenderSystem.Text import *

from AudioSystem.AudioManager import audioManager

class DoubleCheckButtonInfo:
    def __init__(self,btSize,iconLis,txtLis,colorLis,fnt):
        self.buttonSize = btSize
        self.iconLis = iconLis
        self.txtLis = txtLis
        self.colorLis = colorLis
        self.font = fnt

class UIDoubleCheckButton(Canvas):
    def __init__(self, name, screen, priority,btInfo):
        if isinstance(btInfo,DoubleCheckButtonInfo):
            self.btInfo = btInfo
        self.state = 0
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UIDoubleChckButton_Icon("icon",self.screen,-5,self.btInfo.iconLis,self.btInfo.buttonSize))
        self.addChild(UIDoubleCheckButton_Text("txt",self.screen,0,self.btInfo.txtLis,self.btInfo.colorLis,self.btInfo.font))
        self.setState(0)
    def setState(self,state):
        self.state = state
        self.findChild("icon").setState(state)
        self.findChild("txt").setState(state)
    def ResetState(self):
        self.setState(0)
    def OnClick(self, event):
        audioManager.AddEffect("ButtonClick")
        if self.state == 0:
            self.setState(1)
    def OnRightClick(self, event):
        audioManager.AddEffect("ButtonClick")
        self.ResetState()


class UIDoubleChckButton_Icon(Sprite):
    def __init__(self, name, screen, priority,lis,btSize):
        self.iconLis = lis
        self.state = None
        super().__init__(name, screen, priority)
        self.preSize = btSize()
    def setState(self,state):
        self.state = state
        self.setImage(self.preResize(self.iconLis[self.state]))

class UIDoubleCheckButton_Text(Text):
    def __init__(self, name, screen, priority,txtLis,colorLis,fnt):
        self.txtLis = txtLis
        self.colorLis = colorLis
        self.state = None
        super().__init__(name, screen, priority)
        self.setFont(fnt)
    def setState(self,state):
        self.state = state
        self.setColor(self.colorLis[state])
        self.setText(self.txtLis[state],Data.fonts.FontRender.Outline)


class UIExitSceneButton(UIDoubleCheckButton):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        super().__init__(name, screen, priority, DoubleCheckButtonInfo(
            Vector2(330,50),["UI\\buttonBG3.png","UI\\buttonSP3.png"],[u"合上书页",u"确认离开？"],
            [Data.fonts.ColorSimpleTip,Data.fonts.ColorRed],Data.fonts.FontButton3
        ))
        self.setBaseRect(pygame.Rect(0,0,330,50))
    def OnClick(self, event):
        audioManager.AddEffect("ButtonClick")
        if self.state == 0:
            self.setState(1)
        elif self.state == 1:
            self.scene.AtExitButtonClicked()
    