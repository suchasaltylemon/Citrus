import math
from typing import Dict, Optional

from citrus.internal.singleton import singleton

LOAD_ORDER = "__LOAD_ORDER__"


def controller(options: Optional[Dict] = None):
    options = options or {}
    load_order = options.get("load_order", math.inf)

    def decorator(cls):
        setattr(cls, LOAD_ORDER, load_order)

        singleton(cls)
        return cls

    return decorator
