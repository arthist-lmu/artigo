from django.conf import settings

API = 'http://localhost:8000'


def media_url_to_image(x):
    path = f'{x[0:2]}/{x[2:4]}/{x}.jpg'

    return f'{API}{settings.MEDIA_URL}{path}'


def preprocessing_hook(endpoints, **kwargs):
    def in_excluded(path):
        for exclude_path in exclude_paths:
            if path.startswith(exclude_path):
                return True

            if path.startswith(f'/{exclude_path}'):
                return True

        return False

    endpoints_to_include = []
    exclude_paths = ['rest-auth']

    for endpoint in endpoints:
        if not in_excluded(endpoint[0]):
            endpoints_to_include.append(endpoint)

    return endpoints_to_include
