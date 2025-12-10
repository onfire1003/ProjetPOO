"""
Date : 04.12.2025
Nom du fichier : Customer.py
Auteur : Joel Cunha Faria
"""
from Person import Person

class Customer(Person):
    def __init__(self, id_customer, id_person, lastname, firstname, email, birthday, address, city, zipcode):
        super().__init__(id_person,lastname, firstname, email, birthday, address, city, zipcode)
        self.id_customer = id_customer