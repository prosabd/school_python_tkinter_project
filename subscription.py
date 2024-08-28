import tkinter as tk
from tkinter import ttk


class Subscription(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestionnaire Inscriptions")
        self.geometry("1200x750")
        self.positionRight = int(self.winfo_screenwidth()/2 - 800/2)
        
Subscription().mainloop()