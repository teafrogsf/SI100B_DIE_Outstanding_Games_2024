from RenderSystem.Sprite import *
from RenderSystem.CanvasAutosort import *

from enum import Enum
import copy

class StateLight(Enum):
    Full = 1
    OnUse = 2
    Empty = 3
    Selected = 4

class UILightBlock(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        self.lightlines = 2
        self.lightamt = None
        self.lightdit = None
        super().__init__(name, screen, priority,AutoSortType(
            Vector2.Zero,Vector2(0,1),0
        ))
    def init(self):
        for i in range(1,self.lightlines+1):
            self.addChild(UILightLine("lightline"+str(i),self.screen,0))
    def setValue(self,dit):
        '''
        Dict:
        -amt
        -full
        -onuse
        -empty
        -selected
        '''
        self.lightdit = copy.deepcopy(dit)
        self.lightamt = dit["amt"]
        lis = []
        lis.extend([StateLight.Full] * dit["full"])
        lis.extend([StateLight.Selected]*dit["selected"])
        lis.extend([StateLight.OnUse]*dit["onuse"])
        lis.extend([StateLight.Empty]*dit["empty"])
        lis.extend([StateLight.Empty]*(
            dit["amt"]-dit["full"]-dit["selected"]-dit["onuse"]-dit["empty"]
        ))
        if self.lightamt <= 5:
            self.findChild("lightline1").setValue([])
            self.findChild("lightline2").setValue(lis)
        elif self.lightamt <= 10:
            self.findChild("lightline1").setValue(lis[:5])
            self.findChild("lightline2").setValue(lis[5:])
        else:
            self.findChild("lightline1").setValue(lis[:self.lightamt//2])
            self.findChild("lightline2").setValue(lis[self.lightamt//2:])


class UILightLine(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        self.amt = 5
        self.maxiamt = 10
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero,Vector2(1,0),2
        ))
    def init(self):
        self.setBaseRect(pygame.rect.Rect(0,0,160,40))
        for i in range(1,self.maxiamt+1):
            self.addChild(UILight("light"+str(i),self.screen,0))
    def setValue(self,lis):
        self.amt = min(len(lis),self.maxiamt)
        for i in range(self.amt):
            self.children[i].setActive(True)
            self.children[i].setState(lis[i])
        for i in range(self.amt,self.maxiamt):
            self.children[i].setActive(False)
        self.autosort()

class UILight(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.state = None
        self.setState(StateLight.Empty)
    def setState(self,state):
        if self.state == state:
            return
        self.state = state
        if state == StateLight.Full:
            self.setImage("lightFull.png")
        elif state == StateLight.Selected:
            self.setImage("lightSelected.png")
        elif state == StateLight.OnUse:
            self.setImage("lightOnUse.png")
        elif state == StateLight.Empty:
            self.setImage("lightEmpty.png")