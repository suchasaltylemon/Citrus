def singleton(cls, cb=None):
    setattr(cls, "_instance", None)

    def new(_):
        if cls._instance is None:
            obj = super(cls, cls).__new__(cls)

            cls._instance = obj

            if cb is not None:
                cb(obj)

        return cls._instance

    setattr(cls, "__new__", new)
    return cls
