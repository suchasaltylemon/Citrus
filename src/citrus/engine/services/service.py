class Service:
	def __new__(cls, other):
		if not hasattr(other, "_service"):
			setattr(other, "_service", other())

		def meta(_):
			return other._service

		setattr(other, "__new__", meta)

		return lambda: other._service
