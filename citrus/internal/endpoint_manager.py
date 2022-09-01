from .networking.endpoints import load_server_endpoints
from .networking.endpoints.client import load_client_endpoints
from .singleton import singleton


@singleton
class EndpointManager:
    def start(self):
        from .context_manager import ContextManager
        context_manager = ContextManager()

        if context_manager.is_server():
            load_server_endpoints()

        else:
            load_client_endpoints()
