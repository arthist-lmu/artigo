import logging

logger = logging.getLogger(__name__)


def dict_from_proto(proto):
    result = {}

    for x in proto:
        field = x.WhichOneof('value')

        if field == 'string_val':
            result.update({x.key: x.string_val})
        elif field == 'int_val':
            result.update({x.key: x.int_val})
        elif field == 'float_val':
            result.update({x.key: x.float_val})

    return result


def meta_to_proto(proto, data):
    for d in data:
        meta = proto.add()

        if d.get('value_int') is not None:
            meta.int_val = d['value_int']
            meta.key = d['name']
        elif d.get('value_float') is not None:
            meta.float_val = d['value_float']
            meta.key = d['name']
        elif d.get('value_str') is not None:
            meta.string_val = d['value_str']
            meta.key = d['name']

    return proto


def meta_from_proto(proto):
    result = []

    for x in proto:
        field = x.WhichOneof('value')

        if field == 'string_val':
            result.append({
            	'name': x.key,
            	'value_str': x.string_val,
            })
        elif field == 'int_val':
            result.append({
            	'name': x.key,
            	'value_int': x.int_val,
            	'value_str': str(x.int_val),
            })
        elif field == 'float_val':
            result.append({
            	'name': x.key,
            	'value_float': x.float_val,
            	'value_str': str(x.float_val),
            })

    return result


def tags_to_proto(proto, data):
    pass


def tags_from_proto(proto):
    result = []

    for x in proto:
        result.append({
            'id': x.id,
            'name': x.name,
            'language': x.language,
            'count': x.count,
        })

    return result


def read_chunk(iterator, chunksize=64):
    chunk = []

    for x in range(chunksize):
        try:
            chunk.append(next(iterator))
        except StopIteration:
            return chunk

    return chunk
