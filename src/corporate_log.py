"""Acceso Singleton a la tabla CorporateLog de AWS DynamoDB."""

import uuid
from datetime import datetime
from typing import ClassVar

import boto3
from mypy_boto3_dynamodb.service_resource import (
    DynamoDBServiceResource,
    Table,
)


class CorporateLogSingleton:
    """Gestiona una única instancia de acceso a CorporateLog."""

    _instance: ClassVar["CorporateLogSingleton | None"] = None

    dynamodb: DynamoDBServiceResource
    table: Table

    def __new__(cls):
        """Crea una única instancia de la clase."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.dynamodb = boto3.resource("dynamodb")
            cls._instance.table = cls._instance.dynamodb.Table("CorporateLog")

        return cls._instance

    def get_table(self):
        """Devuelve la tabla CorporateLog."""
        return self.table

    def log_action(
        self,
        cpu_uuid,
        session_id,
        action,
        record_id=None,
    ):
        """Registra una acción realizada sobre el sistema."""
        item = {
            "id": str(uuid.uuid4()),
            "UUID": str(cpu_uuid),
            "session": str(session_id),
            "action": action,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        if record_id is not None:
            item["record_id"] = record_id

        self.table.put_item(Item=item)

        return item
