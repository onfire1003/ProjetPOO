"""
Date : 04.12.2025
Nom du fichier : Number_of_copies.py
Auteur : Joel Cunha Faria
"""
from Book import Book

class Number_of_copies(Book):
    def __init__(self, id_number_of_copies, id_book, title, author, number_of_pages, publishing_house, minimum_age, publication_date):
        super().__init__(id_book, title, author, number_of_pages, publishing_house, minimum_age, publication_date)
        self.id_number_of_copies = id_number_of_copies