from typing import Union

from citrus.log import logger

SERVER_CONTEXT = "server"
CLIENT_CONTEXT = "client"

context_logger = logger("ctx")


class ContextManager:
    _context = None

    @classmethod
    def determine_context(cls, service_files, controller_files):
        if cls.context_is_determined() or (len(service_files) == 0 and len(controller_files) == 0):
            return

        cls._context = SERVER_CONTEXT if len(service_files) > 0 else (
            CLIENT_CONTEXT if len(controller_files) > 0 else None)

        context_logger.info(f"No runtime context. Setting as '{cls._context}'")

    @classmethod
    def is_server(cls):
        return cls._context == SERVER_CONTEXT

    @classmethod
    def is_client(cls):
        return cls._context == CLIENT_CONTEXT

    @classmethod
    def context_is_determined(cls):
        return cls._context is not None

    @classmethod
    @property
    def context(cls) -> Union[SERVER_CONTEXT, CLIENT_CONTEXT, None]:
        return cls._context
