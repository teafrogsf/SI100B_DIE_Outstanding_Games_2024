import os,json
class StageSetting:
    def __init__(self):
        self.stageAmt = None
        self.stageCur = 1

        self.stageList = None
    def loadStageInfo(self,fileNam):
        path = os.path.join(os.getcwd(),"Assets","Gdata","Battle")
        files = os.listdir(path)
        for file in files:
            if file == fileNam:
                js = os.path.join(path,file)
                with open(js,"r",encoding="utf-8") as f:
                    self.stageList = json.load(f)
                    if "_StageLen" in self.stageList.keys():
                        self.stageAmt = self.stageList["_StageLen"]
                    else:
                        self.stageAmt = len(self.stageList)
                break
    def getStageInfo(self):
        return self.stageList[str(self.stageCur)]
    def getStageBattleInfo(self):
        return self.stageList[str(self.stageCur)]["receptionInfo"]
    def nextStage(self):
        self.stageCur += 1
        if self.stageCur > self.stageAmt:
            self.stageCur -= 1
            return False
        return True
    def getStageIndex(self):
        return self.stageCur