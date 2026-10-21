"""Cliente para realizar solicitudes al servidor Singleton Proxy Observer."""

import argparse
import json
import logging
import socket
import uuid

logger = logging.getLogger(__name__)

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8080


def parse_arguments():
    """Procesa los argumentos recibidos por línea de comandos."""
    parser = argparse.ArgumentParser(description="Cliente Singleton")

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Archivo JSON de entrada",
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


def load_request(filename):
    """Carga la solicitud desde un archivo JSON."""
    with open(
        filename,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def main():
    """Ejecuta el cliente Singleton."""
    args = parse_arguments()
    configure_logging(args.verbose)

    try:
        request = load_request(args.input)

        request["UUID"] = str(uuid.getnode())

        logger.debug(
            "Solicitud cargada: %s",
            request,
        )

        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

        client_socket.connect((DEFAULT_HOST, DEFAULT_PORT))

        message = json.dumps(request).encode("utf-8")
        client_socket.sendall(message)

        logger.debug("Solicitud enviada al servidor.")

        response_chunks = []

        while True:
            chunk = client_socket.recv(4096)

            if not chunk:
                break

            response_chunks.append(chunk)

        response_data = b"".join(response_chunks)

        if response_data:
            response = json.loads(response_data.decode("utf-8"))

            print(
                json.dumps(
                    response,
                    indent=4,
                    ensure_ascii=False,
                )
            )

            if args.output:
                with open(
                    args.output,
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(
                        response,
                        file,
                        indent=4,
                        ensure_ascii=False,
                    )

        client_socket.close()

    except FileNotFoundError:
        logger.error(
            "No se encontró el archivo de entrada: %s",
            args.input,
        )

    except json.JSONDecodeError:
        logger.error("El archivo de entrada no contiene un JSON válido.")

    except OSError as error:
        logger.error(
            "Error de conexión con el servidor: %s",
            error,
        )


if __name__ == "__main__":
    main()
