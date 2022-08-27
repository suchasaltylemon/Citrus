from .networking.endpoints import load_server_endpoints
from .networking.endpoints.client import load_client_endpoints
from .runtime_manager import RuntimeManager


class EndpointManager:
    @classmethod
    def start(cls):
        if RuntimeManager.is_server():
            load_server_endpoints()

        else:
            load_client_endpoints()
