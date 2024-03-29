from ....db_managers import DBManager
from .....core.endpoint import Endpoint
from .....core.instances.player import Player

db_manager = DBManager()

ServerGetPlayerInfo = Endpoint("GetPlayerInfo")

LOADER = object()


@ServerGetPlayerInfo.Signalled()
def handle_get_info(player: Player):
    info = db_manager.login_db_manager.get_account_info(player.account_id)
    ServerGetPlayerInfo.send_to_player(player, info)
