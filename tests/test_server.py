"""Pruebas del servidor del TPFI."""

import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

import singletonproxyobserver


def test_server_parse_arguments(monkeypatch):
    """Verifica los argumentos del servidor."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "singletonproxyobserver.py",
            "-p",
            "8081",
            "-v",
        ],
    )

    args = singletonproxyobserver.parse_arguments()

    assert args.port == 8081
    assert args.verbose is True


def test_server_malformed_arguments(monkeypatch):
    """Verifica argumentos incorrectos del servidor."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "singletonproxyobserver.py",
            "--incorrecto",
        ],
    )

    with pytest.raises(SystemExit):
        singletonproxyobserver.parse_arguments()


def test_server_configure_logging():
    """Verifica la configuración de logging."""
    with patch("singletonproxyobserver.logging.basicConfig") as logging_mock:
        singletonproxyobserver.configure_logging(True)
        logging_mock.assert_called_once()


def test_receive_valid_request():
    """Verifica una solicitud JSON válida."""
    client_socket = MagicMock()
    client_socket.recv.return_value = json.dumps(
        {
            "UUID": "CPU-TEST",
            "ACTION": "get",
            "ID": "TEST",
        }
    ).encode("utf-8")

    result = singletonproxyobserver.receive_request(client_socket)

    assert result["UUID"] == "CPU-TEST"
    assert result["ACTION"] == "get"
    assert result["ID"] == "TEST"


def test_receive_invalid_json():
    """Verifica el rechazo de un JSON inválido."""
    client_socket = MagicMock()
    client_socket.recv.return_value = b"JSON INVALIDO"

    result = singletonproxyobserver.receive_request(client_socket)

    assert result is None


def test_receive_empty_request():
    """Verifica una solicitud vacía."""
    client_socket = MagicMock()
    client_socket.recv.return_value = b""

    result = singletonproxyobserver.receive_request(client_socket)

    assert result is None


def run_server_with_request(monkeypatch, request):
    """Ejecuta una solicitud simulada contra el servidor."""
    args = SimpleNamespace(
        port=8080,
        verbose=False,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "parse_arguments",
        lambda: args,
    )

    proxy = MagicMock()
    observer = MagicMock()

    monkeypatch.setattr(
        singletonproxyobserver,
        "CorporateDataProxy",
        lambda: proxy,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "CorporateDataObserver",
        lambda: observer,
    )

    client_socket = MagicMock()
    client_socket.recv.return_value = json.dumps(request).encode("utf-8")

    server_socket = MagicMock()
    server_socket.accept.side_effect = [
        (client_socket, ("127.0.0.1", 5000)),
        KeyboardInterrupt(),
    ]

    monkeypatch.setattr(
        singletonproxyobserver.socket,
        "socket",
        lambda *args, **kwargs: server_socket,
    )

    singletonproxyobserver.main()

    return proxy, observer, client_socket, server_socket


def test_server_get(monkeypatch):
    """Verifica que get genere una respuesta."""
    _, _, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "UUID": "CPU-TEST",
            "ACTION": "get",
            "ID": "TEST",
        },
    )

    client_socket.sendall.assert_called_once()


def test_server_get_without_id(monkeypatch):
    """Verifica get sin datos mínimos."""
    _, _, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "UUID": "CPU-TEST",
            "ACTION": "get",
        },
    )

    sent = client_socket.sendall.call_args.args[0]
    response = json.loads(sent.decode("utf-8"))

    assert "Error" in response


def test_server_list(monkeypatch):
    """Verifica el camino de list."""
    _, _, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "UUID": "CPU-TEST",
            "ACTION": "list",
        },
    )

    client_socket.sendall.assert_called_once()


def test_server_list_without_uuid(monkeypatch):
    """Verifica list sin UUID."""
    _, _, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "ACTION": "list",
        },
    )

    sent = client_socket.sendall.call_args.args[0]
    response = json.loads(sent.decode("utf-8"))

    assert "Error" in response


def test_server_set(monkeypatch):
    """Verifica el camino de set."""
    _, observer, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "UUID": "CPU-TEST",
            "ACTION": "set",
            "ID": "TEST",
            "localidad": "Concepcion del Uruguay",
        },
    )

    client_socket.sendall.assert_called_once()
    observer.notify.assert_called_once()


def test_server_set_without_id(monkeypatch):
    """Verifica set sin datos mínimos."""
    _, observer, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "UUID": "CPU-TEST",
            "ACTION": "set",
            "localidad": "Concepcion del Uruguay",
        },
    )

    sent = client_socket.sendall.call_args.args[0]
    response = json.loads(sent.decode("utf-8"))

    assert "Error" in response
    observer.notify.assert_not_called()


def test_server_subscribe(monkeypatch):
    """Verifica la suscripción de un Observer."""
    proxy, observer, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "UUID": "CPU-TEST",
            "ACTION": "subscribe",
        },
    )

    proxy.log.log_action.assert_called_once()
    observer.subscribe.assert_called_once_with(
        "CPU-TEST",
        client_socket,
    )


def test_server_subscribe_without_uuid(monkeypatch):
    """Verifica subscribe sin UUID."""
    _, observer, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "ACTION": "subscribe",
        },
    )

    client_socket.sendall.assert_called_once()
    observer.subscribe.assert_not_called()


def test_server_invalid_action(monkeypatch):
    """Verifica una acción desconocida."""
    _, _, client_socket, _ = run_server_with_request(
        monkeypatch,
        {
            "UUID": "CPU-TEST",
            "ACTION": "incorrecta",
        },
    )

    client_socket.close.assert_called()


def test_server_invalid_request(monkeypatch):
    """Verifica una solicitud JSON inválida."""
    args = SimpleNamespace(
        port=8080,
        verbose=False,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "parse_arguments",
        lambda: args,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "CorporateDataProxy",
        MagicMock,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "CorporateDataObserver",
        MagicMock,
    )

    client_socket = MagicMock()
    client_socket.recv.return_value = b"JSON INVALIDO"

    server_socket = MagicMock()
    server_socket.accept.side_effect = [
        (client_socket, ("127.0.0.1", 5000)),
        KeyboardInterrupt(),
    ]

    monkeypatch.setattr(
        singletonproxyobserver.socket,
        "socket",
        lambda *args, **kwargs: server_socket,
    )

    singletonproxyobserver.main()

    client_socket.close.assert_called()


def test_server_port_in_use(monkeypatch):
    """Verifica el intento de iniciar dos servidores."""
    args = SimpleNamespace(
        port=8080,
        verbose=False,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "parse_arguments",
        lambda: args,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "CorporateDataProxy",
        MagicMock,
    )

    monkeypatch.setattr(
        singletonproxyobserver,
        "CorporateDataObserver",
        MagicMock,
    )

    server_socket = MagicMock()
    server_socket.bind.side_effect = OSError("Puerto ocupado")

    monkeypatch.setattr(
        singletonproxyobserver.socket,
        "socket",
        lambda *args, **kwargs: server_socket,
    )

    singletonproxyobserver.main()

    server_socket.close.assert_called()
