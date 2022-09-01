from typing import Optional, Dict

from .lifecycle_subscriber import lifecycle_subscriber


def controller(options: Optional[Dict] = None):
    return lifecycle_subscriber(options)
