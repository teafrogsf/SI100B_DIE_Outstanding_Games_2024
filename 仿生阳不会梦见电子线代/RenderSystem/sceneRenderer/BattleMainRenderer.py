from RenderSystem.prefab.UICardArray import *
from RenderSystem.prefab.UITeam import *
from RenderSystem.prefab.UICurves import *
from RenderSystem.Canvas import *
from RenderSystem.Sprite import *

from Data.coder import *

from enum import Enum

class BattleTeam(Enum):
    Player = 2
    Enemy = 1

class BattleMainRenderer(Canvas):
    def __init__(self, name, screen, priority,scene):
        self.scene = scene
        super().__init__(name, screen, priority)
    def init(self):
        self.addChild(UICharacterCollection("charTeam1",self.screen,0))
        self.addChild(UICharacterCollection("charTeam2",self.screen,0))
        self.addChild(UITeamInfoBar("infoTeam1",self.screen,10))
        self.addChild(UITeamInfoBar("infoTeam2",self.screen,10))
        self.addChild(UICardArray("cardArray",self.screen,15))
        self.addChild(UIBattleBackground("BG",self.screen,-100))
        self.addChild(UICurveManager("curveManager",self.screen,20))
        self.addChild(UIDisplayCard("displayCardTeam1",self.screen,30))
        self.addChild(UIDisplayCard('displayCardTeam2',self.screen,30))
        self.addChild(UICharacterBriefInfo("charBriefInfoTeam1",self.screen,20,CharFace.Left))
        self.addChild(UICharacterBriefInfo("charBriefInfoTeam2",self.screen,20,CharFace.Right))

        self.controlSys ={
            "DisplayCardArray":False
        }
        self.storedData = {
            "PlayerTeam":BattleTeam.Player.value,
            "SelectedDiceId":None,
            "SelectedCardId":None,
            "DisplayCardArrayCharId":None,
            "PointerEnterDiceId":None#containing the cardDit
        }
        self.posSetChildren()
    def posSetChildren(self):
        super().posSetChildren()
        self.setPos(Vector2(720,360))
        self.findChild("BG").setPos(Vector2.Zero())
        self.findChild("curveManager").setPos(Vector2.Zero())
        self.findChild("cardArray").setPos(Vector2(0,270))
        self.findChild("charTeam1").setPos(Vector2(-300,30))
        self.findChild("charTeam2").setPos(Vector2(300,30))
        self.findChild("infoTeam1").setPos(Vector2(-620,220))
        self.findChild("infoTeam2").setPos(Vector2(620,220))
        self.findChild("displayCardTeam1").setPos(Vector2(-270,-220))
        self.findChild("displayCardTeam2").setPos(Vector2(270,-220))
        self.findChild("charBriefInfoTeam1").setPos(Vector2(-580,-150))
        self.findChild("charBriefInfoTeam2").setPos(Vector2(580,-150))

        self.findChild("cardArray").setScale(Vector2(0.5,0.5))
        self.findChild("displayCardTeam1").setScale(Vector2(0.8,0.8))
        self.findChild("displayCardTeam2").setScale(Vector2(0.8,0.8))
        self.findChild("charBriefInfoTeam1").setScale(Vector2(0.85,0.85))
        self.findChild("charBriefInfoTeam2").setScale(Vector2(0.85,0.85))
    def rayCast(self, event):
        super().rayCast(event)
        if event.type == pygame.MOUSEMOTION:
            self.modifyDynamicSelectingCurve(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            self._refresh(None)
    def update(self):#60fps
        super().update()
        self.findChild("cardArray").setActive(self.controlSys["DisplayCardArray"])

        dice1Info = None if self.storedData["SelectedDiceId"] == None else decodeDiceIdInfo(self.storedData["SelectedDiceId"])
        dice2Info = None if self.storedData["PointerEnterDiceId"] == None else decodeDiceIdInfo(self.storedData["PointerEnterDiceId"])
        if dice1Info == None and dice2Info == None:
            self.findChild("displayCardTeam1").setActive(False)
            self.findChild("displayCardTeam2").setActive(False)
            self.findChild("charBriefInfoTeam1").setActive(False)
            self.findChild("charBriefInfoTeam2").setActive(False)
        elif dice1Info == None or dice2Info == None:
            diceInfo = dice1Info if dice1Info != None else dice2Info
            self.findChild("charBriefInfoTeam"+str(3-diceInfo[0])).setActive(False)
            self.findChild("charBriefInfoTeam"+str(diceInfo[0])).setActive(True)
            self.findChild("charBriefInfoTeam"+str(diceInfo[0])).setValue(
                self.findCharacter(diceInfo[1]).RequestBriefInfo()
            )

            self.findChild("displayCardTeam"+str(3-diceInfo[0])).setActive(False)
            carddit = self.findDice(diceInfo[2]).cardDit
            if carddit == None:
                self.findChild("displayCardTeam"+str(diceInfo[0])).setActive(False)
            else:
                self.findChild("displayCardTeam"+str(diceInfo[0])).setActive(True)
                self.findChild("displayCardTeam"+str(diceInfo[0])).resetValue(carddit)
        else:
            if dice1Info[0] == dice2Info[0]:
                dicesInfo = [dice2Info]
                self.findChild("displayCardTeam"+str(3-dice2Info[0])).setActive(False)
                self.findChild("charBriefInfoTeam"+str(3-dice2Info[0])).setActive(False)
            else:
                dicesInfo = [dice1Info,dice2Info]
            for diceInfo in dicesInfo:
                self.findChild("charBriefInfoTeam"+str(diceInfo[0])).setActive(True)
                self.findChild("charBriefInfoTeam"+str(diceInfo[0])).setValue(
                    self.findCharacter(diceInfo[1]).RequestBriefInfo()
                )

                carddit = self.findDice(diceInfo[2]).cardDit
                if carddit == None:
                    self.findChild("displayCardTeam"+str(diceInfo[0])).setActive(False)
                else:
                    self.findChild("displayCardTeam"+str(diceInfo[0])).setActive(True)
                    self.findChild("displayCardTeam"+str(diceInfo[0])).resetValue(carddit)

        #TODO
        #highlight Info display
    def Render(self):#30fps
        self.draw()
    def setValue(self,dit):
        self._refresh(None)
        dit["charTeam1"]["teamFace"] = CharFace.Left
        dit["charTeam2"]["teamFace"] = CharFace.Right
        self.findChild("BG").setValue(dit["BG"])
        self.findChild("charTeam1").setValue(dit["charTeam1"])
        self.findChild("charTeam2").setValue(dit["charTeam2"])
        self.findChild("infoTeam1").setInitValue(CharFace.Left,dit["charTeam1"]["charList"])
        self.findChild("infoTeam2").setInitValue(CharFace.Right,dit["charTeam2"]["charList"])
        if self.controlSys["DisplayCardArray"]:
            self.setValue_CardArray(self.storedData["DisplayCardArrayCharId"])
        self.findChild("curveManager").genCurve(self.gatherDiceCurves())
    def AtSelectedDice(self,diceId):#call by children
        #print(diceId)
        if self.storedData["SelectedDiceId"] == diceId:
            self._refresh(diceId)
        else:
            if self.storedData["SelectedDiceId"] == None:
                self._firstTimeSelectDice(diceId)
            else:
                if self.storedData["SelectedCardId"] == None:
                    self._firstTimeSelectDice(diceId)
                else:
                    self._secondTimeSelectDice(diceId)
    def AtDeselectedDice(self,diceId):
        self.OperationDeselectCard(diceId)
    def AtHoverDice(self,diceId):
        #print(diceId)
        if self.storedData["PointerEnterDiceId"] != None:
            if self.storedData["PointerEnterDiceId"] != self.storedData["SelectedDiceId"]:
                self.findChild("curveManager").deactiveDice(self.storedData["PointerEnterDiceId"])    
        self.storedData["PointerEnterDiceId"] = diceId
        if diceId != None:
            self.findChild("curveManager").activeDice(diceId)
    def AtSelectedCard(self,charId,cardId):#call by children
        if self.storedData["SelectedDiceId"] == None:
            return
        if self.findDice(self.storedData["SelectedDiceId"]).RequestPageState():
            return
        if self.OperationCardAvilableCheck(charId,cardId):
            if self.storedData["SelectedCardId"] != None:
                self.findHandCard(self.storedData["SelectedCardId"]).RequestSelectedState(False)
            self.storedData["SelectedCardId"] = cardId
            self.findHandCard(self.storedData["SelectedCardId"]).RequestSelectedState(True)
            self.findCharacter(charId).RequestSetHighlightMana(self.findHandCard(self.storedData["SelectedCardId"]).mana)
    def _refresh(self,diceId):
        self.modifyDynamicSelectingCurve(None,-1)
        self.findChild("displayCardTeam1").setActive(False)
        self.findChild("displayCardTeam2").setActive(False)
        self.findChild("charBriefInfoTeam1").setActive(False)
        self.findChild("charBriefInfoTeam2").setActive(False)
        if self.storedData["SelectedDiceId"] != None:
            self.findDice(self.storedData["SelectedDiceId"]).RequestSelectedState(False)
            self.findChild("curveManager").deactiveDice(self.storedData["SelectedDiceId"])    
        if self.storedData["SelectedCardId"] != None:
            self.findHandCard(self.storedData["SelectedCardId"]).RequestSelectedState(False)
            if self.storedData["SelectedDiceId"] != None:
                self.findCharacter(decodeDiceIdInfo(self.storedData["SelectedDiceId"])[1]).RequestSetHighlightMana(0)
        self.storedData["SelectedDiceId"] = None
        self.storedData["SelectedCardId"] = None
        self.controlSys["DisplayCardArray"] = False
    def _firstTimeSelectDice(self,diceId):
        if self.storedData["SelectedDiceId"] != None:
            self.findDice(self.storedData["SelectedDiceId"]).RequestSelectedState(False)
            self.findChild("curveManager").deactiveDice(self.storedData["SelectedDiceId"])
        self.findDice(diceId).RequestSelectedState(True)
        self.findChild("curveManager").activeDice(diceId)
        self.storedData["SelectedDiceId"] = diceId
        #print(decodeDiceIdInfo(diceId)[0])
        #print(self.storedData["PlayerTeam"])
        if decodeDiceIdInfo(diceId)[0] == self.storedData["PlayerTeam"] and self.findDice(diceId).RequestDiceStateNormal():
            self.setValue_CardArray(decodeDiceIdInfo(diceId)[1])
            self.controlSys["DisplayCardArray"] = True
        else:
            self.controlSys["DisplayCardArray"] = False
    def _secondTimeSelectDice(self,diceId):
        self.findHandCard(self.storedData["SelectedCardId"]).RequestSelectedState(False)
        self.findCharacter(decodeDiceIdInfo(self.storedData["SelectedDiceId"])[1]).RequestSetHighlightMana(0)
        if decodeDiceIdInfo(diceId)[0] == self.storedData["PlayerTeam"]:
            self.storedData["SelectedCardId"] = None
        else:
            self.OperationAttackLink(self.storedData["SelectedDiceId"],self.storedData["SelectedCardId"],diceId)
            if self.storedData["SelectedDiceId"] != None:
                self.findDice(self.storedData["SelectedDiceId"]).RequestSelectedState(False)
                self.findChild("curveManager").deactiveDice(self.storedData["SelectedDiceId"])   
            if self.storedData["SelectedCardId"] != None:
                if self.findHandCard(self.storedData["SelectedCardId"]) != None:
                    self.findHandCard(self.storedData["SelectedCardId"]).RequestSelectedState(False)
            self.storedData["SelectedDiceId"] = None
            self.storedData["SelectedCardId"] = None
            self.controlSys["DisplayCardArray"] = False
    def findDice(self,diceId):
        for cname in ["charTeam1","charTeam2"]:
            for char in self.findChild(cname).children:
                for dice in char.findChild("diceArray").children:
                    if dice.diceId == diceId:
                        return dice
        return None
    def findCharacter(self,charId):
        for cname in ["charTeam1","charTeam2"]:
            for char in self.findChild(cname).children:
                if char.charId == charId:
                    return char
        return None
    def findHandCard(self,cardId):
        for card in self.findChild("cardArray").children:
            if card.cardId == cardId:
                return card
        return None
    def setValue_CardArray(self,charId):
        #print(len(self.findCharacter(charId).cardArray["cardArray"]))
        self.storedData["DisplayCardArrayCharId"] = charId
        self.findChild("cardArray").setValue(self.findCharacter(charId).cardArray)
    def gatherDiceCurves(self):
        dit = {
            "dicePos":{},
            "curveList":[]
        }
        for cname in ["charTeam1","charTeam2"]:
            for char in self.findChild(cname).children:
                if char.active == False:
                    continue
                for dice in char.findChild("diceArray").children:
                    dit["dicePos"][dice.diceId] = dice.worldPosition()
                    if dice.targets != None:
                        #print(dice.diceId,dice.targets)
                        if isinstance(dice.targets,list):
                            for target in dice.targets:
                                dit["curveList"].append({
                                    "startId":dice.diceId,"endId":target,"curveType":(
                                        CurveType.Clash if dice.isClashing == True else
                                        CurveType.Enemy if cname == "charTeam1" else
                                        CurveType.Player
                                    )
                                })
                        else:
                            dit["curveList"].append({
                                    "startId":dice.diceId,"endId":dice.targets,"curveType":(
                                        CurveType.Clash if dice.isClashing == True else
                                        CurveType.Enemy if cname == "charTeam1" else
                                        CurveType.Player
                                    )
                                })
        #print(dit)
        return dit
    def modifyDynamicSelectingCurve(self,event,delete=0):
        if delete == -1:
            self.findChild("curveManager").modifyConstantCurve(1,None,None,None,None,-1)
            return
        if self.storedData["SelectedDiceId"] == None or self.storedData["SelectedCardId"] == None:
            self.findChild("curveManager").modifyConstantCurve(1,None,None,None,None,-1)
            return
        self.findChild("curveManager").modifyConstantCurve(1,self.findDice(self.storedData["SelectedDiceId"]).worldPosition(),
                                                           Vector2(event.pos[0],event.pos[1]),False,CurveType.Player) 
    def OperationAttackLink(self,sourceDiceId,cardId,targetDiceId):
        print("AttackLink",sourceDiceId,cardId,targetDiceId)
        if self.scene != None:
            self.scene.battleSystem.SelectPage(
                decodeDiceIdInfo(sourceDiceId)[1],decodeDiceIdInfo(targetDiceId)[1],
                sourceDiceId,targetDiceId,
                cardId
                )
            self.scene.AtValueChanged()
        self.modifyDynamicSelectingCurve(None,-1)
    def OperationDeselectCard(self,sourceDiceId):
        print("Deselect",sourceDiceId)
        if decodeDiceIdInfo(sourceDiceId)[0] != BattleTeam.Player.value:
            return
        if self.scene != None:
            self.scene.battleSystem.DeselectPage(
                decodeDiceIdInfo(sourceDiceId)[1],
                sourceDiceId
            )
            self.scene.AtValueChanged()
    def OperationCardAvilableCheck(self,charId,cardId):
        print("CardAvailableCheck",charId,cardId)
        if self.scene != None:
            return self.scene.battleSystem.CheckPage(charId,cardId)

class UIBattleBackground(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.rcdImg = None
        self.preSize = Vector2(1440,720)
    def setValue(self,img):
        if self.rcdImg != img:
            self.setImage(img)
            self.setImage(self.preResize(self.sprite))
    