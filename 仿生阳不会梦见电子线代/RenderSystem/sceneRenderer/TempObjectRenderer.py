from RenderSystem.Canvas import *
from AnimeSystem.animes.TempObjectAnime import TempObjectAnime
from AnimeSystem.Anime import AnimeInfo,AnimeType

from RenderSystem.prefab.UISimpleTip import UISimpleTip
from RenderSystem.prefab.UITitle import UITitleRoundStart_BG,UITitleRoundStart_Title,UITitleVictory,UITitleDefeat,UITitleResultText,UISceneTransfer
from RenderSystem.prefab.UITitle import UISceneBlurBG,UISceneTitle

import Data.fonts

class TempObjectRenderer(Canvas):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.curID = 0
        self.MODID = 23089928324#eruhgehjndqugiw
        self.setPos(Vector2(720,360))
    def genID(self):
        self.curID += 1
        self.curID %= self.MODID
        return self.curID
    def Render(self):
        self.draw()
    def Add(self,obj,lasFrame,aniInfo=None):
        obj.name = self.genID()
        self.addChild(obj)
        #print(len(self.children))
        TempObjectAnime(lasFrame,obj,aniInfo).start()
    def AddSimpleTip(self,txt,linewidth,pos,lasFrame = 90):
        _tip = UISimpleTip(self.genID(),self.screen,20,txt,linewidth)
        _tip.setPos(pos)
        self.Add(_tip,lasFrame)
    def AddTitleRoundStart(self,roundID,freetxt=None):
        _titleBG = UITitleRoundStart_BG(self.genID(),self.screen,10)
        if freetxt != None:
            _titleTxt = UITitleRoundStart_Title(self.genID(),self.screen,15,freetxt)
        else:    
            _titleTxt = UITitleRoundStart_Title(self.genID(),self.screen,15,u"第"+str(roundID)+u"幕")
        self.Add(_titleBG,60,AnimeInfo(60).enableAlpha().add(AnimeType.Alpha,0,120).add(AnimeType.Alpha,10,255)
                 .add(AnimeType.Alpha,40,255).add(AnimeType.Alpha,60,0))
        self.Add(_titleTxt,60,AnimeInfo(60).disableSprite().add(AnimeType.Active,0,False).add(AnimeType.Active,5,True)
                 .add(AnimeType.Scale,5,Vector2(1.5,1.5)).add(AnimeType.Scale,10,Vector2.One()).add(AnimeType.Scale,45,Vector2.One())
                 .add(AnimeType.Scale,48,Vector2(3.5,3.5)).add(AnimeType.Active,48,False).finish())
    def AddTitleVictory(self):
        _titleBG = UITitleVictory(self.genID(),self.screen,20)
        _titleTxt = UITitleResultText(self.genID(),self.screen,25,Data.fonts.ColorVictory,"VICTORY")
        self.AddBattleResult(_titleBG,_titleTxt)
    def AddTitleDefeat(self):
        _titleBG = UITitleDefeat(self.genID(),self.screen,20)
        _titleTxt = UITitleResultText(self.genID(),self.screen,25,Data.fonts.ColorDefeat,"DEFEAT")
        self.AddBattleResult(_titleBG,_titleTxt)
    def AddBattleResult(self,_titleBG,_titleTxt):
        self.Add(_titleBG,90,AnimeInfo(90).enableAlpha().add(AnimeType.Alpha,0,60).add(AnimeType.Alpha,30,255)
                 .add(AnimeType.Alpha,75,255).add(AnimeType.Alpha,90,0).finish())
        self.Add(_titleTxt,90,AnimeInfo(90).disableSprite().enableAlpha().add(AnimeType.Active,0,False).add(AnimeType.Active,10,True)
                 .add(AnimeType.Alpha,10,20).add(AnimeType.Alpha,60,255).add(AnimeType.Scale,10,Vector2(1,0))
                 .add(AnimeType.Scale,40,Vector2(1,1)).add(AnimeType.Alpha,75,255).add(AnimeType.Alpha,90,0).finish())
    def AddSceneTansfer(self,choice,delay=0):
        if choice == -1:
            if delay == 0:
                self.Add(UISceneTransfer(self.genID(),self.screen,10000),10,AnimeInfo(10).enableAlpha()
                     .add(AnimeType.Alpha,0,0).add(AnimeType.Alpha,10,255).finish())
            else:
                self.Add(UISceneTransfer(self.genID(),self.screen,10000),10,AnimeInfo(10+delay).enableAlpha()
                     .add(AnimeType.Alpha,delay,0).add(AnimeType.Alpha,10+delay,255).add(AnimeType.Active,0,False)
                     .add(AnimeType.Active,delay,True).finish())
        elif choice == 1:
            if delay == 0:
                self.Add(UISceneTransfer(self.genID(),self.screen,10000),10,AnimeInfo(10).enableAlpha()
                     .add(AnimeType.Alpha,0,255).add(AnimeType.Alpha,10,0).finish())
            else:
                self.Add(UISceneTransfer(self.genID(),self.screen,10000),10,AnimeInfo(10+delay).enableAlpha()
                     .add(AnimeType.Alpha,delay,255).add(AnimeType.Alpha,10+delay,0).add(AnimeType.Active,0,False)
                     .add(AnimeType.Active,delay,True).finish())
    def AddBattleSceneEnter(self):
        from GameDataManager import gameDataManager
        _bg = UISceneBlurBG(self.genID(),self.screen,1000,gameDataManager.getBackground("Battle",gameDataManager.STAGE.getStageBattleInfo()["receptionBG"])[0])
        _title = UISceneTitle(self.genID(),self.screen,5000,gameDataManager.STAGE.getStageBattleInfo()["receptionIndex"],gameDataManager.STAGE.getStageBattleInfo()["receptionName"])
        las = 100
        delay = 40
        self.Add(_bg,las)
        self.Add(_title,las)
        self.Add(UISceneTransfer(self.genID(),self.screen,3000),10,AnimeInfo(las).enableAlpha()
                     .add(AnimeType.Alpha,delay,0).add(AnimeType.Alpha,10+delay,255).add(AnimeType.Active,0,False)
                     .add(AnimeType.Active,delay,True).finish())
    def AddFloatingText(self,txt):
        from RenderSystem.prefab.UIFloatingText import UIFloatingText
        from AnimeSystem.animes.TempObjectAnime import FloatingTextAnime
        _obj = UIFloatingText(self.genID(),self.screen,10000)
        _ani = FloatingTextAnime(_obj,txt)
        self.addChild(_obj)
        _ani.start()
