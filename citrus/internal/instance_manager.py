from .component_manager import ComponentManager


class InstanceManager:
    instance_component_map = {}

    @classmethod
    def register_instance_class(cls, instance_class, props):
        components = props.get("components", ())

        cls.instance_component_map[instance_class] = components

    @classmethod
    def attach_components(cls, instance):
        components = [y for x in instance.__class__.mro() if x in cls.instance_component_map for y in
                      cls.instance_component_map[x]]

        for component in components:
            loaded_component = ComponentManager.load_component(component)
            getattr(instance, "_components").append(loaded_component)
