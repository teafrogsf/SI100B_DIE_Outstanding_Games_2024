from RenderSystem.Text import *
from RenderSystem.Sprite import *
from RenderSystem.Canvas import *
from RenderSystem.CanvasAutosort import *

from enum import Enum

class DmgType(Enum):
    Life = 1
    Stagger = 2
class DmgResis(Enum):
    Fatal = u"致命"
    Weak = u"脆弱"
    Normal = u"一般"
    Endured = u"耐受"
    Ineffective = u"抵抗"
    Null = u" "
    Immerse = u"免疫"


class UICombatCommonText(Text):
    def __init__(self,name,screen,priority,txt,color,_scale = Vector2.One()):
        self._txt = txt
        self._color = color
        self._scale = _scale
        super().__init__(name,screen,priority)
    def init(self):
        self.setColor(self._color)
        self.setFont(Data.fonts.FontDmgText)
        self.setText(self._txt,Data.fonts.FontRender.Outline)
        self.setScale(self._scale)

class UICombatCommonDmg(Canvas):
    def __init__(self, name, screen, priority,dmgType,dmgResis,dmgVal,_scale = Vector2.One()):
        self.dmgType = dmgType
        self.dmgResis = dmgResis
        self.dmgVal = dmgVal
        self._scale = _scale
        super().__init__(name, screen, priority)
    def init(self):
        
        _delta = ( 0 if self.dmgResis == DmgResis.Fatal else
                  -40 if self.dmgResis == DmgResis.Weak else
                  -80 if self.dmgResis == DmgResis.Normal or self.dmgResis == DmgResis.Null else
                  -120 if self.dmgResis == DmgResis.Endured else
                  -180
                )
        _color = ((lambda x = (Data.fonts.ColorRed): pygame.color.Color(x[0]+_delta,x[1],x[2]))()
                    if self.dmgType == DmgType.Life else
                    (lambda x = (Data.fonts.ColorYellow): pygame.color.Color(x[0]+_delta,x[1]+_delta,x[2]))())

        self.addChild(UICombatDmg("dmg",self.screen,10,_color,self.dmgVal))
        self.addChild(UICombatDmgText("dmgTxt",self.screen,0,_color,self.dmgResis))
        self.setScale(self._scale*(min(max(self.dmgVal/20,1),1.5)+(0.25 if self.dmgResis == DmgResis.Fatal else 0)))
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.findChild("dmgTxt").setPos(Vector2(0,-30)*self.worldScale())

class UICombatDmg(Text):
    def __init__(self, name, screen, priority,color,val):
        self.dmgColor = color
        self.dmgVal = val
        super().__init__(name, screen, priority)
    def init(self):
        self.setColor(self.dmgColor)
        self.setFont(Data.fonts.FontDmg)
        self.setText(str(self.dmgVal),Data.fonts.FontRender.Outline)

class UICombatDmgText(Text):
    def __init__(self, name, screen, priority,color,resis):
        self.dmgColor = color
        self.dmgResis = resis
        super().__init__(name, screen, priority)
    def init(self):
        self.setColor(self.dmgColor)
        self.setFont(Data.fonts.FontDmgText)
        self.setText(self.dmgResis.value,Data.fonts.FontRender.Outline)


class UICombatBuffDmg(CanvasAutoSort):
    def __init__(self, name, screen, priority,bufTyp,dmgVal,_scale = Vector2.One()):
        self.bufTyp = bufTyp
        self.dmgVal = dmgVal
        self._scale = _scale
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),0
        ))
    def init(self):
        from GameDataManager import gameDataManager
        _buf = gameDataManager.getBuff(self.bufTyp)
        self.addChild(UICombatBuffIcon("icon",self.screen,0,_buf["Icon"]))
        self.addChild(UICombatDmg("val",self.screen,10,(Data.fonts.ColorRed if not "Color" in _buf.keys() else _buf["Color"]),self.dmgVal))
        self.setScale(self._scale*Vector2(0.6,0.6))

class UICombatBuffIcon(Sprite):
    def __init__(self, name, screen, priority,bufIcon):
        super().__init__(name, screen, priority)
        self.setImage(bufIcon)

class UICombatCommonHeal(CanvasAutoSort):
    def __init__(self, name, screen, priority,typ,val, _scale = Vector2.One()):
        self.healType = typ
        self.healVal = val
        self._scale = _scale
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),0
        ))
    def init(self):
        if self.healType == DmgType.Stagger:
            icon = LoadImage("staggerGainIcon.png")
            color = Data.fonts.ColorStaggerGain
        else:
            icon = LoadImage("lifeGainIcon.png")
            color = Data.fonts.ColorLifeGain
        self.addChild(UICombatHealIcon("icon",self.screen,0,icon))
        self.addChild(UICombatDmg("txt",self.screen,0,color,"+"+str(self.healVal)))
        self.setScale(self._scale)
class UICombatHealIcon(Sprite):
    def __init__(self, name, screen, priority,icon):
        super().__init__(name, screen, priority)
        self.setImage(self.preResize(icon,Vector2(60,60)))