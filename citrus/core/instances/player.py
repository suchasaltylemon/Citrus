from citrus import RuntimeManager
from core.instance import instance, BaseInstance
from internal.components.networkable import Networkable
from internal.runtime_manager import SERVER_CONTEXT


@instance({
    "name": "Player",
    "components": []
})
class _ReplicatedPlayer(BaseInstance):
    pass


if RuntimeManager.context == SERVER_CONTEXT:
    @instance({
        "name": "Player",
        "components": [
            Networkable
        ]
    })
    class Player(_ReplicatedPlayer):
        pass

else:
    class Player(_ReplicatedPlayer):
        pass
