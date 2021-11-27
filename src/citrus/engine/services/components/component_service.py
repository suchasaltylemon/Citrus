from ..service import Service

@Service
class ComponentService:
	@staticmethod
	def execute(component):
		service = component._service

		service.register(component())
