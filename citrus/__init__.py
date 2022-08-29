import glob
import importlib
import inspect
import logging
import os.path
from threading import Thread
from typing import List

from .core.component import is_component as _is_component
from .core.errors import GameRunningError, LoggingException, NoModuleEntrypointException
from .internal.component_manager import ComponentManager as _ComponentManager
from .internal.db_managers import DBManager as _DBManager
from .internal.endpoint_manager import EndpointManager as _EndpointManager
from .internal.lifecycle_manager import LifecycleManager as _RuntimeManager, SERVER_CONTEXT, CLIENT_CONTEXT
from .internal.networking.network_manager import NetworkManager as _NetworkManager
from .internal.system_manager import SystemManager as _SystemManager

paths = []

COMPONENT_EXT = "_component.py"
SERVICE_EXT = "_service.py"
CONTROLLER_EXT = "_controller.py"

init_logger = logging.Logger("Init")

logging_to_stream = False
log_paths = []


def log_to_file(path: str):
    if path in log_paths:
        raise LoggingException("Logging is already set to this file")

    init_logger.addHandler(logging.FileHandler(path))


def log_to_stream():
    global logging_to_stream
    if logging_to_stream:
        raise LoggingException("Already logging to stream")

    init_logger.addHandler(logging.StreamHandler())


def add_path(path: str):
    init_logger.info(f"Added path '{path}'")
    paths.append(path)


def _import(file):
    file_name = file.replace("\\", ".").replace("/", ".").replace(".py", "")

    module = importlib.import_module(file_name)
    return vars(module)


def _load_modules(component_files, service_files, controller_files):
    threads: List[Thread] = []
    for file in component_files:
        def _thread():
            namespace = _import(file)
            init_logger.info(f"Loaded file '{file}")

            exported_component = namespace["export"]
            assert _is_component(exported_component)

            _ComponentManager.register_component(exported_component)
            init_logger.info(f"Registered component {exported_component}")

        t = Thread(target=_thread)
        t.start()

        threads.append(t)

    for file in service_files:
        def _thread():
            namespace = _import(file)
            init_logger.info(f"Loaded file '{file}")

            exported_service = namespace["export"]
            assert hasattr(exported_service, "_instance")

            _RuntimeManager.register_service(exported_service())
            init_logger.info(f"Registered service {exported_service}")

        t = Thread(target=_thread)
        t.start()

        threads.append(t)

    for file in controller_files:
        def _thread():
            namespace = _import(file)
            init_logger.info(f"Loaded file '{file}")

            exported_controller = namespace["export"]

            _RuntimeManager.register_controller(exported_controller())
            init_logger.info(f"Registered controller {exported_controller}")

        t = Thread(target=_thread)
        t.start()

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
    _DBManager.start()
    _NetworkManager.update_info(ip, port)
    _NetworkManager.start()
    _SystemManager.start()
    _RuntimeManager.start()
    _EndpointManager.start()


def _determine_context(service_files, controller_files):
    return SERVER_CONTEXT if len(service_files) > 0 else (CLIENT_CONTEXT if len(controller_files) > 0 else None)


def start(ip: str, port: int = None):
    if _RuntimeManager.started:
        init_logger.fatal("Game was already running. Cannot start new instance!")
        raise GameRunningError("Cannot start again, game has already started!")
    else:
        init_logger.info("Game is not running. Beginning to setup")

    importlib.invalidate_caches()
    init_logger.debug("Invalidated caches")

    context = None
    for path in paths:
        component_files, service_files, controller_files = _detect_files(path)
        init_logger.debug(f"Detected files at path '{path}'")

        if context is None:
            context = _determine_context(service_files, controller_files)

            if context is not None:
                init_logger.info(f"No runtime context. Setting as '{context}'")
                _RuntimeManager.set_context(context)

        init_logger.info("Loading scripts")
        threads = _load_modules(component_files, service_files, controller_files)

        for thread in threads:
            thread.join()

        init_logger.info("Loaded scripts")

    if context is not None:
        init_logger.info("Initialising all runtime managers")
        _init_managers(ip, port)
        init_logger.info("Initialised all runtime managers")

    else:
        init_logger.fatal("No entrypoint found!")
        raise NoModuleEntrypointException("No modules could be found to run on server or client")


def export(cls):
    stack = inspect.stack()[1]

    stack.frame.f_locals["export"] = cls
