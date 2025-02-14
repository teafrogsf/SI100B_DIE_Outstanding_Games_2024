from .UILifeBar import *
from .UILight import *
from .UISpeedDice import *
from .UIBuffBar import *
from RenderSystem.Sprite import *
from RenderSystem.Canvas import *
from AnimeSystem.IAnime import *

from enum import Enum
import copy

class CharFace(Enum):
    Right = 1
    Left = 2
class CharSD(Enum):
    Common = "common"
    Move = "move"
    Hurt = "hurt"
    Block = "block"
    Evade = "evade"
    Slash = "slash"
    Pierce = "pierce"
    Blunt = "blunt"

    Aim = "aim"
    Fire = "fire"
    #Combat = "combat"
class CharState(Enum):
    Common = "common"
    Stagger = "stagger"
    Dead = "dead"

class UICharacter(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UICharSprite("charImg",self.screen,10))
        self.addChild(UILifeBarBlock("infoBar",self.screen,0))
        self.addChild(UISpeedDiceArray("diceArray",self.screen,20))
        self.addChild(UILightBlock("lightBlock",self.screen,0))
        self.addChild(UIBuffBarBlock("buffBar",self.screen,5))
        self.charId = None
        self.charTitle = None
        self.infoBar = None
        self.resisBar = None
        self.abilityDesq = None
        self.cardArray = None
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("infoBar").setPos(Vector2(0,120)*self.worldScale())
        self.findChild("infoBar").setScale(Vector2(0.85,0.85))
        self.findChild("diceArray").setPos(Vector2(0,-150)*self.worldScale())
        self.findChild("diceArray").setScale(Vector2(0.95,0.95))
        self.findChild("lightBlock").setPos(Vector2(0,-230)*self.worldScale())
        self.findChild("lightBlock").setScale(Vector2(0.6,0.6))
        self.findChild("buffBar").setScale(Vector2(1.3,1.3))
        self.findChild("buffBar").setPos(Vector2(-150,0)*self.worldScale()
                                         *(Vector2(-1,1) if self.findChild("charImg").face == CharFace.Right else Vector2.One()))
    def setValue(self,dit):
        '''
        Dict:
        -charId
        -char-name
             -state
             -face
        -infoBar
        -diceArray
        -cardArray
        -lightBlock
        '''   
        dit["diceArray"]["charId"] = dit["charId"]
        dit["cardArray"]["charId"] = dit["charId"]
        self.charId = dit["charId"]
        self.cardArray = copy.deepcopy(dit["cardArray"])
        self.infoBar = copy.deepcopy(dit["infoBar"])
        #print(self.cardArray)
        self.findChild("charImg").setValue(dit["char"]["name"],dit["char"]["state"],dit["char"]["face"])
        self.findChild("infoBar").setValue(dit["infoBar"])
        self.findChild("diceArray").setValue(dit["diceArray"])
        self.findChild("lightBlock").setValue(dit["lightBlock"])

        if "buff" in dit["infoBar"].keys():
            self.findChild("buffBar").setValue(dit["infoBar"]["buff"])
            self.findChild("buffBar").setPos(Vector2(-100,0)*self.worldScale()
                                         *(Vector2(-1,1) if self.findChild("charImg").face == CharFace.Right else Vector2.One()))
        
        if "resis" in dit["infoBar"].keys():
            self.resisBar = copy.deepcopy(dit["infoBar"]["resis"])
        if "abilityDesq" in dit.keys():
            self.abilityDesq = copy.deepcopy(dit["abilityDesq"])
        if "charTitle" in dit.keys():
            self.charTitle = dit["charTitle"]
    def RequestSetHighlightMana(self,num):
        dit = self.findChild("lightBlock").lightdit
        dit["full"] += dit["selected"]
        dit["selected"] = num
        dit["full"] -= dit["selected"]
        self.findChild("lightBlock").setValue(dit)
    def RequestBriefInfo(self):
        return {
            "charId":self.charId,
            "charTitle":self.charTitle,
            "name":self.findChild("charImg").charName,
            "resis":self.resisBar,
            "infoBar":self.infoBar,
            "abilityDesq":self.abilityDesq
        }
class UICharSprite(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)  
    def init(self):
        self.charName = None
        self.face = CharFace.Right
        self.SD = None
        self.listSD = {}
        self.preSize = Vector2(0,200)

        self.listSD_drawDelta = {}
    def setValue(self,name,state,face):
        if name != None:
            self.setCharacter(name)#Modified
        if state != None:
            self.setState(state)
        if face != None:
            self.setFace(face)
    def setCharacter(self,name):
        #print(name)
        if self.charName == name:
            return
        from GameDataManager import gameDataManager as gdm
        self.charName = name
        self.SD = None
        if not CheckImageFile("character\\"+name):
            name = "Malkuth"
        for e in CharSD:
            file = "character\\"+name+"\\"+name+"_"+e.value+".png"
            if CheckImageFile(file):
                self.listSD_drawDelta[e] = gdm.getCharSDAlter(name,e.value)
                self.setImage(file)
                if self.listSD_drawDelta[e] == None:
                    self.listSD[e] = self.preResize(self.sprite)
                else:
                    _rct = self.sprite.get_rect()
                    _ori = Vector2(_rct.width,_rct.height)
                    _fixHeight = 200
                    _fixWidth = _fixHeight*(self.listSD_drawDelta[e]["char_width"]/self.listSD_drawDelta[e]["char_height"])
                    _scale = Vector2(_fixWidth/self.listSD_drawDelta[e]["char_width"],_fixHeight/self.listSD_drawDelta[e]["char_height"])
                    self.listSD[e] = self.preResize(self.sprite,_ori*_scale)
                    #print(e,self.listSD_drawDelta[e]["focus_y"],_scale.y)
                    self.listSD_drawDelta[e]["focus_x"] *= _scale.x
                    self.listSD_drawDelta[e]["focus_y"] *= _scale.y
        self.setState(CharSD.Common)
    def setState(self,state):
        if self.SD == state:
            return
        if state in self.listSD.keys():
            self.SD = state
            self.setImage(self.listSD[state])
    def setFace(self,face):
        if self.face != face:
            self.face = face
            self.setRect()
    def setRect(self):
        super().setRect()
        from GameDataManager import gameDataManager as gdm
        if self.SD != None and self.listSD_drawDelta[self.SD] != None:
            #print(self.SD,self.listSD_drawDelta[self.SD]["focus_y"]*self.worldScale().y)
            self.rect.centerx = self.worldPosition().x - self.listSD_drawDelta[self.SD]["focus_x"]*self.worldScale().x*(-1 if self.face == CharFace.Left else 1)
            self.rect.centery = self.worldPosition().y - self.listSD_drawDelta[self.SD]["focus_y"]*self.worldScale().y
        if self.worldSprite != None:
            if self.face == CharFace.Left:
                self.worldSprite = pygame.transform.flip(self.worldSprite,True,False)
    def getCombatScene(self):
        from .UICombatCharacter import UICombatCharacter
        from RenderSystem.sceneRenderer.BattleCombatRenderer import BattleCombatRenderer
        from SceneSystem.BattleScene import BattleScene
        if isinstance(self.parent,UICombatCharacter):
            if isinstance(self.parent.parent,BattleCombatRenderer):
                if isinstance(self.parent.parent.scene,BattleScene):
                    return self.parent.parent.scene
        return None