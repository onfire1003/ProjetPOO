"""
Fenêtre de connexion simple avec Tkinter
Version : 1.0
"""

import tkinter as tk
from tkinter import messagebox

# --------------------------------------------------
# Couleurs
# --------------------------------------------------
COLOR_BG_MAIN = "#B2885E"  # Fond de la fenêtre
COLOR_CARD_BG = "#9D7153"  # Fond du cadre central
COLOR_DARK_RED = "#6D071A"  # Champs + bouton
COLOR_TEXT = "#FFFFFF"  # Texte clair (bouton, titre)

# --------------------------------------------------
# Fenêtre principale
# --------------------------------------------------
root = tk.Tk()
root.title("LOG IN")

root.geometry("850x550")
root.resizable(False, False)
root.configure(bg=COLOR_BG_MAIN)


def on_login():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showwarning("Attention", "Veuillez remplir les deux champs.")
    else:
        messagebox.showinfo("Infos", f"Tentative de connexion de : {username}")


# --------------------------------------------------
# Cadre central
# --------------------------------------------------
card = tk.Frame(
    root,
    bg=COLOR_CARD_BG,
    bd=1,
    relief="solid"
)

card_width = 500
card_height = 275
card.place(relx=0.5, rely=0.5, anchor="center", width=card_width, height=card_height)

# On prépare 3 colonnes pour mieux centrer le contenu
card.grid_columnconfigure(0, weight=1)  # labels
card.grid_columnconfigure(1, weight=1)  # entrées
card.grid_columnconfigure(2, weight=1)  # colonne vide pour équilibrer

# --------------------------------------------------
# Titre "IDENTIFICATION" (centré)
# --------------------------------------------------
label_title = tk.Label(
    card,
    text="IDENTIFICATION",
    bg=COLOR_CARD_BG,
    fg=COLOR_TEXT,
    font=("Arial", 12, "bold")
)
# On occupe les 3 colonnes pour être bien au centre
label_title.grid(row=0, column=0, columnspan=3, pady=(15, 25))

# --------------------------------------------------
# Ligne "Username"
# --------------------------------------------------
label_username = tk.Label(
    card,
    text="Username  : ",
    bg=COLOR_CARD_BG,
    fg="white",
    font=("Arial", 10)
)
# Aligné à droite de la colonne 0, sans gros décalage à gauche
label_username.grid(row=1, column=0, pady=5, sticky="e")

entry_username = tk.Entry(
    card,
    bg=COLOR_DARK_RED,
    fg=COLOR_TEXT,
    insertbackground=COLOR_TEXT,
    width=20,
    relief="flat"
)
# Entrée dans la colonne 1, légèrement vers la gauche
entry_username.grid(row=1, column=1, pady=5, ipady=3, sticky="w")

# --------------------------------------------------
# Ligne "Password"
# --------------------------------------------------
label_password = tk.Label(
    card,
    text="Password  : ",
    bg=COLOR_CARD_BG,
    fg="white",
    font=("Arial", 10)
)
label_password.grid(row=2, column=0, pady=25, sticky="e")

entry_password = tk.Entry(
    card,
    bg=COLOR_DARK_RED,
    fg=COLOR_TEXT,
    insertbackground=COLOR_TEXT,
    width=20,
    show="*",
    relief="flat"
)
entry_password.grid(row=2, column=1, pady=5, ipady=3, sticky="w")

# --------------------------------------------------
# Bouton "Se Connecter" (centré)
# --------------------------------------------------
btn_login = tk.Button(
    card,
    text="Se Connecter",
    bg=COLOR_DARK_RED,
    fg=COLOR_TEXT,
    activebackground=COLOR_DARK_RED,
    activeforeground=COLOR_TEXT,
    font=("Arial", 10),
    relief="flat",
    command=on_login,
    width=14,  # largeur en nombre de caractères
    height=1  # hauteur en nombre de lignes de texte
)

# On occupe les 3 colonnes → bien centré sous les champs
btn_login.grid(row=3, column=0, columnspan=3, padx=(0, 18), pady=(50, 10))

# --------------------------------------------------
# Lancement
# --------------------------------------------------
root.mainloop()