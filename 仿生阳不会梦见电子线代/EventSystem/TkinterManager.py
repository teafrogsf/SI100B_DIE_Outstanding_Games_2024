from Data.instance import *

from .EventManager import ClearEvent

import tkinter.simpledialog
import tkinter as tk

@instance
class TkinterManager:
    def __init__(self):
        self.ROOT = tk.Tk()
        self.ROOT.withdraw()
    def createSimpleDialog(self):
        text = tkinter.simpledialog.askstring(" ", " ")
        ClearEvent()
        return text

tkManager = TkinterManager()