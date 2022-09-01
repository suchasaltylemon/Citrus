from .component_manager import ComponentManager
from .singleton import singleton


@singleton
class InstanceManager:
    instance_component_map = {}

    def register_instance_class(self, instance_class, props):
        components = props.get("components", ())

        self.instance_component_map[instance_class] = components

    def attach_components(self, instance):
        components = [y for x in instance.__class__.mro() if x in self.instance_component_map for y in
                      self.instance_component_map[x]]

        for component in components:
            loaded_component = ComponentManager().load_component(component)
            getattr(instance, "_components").append(loaded_component)
