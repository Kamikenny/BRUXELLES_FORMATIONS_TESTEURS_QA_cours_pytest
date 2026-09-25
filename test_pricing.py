import pytest

from booking import apply_promo, line_total, order_total, ticket_price

"""
Exercices Bloc 1 & 3 — voir J3_exercices_eleves.md.
Lancez : pytest test_pricing.py -v
"""

promo_codes_test_dict = {
    "valid": {
        "code": "VALID",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 1,
    },
    "inactive": {
        "code": "INVALID",
        "percent_off": 10,
        "active": False,
        "max_uses": 10,
        "used_count": 1,
    },
    "max_used": {
        "code": "MAXUSED",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 10,
    },
    "high_percent": {
        "code": "WRONG",
        "percent_off": 101,
        "active": True,
        "max_uses": 10,
        "used_count": 1,
    },
    "low_percent": {
        "code": "WRONG",
        "percent_off": 0,
        "active": True,
        "max_uses": 10,
        "used_count": 1,
    },
}

items_test_dict = {
    "one_of_each": [
        {"category": "early_bird", "quantity": 1},
        {"category": "standard", "quantity": 1},
        {"category": "vip", "quantity": 1},
    ],
    "no_items": [
        {"category": "early_bird", "quantity": 0},
        {"category": "standard", "quantity": 0},
        {"category": "vip", "quantity": 0},
    ],
    "7_items": [
        {"category": "early_bird", "quantity": 3},
        {"category": "standard", "quantity": 3},
        {"category": "vip", "quantity": 1},
    ],
    "6_items": [
        {"category": "early_bird", "quantity": 3},
        {"category": "standard", "quantity": 2},
        {"category": "vip", "quantity": 1},
    ],
}


# À vous d'écrire les tests.


@pytest.mark.parametrize(
    "value, expected", [("early_bird", 2495), ("standard", 3500), ("vip", 7500)]
)
def test_ticket_price_positives(value, expected):
    assert ticket_price(value) == expected


@pytest.mark.parametrize("value", [(""), ("xyz")])
def test_ticket_price_negatives(value):
    with pytest.raises(ValueError):
        ticket_price(value)


@pytest.mark.parametrize(
    "category, quantity, expected",
    [
        ("early_bird", 1, 2495),
        ("early_bird", 2, 2495 * 2),
        ("standard", 1, 3500),
        ("standard", 3, 3500 * 3),
        ("vip", 1, 7500),
        ("vip", 5, 7500 * 5),
    ],
)
def test_line_total(category, quantity, expected):
    assert line_total(category, quantity) == expected


def test_line_total_negative():
    with pytest.raises(ValueError):
        line_total("vip", -1)


@pytest.mark.parametrize(
    "base_total, promo_code, expected",
    [(100, None, 100), (100, promo_codes_test_dict["valid"], 90)],
)
def test_apply_promo_positives(base_total, promo_code, expected):
    assert apply_promo(base_total, promo_code) == expected


@pytest.mark.parametrize(
    "base_total, promo_code, expected_match",
    [
        (100, promo_codes_test_dict["inactive"], r"(?i).*inactif"),
        (100, promo_codes_test_dict["max_used"], r"(?i).*épuisé"),
        (100, promo_codes_test_dict["low_percent"], r"(?i).*invalide"),
        (100, promo_codes_test_dict["high_percent"], r"(?i).*invalide"),
    ],
    ids=[
        "inactive_promo_code",
        "max_used_promo_code",
        "low_percent_promo_code",
        "high_percent_promo_code",
    ],
)
def test_apply_promo_negatives(base_total, promo_code, expected_match):
    with pytest.raises(ValueError, match=expected_match):
        apply_promo(base_total, promo_code)


@pytest.mark.parametrize(
    "value, expected",
    [
        (items_test_dict["one_of_each"], 2495 + 3500 + 7500),
        (items_test_dict["6_items"], 2495 * 3 + 3500 * 2 + 7500),
    ],
    ids=["one_of_each", "6_items"],
)
def test_order_total_positives(value, expected):
    assert order_total(value) == expected


@pytest.mark.parametrize(
    "value, expected_match",
    [
        (items_test_dict["7_items"], r"(?i).*maximum"),
        (items_test_dict["no_items"], r"(?i).*au moins un billet"),
    ],
    ids=["7_items", "no_items"],
)
def test_order_total_negatives(value, expected_match):
    with pytest.raises(ValueError, match=expected_match):
        order_total(value)
