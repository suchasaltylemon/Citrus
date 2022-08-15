from citrus.core.instance import instance, BaseInstance
from example.shared.components.health_component import Health
from example.shared.components.transform_component import Transform


@instance({
    "components": [
        Transform, Health
    ],
    "name": "Player"
})
class Player(BaseInstance):
    pass
