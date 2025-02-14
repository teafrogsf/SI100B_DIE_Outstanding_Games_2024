import time

class Timer:
    def __init__(self,delta=1):
        self.startTime = time.time()
        self.rcdTime = self.startTime
        self.tickDelta = delta
        self.deltaTime = 0
    def tick(self):
        now_time = time.time()
        self.deltaTime += now_time-self.rcdTime
        self.rcdTime = now_time
        if self.deltaTime >= self.tickDelta:
            self.deltaTime -= self.tickDelta
            return True
        return False
    def reset(self):
        self.startTime = time.time()
        self.rcdTime = self.startTime
        self.deltaTime = 0
    def tempSlow(self,tim):
        self.deltaTime -= tim