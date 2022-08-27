from ..core.systems import init_systems


class SystemManager:
    @classmethod
    def start(cls):
        init_systems()
