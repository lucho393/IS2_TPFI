"""Pruebas del patrón Proxy."""

from unittest.mock import MagicMock

from corporate_proxy import CorporateDataProxy


def test_proxy_get():
    """Verifica que el Proxy gestione get y registre la operación."""
    proxy = CorporateDataProxy()

    proxy.data = MagicMock()
    proxy.log = MagicMock()
    proxy.data.get.return_value = {"id": "TEST"}

    result = proxy.get(
        "CPU-TEST",
        "SESSION-TEST",
        "TEST",
    )

    proxy.log.log_action.assert_called_once_with(
        "CPU-TEST",
        "SESSION-TEST",
        "get",
        "TEST",
    )
    proxy.data.get.assert_called_once_with("TEST")

    assert result == {"id": "TEST"}


def test_proxy_list():
    """Verifica que el Proxy gestione list y registre la operación."""
    proxy = CorporateDataProxy()

    proxy.data = MagicMock()
    proxy.log = MagicMock()
    proxy.data.list_all.return_value = [
        {"id": "TEST-1"},
        {"id": "TEST-2"},
    ]

    result = proxy.list_all(
        "CPU-TEST",
        "SESSION-TEST",
    )

    proxy.log.log_action.assert_called_once_with(
        "CPU-TEST",
        "SESSION-TEST",
        "list",
    )
    proxy.data.list_all.assert_called_once_with()

    assert len(result) == 2


def test_proxy_set():
    """Verifica que el Proxy gestione set y registre la operación."""
    proxy = CorporateDataProxy()

    proxy.data = MagicMock()
    proxy.log = MagicMock()

    data = {
        "localidad": "Concepcion del Uruguay",
    }

    proxy.data.set.return_value = {
        "id": "TEST",
        "localidad": "Concepcion del Uruguay",
    }

    result = proxy.set(
        "CPU-TEST",
        "SESSION-TEST",
        "TEST",
        data,
    )

    proxy.data.set.assert_called_once_with(
        "TEST",
        data,
    )

    proxy.log.log_action.assert_called_once_with(
        "CPU-TEST",
        "SESSION-TEST",
        "set",
    )

    assert result["id"] == "TEST"
