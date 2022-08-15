import inspect


class ComponentManager:
    component_classes = []
    dependency_cache = {}

    @classmethod
    def get_component_dependencies(cls, component):
        component_class = component if inspect.isclass(component) else component.__class__

        if component_class in cls.dependency_cache:
            dependencies = cls.dependency_cache[component_class]

        else:
            dependencies = [x.default for x in inspect.signature(component_class).parameters.values() if
                            x.default != inspect.Parameter.empty]
            cls.dependency_cache[component_class] = dependencies

        return dependencies

    @classmethod
    def load_component(cls, component):
        loaded_dependencies = []
        dependencies = cls.get_component_dependencies(component)

        for dependency in dependencies:
            loaded_dependencies.append(cls.load_component(dependency))

        return component(*loaded_dependencies)

    @classmethod
    def register_component(cls, component_class):
        cls.component_classes.append(component_class)
