from typing import Optional, Dict

from .lifecycle_subscriber import lifecycle_subscriber


def service(options: Optional[Dict] = None):
    return lifecycle_subscriber(options)
