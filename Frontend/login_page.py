"""
Nom du fichier : login_page.py
Nom du créateur : Samuel Antunes
Date de création : 17.12.2025
"""


import customtkinter as ctk
from tkinter import messagebox

from theme import COLOR_BG_MAIN, COLOR_CARD_BG, COLOR_DARK_RED, COLOR_TEXT, COLOR_BORDER
import api_client  # <- NEW

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=COLOR_BG_MAIN)
        self.app = app

        CARD_WIDTH = 550
        CARD_HEIGHT = 280

        card = ctk.CTkFrame(
            master=self,
            fg_color=COLOR_CARD_BG,
            corner_radius=10,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            border_width=2,
            border_color=COLOR_BORDER,
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.grid_propagate(False)

        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        label_title = ctk.CTkLabel(
            master=card,
            text="IDENTIFICATION",
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
        )
        label_title.grid(row=0, column=0, columnspan=2, pady=(15, 25))

        label_username = ctk.CTkLabel(
            master=card,
            text="Nom d'utilisateur :",
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(size=12),
        )
        label_username.grid(row=1, column=0, pady=5, sticky="e", padx=(20, 10))

        self.entry_username = ctk.CTkEntry(
            master=card,
            width=180,
            fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT,
            placeholder_text="pseudo",
        )
        self.entry_username.grid(row=1, column=1, pady=5, sticky="w")

        label_password = ctk.CTkLabel(
            master=card,
            text="Mot de passe :",
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(size=12),
        )
        label_password.grid(row=2, column=0, pady=15, sticky="e", padx=(20, 10))

        self.entry_password = ctk.CTkEntry(
            master=card,
            width=180,
            fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT,
            show="*",
            placeholder_text="mot de passe",
        )
        self.entry_password.grid(row=2, column=1, pady=15, sticky="w")

        btn_login = ctk.CTkButton(
            master=card,
            text="Se connecter",
            fg_color=COLOR_DARK_RED,
            hover_color="#8A0A22",
            text_color=COLOR_TEXT,
            width=160,
            height=32,
            corner_radius=20,
            command=self.on_login_clicked,
        )
        btn_login.grid(row=3, column=0, columnspan=2, pady=(30, 10))

    def on_login_clicked(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Attention", "Veuillez remplir les deux champs.")
            return

        if not api_client.login(username, password):
            messagebox.showerror("Erreur", "Identifiants incorrects.")
            return

        self.app.login_success(username)
