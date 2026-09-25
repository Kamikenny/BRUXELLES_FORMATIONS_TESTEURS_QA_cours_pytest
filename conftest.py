import pytest

"""
conftest.py — fixtures partagées entre plusieurs fichiers de test.

Vide au départ : vous y déplacerez vos fixtures au Bloc 5, quand plusieurs
fichiers auront besoin des mêmes données ou des mêmes mocks.
Pytest découvre ce fichier automatiquement : aucune importation nécessaire.
"""


@pytest.fixture
def get_user():
    fixture_user = {"name": "Kenny", "formation": "QA Tester"}
    yield fixture_user
    print("Fermer connexion BD")


@pytest.fixture
def event_1():
    return {
        "id": 1,
        "title": "Nuit electro - Halles Saint-Gery",
        "description": "Une nuit electro au coeur de Bruxelles.",
        "city": "Bruxelles",
        "venue": "Halles Saint-Gery",
        "starts_at": "2026-10-07T11:58:14.086928Z",
        "capacity": 300,
        "status": "published",
        "cover_color": "#6C4DF6",
        "categories": [
            {
                "id": 1,
                "name": "Early bird",
                "price_cents": 2495,
                "quota": 60,
                "available": 60,
            },
            {
                "id": 2,
                "name": "Plein tarif",
                "price_cents": 3500,
                "quota": 150,
                "available": 150,
            },
            {"id": 3, "name": "VIP", "price_cents": 7500, "quota": 30, "available": 30},
        ],
        "available": 240,
    }
