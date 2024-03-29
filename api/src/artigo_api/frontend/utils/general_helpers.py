import json

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def is_url(x):
    try:
        validate = URLValidator()
        validate(x)

        return True
    except ValidationError:
        pass

    return False


def to_url(x, default=''):
    if is_url(x):
        return x

    return default


def to_int(value, default=0):
    try:
        return int(float(value))
    except:
        pass

    return default


def to_float(value, default=1.0):
    try:
        return float(value)
    except:
        pass

    return default


def to_boolean(value, default=False):
    try:
        return str(value).lower() in ('true')
    except:
        pass

    return default


def to_type(value):
    try:
        return json.loads(value)
    except:
        if isinstance(value, (list, set)):
            return value

    return value


def to_lower(value):
    if isinstance(value, str):
        return value.lower()

    if isinstance(value, (list, set)):
        return [x.lower() for x in value]

    raise ValueError(f'{value} is invalid')


def align(value):
    if isinstance(value, str):
        return value.strip().replace('_', '')

    if isinstance(value, (list, set)):
        return [x.strip().replace('_', '') for x in value]

    raise ValueError(f'{value} is invalid')


def to_bare(value):
    return align(to_lower(value))


def is_in(x, y):
    if x is None or y is None:
        return False
        
    if not isinstance(y, (list, set)):
        y = [y]

    return to_bare(x) in to_bare(y)


def to_iregex(x, field):
    if isinstance(x, (list, set)):
        return f"({'|'.join(y[field] for y in x)})"

    raise ValueError('Invalid instance')


def get_iou(roi_1, roi_2):
    try:
        data = {
            'x': [
                max(roi_1['x'], roi_2['x']),
                min(
                    roi_1['x'] + roi_1['width'],
                    roi_2['x'] + roi_2['width'],
                ),
            ],
            'y': [
                max(roi_1['y'], roi_2['y']),
                min(
                    roi_1['y'] + roi_1['height'],
                    roi_2['y'] + roi_2['height'],
                ),
            ],
        }
    except:
        return 0.0

    if data['x'][1] < data['x'][0]:
        return 0.0

    if data['y'][1] < data['y'][0]:
        return 0.0

    overlap = data['x'][1] - data['x'][0]
    overlap *= data['y'][1] - data['y'][0]

    area_1 = roi_1['width'] * roi_1['height']
    area_2 = roi_2['width'] * roi_2['height']

    iou = overlap / (area_1 + area_2 - overlap)

    return iou


def unflat_dict(data, parse_json=False):
    result_map = {}

    if parse_json:
        data_new = {}

        for key, value in data.items():
            try:
                data_new[key] = json.loads(value)
            except:
                data_new[key] = value

        data = data_new

    for key, value in data.items():
        path = key.split('.')
        prev = result_map

        for p in path[:-1]:
            if p not in prev:
                prev[p] = {}

            prev = prev[p]

        prev[path[-1]] = value

    return result_map
