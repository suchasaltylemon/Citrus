import glob
import importlib
import inspect
import os.path

from citrus.core.component import is_component
from citrus.internal.component_manager import ComponentManager
from citrus.internal.runtime_manager import RuntimeManager
from internal.db_managers import DBManager
from internal.network_manager import NetworkManager

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
    assert not RuntimeManager.started, "Cannot start again, game has already started!"

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
            assert is_component(exported_component)

            ComponentManager.register_component(exported_component)

        for file in service_files:
            namespace = _import(file)

            exported_service = namespace["export"]
            assert hasattr(exported_service, "_instance")

            RuntimeManager.register_service(exported_service())

        for file in controller_files:
            namespace = _import(file)

            exported_controller = namespace["export"]

            RuntimeManager.register_controller(exported_controller())

    DBManager.start()
    NetworkManager.update_info(ip, port)
    RuntimeManager.start()
    NetworkManager.start()


def export(cls):
    stack = inspect.stack()[1]

    stack.frame.f_locals["export"] = cls
