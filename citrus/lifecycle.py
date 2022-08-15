from typing import Union

ON_START = "on_start"
ON_TICK = "on_tick"

REGISTERED_SUFFIX = "_registered"
ON_START_REGISTERED = ON_START + REGISTERED_SUFFIX
ON_TICK_REGISTERED = ON_TICK + REGISTERED_SUFFIX


def _register_class_lifecycle(lifecycle_name: Union[ON_START, ON_TICK]):
    def decorator(cls):
        setattr(cls, lifecycle_name + REGISTERED_SUFFIX, True)

        return cls

    return decorator


def onstart():
    return _register_class_lifecycle(ON_START)


def ontick():
    return _register_class_lifecycle(ON_TICK)
