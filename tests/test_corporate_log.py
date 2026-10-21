"""Pruebas de auditoría en CorporateLog."""

from unittest.mock import MagicMock

from corporate_log import CorporateLogSingleton


def test_log_action():
    """Verifica la creación de un registro de auditoría."""
    log = CorporateLogSingleton()
    log.table = MagicMock()

    result = log.log_action(
        "CPU-TEST",
        "SESSION-TEST",
        "get",
        "TEST",
    )

    assert result["UUID"] == "CPU-TEST"
    assert result["session"] == "SESSION-TEST"
    assert result["action"] == "get"
    assert result["record_id"] == "TEST"

    log.table.put_item.assert_called_once()
