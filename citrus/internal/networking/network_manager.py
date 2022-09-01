from signalio import Event, ConditionalEvent
from signalio import SecureServer, SecureClient, SecureConnection
from signalio import Signal
from ..singleton import singleton
from ...core.errors import NetworkError
from ...log import logger

DEFAULT_PORT = 7092

network_logging = logger("net")


@singleton
class NetworkManager:
    NewConnection = Event()
    Signalled = ConditionalEvent(lambda _, signal: [signal.path], default="*")

    ip = "<ip>"
    port = DEFAULT_PORT

    server = None
    client = None
    client_connection = None

    running = False

    def update_info(self, ip, port=None):
        self.ip = ip
        self.port = port or DEFAULT_PORT

        network_logging.warn(f"No port provided. Using default port {DEFAULT_PORT} instead")
        network_logging.info(f"Updated server info. Will now listen at {self.ip}:{self.port}")

    def start(self):
        from ..context_manager import ContextManager
        context_manager = ContextManager()

        network_logging.info("Starting network manager")

        if context_manager.is_server():
            network_logging.info("Configuring server...")
            self.server = SecureServer(self.ip, self.port)
            network_logging.info("Configure server")

            network_logging.info("Starting server...")
            self.server.start()
            network_logging.info("Started server")

            @self.server.Connected()
            def handle_connection(connection: SecureConnection):
                network_logging.info(f"Received connection from {connection.ip}:{connection.port}")

                @connection.Signalled()
                def handle_all(signal):
                    self.Signalled.fire(connection, signal)

                @connection.Disconnected()
                def handle_server_disconnect():
                    network_logging.info(
                        f"Client has disconnected from server. Client was connected from {connection.ip}:{connection.port}")

                if not connection.secure:
                    connection.Secured.wait()

                self.NewConnection.fire(connection)

        elif context_manager.is_client():
            network_logging.info("Configuring client...")
            self.client = SecureClient(self.ip, self.port)
            network_logging.info("Configured client")

            @self.client.Connected()
            def handle_connection(conn: SecureConnection):
                network_logging.info(f"Client has connected to server. Client socket running at {conn.ip}:{conn.port}")
                self.client_connection = conn

                @conn.Signalled()
                def handle_signal(signal):
                    self.Signalled.fire(self.client_connection, signal)

            @self.client.Disconnected()
            def handle_client_disconnect():
                network_logging.info("Client has disconnected from server")

            try:
                network_logging.info(f"Connecting client to server {self.ip}:{self.port}")
                self.client.connect()

            except ConnectionRefusedError as e:
                network_logging.error("Client connection was refused! Maybe the server is not running", exc_info=e)

        else:
            e = NetworkError(f"Could not determine networking context. Context is {ContextManager.context}")

            network_logging.error("Could not determine networking context", exc_info=e)

            raise e

        self.running = True

    def send(self, conn: SecureConnection, data: Signal):
        conn.send(data)
