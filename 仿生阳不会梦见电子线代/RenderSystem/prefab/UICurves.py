from RenderSystem.Canvas import *
from RenderSystem.RenderableObject import *

import Data.fonts
from Data.bezier_curve import *
from enum import Enum
import random

class CurveType(Enum):
    Enemy = Data.fonts.ColorBrightRed
    Player = Data.fonts.ColorBrightBlue
    Clash = Data.fonts.ColorClashingYellow

class UICurveManager(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.constantCurveIndex = []
        self.diceActive = []
        self.diceCurveIndex = {}
        self.curveCache = {}
        self.storedDicePos = {}
    def genCurveId(self,diceId1,diceId2):
        if diceId1 > diceId2:
            diceId2,diceId1 = diceId1,diceId2
        newid = diceId1*(10 ** 6)+diceId2
        newid *= 100
        newid += random.randint(0,99)
        return newid
    def genCurve(self,dit):
        _dicepos = dit["dicePos"]
        _curveList = dit["curveList"]
        #print(_curveList)
        _curCurve = set()
        for curve in _curveList:
            _id = self.genCurveId(curve["startId"],curve["endId"])
            _isNew = False
            if _id in self.curveCache.keys():
                _curCurve.add(_id)
                if (self.storedDicePos[curve["startId"]] == _dicepos[curve["startId"]] and
                    self.storedDicePos[curve["endId"]] == _dicepos[curve["endId"]] and
                    self.curveCache[_id]["curveColor"] == curve["curveType"].value):
                    continue
            else:
                _isNew = True
            self.curveCache[_id] = {
                "dice1":curve["startId"],
                "dice2":curve["endId"],
                "curveColor":curve["curveType"].value,
                "isContinuous":True,
                "curveSpots":bezier_curve(_dicepos[curve["startId"]],_dicepos[curve["endId"]]),
                "triangles":[
                    None if curve["curveType"] != CurveType.Clash else triangle(_dicepos[curve["startId"]],_dicepos[curve["endId"]],triType.Start),
                    triangle(_dicepos[curve["startId"]],_dicepos[curve["endId"]],triType.End)
                ]
            }
            if _isNew:
                if not curve["startId"] in self.diceCurveIndex:
                    self.diceCurveIndex[curve["startId"]] = []
                if not curve["endId"] in self.diceCurveIndex:
                    self.diceCurveIndex[curve["endId"]] = []
                self.diceCurveIndex[curve["startId"]].append(_id)
                self.diceCurveIndex[curve["endId"]].append(_id)
                _curCurve.add(_id)
        self.storedDicePos = _dicepos
        _safeRemove = []
        for key in self.curveCache.keys():
            if "constant" in self.curveCache[key].keys():
                continue
            if not key in _curCurve:
                self.diceCurveIndex[self.curveCache[key]["dice1"]].remove(key)
                self.diceCurveIndex[self.curveCache[key]["dice2"]].remove(key)
                _safeRemove.append(key)
        for key in _safeRemove:
            del(self.curveCache[key])
    def modifyConstantCurve(self,curveId,startPos,endPos,isCtu,curveType,op=0):
        if op == -1:
            if curveId in self.constantCurveIndex:
                self.constantCurveIndex.remove(curveId)
            return
        if not curveId in self.constantCurveIndex:
            self.constantCurveIndex.append(curveId)
        self.curveCache[curveId] = {
            "constant":None,
            "curveColor":curveType.value,
            "isContinuous":isCtu,
            "curveSpots":bezier_curve(startPos,endPos),
            "triangles":[
                None if curveType != CurveType.Clash else triangle(startPos,endPos,triType.Start),
                triangle(startPos,endPos,triType.End)
            ]
        }
    def activeDice(self,diceID):
        if not diceID in self.diceActive:
            self.diceActive.append(diceID)
    def deactiveDice(self,diceID):
        if diceID in self.diceActive:
            self.diceActive.remove(diceID)
    def draw(self):
        if super().draw():
            for dice in self.diceActive:
                if dice in self.diceCurveIndex.keys():
                    for curveId in self.diceCurveIndex[dice]:
                        self.drawCurve(self.curveCache[curveId])
            #print(self.constantCurveIndex)
            for curveId in self.constantCurveIndex:
                self.drawCurve(self.curveCache[curveId])
    def drawCurve(self,dit):
        if dit["isContinuous"]:
            pygame.draw.lines(self.screen,dit["curveColor"],False,dit["curveSpots"],8)
        else:
            #print(slice_bezier_curve(dit["curveSpots"]))
            for lis in slice_bezier_curve(dit["curveSpots"]):
                pygame.draw.lines(self.screen,dit["curveColor"],False,lis,8)
        for tri in dit["triangles"]:
            if isinstance(tri,list):
                pygame.draw.polygon(self.screen, dit["curveColor"], tri, 0)