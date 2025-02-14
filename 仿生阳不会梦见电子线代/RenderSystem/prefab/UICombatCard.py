from .UICard import *
from .UICharacter import CharFace
from AnimeSystem.animes.CardDiceRollingAnime import CardDiceRollingAnime_DiceImg,CardDiceRollingAnime_DiceText
from AnimeSystem.IAnime import *

from enum import Enum

class CombatDiceState(Enum):
    Unrolled = 1
    Rolled = 2

class UICombatCard(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.face = CharFace.Right
        self.addChild(UICombatCardBackGround("BG",self.screen,-20))
        self.addChild(UICombatCardRollingDiceBG("rdiceBG",self.screen,-10))
        self.addChild(UICombatCardBackGround("BGmask",self.screen,3))
        self.addChild(UICombatCardImage("image",self.screen,0))
        self.addChild(UICombatDice("rollingDice",self.screen,40))
        self.addChild(UICombatDiceArray("waitArray",self.screen,20))
        self.addChild(UICombatCardTitle("title",self.screen,20))

        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("BG").setPos(Vector2.Zero())
        self.findChild("BGmask").setPos(Vector2.Zero())
        self.findChild("rdiceBG").setPos(Vector2(-130,-60)*self.worldScale()*(Vector2(-1,1) if self.face == CharFace.Left else Vector2.One()))
        self.findChild("image").setPos(Vector2(0,30)*self.worldScale())
        self.findChild("rollingDice").setPos(Vector2(-130,-60)*self.worldScale()*(Vector2(-1,1) if self.face == CharFace.Left else Vector2.One()))
        self.findChild("title").setPos(Vector2(0,-90)*self.worldScale())
        self.findChild("waitArray").setPos(Vector2(0,-60)*self.worldScale())
        self.findChild("waitArray").setScale(Vector2(0.6,0.6))
    def setValue(self,dit):
        self.face = dit["face"]
        self.findChild("BG").setValue("combatCardBackground.png")
        self.findChild("BGmask").setValue("combatCardFrame.png")
        self.findChild("rdiceBG").setValue("combatCardRollingDice.png")
        self.findChild("image").setValue(dit["cardImg"])
        self.findChild("rollingDice").setValue(dit["rollingDice"],True)
        self.findChild("title").setValue(dit["cardTitle"])
        self.findChild("waitArray").setValue(dit["waitDiceArray"])

class UICombatCardBackGround(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def setValue(self,img):
        self.setImage(img)
        self.setScale(Vector2(1.2,1.2))

class UICombatCardRollingDiceBG(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def setValue(self,img):
        self.preSize = Vector2(75,75)
        self.setImage(self.preResize(img))

class UICombatCardImage(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(180,120)
    def setValue(self,img):
        self.setImage(self.preResize("cardImg/"+img))

class UICombatCardTitle(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontCardTitle)
        self.setShadeColor(Data.fonts.ColorBlack)
        self.setColor(Data.fonts.ColorWhite)
    def setValue(self,title):
        self.setText(title,Data.fonts.FontRender.Outline)

class UIDiceRangeText(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontDiceNum)
        #self.setShadeColor(Data.fonts.ColorBlack)
    def setValue(self,dicedit):
        self.setColor(Data.fonts.ColorYellow if dicedit["category"] == DiceCategory.Counter 
                      else Data.fonts.ColorBlue if dicedit["category"] == DiceCategory.Defense
                      else Data.fonts.ColorRed)
        self.setText(str(dicedit["minDice"])+"-"+str(dicedit["maxDice"]),Data.fonts.FontRender.Null)
class UIDicePointText(Text):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.setFont(Data.fonts.FontMana)
        self.setShadeColor(Data.fonts.ColorBlack)
    def setValue(self,dicedit,isOnRoll):
        self.setColor(Data.fonts.ColorYellow if dicedit["category"] == DiceCategory.Counter 
                      else Data.fonts.ColorBlue if dicedit["category"] == DiceCategory.Defense
                      else Data.fonts.ColorBrightRed)
        self.setText(str(dicedit["dicePoint"]),Data.fonts.FontRender.Outline)
        self.setActive(False)
        if isOnRoll:
            self._anime = CardDiceRollingAnime_DiceText(self)
class UIDiceImage(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.preSize = Vector2(75,75)
    def setValue(self,dicedit,isOnRoll):
        filename = None
        for e in DiceType:
            if e == dicedit["diceType"]:
                filename = "dice_"+e.value+("_counter" if dicedit["isCounter"] else "")+".png"
        self.setImage(self.preResize(filename))
        if isOnRoll:
            self._anime = CardDiceRollingAnime_DiceImg(self,
                self.preResize("combatDiceRolled_Counter.png") if dicedit["category"] == DiceCategory.Counter
                else self.preResize("combatDiceRolled_Defense.png") if dicedit["category"] == DiceCategory.Defense
                else self.preResize("combatDiceRolled_Attack.png"))

class UICombatDice(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UIDiceRangeText("rangeText",self.screen,0))
        self.addChild(UIDicePointText("pointText",self.screen,20))
        self.addChild(UIDiceImage("image",self.screen,10))

        self.setBaseRect(pygame.rect.Rect(0,0,60,60))

        self.isOnRoll = False
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("rangeText").setPos(Vector2(0,-30)*self.worldScale())
        self.findChild("pointText").setPos(Vector2(0,3)*self.worldScale())
    def setValue(self,dicedit,isOnRoll = False):
        self.diceCategory =  (DiceCategory.Counter if dicedit["isCounter"] else DiceCategory.Defense if (dicedit["diceType"] == DiceType.Block or dicedit["diceType"] == DiceType.Evade) else DiceCategory.Attack)
        dicedit["category"] = self.diceCategory

        self.isOnRoll = isOnRoll
        self.findChild("rangeText").setValue(dicedit)
        if isOnRoll:
            self.findChild("pointText").setValue(dicedit,isOnRoll)
        self.findChild("image").setValue(dicedit,isOnRoll)
    def AniActivate(self):
        if not self.isOnRoll:
            return
        self.findChild("image").AniActivate()
        self.findChild("pointText").AniActivate()
    
class UICombatDiceArray(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),10
        ))
    def setValue(self,dicelist):
        self.children.clear()
        index = 0
        for dice in dicelist:
            _dice = UICombatDice("waitDice"+str(index),self.screen,0)
            _dice.setValue(dice)
            _dice.findChild("pointText").setActive(False)
            self.addChild(_dice)
            index += 1
        self.posSetChildren()
