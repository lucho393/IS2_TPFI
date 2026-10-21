"""Pruebas de los patrones Singleton."""

from src.corporate_data import CorporateDataSingleton
from src.corporate_log import CorporateLogSingleton


def test_corporate_data_singleton():
    """Verifica el Singleton de CorporateData."""
    instancia1 = CorporateDataSingleton()
    instancia2 = CorporateDataSingleton()
    assert instancia1 is instancia2


def test_corporate_log_singleton():
    """Verifica el Singleton de CorporateLog."""
    instancia1 = CorporateLogSingleton()
    instancia2 = CorporateLogSingleton()
    assert instancia1 is instancia2
