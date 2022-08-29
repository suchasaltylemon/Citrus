from citrus import export
from citrus.core.instances.player import Player
from citrus.core.service import service
from citrus.core.systems.player_system import PlayerService
from citrus.lifecycle import onstart


@service()
@onstart()
class PlayerGreetingService:
    def on_start(self):
        print("Greet service started")

        @PlayerService.PlayerAdded()
        def greet_player(player: Player):
            print(f"{player.display_name} has joined")


export(PlayerGreetingService)
