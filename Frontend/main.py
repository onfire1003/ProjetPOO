"""
Nom du fichier : main.py
Nom du créateur : Samuel Antunes
Date de création : 17.12.2025
"""


from theme import setup_ctk_theme
from app import App

if __name__ == "__main__":
    setup_ctk_theme()
    app = App()
    app.mainloop()
