import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestionnaire Acceuil")
        self.geometry("1200x750")
        self.positionRight = int(self.winfo_screenwidth()/2 - 800/2)
        
        grey_frame = tk.Frame(self)
        grey_frame.place(relwidth=0.35, relheight=1)

        # Create a frame for the blue box (75% width)
        blue_frame = tk.Frame(self, bg="blue")
        blue_frame.place(relx=0.35, relwidth=0.65, relheight=1)
        
        self.labelmain = ttk.Label(grey_frame, text="Systeme \nde Gestions \ndes formations")
        self.labelmain.grid(row=0, column=1, sticky="nsew")

        # Configure the grid to expand in both directions
        grey_frame.grid_rowconfigure(0, weight=1)
        grey_frame.grid_columnconfigure(0, weight=1)
        grey_frame.grid_columnconfigure(1, weight=1)
        grey_frame.grid_columnconfigure(2, weight=1)

        # Configure the grid to expand in both directions
        blue_frame.grid_rowconfigure(0, weight=1)
        blue_frame.grid_rowconfigure(1, weight=1)
        blue_frame.grid_rowconfigure(2, weight=1)
        blue_frame.grid_rowconfigure(3, weight=1)
        blue_frame.grid_columnconfigure(0, weight=1)
        blue_frame.grid_columnconfigure(1, weight=1)
        blue_frame.grid_columnconfigure(2, weight=1)
        
        # Create empty labels on either side of the button
        self.buttonStudent = ttk.Button(blue_frame, text="Gestion Etudiants", command=lambda: self.on_click("student"))
        self.buttonStudent.grid(row=0, column=1, sticky="nsew")

        self.buttonFormation = ttk.Button(blue_frame, text="Gestion Formation", command=lambda: self.on_click("formation"))
        self.buttonFormation.grid(row=1, column=1, sticky="nsew")

        self.buttonSubscription = ttk.Button(blue_frame, text="Gestion Inscriptions", command=lambda: self.on_click("subscription"))
        self.buttonSubscription.grid(row=2, column=1, sticky="nsew")

        self.buttonTeacher = ttk.Button(blue_frame, text="Gestion Professseurs", command=lambda: self.on_click("teacher"))
        self.buttonTeacher.grid(row=3, column=1, sticky="nsew")
        
    def on_click(self, arg):
        if arg == "student":
            # open student.py
            try:
                import student
                self.destroy()
                student.Student()
            except Exception as e:
                print(e)
            pass
        elif arg == "formation":
            # open formation.py
            try:
                import formation
                formation.Formation()
                self.destroy()
            except Exception as e:
                print(e)
            pass
        elif arg == "subscription":
            # open subscription.py
            try:
                import subscription
                subscription.Subscription()
                self.destroy()
            except Exception as e:
                print(e)
            pass
        elif arg == "teacher":
            # open teacher.py
            try:
                import teacher
                teacher.Teacher()
                self.destroy()
            except Exception as e:
                print(e)
            pass
        
App().mainloop()