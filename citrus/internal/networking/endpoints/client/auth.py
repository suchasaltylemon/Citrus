from signalio import Event

from . import send_to_server
from .info import get_player_info
from ...network_manager import NetworkManager
from ....components.networkable import Networkable
from .....core.instances.player import Player
from .....core.systems import get_system
from .....utils.encoding import sbytes

LoggedIn = Event[Player]()

LOADER = object()


@NetworkManager.Signalled("__session_token")
def handle_session_token(_, signal):
    encoded_session_token = signal.data.get("session_token", None)
    if encoded_session_token is None:
        return

    session_token = sbytes(encoded_session_token)

    player = Player()
    networkable = player.get_component(Networkable)
    networkable.set_session_token(session_token)

    get_system("players")._local_player = player

    player_info, = get_player_info()
    player.account_id = player_info.get("account_id", None)
    player.display_name = player_info.get("username") + player_info.get("tag")
    player.username = player_info.get("username")

    LoggedIn.fire(player)


def login(email, password):
    send_to_server("__login", {
        "email": email,
        "password": password
    })


def signup(email, username, password):
    send_to_server("__signup", {
        "email": email,
        "username": username,
        "password": password
    })
