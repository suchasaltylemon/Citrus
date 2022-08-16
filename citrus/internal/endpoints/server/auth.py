from citrus import NetworkManager, DBManager
from citrus.include.signal import Signal
from citrus.include.signal.net.connection import Connection
from citrus.include.signal.net.event import Event

currently_logged_in = []

LoggedIn = Event()


def send_auth_token(conn):
    pass


@NetworkManager.Signalled("__login")
def handle_signal(conn: Connection, signal: Signal):
    email = signal.data.get("Email", None)
    password = signal.data.get("Password", None)

    if password is None or email is None:
        return

    account_id = DBManager.login_db_manager.get_account_id(email)
    if account_id is None or account_id in currently_logged_in:
        return

    valid_login = DBManager.login_db_manager.verify_login(email, password)
    if not valid_login:
        return

    username = DBManager.login_db_manager.get_username(account_id)

    currently_logged_in.append(account_id)

    LoggedIn.fire(conn, account_id, username)
