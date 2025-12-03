"""
Date : 03.12.2025
Nom du fichier : Bdd_biblio.py
Auteur : Dylan Martini
"""

# --------------------------------------------------
# Imports SQLAlchemy
# --------------------------------------------------
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Date
)

# --------------------------------------------------
# Configuration base de données
# --------------------------------------------------
db_path = "sqlite:///Bdd_biblio.db"
engine = create_engine(db_path)

# --------------------------------------------------
# Connexion à la base
# --------------------------------------------------
try:
    connection = engine.connect()
    print("Connexion réussie à Bdd_biblio.db.")
except Exception as e:
    print("Erreur de connexion :", e)

# --------------------------------------------------
# Définition du schéma (tables)
# --------------------------------------------------
metadata = MetaData()

# Tables Personnes
Personnes = Table(
    "Personnes",
    metadata,
    Column("ID_Personnes", Integer, primary_key=True),
    Column("Nom", String(50)),
    Column("Prenom", String(50)),
    Column("Adresse_mail", String(50)),
    Column("Date_naissance", Date),
    Column("Adresse", String(50)),
    Column("Ville", String(50)),
    Column("NPA", Integer)
)

# Tables Bibliotheque
Bibliotheque = Table(
    "Bibliotheque",
    metadata,
    Column("ID_Bibliotheque", Integer, primary_key=True),
    Column("Nom", String(50)),
    Column("Adresse", String(50)),
    Column("Ville", String(50)),
    Column("NPA", Integer)
)

# Création physique de la table
metadata.create_all(engine)
print("Table 'Personnes' créée (ou déjà existante).")

# Fermeture
connection.close()
