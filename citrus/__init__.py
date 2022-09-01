import glob
import importlib
import inspect
import os.path
from threading import Thread
from typing import List, Optional

from .core.component import is_component as _is_component
from .core.errors import GameRunningError, NoModuleEntrypointException
from .internal.component_manager import ComponentManager as _ComponentManager
from .internal.context_manager import ContextManager as _ContextManager
from .internal.db_managers import DBManager as _DBManager
from .internal.endpoint_manager import EndpointManager as _EndpointManager
from .internal.networking.network_manager import NetworkManager as _NetworkManager
from .internal.registration_manager import RegistrationManager as _RegistrationManager
from .internal.system_manager import SystemManager as _SystemManager
from .log import setup as _setup, logger as _logger

paths = []

COMPONENT_EXT = "_component.py"
SERVICE_EXT = "_service.py"
CONTROLLER_EXT = "_controller.py"

game_started = False

boot_logger = _logger("boot")

context_manager = _ContextManager()
network_manager = _NetworkManager()
db_manager = _DBManager()
system_manager = _SystemManager()
registration_manager = _RegistrationManager()
endpoint_manager = _EndpointManager()
component_manager = _ComponentManager()


def add_path(path: str):
    path = path.replace("/", "\\")
    boot_logger.info(f"Added path '{path}'")
    paths.append(path)


def _import(file):
    file_name = file.replace("\\", ".").replace("/", ".").replace(".py", "")

    module = importlib.import_module(file_name)
    return vars(module)


def _load_modules(component_files, service_files, controller_files):
    threads: List[Thread] = []
    for file in component_files:
        def _thread():
            boot_logger.info(f"Loading file '{file}'")
            namespace = _import(file)
            boot_logger.info(f"Loaded file '{file}")

            exported_component = namespace["export"]
            assert _is_component(exported_component)

            component_manager.register_component(exported_component)

        t = Thread(target=_thread)
        t.start()
        boot_logger.debug(f"Started controller loading thread for {file}")

        threads.append(t)

    for file in service_files:
        def _thread():
            boot_logger.info(f"Loading file '{file}'")
            namespace = _import(file)
            boot_logger.info(f"Loaded file '{file}")

            exported_service = namespace["export"]
            assert hasattr(exported_service, "_instance")

            registration_manager.register_service(exported_service())

        t = Thread(target=_thread)
        t.start()
        boot_logger.debug(f"Started service loading thread for {file}")

        threads.append(t)

    for file in controller_files:
        def _thread():
            boot_logger.info(f"Loading file '{file}'")
            namespace = _import(file)
            boot_logger.info(f"Loaded file '{file}")

            exported_controller = namespace["export"]

            registration_manager.register_controller(exported_controller())
            boot_logger.info(f"Registered controller {exported_controller}")

        t = Thread(target=_thread)
        t.start()
        boot_logger.debug(f"Started controller loading thread for {file}")

        threads.append(t)

    return threads


def _detect_files(path: str):
    component_glob_path = os.path.join(path, "**/*" + COMPONENT_EXT)
    service_glob_path = os.path.join(path, "**/*" + SERVICE_EXT)
    controller_glob_path = os.path.join(path, "**/*" + CONTROLLER_EXT)

    component_files = glob.glob(component_glob_path, recursive=True)
    service_files = glob.glob(service_glob_path, recursive=True)
    controller_files = glob.glob(controller_glob_path, recursive=True)

    return component_files, service_files, controller_files


def _init_managers(ip: str, port: int):
    db_manager.start()

    network_manager.update_info(ip, port)
    network_manager.start()

    system_manager.start()
    registration_manager.start()
    endpoint_manager.start()


def start(ip: str, port: int = None, *, log_path: Optional[str] = None, log_to_stream: Optional[bool] = False,
          do_debug: Optional[bool] = False):
    global game_started

    if game_started:
        boot_logger.fatal("Game was already running. Cannot start new instance!")
        raise GameRunningError("Cannot start again, game has already started!")
    else:
        _setup(log_path, log_to_stream=log_to_stream, do_debug=do_debug)
        boot_logger.info("Game is not running. Beginning to setup")

    importlib.invalidate_caches()
    boot_logger.debug("Invalidated caches")

    for path in paths:
        component_files, service_files, controller_files = _detect_files(path)
        boot_logger.debug(f"Detected files at path '{path}'")

        if not context_manager.context_is_determined():
            context_manager.determine_context(service_files, controller_files)

        boot_logger.info(f"Loading scripts at path '{path}'...")
        threads = _load_modules(component_files, service_files, controller_files)

        for thread in threads:
            thread.join()

        boot_logger.info(f"Loaded scripts at path '{path}'")

    if context_manager.context_is_determined():
        boot_logger.info("Initialising all runtime managers")
        _init_managers(ip, port)
        boot_logger.info("Initialised all runtime managers")

        game_started = True

    else:
        boot_logger.fatal("No entrypoint found!")
        raise NoModuleEntrypointException("No modules could be found to run on server or client")


def export(cls):
    stack = inspect.stack()[1]

    stack.frame.f_locals["export"] = cls
