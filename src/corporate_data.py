"""Acceso Singleton a la tabla CorporateData de AWS DynamoDB."""

from typing import Any, ClassVar

import boto3
from mypy_boto3_dynamodb.service_resource import (
    DynamoDBServiceResource,
    Table,
)


class CorporateDataSingleton:
    """Gestiona una única instancia de acceso a CorporateData."""

    _instance: ClassVar["CorporateDataSingleton | None"] = None

    dynamodb: DynamoDBServiceResource
    table: Table

    def __new__(cls):
        """Crea una única instancia de la clase."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.dynamodb = boto3.resource("dynamodb")
            cls._instance.table = cls._instance.dynamodb.Table("CorporateData")

        return cls._instance

    def get_table(self):
        """Devuelve la tabla CorporateData."""
        return self.table

    def get(self, record_id):
        """Recupera un registro de CorporateData por su ID."""
        response = self.table.get_item(
            Key={
                "id": record_id,
            }
        )

        return response.get("Item")

    def list_all(self):
        """Recupera todos los registros de CorporateData."""
        response = self.table.scan()
        items = response.get("Items", [])

        while "LastEvaluatedKey" in response:
            response = self.table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))

        return items

    def set(self, record_id, data):
        """Crea o actualiza un registro de CorporateData."""
        existing_item = self.get(record_id)

        if existing_item is None:
            item: dict[str, Any] = {
                "id": record_id,
                "cp": "",
                "CUIT": "",
                "domicilio": "",
                "idReq": "",
                "idSeq": "",
                "localidad": "",
                "provincia": "",
                "sede": "",
                "seqID": "",
                "telefono": "",
                "web": "",
            }

            item.update(data)
            item["id"] = record_id

            self.table.put_item(Item=item)
            return item

        updated_item = existing_item.copy()

        for key, value in data.items():
            if key != "id":
                updated_item[key] = value

        self.table.put_item(Item=updated_item)

        return updated_item
