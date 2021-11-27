from .container import Container
from .components.behaviour import Behaviour
from .services import ContainerService as _ContainerService

def start():
	con_service = _ContainerService()

	con_service.load()
