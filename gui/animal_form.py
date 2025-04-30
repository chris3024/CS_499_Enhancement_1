# gui/animal_form.py

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from datetime import datetime

class AnimalFormWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Animal Form")
        self.geometry("400x600")
        self.resizable(False, False)

