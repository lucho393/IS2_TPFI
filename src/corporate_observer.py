"""Implementación del patrón Observer para CorporateData."""


class CorporateDataObserver:
    """Gestiona los clientes suscriptos a cambios en CorporateData."""

    def __init__(self):
        """Inicializa la lista de suscriptores."""
        self.subscribers = []

    def subscribe(self, client_uuid, client_socket):
        """Registra un nuevo cliente suscripto."""
        self.subscribers.append(
            {
                "UUID": client_uuid,
                "socket": client_socket,
            }
        )

    def unsubscribe(self, client_socket):
        """Elimina un cliente de la lista de suscriptores."""
        self.subscribers = [
            subscriber
            for subscriber in self.subscribers
            if subscriber["socket"] is not client_socket
        ]

    def notify(self, message):
        """Envía una modificación a todos los clientes suscriptos."""
        disconnected = []

        for subscriber in self.subscribers:
            client_socket = subscriber["socket"]

            try:
                client_socket.sendall(message)
            except OSError:
                disconnected.append(client_socket)

        for client_socket in disconnected:
            self.unsubscribe(client_socket)
