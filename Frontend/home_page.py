"""
Nom du fichier : home_page.py
Nom du créateur : Samuel Antunes
Date de création : 17.12.2025
"""


import customtkinter as ctk

from theme import COLOR_BG_MAIN
from login_page import LoginPage
from library_page import LibraryPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bibliothèque")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_MAIN)

        self.current_user = None

        # conteneur unique
        self.container = ctk.CTkFrame(self, fg_color=COLOR_BG_MAIN)
        self.container.pack(fill="both", expand=True)

        # pages (plus de HomePage)
        self.pages = {
            "login": LoginPage(self.container, self),
            "library": LibraryPage(self.container, self),
        }

        # placement identique (stack)
        for p in self.pages.values():
            p.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("login")

    def show_page(self, name: str):
        self.pages[name].tkraise()

    def login_success(self, username: str):
        self.current_user = username
        self.pages["library"].set_user(username)
        self.show_page("library")  # DIRECT → bibliothèque

    def logout(self):
        self.current_user = None
        self.show_page("login")
