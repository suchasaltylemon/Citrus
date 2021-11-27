class Component:
	_components = []
	_service = None

	def __init_subclass__(cls):
		@classmethod
		def meta(sub):
			cls._components.append(sub)


		setattr(cls, "__init_subclass__", meta)

