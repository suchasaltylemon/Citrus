import inspect

from .singleton import singleton


@singleton
class ComponentManager:
    component_classes = []
    dependency_cache = {}

    def get_component_dependencies(self, component):
        component_class = component if inspect.isclass(component) else component.__class__

        if component_class in self.dependency_cache:
            dependencies = self.dependency_cache[component_class]

        else:
            dependencies = [x.default for x in inspect.signature(component_class).parameters.values() if
                            x.default != inspect.Parameter.empty]
            self.dependency_cache[component_class] = dependencies

        return dependencies

    def load_component(self, component):
        loaded_dependencies = []
        dependencies = self.get_component_dependencies(component)

        for dependency in dependencies:
            loaded_dependencies.append(self.load_component(dependency))

        return component(*loaded_dependencies)

    def register_component(self, component_class):
        self.component_classes.append(component_class)
