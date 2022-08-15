from citrus import export
from citrus.core.service import service
from citrus.lifecycle import onstart
from example.player import Player
from example.shared.components.health_component import Health
from example.shared.components.transform_component import Transform


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
