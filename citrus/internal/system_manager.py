from .singleton import singleton
from ..core.systems import init_systems


@singleton
class SystemManager:
    def start(self):
        init_systems()
