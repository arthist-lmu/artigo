def name(func=None):
    def wrapper(*args, **kwargs):
        try:
            name = func.__func__.__qualname__
        except:
            name = func.__qualname__

        return func(*args, **kwargs, name=name)

    return wrapper
