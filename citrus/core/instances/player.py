from ..component import component
from ..instance import instance, BaseInstance
from ...internal.components.networkable import Networkable
from ...internal.runtime_manager import RuntimeManager


@component()
class ClientComponent:
    pass


@instance({
    "name": "Player",
    "components": [Networkable]
})
class _Player(BaseInstance):
    username: str = None
    display_name: str = None
    account_id: str = None


if RuntimeManager.is_server():
    @instance({
        "name": "Player"
    })
    class Player(_Player):
        pass

else:
    @instance({
        "name": "Player"
    })
    class Player(_Player):
        pass
