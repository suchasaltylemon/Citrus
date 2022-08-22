from signalio import Event, ConditionalEvent
from signalio import SecureServer, SecureClient, SecureConnection
from signalio import Signal

from ..runtime_manager import RuntimeManager, SERVER_CONTEXT

DEFAULT_PORT = 7092


class NetworkManager:
    NewConnection = Event()
    Signalled = ConditionalEvent(lambda _, signal: [signal.path], default="*")

    ip = "<ip>"
    port = DEFAULT_PORT

    server = None
    client = None
    client_connection = None

    running = False
    context = None

    @classmethod
    def update_info(cls, ip, port=None):
        cls.ip = ip
        cls.port = port or DEFAULT_PORT

    @classmethod
    def start(cls):
        cls.context = RuntimeManager.context

        if cls.context == SERVER_CONTEXT:
            cls.server = SecureServer(cls.ip, cls.port)
            cls.server.start()

            @cls.server.Connected()
            def handle_connection(connection: SecureConnection):
                if not connection.secure:
                    connection.Secured.wait()

                cls.NewConnection.fire(connection)

                @connection.Signalled()
                def handle_all(signal):
                    cls.Signalled.fire(connection, signal)

        else:
            cls.client = SecureClient(cls.ip, cls.port)

            @cls.client.Connected()
            def handle_connection(conn):
                cls.client_connection = conn

                @conn.Signalled()
                def handle_signal(signal):
                    cls.Signalled.fire(cls.client_connection, signal)

            cls.client.connect()

        cls.running = True

    @classmethod
    def send(cls, conn: SecureConnection, data: Signal):
        conn.send(data)
