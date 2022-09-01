import glob as _glob
import logging
import os.path

from signalio import Signal
from ...network_manager import NetworkManager

network_manager = NetworkManager()
path_name = os.path.dirname(__file__)

__all__ = [os.path.relpath(x, path_name).replace(".py", "") for x in _glob.glob(os.path.join(path_name, "*.py")) if
           not x.endswith("__init__.py")]


def send_to_server(signal_name: str, payload: dict):
    logging.warn(f"Sending to server, {network_manager.client}")
    network_manager.send(network_manager.client_connection, Signal(signal_name, payload))


def load_client_endpoints():
    from .info import LOADER
    from .auth import LOADER
