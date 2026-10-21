"""Proxy para gestionar operaciones sobre CorporateData."""

from corporate_data import CorporateDataSingleton
from corporate_log import CorporateLogSingleton


class CorporateDataProxy:
    """Intermedia el acceso a CorporateData y registra las operaciones."""

    def __init__(self):
        """Inicializa los accesos a datos y auditoría."""
        self.data = CorporateDataSingleton()
        self.log = CorporateLogSingleton()

    def get(self, cpu_uuid, session_id, record_id):
        """Recupera un registro y audita la operación."""
        self.log.log_action(cpu_uuid, session_id, "get", record_id)
        return self.data.get(record_id)

    def list_all(self, cpu_uuid, session_id):
        """Lista todos los registros y audita la operación."""
        self.log.log_action(cpu_uuid, session_id, "list")
        return self.data.list_all()

    def set(self, cpu_uuid, session_id, record_id, data):
        """Modifica un registro y audita la operación."""
        result = self.data.set(record_id, data)
        self.log.log_action(cpu_uuid, session_id, "set")
        return result
