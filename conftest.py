import pytest

"""
conftest.py — fixtures partagées entre plusieurs fichiers de test.

Vide au départ : vous y déplacerez vos fixtures au Bloc 5, quand plusieurs
fichiers auront besoin des mêmes données ou des mêmes mocks.
Pytest découvre ce fichier automatiquement : aucune importation nécessaire.
"""


@pytest.fixture(scope="function")
def get_user():
    fixture_user = {"name": "Kenny", "formation": "QA Tester"}
    yield fixture_user
    print("Fermer connexion BD")


@pytest.fixture
def event_1_mock():
    yield {
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
            {
                "id": 3,
                "name": "VIP",
                "price_cents": 7500,
                "quota": 30,
                "available": 30,
            },
        ],
        "available": 240,
    }


@pytest.fixture
def user_fixture_active():
    yield {
        "id": 1,
        "active": True,
        "email": "user_1@test.test",
        "payment_token": "user_pay_token",
    }


@pytest.fixture
def user_fixture_inactive():
    yield {
        "id": 1,
        "active": False,
        "email": "user_1@test.test",
        "payment_token": "user_pay_token",
    }


@pytest.fixture
def yield_promo_code_valid():
    yield {
        "code": "VALID",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 1,
    }


@pytest.fixture
def yield_promo_code_invalid():
    yield {
        "code": "INVALID",
        "percent_off": 10,
        "active": False,
        "max_uses": 10,
        "used_count": 1,
    }


@pytest.fixture
def yield_promo_code_max_used():
    yield {
        "code": "MAXUSED",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 10,
    }


@pytest.fixture
def yield_promo_code_high_percent():
    yield {
        "code": "WRONG",
        "percent_off": 101,
        "active": True,
        "max_uses": 10,
        "used_count": 1,
    }


@pytest.fixture
def yield_promo_code_low_percent():
    yield {
        "code": "WRONG",
        "percent_off": 0,
        "active": True,
        "max_uses": 10,
        "used_count": 1,
    }


@pytest.fixture
def yield_items_list_one_of_each():
    yield [
        {"category": "early_bird", "quantity": 1},
        {"category": "standard", "quantity": 1},
        {"category": "vip", "quantity": 1},
    ]


@pytest.fixture
def yield_items_list_no_items():
    yield [
        {"category": "early_bird", "quantity": 0},
        {"category": "standard", "quantity": 0},
        {"category": "vip", "quantity": 0},
    ]


@pytest.fixture
def yield_items_list_seven_items():
    yield [
        {"category": "early_bird", "quantity": 3},
        {"category": "standard", "quantity": 3},
        {"category": "vip", "quantity": 1},
    ]


@pytest.fixture
def yield_items_list_six_items():
    yield [
        {"category": "early_bird", "quantity": 3},
        {"category": "standard", "quantity": 2},
        {"category": "vip", "quantity": 1},
    ]
