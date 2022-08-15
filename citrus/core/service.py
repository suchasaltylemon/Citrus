from citrus.internal.singleton import singleton


def service():
    def decorator(cls):
        singleton(cls)
        return cls

    return decorator
