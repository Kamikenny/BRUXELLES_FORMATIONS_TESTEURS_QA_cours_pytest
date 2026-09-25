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
