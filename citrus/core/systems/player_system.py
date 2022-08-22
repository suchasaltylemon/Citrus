from typing import List

from ..instances.player import Player
from ...internal.runtime_manager import RuntimeManager
from ...internal.singleton import singleton


@singleton
class _PlayerSystem:
    pass


if RuntimeManager.is_server():
    class PlayerSystem(_PlayerSystem):
        def get_players(self) -> List[Player]:
            return []

else:
    class PlayerSystem(_PlayerSystem):
        _player: Player = None

        @property
        def local_player(self):
            return self._player
