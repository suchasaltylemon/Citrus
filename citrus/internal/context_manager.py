from typing import Union

from .singleton import singleton
from ..log import logger

SERVER_CONTEXT = "server"
CLIENT_CONTEXT = "client"

context_logger = logger("ctx")


@singleton
class ContextManager:
    _context = None

    def determine_context(self, service_files, controller_files):
        if self.context_is_determined() or (len(service_files) == 0 and len(controller_files) == 0):
            return

        self._context = SERVER_CONTEXT if len(service_files) > 0 else (
            CLIENT_CONTEXT if len(controller_files) > 0 else None)

        context_logger.info(f"No runtime context. Setting as '{self._context}'")

    def is_server(self):
        return self._context == SERVER_CONTEXT

    def is_client(self):
        return self._context == CLIENT_CONTEXT

    def context_is_determined(self):
        return self._context is not None

    @property
    def context(self) -> Union[SERVER_CONTEXT, CLIENT_CONTEXT, None]:
        return self._context
