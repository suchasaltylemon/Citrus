from citrus import RuntimeManager
from citrus.internal.auth_manager import AuthManager
from citrus.internal.runtime_manager import SERVER_CONTEXT
from include.signal import Server, Client
from include.signal.net import Connection
from include.signal.net.event import Event, ConditionalEvent

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
            cls.server = Server(cls.ip, cls.port)
            cls.server.start()

            @cls.server.Connected()
            def handle_connection(connection):
                cls.NewConnection.fire(connection)

                AuthManager.handle_connection(connection)

                @connection.Signalled()
                def handle_all(signal):
                    cls.Signalled.fire(connection, signal)

        else:
            cls.client = Client(cls.ip, cls.port)

            cls.client_connection = cls.client.connect()

            @cls.client_connection.Signalled()
            def handle_signal(signal):
                cls.Signalled.fire(cls.client_connection, signal)

        cls.running = True

    @classmethod
    def send(cls, conn: Connection, data):
        conn.send(data)
