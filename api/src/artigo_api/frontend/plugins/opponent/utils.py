import logging

from itertools import chain
from collections import defaultdict


def gamerounds_per_resource(gamerounds, resource_ids, limit=1):
    data = defaultdict(list)

    for x in gamerounds:
        data[x['resource_id']].append(x['gameround_id'])

        if limit == 1 and len(data) == len(resource_ids):
            break

    data = {k: v[:limit] for k, v in data.items()}

    return list(chain(*data.values()))
