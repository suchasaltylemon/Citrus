COMPONENT_NAME = "__component_name"


def is_component(obj):
    return hasattr(obj, COMPONENT_NAME)


def get_component(instance, comp):
    component_name = getattr(comp, COMPONENT_NAME)
    components: list = getattr(instance, "_components")

    target_component = next((x for x in components if getattr(x, COMPONENT_NAME, "") == component_name), None)
    return target_component


def component():
    def decorator(cls):
        setattr(cls, COMPONENT_NAME, cls.__name__)

        return cls

    return decorator


class Component:
    pass
