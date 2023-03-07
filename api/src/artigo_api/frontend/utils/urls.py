from django.conf import settings


def media_url_to_image(x):
    file_path = f'{x[0:2]}/{x[2:4]}/{x}.{settings.IMAGE_EXT}'

    return f'{settings.API_URL}{settings.MEDIA_URL}{file_path}'


def media_url_to_preview(x):
    file_path = f'{x[0:2]}/{x[2:4]}/{x}_m.{settings.IMAGE_EXT}'

    return f'{settings.API_URL}{settings.MEDIA_URL}{file_path}'
