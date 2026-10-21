"""Pruebas de los clientes del TPFI."""

import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, mock_open, patch

import pytest

import observerclient
import singletonclient


def test_singletonclient_parse_arguments(monkeypatch):
    """Verifica los argumentos del SingletonClient."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "singletonclient.py",
            "-i",
            "input.json",
            "-o",
            "output.json",
            "-v",
        ],
    )

    args = singletonclient.parse_arguments()

    assert args.input == "input.json"
    assert args.output == "output.json"
    assert args.verbose is True


def test_singletonclient_malformed_arguments(monkeypatch):
    """Verifica el rechazo de argumentos incorrectos."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["singletonclient.py", "--incorrecto"],
    )

    with pytest.raises(SystemExit):
        singletonclient.parse_arguments()


def test_singletonclient_configure_logging():
    """Verifica la configuración de logging."""
    with patch("singletonclient.logging.basicConfig") as logging_mock:
        singletonclient.configure_logging(True)
        logging_mock.assert_called_once()


def test_singletonclient_load_request():
    """Verifica la carga de una solicitud JSON."""
    content = '{"ACTION": "get", "ID": "TEST"}'

    with patch(
        "builtins.open",
        mock_open(read_data=content),
    ):
        result = singletonclient.load_request("input.json")

    assert result["ACTION"] == "get"
    assert result["ID"] == "TEST"


def test_singletonclient_success(monkeypatch):
    """Verifica una comunicación correcta del SingletonClient."""
    args = SimpleNamespace(
        input="input.json",
        output="output.json",
        verbose=False,
    )

    monkeypatch.setattr(
        singletonclient,
        "parse_arguments",
        lambda: args,
    )

    monkeypatch.setattr(
        singletonclient,
        "load_request",
        lambda filename: {
            "ACTION": "get",
            "ID": "TEST",
        },
    )

    client_socket = MagicMock()
    client_socket.recv.side_effect = [
        json.dumps({"id": "TEST"}).encode("utf-8"),
        b"",
    ]
    monkeypatch.setattr(
        singletonclient.socket,
        "socket",
        lambda *args, **kwargs: client_socket,
    )

    with patch("builtins.open", mock_open()) as output_file:
        singletonclient.main()

    client_socket.connect.assert_called_once()
    client_socket.sendall.assert_called_once()
    client_socket.close.assert_called_once()
    output_file.assert_called_once()


def test_singletonclient_connection_error(monkeypatch):
    """Verifica el manejo de servidor no disponible."""
    args = SimpleNamespace(
        input="input.json",
        output=None,
        verbose=False,
    )

    monkeypatch.setattr(
        singletonclient,
        "parse_arguments",
        lambda: args,
    )

    monkeypatch.setattr(
        singletonclient,
        "load_request",
        lambda filename: {
            "ACTION": "get",
            "ID": "TEST",
        },
    )

    client_socket = MagicMock()
    client_socket.connect.side_effect = OSError("Servidor no disponible")

    monkeypatch.setattr(
        singletonclient.socket,
        "socket",
        lambda *args, **kwargs: client_socket,
    )

    singletonclient.main()

    client_socket.connect.assert_called_once()


def test_singletonclient_file_not_found(monkeypatch):
    """Verifica el manejo de archivo inexistente."""
    args = SimpleNamespace(
        input="inexistente.json",
        output=None,
        verbose=False,
    )

    monkeypatch.setattr(
        singletonclient,
        "parse_arguments",
        lambda: args,
    )

    monkeypatch.setattr(
        singletonclient,
        "load_request",
        MagicMock(side_effect=FileNotFoundError),
    )

    singletonclient.main()


def test_singletonclient_invalid_json(monkeypatch):
    """Verifica el manejo de un JSON inválido."""
    args = SimpleNamespace(
        input="input.json",
        output=None,
        verbose=False,
    )

    monkeypatch.setattr(
        singletonclient,
        "parse_arguments",
        lambda: args,
    )

    monkeypatch.setattr(
        singletonclient,
        "load_request",
        MagicMock(side_effect=json.JSONDecodeError("", "", 0)),
    )

    singletonclient.main()


def test_observer_parse_arguments(monkeypatch):
    """Verifica los argumentos del ObserverClient."""
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "observerclient.py",
            "-s",
            "localhost",
            "-p",
            "8080",
            "-o",
            "output.json",
            "-v",
        ],
    )

    args = observerclient.parse_arguments()

    assert args.server == "localhost"
    assert args.port == 8080
    assert args.output == "output.json"
    assert args.verbose is True


def test_observer_malformed_arguments(monkeypatch):
    """Verifica el rechazo de argumentos incorrectos."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["observerclient.py", "--incorrecto"],
    )

    with pytest.raises(SystemExit):
        observerclient.parse_arguments()


def test_observer_configure_logging():
    """Verifica la configuración de logging."""
    with patch("observerclient.logging.basicConfig") as logging_mock:
        observerclient.configure_logging(True)
        logging_mock.assert_called_once()


def test_observer_save_response():
    """Verifica que ObserverClient guarde una respuesta."""
    response = {"id": "TEST"}

    mocked_file = mock_open()

    with patch("builtins.open", mocked_file):
        observerclient.save_response(
            "output.json",
            response,
        )

    mocked_file.assert_called_once_with(
        "output.json",
        "w",
        encoding="utf-8",
    )


def test_observer_save_response_without_file():
    """Verifica salida sin archivo opcional."""
    with patch("builtins.open") as mocked_file:
        observerclient.save_response(
            None,
            {"id": "TEST"},
        )

    mocked_file.assert_not_called()


def test_observer_receives_notification(monkeypatch):
    """Verifica recepción de una notificación."""
    args = SimpleNamespace(
        server="localhost",
        port=8080,
        output=None,
        verbose=False,
    )

    monkeypatch.setattr(
        observerclient,
        "parse_arguments",
        lambda: args,
    )

    client_socket = MagicMock()

    client_socket.recv.side_effect = [
        json.dumps({"id": "TEST"}).encode("utf-8"),
        KeyboardInterrupt(),
    ]

    monkeypatch.setattr(
        observerclient.socket,
        "socket",
        lambda *args, **kwargs: client_socket,
    )

    observerclient.main()

    client_socket.connect.assert_called_once()
    client_socket.sendall.assert_called_once()
    client_socket.close.assert_called_once()


def test_observer_connection_error(monkeypatch):
    """Verifica el manejo de pérdida de conexión."""
    args = SimpleNamespace(
        server="localhost",
        port=8080,
        retry=30,
        output=None,
        verbose=False,
    )

    monkeypatch.setattr(
        observerclient,
        "parse_arguments",
        lambda: args,
    )

    client_socket = MagicMock()
    client_socket.connect.side_effect = OSError("Servidor no disponible")

    monkeypatch.setattr(
        observerclient.socket,
        "socket",
        lambda *args, **kwargs: client_socket,
    )

    monkeypatch.setattr(
        observerclient.time,
        "sleep",
        MagicMock(side_effect=KeyboardInterrupt),
    )

    with pytest.raises(KeyboardInterrupt):
        observerclient.main()
