from signalio import Event, ConditionalEvent
from signalio import SecureServer, SecureClient, SecureConnection
from signalio import Signal
from ...core.errors import NetworkError
from ...log import logger

DEFAULT_PORT = 7092

network_logging = logger("net")


class NetworkManager:
    NewConnection = Event()
    Signalled = ConditionalEvent(lambda _, signal: [signal.path], default="*")

    ip = "<ip>"
    port = DEFAULT_PORT

    server = None
    client = None
    client_connection = None

    running = False

    @classmethod
    def update_info(cls, ip, port=None):
        cls.ip = ip
        cls.port = port or DEFAULT_PORT

        network_logging.warn(f"No port provided. Using default port {DEFAULT_PORT} instead")
        network_logging.info(f"Updated server info. Will now listen at {cls.ip}:{cls.port}")

    @classmethod
    def start(cls):
        from ..context_manager import ContextManager
        network_logging.info("Starting network manager")

        if ContextManager.is_server():
            network_logging.info("Configuring server...")
            cls.server = SecureServer(cls.ip, cls.port)
            network_logging.info("Configure server")

            network_logging.info("Starting server...")
            cls.server.start()
            network_logging.info("Started server")

            @cls.server.Connected()
            def handle_connection(connection: SecureConnection):
                network_logging.info(f"Received connection from {connection.ip}:{connection.port}")

                @connection.Signalled()
                def handle_all(signal):
                    cls.Signalled.fire(connection, signal)

                @connection.Disconnected()
                def handle_server_disconnect():
                    network_logging.info(
                        f"Client has disconnected from server. Client was connected from {connection.ip}:{connection.port}")

                if not connection.secure:
                    connection.Secured.wait()

                cls.NewConnection.fire(connection)

        elif ContextManager.is_client():
            network_logging.info("Configuring client...")
            cls.client = SecureClient(cls.ip, cls.port)
            network_logging.info("Configured client")

            @cls.client.Connected()
            def handle_connection(conn: SecureConnection):
                network_logging.info(f"Client has connected to server. Client socket running at {conn.ip}:{conn.port}")
                cls.client_connection = conn

                @conn.Signalled()
                def handle_signal(signal):
                    cls.Signalled.fire(cls.client_connection, signal)

            @cls.client.Disconnected()
            def handle_client_disconnect():
                network_logging.info("Client has disconnected from server")

            try:
                network_logging.info(f"Connecting client to server {cls.ip}:{cls.port}")
                cls.client.connect()

            except ConnectionRefusedError as e:
                network_logging.error("Client connection was refused! Maybe the server is not running", exc_info=e)

        else:
            e = NetworkError(f"Could not determine networking context. Context is {ContextManager.context}")

            network_logging.error("Could not determine networking context", exc_info=e)

            raise e

        cls.running = True

    @classmethod
    def send(cls, conn: SecureConnection, data: Signal):
        conn.send(data)
