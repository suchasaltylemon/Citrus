from citrus import RuntimeManager
from citrus.internal.runtime_manager import SERVER_CONTEXT
from citrus.signal import Server, Client
from citrus.signal.net.connection import Connection

DEFAULT_PORT = 7092


class NetworkManager:
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
                @connection.Signalled()
                def _():
                    pass  # TODO: Handle player creation + networkable component addition

        else:
            cls.client = Client(cls.ip, cls.port)

            cls.client_connection = cls.client.connect()

        cls.running = True

    @classmethod
    def send(cls, conn: Connection, data):
        conn.send(data)
