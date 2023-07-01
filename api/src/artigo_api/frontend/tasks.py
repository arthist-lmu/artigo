import os
import re
import uuid
import imageio
import logging
import traceback

from celery import shared_task
from django.conf import settings
from django.core.exceptions import BadRequest
from django.core.management import call_command
from frontend import cache
from frontend.utils import (
    to_int,
    TarArchive,
    ZipArchive,
    resize_image,
    check_extension,
)
from frontend.models import *

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def renew_cache(renew=True):
    call_command('renew_cache', renew=renew)


@shared_task(ignore_result=True)
def send_user_scores():
    call_command('send_user_scores')


@shared_task(bind=True)
def upload_collection(self, data):
    try:
        user = CustomUser.objects.get(id=data.get('user_id'))
    except CustomUser.DoesNotExist:
        raise BadRequest('unknown_user')

    if not data.get('collection_title'):
        raise BadRequest('collection_title_is_required')

    collection = Collection.objects.filter(
            user=user,
            titles__name__in=data['collection_title'].values(),
        ) \
        .first()

    if collection is None:
        if not data.get('collection_id'):
            raise BadRequest('collection_id_is_required')

        access = data.get('access', 'R')
        
        if access.lower() == 'open':
            access = 'O'
        elif access.lower() == 'pending':
            access = 'P'
        elif access.lower() == 'restricted':
            access = 'R'

        collection = Collection.objects.create(
            user=user,
            hash_id=data['collection_id'],
            access=access,
            status='U',
            progress=0.0,
        )

        for lang, name in data['collection_title'].items():
            try:
                title = CollectionTitle.objects.create(
                    name=name,
                    language=lang,
                )
                title.save()
            except:
                title = CollectionTitle.objects.filter(
                        name=name,
                        language=lang,
                    ) \
                    .first()

            collection.titles.add(title)

        collection.save()

    entries = data.get('entries', [])
    image_path = data.get('image_path')

    if check_extension(image_path, ['.zip']):
        archive = ZipArchive(image_path)
    elif check_extension(image_path, [
        '.tar',
        '.tar.gz',
        '.tar.bz2',
        '.tar.xz',
    ]):
        archive = TarArchive(image_path)
    else:
        BadRequest('corrupt_archives_file')

    count = 0

    with archive as file_obj:
        for entry in entries:
            try:
                img_obj = file_obj.read(entry['path'])
                image = imageio.imread(img_obj, pilmode='RGB')
            except:
                continue

            hash_id = uuid.uuid4().hex
            image_output_file = None

            for resolution in settings.IMAGE_RESOLUTIONS:
                max_dim = resolution.get('max_dim', 200)
                suffix = resolution.get('suffix', '')

                resized_image = resize_image(image, max_dim=max_dim)

                image_output_dir = os.path.join(
                    settings.MEDIA_ROOT,
                    hash_id[0:2],
                    hash_id[2:4],
                )

                os.makedirs(image_output_dir, exist_ok=True)
                image_output_file = os.path.join(
                    image_output_dir,
                    f'{hash_id}{suffix}.jpg',
                )

                try:
                    imageio.imwrite(image_output_file, resized_image)
                    logger.info(f'Created image {image_output_file}')
                except:
                    continue

            if image_output_file is not None:
                resource = Resource.objects.create(
                    collection=collection,
                    hash_id=hash_id,
                )

                if entry.get('creator_name'):
                    creator = Creator.objects.filter(name=entry['creator_name']).first()

                    if creator is None:
                        creator = Creator.objects.create(name=entry['creator_name'])
                        creator.save()

                    resource.creators.add(creator)

                for key in ['title_name', 'title_name_de', 'title_name_en']:
                    if entry.get(key):
                        _, lang = key.rsplit('_', 1)

                        if not lang in ('de', 'en'):
                            lang = data.get('lang', 'de')

                        title = Title.objects.filter(
                                name=entry[key],
                                language=lang,
                            ) \
                            .first()

                        if title is None:
                            title = Title.objects.create(
                                name=entry[key],
                                language=lang,
                            )
                            title.save()
                            
                        resource.titles.add(title)

                if entry.get('source_name'):
                    source = Source.objects.filter(name=entry['source_name']).first()

                    if source is None:
                        source = Source.objects.create(name=entry['source_name'])

                        if entry.get('source_url'):
                            source.url = entry['source_url']

                        source.save()

                    resource.source = source

                if to_int(entry.get('created_start'), default=None):
                    resource.created_start = to_int(entry['created_start'])

                    if to_int(entry.get('created_end'), default=None):
                        resource.created_end = to_int(entry['created_end'])
                    else:
                        resource.created_end = to_int(entry['created_start'])

                if entry.get('location'):
                    resource.location = entry['location']

                if entry.get('institution'):
                    resource.institution = entry['institution']

                if entry.get('origin'):
                    resource.origin = entry['origin']

                for key in ['tags_name', 'tags_name_de', 'tags_name_en']:
                    if entry.get(key):
                        _, lang = key.rsplit('_', 1)

                        if not lang in ('de', 'en'):
                            lang = data.get('lang', 'de')

                        if isinstance(entry[key], str):
                            entry[key] = re.split(';|,', entry[key])

                        if not isinstance(entry[key], (list, set)):
                            entry[key] = [entry[key]]

                        for tag_name in entry[key]:
                            tag = Tag.objects.filter(
                                    name=tag_name.strip(),
                                    language=lang,
                                ) \
                                .first()

                            if tag is None:
                                tag = Tag.objects.create(
                                    name=tag_name.strip(),
                                    language=lang,
                                )
                                tag.save()

                            tagging = UserTagging.objects.create(
                                user=user,
                                resource=resource,
                                tag=tag,
                                uploaded=True,
                            )
                            tagging.save()

                resource.save()
                count += 1

            if count % 10 == 0:
                collection.progress = count / len(entries)
                collection.save()

        collection.progress = count / len(entries)
        collection.save()

    os.remove(image_path)

    if count == 0:
        collection.status = 'E'
        collection.save()

        raise BadRequest('no_images_uploaded')

    if count == len(entries):
        collection.status = 'F'
        collection.progress = 1.0
        collection.save()

        return {'status': 'ok'}

    collection.status = 'E'
    collection.save()

    raise BadRequest('unknown_error')
