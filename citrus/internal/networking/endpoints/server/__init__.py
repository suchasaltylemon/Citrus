import glob as _glob
import os.path

path_name = os.path.dirname(__file__)

__all__ = [os.path.relpath(x, path_name).replace(".py", "") for x in _glob.glob(os.path.join(path_name, "*.py")) if
           not x.endswith("__init__.py")]


def load_server_endpoints():
    from .auth import LOADER
    from .info import LOADER
    from .replication import LOADER
