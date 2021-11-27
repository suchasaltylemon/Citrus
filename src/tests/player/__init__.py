from citrus.engine import Container

from .inventory import Inventory

class Player(Container):
	inventory = Inventory
