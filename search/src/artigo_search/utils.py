def dict_from_proto(proto):
    result = {}

    for x in proto:
        field = x.WhichOneof('value')

        if field == 'string_val' and x.string_val:
            result.update({x.key: x.string_val})
        elif field == 'int_val':
            result.update({x.key: x.int_val})
        elif field == 'float_val':
            result.update({x.key: x.float_val})

    return result


def meta_to_proto(proto, data):
    for d in data:
        field = proto.add()
        field.key = d['name']

        if d.get('value_int') is not None:
            field.int_val = d['value_int']
        elif d.get('value_float') is not None:
            field.float_val = d['value_float']
        elif d.get('value_str'):
            field.string_val = d['value_str']

    return proto


def meta_from_proto(proto):
    result = []

    for x in proto:
        field = x.WhichOneof('value')

        if field == 'string_val' and x.string_val:
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
    for d in data:
        field = proto.add()

        field.id = d['id']
        field.name = d['name']
        field.language = d['language']
        field.count = d['count']

    return proto


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
