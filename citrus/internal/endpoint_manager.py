from .lifecycle_manager import LifecycleManager
from .networking.endpoints import load_server_endpoints
from .networking.endpoints.client import load_client_endpoints


class EndpointManager:
    @classmethod
    def start(cls):
        if LifecycleManager.is_server():
            load_server_endpoints()

        else:
            load_client_endpoints()
