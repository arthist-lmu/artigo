from django.conf import settings

def media_url_to_image(x):
    path = f'{x[0:2]}/{x[2:4]}/{x}.jpg'

    return f'{settings.API}{settings.MEDIA_URL}{path}'


def preprocessing_hook(endpoints, **kwargs):
    def in_excluded(path):
        for exclude_path in exclude_paths:
            if path.startswith(
                (exclude_path, f'/{exclude_path}')
            ):
                return True

        return False

    endpoints_to_include = []
    exclude_paths = ['rest-auth']

    return [
        endpoint for endpoint in endpoints
        if not in_excluded(endpoint[0])
    ]
