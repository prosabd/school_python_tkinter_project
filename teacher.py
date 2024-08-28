import tkinter as tk
from tkinter import ttk


class Teacher(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestionnaire Professeurs")
        self.geometry("1200x750")
        self.positionRight = int(self.winfo_screenwidth()/2 - 800/2)
        
Teacher().mainloop()