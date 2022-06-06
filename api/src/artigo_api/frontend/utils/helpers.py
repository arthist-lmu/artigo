import json


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


def to_type(value):
    try:
        return json.loads(value)
    except:
        pass


def to_lower(value):
    if isinstance(value, str):
        return value.lower()

    if isinstance(value, (list, set)):
        return [x.lower() for x in value]

    raise ValueError(f'Invalid: {value}')


def align(value):
    if isinstance(value, str):
        return value.strip().replace('_', '')

    if isinstance(value, (list, set)):
        return [x.strip().replace('_', '') for x in value]

    raise ValueError(f'Invalid: {value}')


def to_bare(value):
    return align(to_lower(value))


def is_in(x, y):
    if x is None or y is None:
        return False
        
    if not isinstance(y, (list, set)):
        y = [y]

    return to_bare(x) in to_bare(y)
