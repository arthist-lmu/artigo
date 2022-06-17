def get_configs(query, plugin):
    return [
        {
            'type': plugin_type,
            'params': query[f'{plugin}_options'],
        }
        for plugin_type in query[f'{plugin}_type']
    ]
