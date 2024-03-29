from signalio import Event, Signal
from .instances.player import Player
from .systems import get_system
from ..internal.components.networkable import Networkable
from ..internal.context_manager import ContextManager
from ..internal.networking.network_manager import NetworkManager
from ..utils.encoding import bstring, sbytes

ENDPOINT_PREFIX = "__endpoint/"

context_manager = ContextManager()
network_manager = NetworkManager()


class _Endpoint:
    def __init__(self, endpoint_name: str):
        self.name = endpoint_name
        self._path = ENDPOINT_PREFIX + self.name

        self.Signalled = Event()

        @network_manager.Signalled(self._path)
        def handle_signal(conn, signal):
            if context_manager.is_server():
                players = get_system("players").get_players()

                player = next((p for p in players if p.get_component(Networkable).get_connection() == conn), None)
                if player is None:
                    return

                valid_session_token = player.get_component(Networkable).get_session_token()
                provided_session_token = signal.data.get("session_token", None)

                if provided_session_token is None or sbytes(provided_session_token) != valid_session_token:
                    return

                data = signal.data.get("data", None)
                if data is None:
                    return

                self.Signalled.fire(player, data)

            else:
                self.Signalled.fire(signal.data)


if context_manager.is_server():
    class Endpoint(_Endpoint):
        def send_to_player(self, player: Player, data: dict):
            player_connection = player.get_component(Networkable).get_connection()

            network_manager.send(player_connection, Signal(self._path, data))

else:
    class Endpoint(_Endpoint):
        def send_to_server(self, data: dict):
            networkable = get_system("players").local_player.get_component(Networkable)
            session_token = networkable.get_session_token()

            client_data = {
                "data": data,
                "session_token": bstring(session_token)
            }

            network_manager.send(network_manager.client_connection, Signal(self._path, client_data))
