import typing
from uuid import uuid4

from citrus.core.component import get_component
from citrus.internal.instance_manager import InstanceManager

T = typing.TypeVar("T")


class BaseInstance:
    _components = []

    name = "$instance"
    uuid = "$uuid"

    def get_component(self, component: T) -> typing.Type[T]:
        return get_component(self, component)


def instance(props: dict):
    def decorator(cls):
        assert hasattr(cls, "_components"), "Class must extend `BaseInstance`"

        name = props.get("name", "$instance")
        InstanceManager.register_instance_class(cls, props)

        def init(self):
            self.name = name
            self.uuid = uuid4().hex

            InstanceManager.attach_components(self)

        setattr(cls, "__init__", init)

        return cls

    return decorator
