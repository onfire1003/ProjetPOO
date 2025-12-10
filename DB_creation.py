"""
Date : 10.12.2025
Nom du fichier : Bdd_biblio.py
Auteur : Dylan Martini
"""
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Date, ForeignKey, SmallInteger
)

# Création de la base SQLite
engine = create_engine("sqlite:///Bdd_biblio.db")
metadata = MetaData()

# TABLE : Personnes
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

# TABLE : Client (spécialisation de Personnes)
Client = Table(
    "Client",
    metadata,
    Column("ID_Client", String(50), primary_key=True),
    Column("ID_Personnes", Integer, ForeignKey("Personnes.ID_Personnes"))
)

# TABLE : Bibliothecaires (spécialisation de Personnes)
Bibliothecaires = Table(
    "Bibliothecaires",
    metadata,
    Column("ID_Bibliothecaire", Integer, primary_key=True),
    Column("Pseudo", String(50)),
    Column("Mot_de_passe", String(50)),
    Column("ID_Personnes", Integer, ForeignKey("Personnes.ID_Personnes"))
)

# TABLE : Livres
Livres = Table(
    "Livres",
    metadata,
    Column("ID_Livres", String(32), primary_key=True),
    Column("Titre", String(50)),
    Column("Auteur", String(50)),
    Column("Nb_pages", SmallInteger),
    Column("Maison_edition", String(50)),
    Column("Age_min", Integer),
    Column("Date_publication", Date)
)

# TABLE : Nb_Exemplaires (une ligne par exemplaire)
Nb_Exemplaires = Table(
    "Nb_Exemplaires",
    metadata,
    Column("Numero_exemplaire", Integer, primary_key=True),
    Column("ID_Livres", String(32), ForeignKey("Livres.ID_Livres"))
)

# TABLE : Emprunts (association Personnes – Livres)
Emprunts = Table(
    "Emprunts",
    metadata,
    Column("ID_Personne", Integer, ForeignKey("Personnes.ID_Personnes")),
    Column("ID_Livre", String(32), ForeignKey("Livres.ID_Livres")),
    Column("Date_emprunte", Date),
    Column("Date_retour", Date)
)

# Création des tables
metadata.create_all(engine)
print("Toutes les tables ont été créées.")



