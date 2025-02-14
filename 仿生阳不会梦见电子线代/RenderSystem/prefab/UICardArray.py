from .UICard import *
from RenderSystem.CanvasAutosort import *

class UICardArray(CanvasAutoSort):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, AutoSortType(
            Vector2.Zero(),Vector2(1,0),0
        ))
    def init(self):
        self.charId = None
        self.cardArray = []

        self.selectedCard = None
    def setValue(self,dit):
        isChangeChar = False
        if self.charId != dit["charId"]:
            self.charId = dit["charId"]
            isChangeChar = True
        self.cardArray = dit["cardArray"]

        self.setCard(isChangeChar)
    def setCard(self,isChangeChar):
        if isChangeChar:
            self.children.clear()
            for card in self.cardArray:
                self.addChild(UICard(card["cardId"],self.screen,0,card))
        else:
            lisname = [card.get("cardId",-1) for card in self.cardArray]
            lisUpdatedCard = []
            if -1 in lisname:
                raise ValueError("Unknown Id for some of the Cards")
            for card in self.cardArray:
                cardExist = False
                for child in self.children:
                    if child.cardId == card["cardId"]:
                        lisUpdatedCard.append(child)
                        child.setValue(card)
                        cardExist = True
                        break
                if not cardExist:
                    lisUpdatedCard.append(UICard(card["cardId"],self.screen,0,card))
            self.children.clear()
            for card in lisUpdatedCard:
                self.addChild(card)
        self.posSetChildren()
    def findCard(self,id):
        for child in self.children:
            if child.cardId == id:
                return child
    def AtSetDisplayType(self,id,typ):#call by children
        if typ == CardDisplayType.Small:
            self.findCard(id).setDisplayType(CardDisplayType.Small)
            if id == self.selectedCard:
                self.selectedCard = None
            self.autosort()
        else:
            if id != self.selectedCard:
                for child in self.children:
                    child.setDisplayType(CardDisplayType.Small)
                self.findCard(id).setDisplayType(CardDisplayType.Large)
                self.selectedCard = id
                self.autosort()
    def AtSelectedCard(self,id):#call by children
        self.parent.AtSelectedCard(self.charId,id)

class UIDisplayCard(UICard):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority, None)
        self.preventRay(True)
    def resetValue(self, dit):
        super().setValue(dit, True)
        self.setDisplayType(CardDisplayType.Large)