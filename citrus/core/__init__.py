from ..internal.networking.endpoints.client.auth import login as _login, signup as _signup, LoggedIn as _LoggedIn


def login(email: str, password: str):
    _login(email, password)
    return _LoggedIn.wait(time_out=3)


def signup(email: str, username: str, password: str):
    _signup(email, username, password)
    return _LoggedIn.wait(time_out=3)
