from signalio import Signal
from ...network_manager import NetworkManager


def send_to_server(signal_name: str, payload: dict):
    NetworkManager.send(NetworkManager.client_connection, Signal(signal_name, payload))
