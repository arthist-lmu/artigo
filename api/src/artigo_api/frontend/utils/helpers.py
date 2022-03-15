def to_int(value, default=0):
    try:
        return int(value)
    except:
        pass

    return default


def to_float(value, default=1.0):
    try:
        return float(value)
    except:
        pass

    return default
