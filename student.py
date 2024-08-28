import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmb

class Student(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestionnaire Etudiant")
        self.geometry("1200x750")
        self.positionRight = int(self.winfo_screenwidth()/2 - 800/2)
        
        #make the first row with 3 buttons to switch with formation.py, subscription.py, teacher.py
        # First row with 3 buttons
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x")
        self.button_formation = ttk.Button(button_frame, text="Gestion formations", command=lambda: self.on_click("formation"))
        self.button_formation.pack(side="left")
        self.button_student = ttk.Button(button_frame, text="Gestion Inscriptions", command=lambda: self.on_click("subscription"))
        self.button_student.pack(side="left")
        self.button_teacher = ttk.Button(button_frame, text="Gestion professeurs", command=lambda: self.on_click("teacher"))
        self.button_teacher.pack(side="left")

        # Second row with 2 columns
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Left column with fields and buttons
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="y")
        tk.Label(left_frame, text="INE:").pack()
        self.ine_entry = tk.Entry(left_frame)
        self.ine_entry.pack()
        tk.Label(left_frame, text="Nom:").pack()
        self.nom_entry = tk.Entry(left_frame)
        self.nom_entry.pack()
        tk.Label(left_frame, text="Prénom:").pack()
        self.prenom_entry = tk.Entry(left_frame)
        self.prenom_entry.pack()
        tk.Label(left_frame, text="Adresse mail:").pack()
        self.mail_entry = tk.Entry(left_frame)
        self.mail_entry.pack()
        tk.Label(left_frame, text="Adresse:").pack()
        self.adresse_entry = tk.Entry(left_frame)
        self.adresse_entry.pack()
        tk.Label(left_frame, text="Ville:").pack()
        self.ville_entry = tk.Entry(left_frame)
        self.ville_entry.pack()
        button_frame = tk.Frame(left_frame)
        button_frame.pack()
        self.add_button = ttk.Button(button_frame, text="Ajouter", command=self.add_student)
        self.add_button.pack(side="left")
        self.remove_button = ttk.Button(button_frame, text="Supprimer", command=self.remove_student)
        self.remove_button.pack(side="left")
        self.edit_button = ttk.Button(button_frame, text="Éditer", command=self.edit_student)
        self.edit_button.pack(side="left")
        self.refresh_button = ttk.Button(button_frame, text="Rafraîchir", command=self.refresh_table)
        self.refresh_button.pack(side="left")

        # Right column with search field and table
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        tk.Label(right_frame, text="Recherche:").pack()
        self.search_entry = tk.Entry(right_frame)
        self.search_entry.pack()
        self.search_entry.bind('<KeyRelease>', self.search_treeview)
        self.treeview = ttk.Treeview(right_frame, columns=("INE", "Nom", "Prénom", "Adresse mail", "Adresse", "Ville"))
        self.treeview.pack(fill="both", expand=True)
        treeview_width = self.treeview.winfo_width()
        self.treeview.column("#0", width=int(treeview_width * 0))
        self.treeview.column("INE", width=int(treeview_width * 0.15))
        self.treeview.column("Nom", width=int(treeview_width * 0.25))
        self.treeview.column("Prénom", width=int(treeview_width * 0.25))
        self.treeview.column("Adresse mail", width=int(treeview_width * 0.3))
        self.treeview.column("Adresse", width=int(treeview_width * 0.3))
        self.treeview.column("Ville", width=int(treeview_width * 0.3))
        self.treeview.heading("#0", text="")
        self.treeview.heading("INE", text="INE")
        self.treeview.heading("Nom", text="Nom")
        self.treeview.heading("Prénom", text="Prénom")
        self.treeview.heading("Adresse mail", text="Adresse mail")
        self.treeview.heading("Adresse", text="Adresse")
        self.treeview.heading("Ville", text="Ville")
        self.treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)
        
        #Connection Base de donnees
        self.conn = sqlite3.connect('gestionnaire.db')
        self.cursor = self.conn.cursor()

        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS etudiant
        #                      (ine text, nom text, prenom text, mail text, adresse text)''')
        self.conn.commit()
        self.refresh_table()

    def add_student(self):
        if self.verify_fields():
            ine = int(self.ine_entry.get())
            nom = self.nom_entry.get()
            prenom = self.prenom_entry.get()
            mail = self.mail_entry.get()
            adresse = self.adresse_entry.get()
            ville = self.ville_entry.get()

            self.cursor.execute("INSERT INTO etudiant VALUES (?, ?, ?, ?, ?, ?)",
                               (ine, nom, prenom, mail, adresse, ville))
            self.conn.commit()

            self.ine_entry.delete(0, tk.END)
            self.nom_entry.delete(0, tk.END)
            self.prenom_entry.delete(0, tk.END)
            self.mail_entry.delete(0, tk.END)
            self.adresse_entry.delete(0, tk.END)
            self.ville_entry.delete(0, tk.END)
            self.refresh_table()

    def remove_student(self):
        if self.verify_fields():
            ine = self.ine_entry.get()
            try:
                self.cursor.execute("DELETE FROM etudiant WHERE ine=?", (ine,))
                self.conn.commit()
                
                if self.cursor.rowcount == 0:
                    tk.messagebox.showerror("Erreur", "INE n'existe pas ou est incorrect")
                else:
                    self.ine_entry.delete(0, tk.END)
                    self.nom_entry.delete(0, tk.END)
                    self.prenom_entry.delete(0, tk.END)
                    self.mail_entry.delete(0, tk.END)
                    self.adresse_entry.delete(0, tk.END)
                    self.ville_entry.delete(0, tk.END)
                    self.refresh_table()
            except Exception as e:
                print(e)         

    def edit_student(self):
        if self.verify_fields():
            ine = self.ine_entry.get()
            nom = self.nom_entry.get()
            prenom = self.prenom_entry.get()
            mail = self.mail_entry.get()
            adresse = self.ville_entry.get()
            ville = self.ville_entry.get()

            try:
                self.cursor.execute("UPDATE etudiant SET nom=?, prenom=?, email=?, adresse=?, ville=? WHERE ine=?",
                                (nom, prenom, mail, adresse, ville, ine))
                self.conn.commit()

                if self.cursor.rowcount == 0:
                    tk.messagebox.showerror("Erreur", "INE n'existe pas ou est incorrect")
                else:
                    self.ine_entry.delete(0, tk.END)
                    self.nom_entry.delete(0, tk.END)
                    self.prenom_entry.delete(0, tk.END)
                    self.mail_entry.delete(0, tk.END)
                    self.adresse_entry.delete(0, tk.END)
                    self.ville_entry.delete(0, tk.END)
                    self.refresh_table()
            except Exception as e:
                print(e)                

    def refresh_table(self):
        self.treeview.delete(*self.treeview.get_children())
        self.cursor.execute("SELECT * FROM etudiant")
        rows = self.cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
            
    def on_treeview_select(self, event):
        selected_item = self.treeview.selection()[0]
        values = self.treeview.item(selected_item, 'values')
        self.ine_entry.delete(0, tk.END)
        self.ine_entry.insert(0, values[0])
        self.nom_entry.delete(0, tk.END)
        self.nom_entry.insert(0, values[1])
        self.prenom_entry.delete(0, tk.END)
        self.prenom_entry.insert(0, values[2])
        self.mail_entry.delete(0, tk.END)
        self.mail_entry.insert(0, values[3])
        self.adresse_entry.delete(0, tk.END)
        self.adresse_entry.insert(0, values[4])
        self.ville_entry.delete(0, tk.END)
        self.ville_entry.insert(0, values[4])
        
    def search_treeview(self, event):
        # Get the search term
        search_term = self.search_entry.get()
    
        # Clear the treeview
        for i in self.treeview.get_children():
            self.treeview.delete(i)
    
        # Execute the search query
        # self.cursor.execute("SELECT * FROM etudiant WHERE ine LIKE ? OR nom LIKE ? OR prenom LIKE ? OR mail LIKE ? OR adresse LIKE ?",
        #             ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        self.cursor.execute("SELECT * FROM etudiant WHERE ine LIKE ? OR nom LIKE ? OR prenom LIKE ? OR mail LIKE ? OR adresse LIKE ? OR ville LIKE ?", (f'%{search_term}%',) * 5)
        rows = self.cursor.fetchall()
    
        # Insert the search results into the treeview
        for row in rows:
            self.treeview.insert('', 'end', values=row)
        
    def on_click(self, arg):
        if arg == "formation":
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
        
    # Verification des champs
    def verify_fields(self):
        if not self.ine_entry.get():
            tkmb.showerror("Error", "INE is required")
            return False
        try:
            ine = int(self.ine_entry.get())
        except ValueError:
            tkmb.showerror("Erreur", "INE doit être un entier")
            return False
        if not self.nom_entry.get():
            tkmb.showerror("Error", "Nom is required")
            return False
        if not self.prenom_entry.get():
            tkmb.showerror("Error", "Prénom is required")
            return False
        if not self.mail_entry.get():
            tkmb.showerror("Error", "Adresse mail is required")
            return False
        if not self.adresse_entry.get():
            tkmb.showerror("Error", "Adresse is required")
            return False
        if not self.ville_entry.get():
            tkmb.showerror("Error", "Ville is required")
            return False
        return True

Student().mainloop()