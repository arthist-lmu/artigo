from django.conf import settings


def media_url_to_image(x):
    path = f'{x[0:2]}/{x[2:4]}/{x}.jpg'

    return f'{settings.API_URL}{settings.MEDIA_URL}{path}'
