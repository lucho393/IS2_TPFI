"""Servidor principal Singleton Proxy Observer del TPFI."""

import argparse
import json
import logging
import socket
import uuid

from corporate_observer import CorporateDataObserver
from corporate_proxy import CorporateDataProxy

logger = logging.getLogger(__name__)

DEFAULT_PORT = 8080


def parse_arguments():
    """Procesa los argumentos recibidos por línea de comandos."""
    parser = argparse.ArgumentParser(description="Servidor Singleton Proxy Observer")

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Puerto TCP del servidor",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Activa mensajes de depuración",
    )

    return parser.parse_args()


def configure_logging(verbose):
    """Configura los mensajes de ejecución."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def receive_request(client_socket):
    """Recibe y convierte una solicitud JSON enviada por un cliente."""
    data = client_socket.recv(4096)

    if not data:
        return None

    try:
        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def main():
    """Inicia el servidor TCP."""
    args = parse_arguments()
    configure_logging(args.verbose)

    session_id = str(uuid.uuid4())

    proxy = CorporateDataProxy()
    observer = CorporateDataObserver()

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    try:
        server_socket.bind(("", args.port))
        server_socket.listen()

        # Permite responder a Ctrl+C en Windows.
        server_socket.settimeout(1.0)

        logger.info(
            "Servidor iniciado en puerto %s - Session ID: %s",
            args.port,
            session_id,
        )

        while True:
            try:
                client_socket, client_address = server_socket.accept()
            except TimeoutError:
                continue

            logger.debug(
                "Cliente conectado desde %s",
                client_address,
            )

            request = receive_request(client_socket)

            if request is None:
                logger.error("Solicitud JSON inválida.")
                client_socket.close()
                continue

            logger.debug(
                "Solicitud recibida: %s",
                request,
            )

            action = request.get("ACTION")

            if action not in (
                "get",
                "set",
                "list",
                "subscribe",
            ):
                logger.error(
                    "Acción inválida: %s",
                    action,
                )
                client_socket.close()
                continue

            logger.debug(
                "Acción solicitada: %s",
                action,
            )

            if action == "get":
                cpu_uuid = request.get("UUID")
                record_id = request.get("ID")

                if cpu_uuid is None or record_id is None:
                    response = {"Error": ("Faltan datos requeridos para la acción get")}
                else:
                    result = proxy.get(
                        cpu_uuid,
                        session_id,
                        record_id,
                    )

                    if result is None:
                        response = {"Error": ("Registro no encontrado")}
                    else:
                        response = result

                message = json.dumps(
                    response,
                    default=str,
                ).encode("utf-8")

                client_socket.sendall(message)

            if action == "subscribe":
                cpu_uuid = request.get("UUID")

                if cpu_uuid is None:
                    response = {
                        "Error": ("Faltan datos requeridos para la acción subscribe")
                    }

                    message = json.dumps(
                        response,
                        default=str,
                    ).encode("utf-8")

                    client_socket.sendall(message)
                    client_socket.close()
                    continue

                proxy.log.log_action(
                    cpu_uuid,
                    session_id,
                    "subscribe",
                )

                observer.subscribe(
                    cpu_uuid,
                    client_socket,
                )

                logger.info(
                    "Cliente %s suscripto correctamente.",
                    cpu_uuid,
                )

                continue

            if action == "list":
                cpu_uuid = request.get("UUID")

                if cpu_uuid is None:
                    response = {
                        "Error": ("Faltan datos requeridos para la acción list")
                    }
                else:
                    response = proxy.list_all(
                        cpu_uuid,
                        session_id,
                    )

                message = json.dumps(
                    response,
                    default=str,
                ).encode("utf-8")

                client_socket.sendall(message)

            if action == "set":
                cpu_uuid = request.get("UUID")
                record_id = request.get("ID")

                if cpu_uuid is None or record_id is None:
                    response = {"Error": ("Faltan datos requeridos para la acción set")}
                else:
                    data = request.copy()

                    data.pop(
                        "UUID",
                        None,
                    )
                    data.pop(
                        "ACTION",
                        None,
                    )
                    data.pop(
                        "ID",
                        None,
                    )

                    response = proxy.set(
                        cpu_uuid,
                        session_id,
                        record_id,
                        data,
                    )

                    notification = json.dumps(
                        response,
                        default=str,
                    ).encode("utf-8")

                    observer.notify(notification)

                message = json.dumps(
                    response,
                    default=str,
                ).encode("utf-8")

                client_socket.sendall(message)

            client_socket.close()

    except OSError as error:
        logger.error(
            "No se pudo iniciar el servidor: %s",
            error,
        )

    except KeyboardInterrupt:
        logger.info("Servidor detenido manualmente.")

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
