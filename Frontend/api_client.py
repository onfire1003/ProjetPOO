"""
Nom du fichier : api_client.py
Nom du créateur : Samuel Antunes
Date de création : 17.12.2025
"""


# api_client.py
# ==================================================
# FAKE BACKEND / FAKE BASE DE DONNÉES (TEMPORAIRE)
# ==================================================

# ---------- UTILISATEURS ----------
_USERS = {
    "alice": {
        "password": "1234",
        "card_id": "C001"
    },
    "bob": {
        "password": "abcd",
        "card_id": "C002"
    },
    "chef": {
        "password": "bebe",
        "card_id": "C003"
    },
    "samuel": {
        "password": "antunes",
        "card_id": "C004"
    },
}

# ---------- LIVRES ----------
_BOOKS = [
    {
        "id": 1,
        "title": "Le petit prince",
        "description": "Un aviateur rencontre un jeune prince venu d'une autre planète.",
        "author": "Antoine de Saint-Exupéry",
        "year": 1943,
        "publisher": "Reynal & Hitchcock",
        "in_stock": True,
    },
    {
        "id": 2,
        "title": "Les misérables",
        "description": "L'histoire de Jean Valjean dans une France marquée par la misère.",
        "author": "Victor Hugo",
        "year": 1862,
        "publisher": "A. Lacroix, Verboeckhoven & Cie.",
        "in_stock": True,
    },
    {
        "id": 3,
        "title": "Dune",
        "description": "Intrigues politiques et prophéties sur la planète désertique Arrakis.",
        "author": "Frank Herbert",
        "year": 1965,
        "publisher": "Chilton Books",
        "in_stock": True,
    },
    {
        "id": 4,
        "title": "Hunger Games",
        "description": "essai de livre",
        "author": "jsp",
        "year": 1000,
        "publisher": "Chilton Books",
        "in_stock": False,
    },
]

# ---------- EMPRUNTS ----------
_EMPRUNTS = []   # liste de dicts


# ==================================================
# API PUBLIQUE (UTILISÉE PAR LE FRONTEND)
# ==================================================

def login(username: str, password: str) -> bool:
    """Vérifie les identifiants utilisateur"""
    user = _USERS.get(username)
    return user is not None and user["password"] == password


def get_card_id(username: str) -> str | None:
    """Retourne l'ID de carte de l'utilisateur"""
    user = _USERS.get(username)
    return user["card_id"] if user else None


def search_books(query: str) -> list[dict]:
    """Recherche de livres par titre"""
    q = (query or "").lower().strip()
    if not q:
        return []
    return [b for b in _BOOKS if q in b["title"].lower()]


def borrow_book(book_id: int, card_id: str) -> bool:
    """Simule un emprunt"""
    # vérifie carte
    if card_id not in [u["card_id"] for u in _USERS.values()]:
        return False

    # vérifie livre
    for book in _BOOKS:
        if book["id"] == book_id and book["in_stock"]:
            book["in_stock"] = False
            _EMPRUNTS.append({
                "book_id": book_id,
                "card_id": card_id
            })
            return True

    return False


def get_all_emprunts() -> list[dict]:
    """Debug / futur écran 'Mes emprunts'"""
    return _EMPRUNTS


def is_valid_card_id(card_id: str) -> bool:
    """Vérifie si l'ID de carte existe"""
    card_id = (card_id or "").strip()
    return card_id in [u["card_id"] for u in _USERS.values()]