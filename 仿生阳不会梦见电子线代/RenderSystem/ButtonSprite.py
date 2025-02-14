from .Sprite import *
class ButtonSprite(Sprite):
    def __init__(self, name, screen, priority):
        super().__init__(name, screen, priority)
    def init(self):
        self.preventRay(False)