"""
Nom du fichier : library_page.py
Nom du créateur : Samuel Antunes
Date de création : 17.12.2025
"""


import customtkinter as ctk
from tkinter import messagebox

from theme import (
    COLOR_BG_MAIN, COLOR_CARD_BG, COLOR_DARK_RED, COLOR_TEXT,
    COLOR_BORDER, COLOR_SUCCESS
)
import api_client
from borrow_dialog import BorrowDialog
from account_dialog import AccountDialog

class LibraryPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=COLOR_BG_MAIN)
        self.app = app

        self.current_user = None
        self.current_book = None
        self.current_book = None
        self.success_label = None

        # grille principale
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # ---------- Barre du haut ----------
        top_bar = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_BORDER,
            border_width=1,
        )
        top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")

        top_bar.grid_columnconfigure(0, weight=0)
        top_bar.grid_columnconfigure(1, weight=0)
        top_bar.grid_columnconfigure(2, weight=1)
        top_bar.grid_columnconfigure(3, weight=0)
        top_bar.grid_columnconfigure(4, weight=0)

        self.lbl_name = ctk.CTkLabel(
            top_bar, text="NAME", font=ctk.CTkFont(size=14, weight="bold"), text_color="black"
        )
        self.lbl_name.grid(row=0, column=0, padx=10, pady=5)

        self.lbl_card = ctk.CTkLabel(
            top_bar, text="Numéro_Carte", font=ctk.CTkFont(size=14, weight="bold"), text_color="black"
        )
        self.lbl_card.grid(row=0, column=1, padx=10, pady=5)

        lbl_search = ctk.CTkLabel(
            top_bar, text="Recherche :", font=ctk.CTkFont(size=14), text_color="black"
        )
        lbl_search.grid(row=0, column=2, sticky="e", pady=5, padx=(50, 5))

        self.entry_search = ctk.CTkEntry(top_bar, width=180)
        self.entry_search.grid(row=0, column=2, sticky="e", pady=5, padx=(140, 10))

        btn_search = ctk.CTkButton(
            top_bar, text="OK", width=50, fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT, command=self.search_books
        )
        btn_search.grid(row=0, column=2, sticky="e", pady=5, padx=(330, 10))

        btn_account = ctk.CTkButton(
            top_bar, text="Compte", width=80, fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT, command=self.open_account_dialog
        )
        btn_account.grid(row=0, column=3, padx=10, pady=5)

        btn_logout = ctk.CTkButton(
            top_bar,
            text="Déconnexion",
            width=100,
            fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT,
            command=self.app.logout
        )
        btn_logout.grid(row=0, column=4, padx=10, pady=5)

        # ---------- Colonne gauche ----------
        left_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_BORDER,
            border_width=1,
        )
        left_frame.grid(row=1, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)

        self.label_result = ctk.CTkLabel(
            left_frame,
            text="Attente d'une recherche pour afficher un résultat",
            anchor="w",
            text_color="black",
        )
        self.label_result.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.books_list_frame = ctk.CTkFrame(left_frame, fg_color=COLOR_CARD_BG)
        self.books_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # ---------- Détails (droite) ----------
        self.detail_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_BORDER,
            border_width=1,
        )
        self.detail_frame.grid(row=1, column=1, sticky="nsew")
        self.detail_frame.grid_rowconfigure(1, weight=1)

        self._show_welcome()

        self.btn_emprunter = ctk.CTkButton(
            self.detail_frame,
            text="Emprunter",
            fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT,
            width=160,
            height=32,
            corner_radius=20,
            command=self.open_borrow_dialog,
        )
        self.btn_emprunter.grid(row=2, column=0, pady=(40, 20))

    # ---------- API ----------
    def set_user(self, username):
        self.current_user = username
        # affiche dans barre du haut
        self.lbl_name.configure(text=username)
        # si tu veux aussi afficher un "card id" ici, tu peux le récupérer depuis data.USERS

    # ---------- UI helpers ----------
    def _clear_detail_except_borrow(self):
        for widget in self.detail_frame.grid_slaves():
            if widget not in (self.btn_emprunter,):
                widget.grid_forget()

        if self.success_label is not None:
            self.success_label.destroy()
            self.success_label = None

    def _show_welcome(self):
        self._clear_detail_except_borrow()

        label_welcome = ctk.CTkLabel(
            self.detail_frame,
            text="Bibliothèque",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="black",
        )
        label_welcome.grid(row=0, column=0, pady=(30, 15), padx=20, sticky="w")

        label_text = ctk.CTkLabel(
            self.detail_frame,
            text=(
                "Recherchez un livre avec la barre de recherche.\n"
                "Cliquez sur un titre pour afficher ses détails.\n"
                "Puis empruntez-le via le bouton Emprunter."
            ),
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color="black",
        )
        label_text.grid(row=1, column=0, sticky="nw", padx=20)

    # ---------- Recherche / affichage ----------
    def search_books(self):
        query = self.entry_search.get().strip().lower()

        for widget in self.books_list_frame.winfo_children():
            widget.destroy()

        if not query:
            self.label_result.configure(text="Veuillez saisir un terme de recherche.")
            return

        results = api_client.search_books(query)

        if not results:
            self.label_result.configure(text=f"Aucun résultat pour '{query}'.")
            return

        self.label_result.configure(text=f"Résultat pour {query}")

        for book in results:
            btn = ctk.CTkButton(
                self.books_list_frame,
                text=book["title"],
                fg_color=COLOR_DARK_RED,
                text_color=COLOR_TEXT,
                corner_radius=0,
                command=lambda b=book: self.show_book_details(b),
            )
            btn.pack(fill="x", pady=3)

        self.show_book_details(results[0])

    def show_book_details(self, book):
        self.current_book = book
        self._clear_detail_except_borrow()

        lbl_title = ctk.CTkLabel(
            self.detail_frame,
            text=book["title"],
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="black",
        )
        lbl_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        stock_txt = "Oui" if book.get("in_stock") else "Non"

        description_text = (
            f"{book['description']}\n\n"
            f"Auteur : {book['author']}\n"
            f"Date de parution : {book['year']}\n"
            f"Maison d'édition : {book['publisher']}\n"
            f"En stock : {stock_txt}"
        )

        lbl_desc = ctk.CTkLabel(
            self.detail_frame,
            text=description_text,
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color="black",
        )
        lbl_desc.grid(row=1, column=0, sticky="nw", padx=20, pady=(5, 10))

        self.btn_emprunter.grid(row=2, column=0, pady=(20, 20))

    # ---------- Emprunt ----------
    def open_borrow_dialog(self):
        if self.current_book is None:
            messagebox.showinfo("Info", "Veuillez d'abord sélectionner un livre.")
            return
        BorrowDialog(self, self.current_book, self.on_borrow_success)

    def on_borrow_success(self, book, card_id):

        book_id = book.get("id")
        ok = api_client.borrow_book(book_id, card_id)

        if not ok:
            messagebox.showerror("Erreur", "Emprunt impossible.")
            return

        if self.success_label is not None:
            self.success_label.destroy()

        self.success_label = ctk.CTkLabel(
            self.detail_frame,
            text="Le livre a été emprunté",
            text_color="white",
            fg_color=COLOR_SUCCESS,
            corner_radius=20,
            font=ctk.CTkFont(size=16, weight="bold"),
            padx=20,
            pady=5,
        )
        self.success_label.grid(row=0, column=0, pady=(5, 0), sticky="n")

    # ---------- Compte ----------
    def open_account_dialog(self):
        if self.current_user is None:
            messagebox.showinfo("Info", "Aucun utilisateur connecté.")
            return
        AccountDialog(self, self.current_user, self.app.logout)
