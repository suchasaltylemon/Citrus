from example.player import Player
from example.shared.components.health_component import Health
from example.shared.components.transform_component import Transform
from lib import export
from lib.core.service import service
from lib.lifecycle import onstart


@onstart()
@service()
class PlayerService:
    def on_start(self):
        player_instance = Player()
        transform = player_instance.get_component(Transform)

        print(transform.X)

        transform.X = 3

        print(transform.X)

        health = player_instance.get_component(Health)
        print(health.health)

        health.kill()
        print(health.health)


export(PlayerService)
