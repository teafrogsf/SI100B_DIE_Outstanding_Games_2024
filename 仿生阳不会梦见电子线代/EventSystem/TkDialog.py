import tkinter as tk

from Data.types import *

class TkDialog(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.title("")
        self.resizable(False, False)
        self.overrideredirect(True)
    