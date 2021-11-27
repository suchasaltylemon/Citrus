from .services import ContainerService
from .services.components import ComponentService

containers = ContainerService()
comp_service = ComponentService()

class Container:
	def __init_subclass__(cls):
		containers.register(cls)


	@classmethod
	def instantiate(cls):
		attrs = [getattr(cls, attr) for attr in dir(cls)]
		components = [comp for comp in attrs if hasattr(comp, "_components")]

		for comp in components:
			comp_service.execute(comp)

