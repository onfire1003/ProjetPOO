"""
Nom du fichier : theme.py
Nom du créateur : Samuel Antunes
Date de création : 17.12.2025
"""


import customtkinter as ctk

# --------------------------------------------------
# Couleurs
# --------------------------------------------------
COLOR_BG_MAIN   = "#B2885E"
COLOR_CARD_BG   = "#9D7153"
COLOR_DARK_RED  = "#6D071A"
COLOR_TEXT      = "#FFFFFF"
COLOR_BORDER    = "#000000"
COLOR_SUCCESS   = "#00AA55"

def setup_ctk_theme():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
