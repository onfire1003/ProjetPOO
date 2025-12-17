import customtkinter as ctk
from tkinter import messagebox

# --------------------------------------------------
# "Fake" base de données
# --------------------------------------------------
# utilisateurs pour le login
USERS = {
    "alice": {"password": "1234", "card_id": "C001"},
    "bob":   {"password": "abcd", "card_id": "C002"},
    "chef": {"password": "bebe", "card_id": "C003"},
}

# dictionnaire pour vérifier rapidement une carte
CARD_ID_TO_USER = {u["card_id"]: name for name, u in USERS.items()}

# quelques livres pour la démo
BOOKS = [
    {
        "title": "Le petit prince",
        "description": "Un aviateur rencontre un jeune prince venu d'une autre planète.",
        "author": "Antoine de Saint-Exupéry",
        "year": 1943,
        "publisher": "Reynal & Hitchcock",
    },
    {
        "title": "Les misérables",
        "description": "L'histoire de Jean Valjean dans une France marquée par la misère.",
        "author": "Victor Hugo",
        "year": 1862,
        "publisher": "A. Lacroix, Verboeckhoven & Cie.",
    },
    {
        "title": "Le Hobbit",
        "description": "Bilbo Sacquet se lance dans une aventure inattendue avec des nains.",
        "author": "J. R. R. Tolkien",
        "year": 1937,
        "publisher": "George Allen & Unwin",
    },
    {
        "title": "Dune",
        "description": "Intrigues politiques et prophéties sur la planète désertique Arrakis.",
        "author": "Frank Herbert",
        "year": 1965,
        "publisher": "Chilton Books",
    },
    {
        "title": "1984",
        "description": "Une dystopie sur la surveillance totale d'un régime totalitaire.",
        "author": "George Orwell",
        "year": 1949,
        "publisher": "Secker & Warburg",
    },
    {
        "title": "Hunger Games 1",
        "description": "Katniss participe aux Hunger Games et devient un symbole de rébellion.",
        "author": "Suzanne Collins",
        "year": 2008,
        "publisher": "Scholastic Press",
    },
    {
        "title": "Hunger Games 2",
        "description": "La révolte gronde alors que Katniss devient le Geai Moqueur.",
        "author": "Suzanne Collins",
        "year": 2009,
        "publisher": "Scholastic Press",
    },
    {
        "title": "Hunger Games 3",
        "description": "Conclusion de la trilogie, la guerre ouverte contre le Capitole.",
        "author": "Suzanne Collins",
        "year": 2010,
        "publisher": "Scholastic Press",
    },
]

# --------------------------------------------------
# Couleurs
# --------------------------------------------------
COLOR_BG_MAIN   = "#B2885E"   # Fond de la fenêtre
COLOR_CARD_BG   = "#9D7153"   # Fond des cadres
COLOR_DARK_RED  = "#6D071A"   # Boutons / champs
COLOR_TEXT      = "#FFFFFF"   # Texte clair
COLOR_BORDER    = "#000000"   # Contours noirs
COLOR_SUCCESS   = "#00AA55"   # Message succès


# --------------------------------------------------
# Config CustomTkinter globale
# --------------------------------------------------
ctk.set_appearance_mode("light")          # "light" / "dark" / "system"
ctk.set_default_color_theme("blue")


# --------------------------------------------------
# Fenêtre "popup" pour emprunter
# --------------------------------------------------
class BorrowDialog(ctk.CTkToplevel):
    def __init__(self, master, book, on_success):
        super().__init__(master)
        self.title("remplir info pour emprunter")
        self.geometry("350x220")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_CARD_BG)

        self.book = book
        self.on_success = on_success

        # centrer la fenetre par rapport au parent
        self.update_idletasks()
        if master is not None:
            x = master.winfo_x() + master.winfo_width() // 2 - self.winfo_width() // 2
            y = master.winfo_y() + master.winfo_height() // 2 - self.winfo_height() // 2
            self.geometry(f"+{x}+{y}")

        # Titre
        label_title = ctk.CTkLabel(
            self,
            text="Entrez informations",
            font=ctk.CTkFont(family="Arial", size=20, weight="bold"),
            text_color="black",
        )
        label_title.pack(pady=(15, 10))

        # Label + champ
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

        # Bouton enregistrer
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

        # empêcher interaction avec la fenêtre principale tant que celle-ci est ouverte
        self.grab_set()
        self.entry_card.focus()

    def validate_card(self):
        card_id = self.entry_card.get().strip()

        if not card_id:
            messagebox.showerror("Erreur", "Veuillez saisir un ID de carte.")
            return

        if card_id not in CARD_ID_TO_USER:
            messagebox.showerror("Erreur", "ID de carte inconnu.")
            return

        # Succès : on appelle le callback et on ferme la fenêtre
        self.on_success(self.book, card_id)
        self.destroy()


