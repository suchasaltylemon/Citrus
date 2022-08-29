from citrus import export
from citrus.core.instances.player import Player
from citrus.core.service import service
from citrus.core.systems.player_system import PlayerSystem
from citrus.lifecycle import onstart


@service()
@onstart()
class RequiredService:
    def on_start(self):
        @PlayerSystem.PlayerAdded()
        def greet_player(player: Player):
            print(f"{player.display_name} has joined")


export(RequiredService)
