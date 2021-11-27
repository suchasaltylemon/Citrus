from ..service import Service

@Service
class BehaviourService:
	def __init__(self):
		self.components = []


	def register(self, component):
		component.start()

		self.components.append(component)