# --------------------------------------------------
# Fenêtre "compte" pour changer d'utilisateur
# --------------------------------------------------
class AccountDialog(ctk.CTkToplevel):
    def __init__(self, master, username, on_logout):
        super().__init__(master)
        self.title("Compte utilisateur")
        self.geometry("260x200")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_CARD_BG)

        # centrer la fenetre
        self.update_idletasks()
        if master is not None:
            x = master.winfo_x() + master.winfo_width() // 2 - self.winfo_width() // 2
            y = master.winfo_y() + master.winfo_height() // 2 - self.winfo_height() // 2
            self.geometry(f"+{x}+{y}")

        # Bouton avec nom d'utilisateur (juste informatif)
        btn_user = ctk.CTkButton(
            self,
            text=f"Nom d'utilisateur : {username}",
            fg_color=COLOR_DARK_RED,
            hover_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT,
            corner_radius=20,
        )
        btn_user.pack(pady=(30, 15), padx=20, fill="x")

        # Bouton de déconnexion
        btn_logout = ctk.CTkButton(
            self,
            text="Déconnexion",
            fg_color=COLOR_DARK_RED,
            hover_color="#8A0A22",
            text_color=COLOR_TEXT,
            corner_radius=20,
            command=lambda: self._logout(on_logout),
        )
        btn_logout.pack(pady=10, padx=20, fill="x")

        self.grab_set()

    def _logout(self, on_logout):
        on_logout()
        self.destroy()


