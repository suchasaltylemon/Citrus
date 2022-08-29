from .networking.endpoints import load_server_endpoints
from .networking.endpoints.client import load_client_endpoints


class EndpointManager:
    @classmethod
    def start(cls):
        from .context_manager import ContextManager
        if ContextManager.is_server():
            load_server_endpoints()

        else:
            load_client_endpoints()
