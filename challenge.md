# Livrable de l'exercice 'Challenge final' concernant la fonction `process_refund()`


***Fonction concernée par les tests*** : 
```py
def process_refund(order, payment_gateway, email_service, hours_before_event):
    """Rembourse une commande confirmée si les règles le permettent.

    Dépendances injectées :
    - payment_gateway.refund(amount_cents, transaction_id) -> {"success": bool}
    - email_service.send(to, subject, body)

    Règles (inspirées de RM6 EventFlow) :
    - commande non "confirmed"                  -> ValueError
    - moins de 48h avant l'événement            -> ValueError (48h pile = autorisé)
    - remboursement refusé par la passerelle    -> PaymentError, aucun e-mail
    - succès                                    -> e-mail, puis dict remboursement
    """
    if order["status"] != "confirmed":
        raise ValueError("Seule une commande confirmée peut être remboursée")
    if hours_before_event < 48:
        raise ValueError("Remboursement impossible à moins de 48h de l'événement")

    refund_result = payment_gateway.refund(
        order["total_cents"], order["transaction_id"]
    )
    if not refund_result["success"]:
        raise PaymentError("Remboursement refusé")

    email_service.send(
        order["user_email"],
        "Remboursement effectué",
        f"Votre commande a été remboursée de {order['total_cents']} centimes.",
    )

    return {"status": "refunded", "amount_cents": order["total_cents"]}
```

***conftest.py*** :
```py
@pytest.fixture
def yield_order_confirmed():
    yield {
        "id": 1,
        "event_id": 1,
        "event_title": "Title of the Event",
        "event_city": "City of the Event",
        "event_starts_at": "start of the Event",
        "status": "confirmed",
        "total_cents": 2495 + 3500 + 7500,
        "created_at": "creation of the event",
        "expires_at": "epiration of the event",
        "items": [
            {"category": "early_bird", "quantity": 1},
            {"category": "standard", "quantity": 1},
            {"category": "vip", "quantity": 1},
        ],
        "transaction_id": "t_id_ok",
        "user_email": "user_1@test.be",
    }


@pytest.fixture
def yield_order_not_confirmed():
    yield {
        "id": 1,
        "event_id": 1,
        "event_title": "Title of the Event",
        "event_city": "City of the Event",
        "event_starts_at": "start of the Event",
        "status": "",
        "total_cents": 2495 + 3500 + 7500,
        "created_at": "creation of the event",
        "expires_at": "epiration of the event",
        "items": [
            {"category": "early_bird", "quantity": 1},
            {"category": "standard", "quantity": 1},
            {"category": "vip", "quantity": 1},
        ],
        "transaction_id": "t_id_ok",
        "user_email": "user_1@test.be",
    }
```


***test_challenge.py*** :
```py
from unittest.mock import Mock

import pytest

from booking import process_refund
from payment import PaymentError


def test_process_refund_positives(yield_order_confirmed):

    # Création des mocks 'payment' et 'email'
    mock_payment = Mock()
    mock_payment.refund.return_value = {"success": True}  # Le paiement sera confirmé
    mock_email = Mock()

    # Check du `return` de la fonction, avec les bonnes valeurs et une valeur limite pour 'hours_before_event'
    assert process_refund(yield_order_confirmed, mock_payment, mock_email, 48) == {
        "status": "refunded",
        "amount_cents": 2495 + 3500 + 7500,
    }

    # Check des appels de composants, avec les bonnes valeurs
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
        process_refund(yield_order_not_confirmed, mock_payment, mock_email, 48)

    # Check des 'non-appels' de composants
    mock_payment.refund.assert_not_called()
    mock_email.send.assert_not_called()


def test_process_refund_less_than_48h(yield_order_confirmed):

    mock_payment = Mock()
    mock_payment.refund.return_value = {"success": True}
    mock_email = Mock()

    # Check valeur limite inférieure
    with pytest.raises(ValueError, match=r"(?i).*moins de 48h"):
        process_refund(yield_order_confirmed, mock_payment, mock_email, 47)

    mock_payment.refund.assert_not_called()
    mock_email.send.assert_not_called()


def test_process_refund_payment_error(yield_order_confirmed):

    mock_payment = Mock()
    mock_payment.refund.return_value = {"success": False}  # Le paiement sera refusé
    mock_email = Mock()

    with pytest.raises(PaymentError, match=r"(?i).*refusé"):
        process_refund(yield_order_confirmed, mock_payment, mock_email, 48)

    mock_payment.refund.assert_called_once_with(2495 + 3500 + 7500, "t_id_ok")
    mock_email.send.assert_not_called()
```