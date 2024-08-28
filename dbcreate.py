import sqlite3

# Connect to the database
conn = sqlite3.connect("gestionnaire.db")
cursor = conn.cursor()

# Create the "etudiant" table
cursor.execute("""
    CREATE TABLE etudiant (
        ine INTEGER PRIMARY KEY,
        nom TEXT,
        prenom TEXT,
        email TEXT,
        adresse TEXT,
        ville TEXT
    )
""")

# Create the "formation" table
cursor.execute("""
    CREATE TABLE formation (
        code INTEGER PRIMARY KEY,
        intitule TEXT,
        langue TEXT,
        niveau TEXT,
        objectif TEXT,
        ine_professeur INTEGER,
        FOREIGN KEY (ine_professeur) REFERENCES professeur (ine)
    )
""")

# Create the "inscription" table
cursor.execute("""
    CREATE TABLE inscription (
        id INTEGER PRIMARY KEY,
        ine_etudiant INTEGER,
        code_formation INTEGER,
        date_inscription DATE,
        FOREIGN KEY (ine_etudiant) REFERENCES etudiant (ine),
        FOREIGN KEY (code_formation) REFERENCES formation (code)
    )
""")

# Create the "professeur" table
cursor.execute("""
    CREATE TABLE professeur (
        ine INTEGER PRIMARY KEY,
        nom TEXT,
        prenom TEXT
    )
""")

# Commit the changes
conn.commit()

# Close the connection
conn.close()