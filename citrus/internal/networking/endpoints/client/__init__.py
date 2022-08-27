import glob as _glob
import os.path

from signalio import Signal
from ...network_manager import NetworkManager

path_name = os.path.dirname(__file__)

__all__ = [os.path.relpath(x, path_name).replace(".py", "") for x in _glob.glob(os.path.join(path_name, "*.py")) if
           not x.endswith("__init__.py")]


def send_to_server(signal_name: str, payload: dict):
    NetworkManager.send(NetworkManager.client_connection, Signal(signal_name, payload))


def load_client_endpoints():
    from .info import LOADER
    from .auth import LOADER
