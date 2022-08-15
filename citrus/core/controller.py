from citrus.internal.singleton import singleton


def controller():
    def decorator(cls):
        singleton(cls)
        return cls

    return decorator
