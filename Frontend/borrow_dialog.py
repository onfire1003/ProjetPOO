"""
Nom du fichier : borrow_dialog.py
Nom du créateur : Samuel Antunes
Date de création : 17.12.2025
"""


import customtkinter as ctk
from tkinter import messagebox

from theme import COLOR_CARD_BG, COLOR_DARK_RED, COLOR_TEXT
import api_client

class BorrowDialog(ctk.CTkToplevel):
    def __init__(self, master, book, on_success):
        super().__init__(master)
        self.title("Remplir info pour emprunter")
        self.geometry("350x220")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_CARD_BG)

        self.book = book
        self.on_success = on_success

        # centrer la fenêtre par rapport au parent
        self.update_idletasks()
        if master is not None:
            x = master.winfo_x() + master.winfo_width() // 2 - self.winfo_width() // 2
            y = master.winfo_y() + master.winfo_height() // 2 - self.winfo_height() // 2
            self.geometry(f"+{x}+{y}")

        label_title = ctk.CTkLabel(
            self,
            text="Entrez informations",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="black",
        )
        label_title.pack(pady=(15, 10))

        frame_center = ctk.CTkFrame(self, fg_color=COLOR_CARD_BG)
        frame_center.pack(pady=5)

        label_id = ctk.CTkLabel(
            frame_center,
            text="ID de la carte du lecteur",
            text_color="black",
            font=ctk.CTkFont(size=14),
        )
        label_id.pack(pady=(0, 5))

        self.entry_card = ctk.CTkEntry(
            frame_center,
            width=180,
            fg_color="white",
            text_color="black",
        )
        self.entry_card.pack()

        btn_save = ctk.CTkButton(
            self,
            text="Enregistrer",
            fg_color=COLOR_DARK_RED,
            hover_color="#8A0A22",
            text_color=COLOR_TEXT,
            width=160,
            height=32,
            command=self.validate_card,
            corner_radius=20,
        )
        btn_save.pack(pady=(20, 10))

        self.grab_set()
        self.entry_card.focus()

    def validate_card(self):
        card_id = self.entry_card.get().strip()

        if not card_id:
            messagebox.showerror("Erreur", "Veuillez saisir un ID de carte.")
            return

        if not api_client.is_valid_card_id(card_id):
            messagebox.showerror("Erreur", "ID de carte inconnu.")
            return

        self.on_success(self.book, card_id)
        self.destroy()
