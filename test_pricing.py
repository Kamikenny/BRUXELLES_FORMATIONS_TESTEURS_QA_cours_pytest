"""
Exercices Bloc 1 & 3 — voir J3_exercices_eleves.md.
Lancez : pytest test_pricing.py -v
"""
from booking import ticket_price, line_total, apply_promo, order_total

# À vous d'écrire les tests.


def test_ticket_price():
    assert ticket_price("early_bird") == 2495
    assert ticket_price("standard") == 3500
    assert ticket_price("vip") == 7500
    # assert ticket_price("") == 2495
    # assert ticket_price("xyz") == 2495

def test_line_total():
    assert line_total("early_bird", 1) == 2495
    assert line_total("early_bird", 2) == 2495 * 2
    assert line_total("vip", 2) == 15000