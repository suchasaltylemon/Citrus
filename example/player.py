from example.shared.components.health_component import Health
from example.shared.components.transform_component import Transform
from lib.core.instance import instance, BaseInstance


@instance({
    "components": [
        Transform, Health
    ],
    "name": "Player"
})
class Player(BaseInstance):
    pass
