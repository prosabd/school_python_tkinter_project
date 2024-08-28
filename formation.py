import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmb

class Formation(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestionnaire Formations")
        self.geometry("1200x750")
        self.positionRight = int(self.winfo_screenwidth()/2 - 800/2)
        
        #Connection Base de donnees
        self.conn = sqlite3.connect('gestionnaire.db')
        self.cursor = self.conn.cursor()

        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS formation
        #                      (code text, intitule text, niveau text, langue text, objectif text, professeur text)''')
        self.conn.commit()
        
        #make the first row with 3 buttons to switch with formation.py, subscription.py, teacher.py
        # First row with 3 buttons
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x")
        self.button_formation = ttk.Button(button_frame, text="Gestion Etudiants", command=lambda: self.on_click("student"))
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
        tk.Label(left_frame, text="Code:").pack()
        self.code_entry = tk.Entry(left_frame)
        self.code_entry.pack()
        tk.Label(left_frame, text="Intitulé:").pack()
        self.intitule_entry = tk.Entry(left_frame)
        self.intitule_entry.pack()
        tk.Label(left_frame, text="Niveau:").pack()
        self.niveau_entry = tk.Entry(left_frame)
        self.niveau_entry.pack()
        tk.Label(left_frame, text="Langue:").pack()
        self.langue_entry = tk.Entry(left_frame)
        self.langue_entry.pack()
        tk.Label(left_frame, text="Objectif:").pack()
        self.objectif_entry = tk.Entry(left_frame)
        self.objectif_entry.pack()
        tk.Label(left_frame, text="Professeur:").pack()
        self.professeur_combobox = ttk.Combobox(left_frame, values=self.get_professeur_names())
        self.professeur_combobox.pack()
        button_frame = tk.Frame(left_frame)
        button_frame.pack()
        self.add_button = ttk.Button(button_frame, text="Ajouter", command=self.add_formation)
        self.add_button.pack(side="left")
        self.remove_button = ttk.Button(button_frame, text="Supprimer", command=self.remove_formation)
        self.remove_button.pack(side="left")
        self.edit_button = ttk.Button(button_frame, text="Éditer", command=self.edit_formation)
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
        self.treeview = ttk.Treeview(right_frame, columns=("Code", "Intitulé", "Niveau", "Langue", "Objectif", "Professeur"))
        self.treeview.pack(fill="both", expand=True)
        treeview_width = self.treeview.winfo_width()
        self.treeview.column("#0", width=0)
        self.treeview.column("Code", width=int(treeview_width * 0.2))
        self.treeview.column("Intitulé", width=int(treeview_width * 0.3))
        self.treeview.column("Niveau", width=int(treeview_width * 0.1))
        self.treeview.column("Langue", width=int(treeview_width * 0.1))
        self.treeview.column("Objectif", width=int(treeview_width * 0.2))
        self.treeview.column("Professeur", width=int(treeview_width * 0.2))
        self.treeview.heading("#0", text="")
        self.treeview.heading("Code", text="Code")
        self.treeview.heading("Intitulé", text="Intitulé")
        self.treeview.heading("Niveau", text="Niveau")
        self.treeview.heading("Langue", text="Langue")
        self.treeview.heading("Objectif", text="Objectif")
        self.treeview.heading("Professeur", text="Professeur")
        self.treeview.bind('<<TreeviewSelect>>', self.on_treeview_select)
        
        self.refresh_table()

    def add_formation(self):
        if self.verify_fields():
            code = self.code_entry.get()
            intitule = self.intitule_entry.get()
            niveau = self.niveau_entry.get()
            langue = self.langue_entry.get()
            objectif = self.objectif_entry.get()
            nom_professeur = self.professeur_combobox.get()
            
            self.cursor.execute("SELECT ine FROM professeur WHERE nom=? AND prenom=?", (nom_professeur.split()[0], nom_professeur.split()[1]))
            professeur_ine = self.cursor.fetchone()[0]

            self.cursor.execute("INSERT INTO formation VALUES (?, ?, ?, ?, ?, ?)",
                            (code, intitule, niveau, langue, objectif, professeur_ine))
            self.conn.commit()

            self.code_entry.delete(0, tk.END)
            self.intitule_entry.delete(0, tk.END)
            self.niveau_entry.delete(0, tk.END)
            self.langue_entry.delete(0, tk.END)
            self.objectif_entry.delete(0, tk.END)
            self.professeur_combobox.delete(0, tk.END)
            self.refresh_table()

    def remove_formation(self):
        if self.verify_fields():
            code = self.code_entry.get()
            try:
                self.cursor.execute("DELETE FROM formation WHERE code=?", (code,))
                self.conn.commit()
            
                if self.cursor.rowcount == 0:
                    tk.messagebox.showerror("Erreur", "Code n'existe pas ou est incorrect")
                else:
                    self.code_entry.delete(0, tk.END)
                    self.intitule_entry.delete(0, tk.END)
                    self.niveau_entry.delete(0, tk.END)
                    self.langue_entry.delete(0, tk.END)
                    self.objectif_entry.delete(0, tk.END)
                    self.professeur_combobox.delete(0, tk.END)
                    self.refresh_table()
            except Exception as e:
                print(e)

    def edit_formation(self):
        if self.verify_fields():
            code = self.code_entry.get()
            intitule = self.intitule_entry.get()
            niveau = self.niveau_entry.get()
            langue = self.langue_entry.get()
            objectif = self.objectif_entry.get()
            nom_professeur = self.professeur_combobox.get()
            
            self.cursor.execute("SELECT id_professeur FROM professeur WHERE nom=? AND prenom=?", (nom_professeur.split()[0], nom_professeur.split()[1]))
            professeur_id = self.cursor.fetchone()[0]

            try:
                self.cursor.execute("UPDATE formation SET intitule=?, niveau=?, langue=?, objectif=?, professeur=? WHERE code=?",
                                (intitule, niveau, langue, objectif, professeur_id, code))
                self.conn.commit()

                if self.cursor.rowcount == 0:
                    tkmb.showerror("Erreur", "Code n'existe pas ou est incorrect")
                else:
                    self.code_entry.delete(0, tk.END)
                    self.intitule_entry.delete(0, tk.END)
                    self.niveau_entry.delete(0, tk.END)
                    self.langue_entry.delete(0, tk.END)
                    self.objectif_entry.delete(0, tk.END)
                    self.professeur_combobox.delete(0, tk.END)
                    self.refresh_table()
            except Exception as e:
                print(e)

    def refresh_table(self):
        self.treeview.delete(*self.treeview.get_children())
        self.cursor.execute("SELECT f.code, f.intitule, f.niveau, f.langue, f.objectif, (p.nom+ ' ' +p.prenom)"
                            "FROM formation f "
                            "JOIN professeur p ON f.ine_professeur = p.ine")
        rows = self.cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
                
    def on_treeview_select(self, event):
        selected_item = self.treeview.selection()[0]
        values = self.treeview.item(selected_item, 'values')
        self.code_entry.delete(0, tk.END)
        self.code_entry.insert(0, values[0])
        self.intitule_entry.delete(0, tk.END)
        self.intitule_entry.insert(0, values[1])
        self.niveau_entry.delete(0, tk.END)
        self.niveau_entry.insert(0, values[2])
        self.langue_entry.delete(0, tk.END)
        self.langue_entry.insert(0, values[3])
        self.objectif_entry.delete(0, tk.END)
        self.objectif_entry.insert(0, values[4])
        self.professeur_combobox.delete(0, tk.END)
        self.professeur_combobox.insert(0, f"{values[5]} {values[6]}")
        
    def search_treeview(self, event):
        search_term = self.search_entry.get()

        self.treeview.delete(*self.treeview.get_children())
        self.cursor.execute("SELECT f.code, f.intitule, f.niveau, f.langue, f.objectif, p.nom, p.prenom "
                            "FROM formation f "
                            "JOIN professeur p ON f.ine_professeur = p.id_professeur "
                            "WHERE f.code LIKE ? OR f.intitule LIKE ? OR f.niveau LIKE ? OR f.langue LIKE ? OR f.objectif LIKE ? OR p.nom LIKE ? OR p.prenom LIKE ?",
                            (f'%{search_term}%',) * 7)
        rows = self.cursor.fetchall()
        for row in rows:
            self.treeview.insert('', 'end', values=row)
            
    def on_click(self, arg):
        if arg == "student":
            # open student.py
            try:
                import student
                student.Student()
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
        
    def verify_fields(self):
        if not self.code_entry.get():
            tkmb.showerror("Error", "Code is required")
            return False
        try:
            code = int(self.code_entry.get())
        except ValueError:
            tkmb.showerror("Erreur", "Code doit être un entier")
            return False
        if not self.intitule_entry.get():
            tkmb.showerror("Error", "Intitule is required")
            return False
        if not self.niveau_entry.get():
            tkmb.showerror("Error", "Niveau is required")
            return False
        if not self.langue_entry.get():
            tkmb.showerror("Error", "Langue is required")
            return False
        if not self.objectif_entry.get():
            tkmb.showerror("Error", "Objectif is required")
            return False
        if not self.professeur_combobox.get():
            tkmb.showerror("Error", "Professeur is required")
            return False
        return True
    
    def get_professeur_names(self):
        # Execute the query
        self.cursor.execute("SELECT nom, prenom FROM professeur")
        rows = self.cursor.fetchall()

        # Create the list of professor names
        professeur_names = [f"{row[0]} {row[1]}" for row in rows]

        return professeur_names
        
Formation().mainloop()