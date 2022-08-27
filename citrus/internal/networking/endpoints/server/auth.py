from Crypto import Random
from signalio import SecureConnection, Event, Signal

from ...network_manager import NetworkManager
from ....components.networkable import Networkable
from ....db_managers import DBManager
from .....core.instances.player import Player
from .....utils.encoding import bstring

currently_logged_in = []

LoggedIn = Event[Player]()

SESSION_TOKEN_SIZE_BYTES = 7

session_tokens = {}

LOADER = object()


def send_session_token(conn: SecureConnection, session_token: bytes):
    encoded_session_token = bstring(session_token)

    NetworkManager.send(conn, Signal("__session_token", {
        "session_token": encoded_session_token
    }))


def generate_session_token():
    return Random.get_random_bytes(SESSION_TOKEN_SIZE_BYTES)


def player_login(conn: SecureConnection, account_id: str):
    username = DBManager.login_db_manager.get_username(account_id)
    tag = DBManager.login_db_manager.get_tag(account_id)

    session_token = generate_session_token()
    session_tokens[conn] = session_token
    send_session_token(conn, session_token)

    player = Player()
    player.username = username
    player.account_id = account_id
    player.display_name = username + tag

    networkable = player.get_component(Networkable)
    networkable.set_session_token(session_token)
    networkable.set_connection(conn)

    LoggedIn.fire(player)


@NetworkManager.Signalled("__signup")
def handle_signup(conn: SecureConnection, signal: Signal):
    email = signal.data.get("email", None)
    username = signal.data.get("username", None)
    password = signal.data.get("password", None)

    if password is None or email is None or username is None:
        return

    if DBManager.login_db_manager.account_exists(email):
        return

    success = DBManager.login_db_manager.create_account(email, username, password)

    if not success:
        return

    account_id = DBManager.login_db_manager.get_account_id(email)
    player_login(conn, account_id)


@NetworkManager.Signalled("__login")
def handle_login(conn: SecureConnection, signal: Signal):
    email = signal.data.get("email", None)
    password = signal.data.get("password", None)

    if password is None or email is None:
        return

    account_id = DBManager.login_db_manager.get_account_id(email)
    if account_id is None or account_id in currently_logged_in:
        return

    valid_login = DBManager.login_db_manager.verify_login(email, password)
    if not valid_login:
        return

    player_login(conn, account_id)
