from .service import Service

@Service
class ContainerService:
	def __init__(self):
		self.containers = []


	def register(self, container):
		self.containers.append(container)

	def load(self):
		for container in self.containers:
			container.instantiate()
