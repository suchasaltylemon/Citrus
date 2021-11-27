from .component import Component
from ..services.components import BehaviourService

class Behaviour(Component):
	_service = BehaviourService()

	def start(self):
		pass
