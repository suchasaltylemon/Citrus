import base64

from citrus import RuntimeManager, NetworkManager
from citrus.core.instances.player import Player
from citrus.internal.components.networkable import Networkable
from citrus.internal.runtime_manager import SERVER_CONTEXT
from include.signal import Signal
from include.signal.net.event import Event

ENDPOINT_PREFIX = "__endpoint/"


class _Endpoint:
    def __init__(self, endpoint_name: str):
        self.name = endpoint_name
        self._path = ENDPOINT_PREFIX + self.name

        self.Signalled = Event()

        @NetworkManager.Signalled(self._path)
        def handle_signal(conn, signal):
            if NetworkManager.context == SERVER_CONTEXT:
                # Get player object then fire

                pass

            else:
                self.Signalled.fire(signal.data)

    @staticmethod
    def _serialise(data: dict):
        return {k: base64.b64encode(v) for k, v in data.items()}

    @staticmethod
    def _deserialise(serialised: dict):
        return {k: base64.b64decode(v) for k, v in serialised.items()}


if RuntimeManager.context == SERVER_CONTEXT:
    class Endpoint(_Endpoint):
        def send_to_player(self, player: Player, data: dict):
            serialised = self._serialise(data)

            player_connection = player.get_component(Networkable).get_connection()

            NetworkManager.send(player_connection, Signal(self._path, serialised))

else:
    class Endpoint(_Endpoint):
        def send_to_server(self, data: dict):
            serialised = self._serialise(data)

            NetworkManager.send(NetworkManager.client_connection, Signal(self._path, serialised))
