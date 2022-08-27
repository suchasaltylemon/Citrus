from typing import List

from ..instances.player import Player
from ...internal.networking.endpoints.server.auth import LoggedIn
from ...internal.runtime_manager import RuntimeManager
from ...internal.singleton import singleton


class _PlayerSystem:
    pass


if RuntimeManager.is_server():
    @singleton
    class PlayerSystem(_PlayerSystem):
        def __init__(self):
            self._players: List[Player] = []

            @LoggedIn
            def handle_login(player: Player):
                self._players.append(player)

        def get_players(self) -> List[Player]:
            return self._players

else:
    @singleton
    class PlayerSystem(_PlayerSystem):
        _local_player: Player = None

        @property
        def local_player(self):
            return self._local_player
