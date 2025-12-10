"""
Date : 04.12.2025
Nom du fichier : Librarian.py
Auteur : Joel Cunha Faria
"""
from Person import Person

class Librarian(Person):
    def __init__(self, id_librarian, username, password, id_person, lastname, firstname, email, birthday, address, city, zipcode):
        super().__init__(id_person, lastname, firstname, email, birthday, address, city, zipcode)
        self.id_librarian = id_librarian
        self.username = username
        self.password = password