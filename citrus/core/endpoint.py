import base64

from citrus import RuntimeManager, NetworkManager
from citrus.core.instances.player import Player
from citrus.internal.components.networkable import Networkable
from citrus.internal.runtime_manager import SERVER_CONTEXT
from citrus.signal import Signal
from citrus.signal.net.event import Event

ENDPOINT_PREFIX = "__endpoint/"


class _Endpoint:
    def __init__(self, endpoint_name: str):
        self.name = endpoint_name

        self.Signalled = Event()

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

            NetworkManager.send(player_connection, Signal(ENDPOINT_PREFIX + self.name, serialised))

else:
    class Endpoint(_Endpoint):
        def send_to_server(self, data: dict):
            serialised = self._serialise(data)

            NetworkManager.send(NetworkManager.client_connection, Signal(ENDPOINT_PREFIX + self.name, serialised))
