import pytest

"""
Exercices Bloc 1 & 3 — voir J3_exercices_eleves.md.
Lancez : pytest test_pricing.py -v
"""
from booking import ticket_price, line_total, apply_promo, order_total

promo_codes_test_dict = {
    "valid": {
        "code": "VALID",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    }, 
    "inactive": {
        "code": "INVALID",
        "percent_off": 10,
        "active": False,
        "max_uses": 10,
        "used_count": 1
    },
    "max_used": {
        "code": "MAXUSED",
        "percent_off": 10,
        "active": True,
        "max_uses": 10,
        "used_count": 10
    },
    "high_percent": {
        "code": "WRONG",
        "percent_off": 101,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    },
    "low_percent": {
        "code": "WRONG",
        "percent_off": 0,
        "active": True,
        "max_uses": 10,
        "used_count": 1
    },
}

items_test_dict = {
    "one_of_each": [
        {
            "category": "early_bird",
            "quantity": 1
        },
        {
            "category": "standard",
            "quantity": 1
        },
        {
            "category": "vip",
            "quantity": 1
        }
    ],
    "no_items": [
        {
            "category": "early_bird",
            "quantity": 0
        },
        {
            "category": "standard",
            "quantity": 0
        },
        {
            "category": "vip",
            "quantity": 0
        }
    ],
    "7_items": [
        {
            "category": "early_bird",
            "quantity": 3
        },
        {
            "category": "standard",
            "quantity": 3
        },
        {
            "category": "vip",
            "quantity": 1
        }
    ],
    "6_items": [
        {
            "category": "early_bird",
            "quantity": 3
        },
        {
            "category": "standard",
            "quantity": 2
        },
        {
            "category": "vip",
            "quantity": 1
        }
    ]
}


# À vous d'écrire les tests.


def test_ticket_price():
    assert ticket_price("early_bird") == 2495
    assert ticket_price("standard") == 3500
    assert ticket_price("vip") == 7500

def test_ticket_price_value_error_empty():
    with pytest.raises(ValueError):
        ticket_price("")

def test_ticket_price_value_error_wrong():
    with pytest.raises(ValueError):
        ticket_price("xyz")

def test_line_total():
    assert line_total("early_bird", 1) == 2495
    assert line_total("early_bird", 2) == 2495 * 2
    assert line_total("vip", 2) == 15000

def test_line_total_negative_value_error():
    with pytest.raises(ValueError):
        line_total("vip", -1)


def test_apply_promo():
    assert apply_promo(100, None) == 100
    assert apply_promo(100, promo_codes_test_dict["valid"]) == 100 - (100 * 10 // 100)

def test_apply_promo_inactive():
    with pytest.raises(ValueError, match=r"(?i).*inactif"):
        apply_promo(100, promo_codes_test_dict["inactive"])

def test_apply_promo_max_used():
    with pytest.raises(ValueError, match=r"(?i).*épuisé"):
        apply_promo(100, promo_codes_test_dict["max_used"])

def test_apply_promo_low_percent():
    with pytest.raises(ValueError, match=r"(?i).*invalide"):
        apply_promo(100, promo_codes_test_dict["low_percent"])

def test_apply_promo_high_percent():
    with pytest.raises(ValueError, match=r"(?i).*invalide"):
        apply_promo(100, promo_codes_test_dict["high_percent"])


def test_order_total():
    assert order_total(items_test_dict["one_of_each"]) == 2495 + 3500 + 7500
    assert order_total(items_test_dict["6_items"]) == 2495 * 3 + 3500 * 2 + 7500

def test_order_total_no_items():
    with pytest.raises(ValueError, match=r"(?i).*au moins un billet"):
        order_total(items_test_dict["no_items"])

def test_order_total_7_items():
    with pytest.raises(ValueError, match=r"(?i).*maximum"):
        order_total(items_test_dict["7_items"])