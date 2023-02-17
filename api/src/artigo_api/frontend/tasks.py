import os
import uuid
import imageio
import logging
import traceback

from celery import shared_task
from django.conf import settings
from django.core.exceptions import BadRequest
from frontend import cache
from frontend.utils import (
    to_int,
    TarArchive,
    ZipArchive,
    resize_image,
    check_extension,
)
from frontend.models import (
    Title,
    Source,
    Creator,
    Resource,
    Collection,
    CustomUser,
)

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def renew_cache(renew=True):
    for name in dir(cache):
        item = getattr(cache, name)

        if callable(item):
            try:
                item(renew=renew)
            except:
                pass


@shared_task(bind=True)
def upload_collection(self, args):
    image_path = args.get('image_path')
    entries = args.get('entries')
    user_id = args.get('user_id')
    access = args.get('access', 'R')
    
    if access.lower() == 'open':
        access = 'O'
    elif access.lower() == 'pending':
        access = 'P'
    elif access.lower() == 'restricted':
        access = 'R'

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        raise BadRequest('unknown_user')

    if not args.get('collection_name'):
        raise BadRequest('collection_name_is_required')

    collection = Collection.objects.filter(
            user=user,
            name=args['collection_name'],
        ) \
        .first()

    if collection is None:
        if not args.get('collection_id'):
            raise BadRequest('collection_id_is_required')

        collection = Collection.objects.create(
            user=user,
            hash_id=args['collection_id'],
            name=args['collection_name'],
            access=access,
            status='U',
            progress=0.0,
        )
        collection.save()

    if check_extension(image_path, ['.zip']):
        archive = ZipArchive(image_path)
    elif check_extension(image_path, [
        '.tar',
        '.tar.gz',
        '.tar.bz2',
        '.tar.xz',
    ]):
        archive = TarArchive(image_path)

    count, resources = 0, []
    args = {'ignore_conflicts': True}

    with archive as file_obj:
        for entry in entries:
            try:
                img_obj = file_obj.read(entry['path'])
                image = imageio.imread(img_obj)
            except:
                continue

            hash_id = uuid.uuid4().hex
            image_output_file = None

            for resolution in settings.IMAGE_RESOLUTIONS:
                min_size = resolution.get('min_size', 200)
                suffix = resolution.get('suffix', '')

                resized_image = resize_image(image, min_dim=min_size)

                if settings.IS_DEV:
                    image_output_dir = os.path.join(
                        settings.UPLOAD_ROOT,
                        hash_id[0:2],
                        hash_id[2:4],
                    )
                else:
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

                logger.info(f'Created image {image_output_file}')
                imageio.imwrite(image_output_file, resized_image)

            if image_output_file is not None:
                resource = Resource.objects.create(
                    collection=collection,
                    hash_id=hash_id,
                )

                if entry.get('creator'):
                    creator = Creator.objects.filter(name=entry['creator_name']).first()

                    if creator is None:
                        creator = Creator.objects.create(name=entry['creator_name'])
                        creator.save()

                    resource.creators.add(creator)

                if entry.get('title_name'):
                    title = Title.objects.filter(name=entry['title_name']).first()

                    if title is None:
                        title = Title.objects.create(name=entry['title_name'])
                        title.save()
                        
                    resource.titles.add(title)

                if entry.get('source_name'):
                    source = Source.objects.filter(name=entry['source_name']).first()

                    if source is None:
                        source = Source.objects.create(name=entry['source_name'])

                        if entry.get('entry_url'):
                            source.url = entry['entry_url']

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

                resources.append(resource)
                count += 1

                if len(resources) > 100:
                    try:
                        Resource.objects.bulk_create(resources, **args)
                    except Exception as error:
                        logger.error(traceback.format_exc())

                    resources = []

            if count % 10 == 0:
                collection.progress = count / len(entries)
                collection.save()

        if resources:
            try:
                Resource.objects.bulk_create(resources, **args)
            except Exception as error:
                logger.error(traceback.format_exc())

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
