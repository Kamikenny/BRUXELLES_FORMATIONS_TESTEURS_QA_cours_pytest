"""
Challenge final — process_refund (voir J3_exercices_eleves.md).

Lisez la spécification (énoncé + docstring de process_refund) et écrivez une
suite de tests pertinente et complète.

À VOUS de décider ce dont vous avez besoin : assertions, gestion des cas
interdits, jeux de données, préparation réutilisable, isolation des dépendances…
Rien ne vous est imposé ni suggéré ici : ces choix font partie de l'exercice.

Lancez : pytest test_challenge.py -v
"""

# À vous.

from unittest.mock import Mock

import pytest

from booking import process_refund
from payment import PaymentError


def test_process_refund_positives(yield_order_confirmed):

    mock_payment = Mock()
    mock_payment.refund.return_value = {"success": True}
    mock_email = Mock()

    assert process_refund(yield_order_confirmed, mock_payment, mock_email, 48) == {
        "status": "refunded",
        "amount_cents": 2495 + 3500 + 7500,
    }
    mock_payment.refund.assert_called_once()
    mock_payment.refund.assert_called_once_with(2495 + 3500 + 7500, "t_id_ok")
    mock_email.send.assert_called_once_with(
        "user_1@test.be",
        "Remboursement effectué",
        f"Votre commande a été remboursée de {2495 + 3500 + 7500} centimes.",
    )


def test_process_refund_unconfirmed_order(yield_order_not_confirmed):

    mock_payment = Mock()
    mock_payment.refund.return_value = {"success": True}
    mock_email = Mock()

    with pytest.raises(ValueError, match=r"(?i).*confirmée.*remboursée"):
        process_refund(yield_order_not_confirmed, mock_payment, mock_email, 49)

    mock_payment.refund.assert_not_called()
    mock_email.send.assert_not_called()


def test_process_refund_less_than_48h(yield_order_confirmed):

    mock_payment = Mock()
    mock_payment.refund.return_value = {"success": True}
    mock_email = Mock()

    with pytest.raises(ValueError, match=r"(?i).*moins de 48h"):
        process_refund(yield_order_confirmed, mock_payment, mock_email, 47)

    mock_payment.refund.assert_not_called()
    mock_email.send.assert_not_called()


def test_process_refund_payment_error(yield_order_confirmed):

    mock_payment = Mock()
    mock_payment.refund.return_value = {"success": False}
    mock_email = Mock()

    with pytest.raises(PaymentError, match=r"(?i).*refusé"):
        process_refund(yield_order_confirmed, mock_payment, mock_email, 48)

    mock_payment.refund.assert_called_once_with(2495 + 3500 + 7500, "t_id_ok")
    mock_email.send.assert_not_called()
