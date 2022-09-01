from typing import List

from signalio import Event
from ..instances.player import Player
from ...internal.context_manager import ContextManager
from ...internal.networking.endpoints.server.auth import LoggedIn
from ...internal.singleton import singleton
from ...log import logger

core_system_logger = logger("core_system")

context_manager = ContextManager()


class _PlayerService:
    pass


if context_manager.is_server():
    @singleton
    class PlayerService(_PlayerService):
        PlayerAdded = Event[Player]()

        def __init__(self):
            self._players: List[Player] = []

            @LoggedIn
            def handle_login(player: Player):
                self._players.append(player)
                self.PlayerAdded.fire(player)

                core_system_logger.info("Player has been registered to PlayerService")

        def get_players(self) -> List[Player]:
            return self._players

else:
    @singleton
    class PlayerService(_PlayerService):
        _local_player: Player = None

        @property
        def local_player(self):
            return self._local_player
