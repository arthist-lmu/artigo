import random

from frontend import cache


def random_resources(resources, limit, max_tries=1000):
    try_count = 1
    resource_ids = set()

    while try_count < max_tries:
        key = random.randint(0, cache.resource_count() - 1)

        try: 
            resource = resources.get(id=key)
            resource_ids.add(resource['id'])
        except:
            try_count += 1
            continue

        if len(resource_ids) == limit:
            break

    if len(resource_ids) < limit:
        for resource in resources:
            resource_ids.add(resource.id)

            if len(resource_ids) == limit:
                break

    return list(resource_ids)
