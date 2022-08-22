from ....db_managers import DBManager
from .....core.endpoint import Endpoint
from .....core.instances.player import Player

ServerGetPlayerInfo = Endpoint("GetPlayerInfo")


@ServerGetPlayerInfo.Signalled()
def handle_get_info(player: Player, _):
    info = DBManager.login_db_manager.get_account_info(player.account_id)
    ServerGetPlayerInfo.send_to_player(player, info)