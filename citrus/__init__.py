import glob
import importlib
import inspect
import os.path

from .core.component import is_component as _is_component
from .internal.component_manager import ComponentManager as _ComponentManager
from .internal.db_managers import DBManager as _DBManager
from .internal.endpoint_manager import EndpointManager as _EndpointManager
from .internal.networking.network_manager import NetworkManager as _NetworkManager
from .internal.runtime_manager import RuntimeManager as _RuntimeManager
from .internal.system_manager import SystemManager as _SystemManager

paths = []

COMPONENT_EXT = "_component.py"
SERVICE_EXT = "_service.py"
CONTROLLER_EXT = "_controller.py"


def add_path(path: str):
    paths.append(path)


def _import(file):
    file_name = file.replace("\\", ".").replace("/", ".").replace(".py", "")

    module = importlib.import_module(file_name)
    return vars(module)


def start(ip: str, port: int = None):
    assert not _RuntimeManager.started, "Cannot start again, game has already started!"

    importlib.invalidate_caches()
    for path in paths:
        component_glob_path = os.path.join(path, "**/*" + COMPONENT_EXT)
        service_glob_path = os.path.join(path, "**/*" + SERVICE_EXT)
        controller_glob_path = os.path.join(path, "**/*" + CONTROLLER_EXT)

        component_files = glob.glob(component_glob_path, recursive=True)
        service_files = glob.glob(service_glob_path, recursive=True)
        controller_files = glob.glob(controller_glob_path, recursive=True)

        for file in component_files:
            namespace = _import(file)

            exported_component = namespace["export"]
            assert _is_component(exported_component)

            _ComponentManager.register_component(exported_component)

        for file in service_files:
            namespace = _import(file)

            exported_service = namespace["export"]
            assert hasattr(exported_service, "_instance")

            _RuntimeManager.register_service(exported_service())

        for file in controller_files:
            namespace = _import(file)

            exported_controller = namespace["export"]

            _RuntimeManager.register_controller(exported_controller())

    _DBManager.start()
    _NetworkManager.update_info(ip, port)
    _NetworkManager.start()
    _SystemManager.start()
    _RuntimeManager.start()
    _EndpointManager.start()


def export(cls):
    stack = inspect.stack()[1]

    stack.frame.f_locals["export"] = cls
