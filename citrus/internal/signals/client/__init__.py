from citrus import NetworkManager
from signal import Signal


def send_to_server(signal_name: str, payload: dict):
    NetworkManager.send(NetworkManager.client_connection, Signal(signal_name, payload))
