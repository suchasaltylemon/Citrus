from .context_manager import ContextManager
from ..core.errors import LifecycleException
from ..lifecycle import ON_START, ON_START_REGISTERED
from ..log import logger

registration_logger = logger("reg")


class RegistrationManager:
    services = []
    controllers = []

    context = None

    @classmethod
    def register_service(cls, service_object):
        if ContextManager.is_client():
            e = RuntimeError("Runtime is not running as server! Cannot register any services!")

            registration_logger.error("Runtime is not running as server! Cannot register any services!", exc_info=e)
            raise e

        cls.services.append(service_object)
        registration_logger.info(f"Registered service '{service_object}'")

    @classmethod
    def register_controller(cls, controller_object):
        if ContextManager.is_server():
            e = RuntimeError("Runtime is not running as client! Cannot register any controllers!")

            registration_logger.error("Runtime is not running as client! Cannot register any controllers!", exc_info=e)
            raise e

        cls.controllers.append(controller_object)
        registration_logger.info(f"Registered controller '{controller_object}'")

    @classmethod
    def start(cls):
        for service in cls.services:
            if hasattr(service, ON_START_REGISTERED):
                if not hasattr(service, ON_START):
                    e = LifecycleException(
                        f"'{service}' has subscribed to 'on_start' lifecycle, but has not implemented method")

                    registration_logger.error("Service has not subscribed to lifecycle method", exc_info=e)
                    raise e

                registration_logger.info(f"Running on_start lifecycle method for '{service}'")
                getattr(service, ON_START)()
                registration_logger.info(f"Finished running on_start lifecycle method for '{service}'")

        for controller in cls.controllers:
            if hasattr(controller, ON_START_REGISTERED):
                if not hasattr(controller, ON_START):
                    e = LifecycleException(
                        f"'{controller}' has subscribed to 'on_start' lifecycle, but has not implemented method")

                    registration_logger.error("Controller has not subscribed to lifecycle method", exc_info=e)
                    raise e

                registration_logger.info(f"Running on_start lifecycle method for '{controller}'")
                getattr(controller, ON_START)()
                registration_logger.info(f"Finished running on_start lifecycle method for '{controller}'")
