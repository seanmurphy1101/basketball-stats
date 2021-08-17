from tkinter import *
from tkinter import Frame, Label, ttk, font
from tkinter.constants import CENTER
from ttkthemes import THEMES, ThemedTk

class SubWindow():
    def __init__(self, frame):
        self.window = ttk.Frame(frame, width=300)
        self.hidden = True

class Miss():
    def __init__(self):
        self.isRed = False
        self.missed = False

class Contested():
    def __init__(self):
        self.isRed = False
        self.contested = False
