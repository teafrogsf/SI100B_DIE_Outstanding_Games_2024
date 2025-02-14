from Data.instance import *

from LLMSystem.InteractionWithGPT import LLMSystem
from LLMSystem.ChatWithGPT import Chater

from SceneSystem.Timer import Timer

@instance
class LLMStorage:
    def __init__(self):
        print("INIT: LLM")
        self.LLM_SYSTEM = LLMSystem()
        self.CHATER = Chater()

        self.inGenerating = False
        self.genTime = None
        self.genThread = None

        self.genPageDialog = " "

        self.loadGenPageProcess()
    def loadGenPageProcess(self):
        self.GENPAGE_PROCESS = 0
        self.GENPAGE_PROCESS_MAX = 1
        self.GENPAGE_PROCESS_PAGE = 0
        self.GENPAGE_SHUTDOWN = False
    def modifyGenPageProcess(self,process,processMax,pageCnt):
        #print(process,processMax,pageCnt)
        self.GENPAGE_PROCESS = process
        self.GENPAGE_PROCESS_MAX = processMax
        self.GENPAGE_PROCESS_PAGE = pageCnt
    def modifyGenPageDialog(self,txt):
        self.genPageDialog = txt
    def shutDown(self):
        self.GENPAGE_SHUTDOWN = True
    def refresh(self):
        self.loadGenPageProcess()
        self.genTime = self.genThread = None
    def gather(self):
        if self.GENPAGE_PROCESS_PAGE >= 4 or self.GENPAGE_PROCESS_PAGE < 0:
            self.inGenerating = False
            self.genThread.result()
            if self.GENPAGE_PROCESS_PAGE < 0:
                print("Debug: shut down success")
    def register(self,tim,thread):
        self.inGenerating = True
        self.genTime = Timer(tim)
        self.genThread = thread
    def genCardDialog(self,txt):
        return self.CHATER.chat(txt)

llmStorage = LLMStorage()