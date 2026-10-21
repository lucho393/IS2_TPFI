"""Pruebas de acceso a CorporateData."""

from unittest.mock import MagicMock

from corporate_data import CorporateDataSingleton


def create_data_instance():
    """Crea una instancia con tabla simulada."""
    instance = CorporateDataSingleton()
    instance.table = MagicMock()
    return instance


def test_get_existing_record():
    """Verifica la recuperación de un registro."""
    data = create_data_instance()

    data.table.get_item.return_value = {"Item": {"id": "TEST"}}

    result = data.get("TEST")

    assert result == {"id": "TEST"}


def test_list_all():
    """Verifica el listado de registros."""
    data = create_data_instance()

    data.table.scan.return_value = {
        "Items": [
            {"id": "TEST-1"},
            {"id": "TEST-2"},
        ]
    }

    result = data.list_all()

    assert len(result) == 2


def test_set_existing_record():
    """Verifica la modificación parcial de un registro."""
    data = create_data_instance()

    data.table.get_item.return_value = {
        "Item": {
            "id": "TEST",
            "localidad": "Anterior",
            "sede": "FCyT",
        }
    }

    result = data.set(
        "TEST",
        {"localidad": "Concepcion del Uruguay"},
    )

    assert result["localidad"] == "Concepcion del Uruguay"
    assert result["sede"] == "FCyT"

    data.table.put_item.assert_called_once()


def test_set_new_record():
    """Verifica la creación de un registro inexistente."""
    data = create_data_instance()

    data.table.get_item.return_value = {}

    result = data.set(
        "NUEVO",
        {"localidad": "Concepcion del Uruguay"},
    )

    assert result["id"] == "NUEVO"
    assert result["localidad"] == "Concepcion del Uruguay"
    assert result["telefono"] == ""

    data.table.put_item.assert_called_once()


def test_list_all_with_pagination():
    """Verifica que list_all recupere todas las páginas."""
    corporate_data = CorporateDataSingleton()

    corporate_data.table = MagicMock()

    corporate_data.table.scan.side_effect = [
        {
            "Items": [{"id": "1"}],
            "LastEvaluatedKey": {"id": "1"},
        },
        {
            "Items": [{"id": "2"}],
        },
    ]

    result = corporate_data.list_all()

    assert result == [
        {"id": "1"},
        {"id": "2"},
    ]

    assert corporate_data.table.scan.call_count == 2