# --------------------------------------------------
# Page d'accueil (recherche + emprunt)
# --------------------------------------------------
class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=COLOR_BG_MAIN)
        self.app = app
        self.current_user = None
        self.current_book = None
        self.success_label = None   # label pour "Le livre a été emprunté"

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

        # colonnes
        top_bar.grid_columnconfigure(0, weight=0)
        top_bar.grid_columnconfigure(1, weight=0)
        top_bar.grid_columnconfigure(2, weight=1)
        top_bar.grid_columnconfigure(3, weight=0)

        lbl_name = ctk.CTkLabel(
            top_bar,
            text="NAME",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black",
        )
        lbl_name.grid(row=0, column=0, padx=10, pady=5)

        lbl_card = ctk.CTkLabel(
            top_bar,
            text="Numéro_Carte",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black",
        )
        lbl_card.grid(row=0, column=1, padx=10, pady=5)

        lbl_search = ctk.CTkLabel(
            top_bar,
            text="Recherche :",
            font=ctk.CTkFont(size=14),
            text_color="black",
        )
        lbl_search.grid(row=0, column=2, sticky="e", pady=5, padx=(50, 5))

        self.entry_search = ctk.CTkEntry(
            top_bar,
            width=180,
        )
        self.entry_search.grid(row=0, column=2, sticky="e", pady=5, padx=(140, 10))

        btn_search = ctk.CTkButton(
            top_bar,
            text="OK",
            width=50,
            fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT,
            command=self.search_books,
        )
        btn_search.grid(row=0, column=2, sticky="e", pady=5, padx=(330, 10))

        # bouton compte (pour changer d'utilisateur)
        btn_account = ctk.CTkButton(
            top_bar,
            text="Compte",
            width=80,
            fg_color=COLOR_DARK_RED,
            text_color=COLOR_TEXT,
            command=self.open_account_dialog,
        )
        btn_account.grid(row=0, column=3, padx=10, pady=5)

        # ---------- Colonne de gauche : liste / infos ----------
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

        self.books_list_frame = ctk.CTkFrame(
            left_frame,
            fg_color=COLOR_CARD_BG,
        )
        self.books_list_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # ---------- Zone principale : détail du livre ----------
        self.detail_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_BORDER,
            border_width=1,
        )
        self.detail_frame.grid(row=1, column=1, sticky="nsew")

        self.detail_frame.grid_rowconfigure(1, weight=1)

        self.label_welcome = ctk.CTkLabel(
            self.detail_frame,
            text="Bienvenue",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="black",
        )
        self.label_welcome.grid(row=0, column=0, pady=(30, 15), padx=20)

        self.label_text = ctk.CTkLabel(
            self.detail_frame,
            text=(
                "Vous êtes sur notre bibliothèque numérique !\n\n"
                "Découvrez un espace dédié à la lecture et à la découverte.\n"
                "Recherchez facilement nos ouvrages grâce à notre barre de recherche intégrée,\n"
                "explorez les titres disponibles et consultez leurs informations détaillées."
            ),
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color="black",
        )
        self.label_text.grid(row=1, column=0, sticky="nw", padx=20)

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

    # ------------- API ---------------

    def set_user(self, username):
        self.current_user = username

    # ------------- Recherche / affichage livres ---------------

    def search_books(self):
        query = self.entry_search.get().strip().lower()
        for widget in self.books_list_frame.winfo_children():
            widget.destroy()

        if not query:
            self.label_result.configure(text="Veuillez saisir un terme de recherche.")
            return

        results = [book for book in BOOKS if query in book["title"].lower()]

        if not results:
            self.label_result.configure(text=f"Aucun résultat pour '{query}'.")
            return

        self.label_result.configure(text=f"Résultat pour {query}")

        # création des boutons de livres
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

        # afficher le premier par défaut
        self.show_book_details(results[0])

    def show_book_details(self, book):
        self.current_book = book

        # on efface les widgets "centrés" (sauf le bouton emprunter)
        for widget in self.detail_frame.grid_slaves():
            if widget not in (self.btn_emprunter,):
                widget.grid_forget()

        # éventuellement enlever ancien message succès
        if self.success_label is not None:
            self.success_label.destroy()
            self.success_label = None

        # Titre du livre
        lbl_title = ctk.CTkLabel(
            self.detail_frame,
            text=book["title"],
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="black",
        )
        lbl_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Description
        description_text = (
            f"{book['description']}\n\n"
            f"Auteur : {book['author']}\n"
            f"Date de parution : {book['year']}\n"
            f"Maison d'édition : {book['publisher']}\n"
            "En stock : Oui/Non"
        )

        lbl_desc = ctk.CTkLabel(
            self.detail_frame,
            text=description_text,
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color="black",
        )
        lbl_desc.grid(row=1, column=0, sticky="nw", padx=20, pady=(5, 10))

        # le bouton "Emprunter" reste en row=2
        self.btn_emprunter.grid(row=2, column=0, pady=(20, 20))

    # ------------- Emprunt ---------------

    def open_borrow_dialog(self):
        if self.current_book is None:
            messagebox.showinfo("Info", "Veuillez d'abord sélectionner un livre.")
            return

        BorrowDialog(self, self.current_book, self.on_borrow_success)

    def on_borrow_success(self, book, card_id):
        # Ici tu pourrais mettre à jour une vraie BDD, enregistrer l'emprunt, etc.
        # On affiche juste un label de succès tout en haut.

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

    # ------------- Compte / déconnexion ---------------

    def open_account_dialog(self):
        if self.current_user is None:
            messagebox.showinfo("Info", "Aucun utilisateur connecté.")
            return
        AccountDialog(self, self.current_user, self.app.logout)


# --------------------------------------------------
# Page de login
# --------------------------------------------------
class LoginFrame(ctk.CTkFrame):
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

        # Username
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

        # Password
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

        # Bouton login
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

        if username not in USERS or USERS[username]["password"] != password:
            messagebox.showerror("Erreur", "Identifiants incorrects.")
            return

        # succès → on passe à l'accueil
        self.app.login_success(username)


# --------------------------------------------------
# Application principale
# --------------------------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bibliothèque")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_MAIN)

        self.current_user = None

        self.login_frame = LoginFrame(self, self)
        self.home_frame = HomeFrame(self, self)

        self.show_login()

    def show_login(self):
        self.home_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)

    def show_home(self):
        self.login_frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)

    def login_success(self, username):
        self.current_user = username
        self.home_frame.set_user(username)
        self.show_home()

    def logout(self):
        # déconnexion → retour au login
        self.current_user = None
        self.show_login()


if __name__ == "__main__":
    app = App()
    app.mainloop()