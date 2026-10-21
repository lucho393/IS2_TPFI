"""Pruebas del patrón Observer."""

from unittest.mock import MagicMock

from corporate_observer import CorporateDataObserver


def test_subscribe():
    """Verifica que un cliente pueda suscribirse."""
    observer = CorporateDataObserver()
    client_socket = MagicMock()

    observer.subscribe(
        "CPU-1",
        client_socket,
    )

    assert len(observer.subscribers) == 1
    assert observer.subscribers[0]["UUID"] == "CPU-1"
    assert observer.subscribers[0]["socket"] is client_socket


def test_multiple_subscriptions_same_uuid():
    """Verifica múltiples sockets para un mismo UUID."""
    observer = CorporateDataObserver()

    first_socket = MagicMock()
    second_socket = MagicMock()

    observer.subscribe(
        "CPU-1",
        first_socket,
    )
    observer.subscribe(
        "CPU-1",
        second_socket,
    )

    assert len(observer.subscribers) == 2
    assert observer.subscribers[0]["socket"] is first_socket
    assert observer.subscribers[1]["socket"] is second_socket


def test_unsubscribe():
    """Verifica que pueda eliminarse una suscripción."""
    observer = CorporateDataObserver()
    client_socket = MagicMock()

    observer.subscribe(
        "CPU-1",
        client_socket,
    )

    observer.unsubscribe(client_socket)

    assert observer.subscribers == []


def test_notify():
    """Verifica que todos los suscriptores reciban el mensaje."""
    observer = CorporateDataObserver()

    first_socket = MagicMock()
    second_socket = MagicMock()

    observer.subscribe(
        "CPU-1",
        first_socket,
    )
    observer.subscribe(
        "CPU-2",
        second_socket,
    )

    message = b'{"id": "TEST"}'

    observer.notify(message)

    first_socket.sendall.assert_called_once_with(message)
    second_socket.sendall.assert_called_once_with(message)


def test_notify_removes_disconnected_client():
    """Verifica que se eliminen clientes desconectados."""
    observer = CorporateDataObserver()

    connected_socket = MagicMock()
    disconnected_socket = MagicMock()
    disconnected_socket.sendall.side_effect = OSError("Cliente desconectado")

    observer.subscribe(
        "CPU-1",
        connected_socket,
    )
    observer.subscribe(
        "CPU-2",
        disconnected_socket,
    )

    message = b'{"id": "TEST"}'

    observer.notify(message)

    connected_socket.sendall.assert_called_once_with(message)

    assert len(observer.subscribers) == 1
    assert observer.subscribers[0]["socket"] is connected_socket
