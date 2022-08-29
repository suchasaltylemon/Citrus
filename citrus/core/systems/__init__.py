_loaded_systems = {}


def init_systems():
    from .player_system import PlayerService

    _loaded_systems["players"] = PlayerService()


def get_system(system_name: str):
    return _loaded_systems[system_name]
