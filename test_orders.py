"""
Exercices 5 & 6 — voir J3_exercices_eleves.md.
Lancez : pytest test_orders.py -v

Exercice 5 (fixtures) : create_order a besoin d'un utilisateur, d'un événement
et de deux services externes (paiement, e-mail). Les deux faux services sont
fournis ci-dessous, prêts à l'emploi. Pour l'instant, considérez-les comme des
boîtes noires : on comprendra leur fonctionnement au bloc mocks (exercice 6).

Votre travail ici : écrire le cas nominal de create_order, repérer la répétition
du setup, l'extraire en fixtures, en déplacer dans conftest.py, écrire une
fixture avec yield.

Exercice 6 (mocks) : ensuite seulement, concevez la vraie suite des interactions
de create_order avec ses dépendances (voir énoncé).
"""

from unittest.mock import Mock

import pytest

from booking import create_order
from payment import PaymentError

# À vous d'écrire le cas nominal puis de travailler les fixtures.


def test_create_order_positive(
    event_1_mock, yield_items_list_one_of_each, user_fixture_active
):
    payment_mock = Mock()
    payment_mock.charge.return_value = {"success": True, "transaction_id": "tx_1"}
    email = Mock()

    assert create_order(
        event_1_mock,
        yield_items_list_one_of_each,
        user_fixture_active,
        payment_mock,
        email,
    ) == {
        "status": "confirmed",
        "total_cents": 2495 + 3500 + 7500,
        "tickets": 3,
        "user_email": "user_1@test.test",
        "transaction_id": "tx_1",
    }
    payment_mock.charge.assert_called_once()
    payment_mock.charge.assert_called_once_with(2495 + 3500 + 7500, "user_pay_token")
    email.send.assert_called_once()


def test_create_order_inactive_user(
    event_1_mock, yield_items_list_one_of_each, user_fixture_inactive
):
    payment_mock = Mock()
    payment_mock.charge.return_value = {"success": True, "transaction_id": "tx_1"}
    email = Mock()

    with pytest.raises(ValueError, match=r"(?i).*inactif"):
        create_order(
            event_1_mock,
            yield_items_list_one_of_each,
            user_fixture_inactive,
            payment_mock,
            email,
        )
    payment_mock.charge.assert_not_called()
    email.send.assert_not_called()


def test_create_order_failed_payment(
    event_1_mock, yield_items_list_one_of_each, user_fixture_active
):
    payment_mock = Mock()
    payment_mock.charge.return_value = {"success": False, "transaction_id": "tx_1"}
    email = Mock()

    with pytest.raises(PaymentError, match=r"(?i).*refus.*"):
        create_order(
            event_1_mock,
            yield_items_list_one_of_each,
            user_fixture_active,
            payment_mock,
            email,
        )
    email.send.assert_not_called()


def test_create_order_empty_items_list(
    event_1_mock, yield_items_list_no_items, user_fixture_active
):
    payment_mock = Mock()
    payment_mock.charge.return_value = {"success": True, "transaction_id": "tx_1"}
    email = Mock()

    with pytest.raises(ValueError, match=r"(?i).*doit être positif.*"):
        create_order(
            event_1_mock,
            yield_items_list_no_items,
            user_fixture_active,
            payment_mock,
            email,
        )
    email.send.assert_not_called()
