from django.conf import settings

API_LOCATION = 'http://localhost:8000'


def media_url_to_image(x):
    path = f'{x[0:2]}/{x[2:4]}/{x}.jpg'

    return f'{API_LOCATION}{settings.MEDIA_URL}{path}'
