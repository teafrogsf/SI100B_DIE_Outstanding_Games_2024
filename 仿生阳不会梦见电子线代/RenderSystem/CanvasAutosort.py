from .Canvas import *
class AutoSortType:
    def __init__(self,startpoint,direction,spaceinline):
        self.direction = direction
        self.space_inline = spaceinline
        self.startpoint = startpoint
class CanvasAutoSort(Canvas):
    def __init__(self, name, screen, priority,sorttype):
        self.sortType = sorttype
        super().__init__(name, screen, priority)
    def setScale(self, scale):
        if super().setScale(scale):
            self.autosort()
    def addChild(self, object,sot=True):
        if super().addChild(object):
            if sot:
                self.autosort()
    def delChild(self, name,sot=True):
        if super().delChild(name):
            if sot:
                self.autosort()
    def forceClean(self):
        for child in self.children:
            child.Clean()
    def posSetChildren(self):
        super().posSetChildren()
        self.autosort()
    def elcsort(self,elm):
        return elm
    def autosort(self,ignoreActivity=False):
        self.forceClean()
        elm = []
        for child in self.children:
            if ignoreActivity:
                if hasattr(child,"rect") and child.rect != None:
                    elm.append(child)
            else:    
                if child.active and hasattr(child,"rect") and child.rect != None:
                    elm.append(child)
        elm = self.elcsort(elm)
        if self.sortType.direction().x == 1:
            sm = sum(e.rect.width for e in elm)
            sm += self.sortType.space_inline * (len(elm)-1)
            dy = self.sortType.direction().y/self.sortType.direction().x
            smy = (len(elm)-1)*dy/2
            stx = self.sortType.startpoint().x - sm/2
            sty = self.sortType.startpoint().y -smy
            for e in elm:
                stx += e.rect.width/2
                e.setPos(Vector2(int(stx),int(sty)))
                stx += e.rect.width/2 + self.sortType.space_inline
                sty += dy
        elif self.sortType.direction().y == 1:
            sm = sum(e.rect.height for e in elm)
            sm += self.sortType.space_inline * (len(elm)-1)
            dx = self.sortType.direction().x/self.sortType.direction().y
            smx = (len(elm)-1)*dx/2
            stx = self.sortType.startpoint().x - smx
            sty = self.sortType.startpoint().y- sm/2
            for e in elm:
                sty += e.rect.height/2
                e.setPos(Vector2(int(stx),int(sty)))
                sty += e.rect.height/2 + self.sortType.space_inline
                stx += dx