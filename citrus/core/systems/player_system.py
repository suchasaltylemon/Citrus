from typing import List

from signalio import Event
from ..instances.player import Player
from ...internal.lifecycle_manager import LifecycleManager
from ...internal.networking.endpoints.server.auth import LoggedIn
from ...internal.singleton import singleton


class _PlayerSystem:
    pass


if LifecycleManager.is_server():
    @singleton
    class PlayerSystem(_PlayerSystem):
        PlayerAdded = Event[Player]()

        def __init__(self):
            self._players: List[Player] = []

            @LoggedIn
            def handle_login(player: Player):
                self._players.append(player)
                self.PlayerAdded.fire(player)

        def get_players(self) -> List[Player]:
            return self._players

else:
    @singleton
    class PlayerSystem(_PlayerSystem):
        _local_player: Player = None

        @property
        def local_player(self):
            return self._local_player
