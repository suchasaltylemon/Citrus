from .instances.player import Player
from ..internal.networking.endpoints.client.auth import login as _login, LoggedIn as _LoggedIn, signup as _signup

TIME_OUT = 3


def login(email: str, password: str) -> Player:
    _login(email, password)
    player = _LoggedIn.wait(time_out=TIME_OUT)

    if player is not None:
        return player[0]


def signup(email: str, username: str, password: str):
    _signup(email, username, password)
    player = _LoggedIn.wait(time_out=TIME_OUT)

    if player is not None:
        return player[0]
