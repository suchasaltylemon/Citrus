class Service:
	def __new__(cls, target_cls):
		if not hasattr(target_cls, "_singleton"):
			setattr(target_cls, "_singleton", target_cls())

		def meta(_):
			return target_cls._singleton

		setattr(target_cls, "__new__", meta)

		return target_cls
