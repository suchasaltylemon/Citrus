from .....core.endpoint import Endpoint

LOADER = object()

ClientGetPlayerInfo = Endpoint("GetPlayerInfo")


def get_player_info() -> dict:
    ClientGetPlayerInfo.send_to_server({})
    return ClientGetPlayerInfo.Signalled.wait()
