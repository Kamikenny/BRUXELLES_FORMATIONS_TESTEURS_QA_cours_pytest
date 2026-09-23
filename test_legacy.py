import pytest

"""
Exercice Bloc 2 — Code hérité (voir énoncé).
Lisez la spécification dans legacy_pricing.py, concevez vos cas, écrivez vos
tests, lancez-les, et diagnostiquez tout écart avec la spécification.
Lancez : pytest test_legacy.py -v
"""
from legacy_pricing import loyalty_discount_percent, price_with_loyalty

# À vous d'écrire les tests.

def test_loyalty_discount_percent_negative_value_error():
    with pytest.raises(ValueError):
        loyalty_discount_percent(-1)

def test_loyalty_discount_percent_float_value_error():
    with pytest.raises(ValueError):
        loyalty_discount_percent(1.5)

def test_low_loyalty_discount_percent():
    assert loyalty_discount_percent(0) == 0
    assert loyalty_discount_percent(2) == 0

def test_medium_loyalty_discount_percent():
    assert loyalty_discount_percent(3) == 5
    assert loyalty_discount_percent(9) == 5

def test_high_loyalty_discount_percent():
    assert loyalty_discount_percent(10) == 10 # Erreur à corriger dans le code - corrigé
    assert loyalty_discount_percent(11) == 10


def test_low_price_with_loyalty():
    assert price_with_loyalty(100, 0) == 100
    assert price_with_loyalty(100, 2) == 100

def test_medium_price_with_loyalty():
    assert price_with_loyalty(2495, 3) == 2495 - (2495 * 5 // 100)
    assert price_with_loyalty(3500, 9) == 3500 - (3500 * 5 // 100)

def test_high_price_with_loyalty():
    assert price_with_loyalty(100, 10) == 100 - (100 * 10 // 100)
    assert price_with_loyalty(7500, 11) == 7500 - (7500 * 10 // 100)