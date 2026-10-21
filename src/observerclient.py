"""Cliente Observer para recibir cambios de CorporateData."""

import argparse
import json
import logging
import socket
import time
import uuid

logger = logging.getLogger(__name__)

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8080
RETRY_SECONDS = 30


def parse_arguments():
    """Procesa los argumentos recibidos por línea de comandos."""
    parser = argparse.ArgumentParser(description="Cliente Observer")

    parser.add_argument(
        "-s",
        "--server",
        default=DEFAULT_HOST,
        help="Nombre o dirección del servidor",
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Puerto TCP del servidor",
    )

    parser.add_argument(
        "-r",
        "--retry",
        type=int,
        default=RETRY_SECONDS,
        help="Segundos de espera antes de reconectar",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Archivo JSON de salida",
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


def save_response(filename, response):
    """Guarda una notificación recibida en un archivo JSON."""
    if filename:
        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                response,
                file,
                indent=4,
                ensure_ascii=False,
            )


def main():
    """Se suscribe al servidor y espera modificaciones."""
    args = parse_arguments()
    configure_logging(args.verbose)

    cpu_uuid = str(uuid.getnode())

    while True:
        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        try:
            client_socket.connect((args.server, args.port))

            request = {
                "UUID": cpu_uuid,
                "ACTION": "subscribe",
            }

            message = json.dumps(request).encode("utf-8")
            client_socket.sendall(message)

            logger.info("Cliente suscripto. Esperando modificaciones...")

            while True:
                response_data = client_socket.recv(4096)

                if not response_data:
                    raise ConnectionError("Se perdió la conexión con el servidor.")

                response = json.loads(response_data.decode("utf-8"))

                print(
                    json.dumps(
                        response,
                        indent=4,
                        ensure_ascii=False,
                    )
                )

                save_response(
                    args.output,
                    response,
                )

        except KeyboardInterrupt:
            logger.info("Cliente Observer detenido manualmente.")
            client_socket.close()
            break

        except (
            OSError,
            ConnectionError,
            json.JSONDecodeError,
        ) as error:
            logger.error(
                "Error de conexión: %s",
                error,
            )

            client_socket.close()

            logger.info(
                "Reintentando conexión en %s segundos...",
                args.retry,
            )

            time.sleep(args.retry)


if __name__ == "__main__":
    main()
