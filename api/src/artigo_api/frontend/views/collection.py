import os
import io
import csv
import json
import uuid
import logging
import zipfile
import tarfile
import traceback

from pathlib import Path
from django.conf import settings
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema
from frontend.tasks import upload_collection
from frontend.utils import (
    unflat_dict,
    download_file,
    check_extension,
)
from frontend.models import Collection, Resource

logger = logging.getLogger(__name__)


@extend_schema(methods=['POST'], exclude=True)
class CollectionAddView(APIView):
    mapping = {
        'title': 'title_name',
        'titel': 'title_name',
        'titles': 'title_name',
        'meta.title': 'title_name',
        'creator': 'creator_name',
        'künstler': 'creator_name',
        'artist': 'creator_name',
        'meta.creator': 'creator_name',
        'created_start': 'created_start',
        'entstehung_beginn': 'created_start',
        'entstehung': 'created_start',
        'date': 'created_start',
        'meta.created': 'created_start',
        'created_end': 'created_end',
        'entstehung_ende': 'created_end',
        'location': 'location',
        'standort': 'location',
        'institution': 'institution',
        'source': 'source_name',
        'quelle': 'source_name',
        'source_name': 'source_name',
        'source_url': 'source_url',
        'origin': 'origin',
        'origin_url': 'origin',
        'url': 'origin',
    }

    def parse_header(self, header):
        fields = {}

        for column in header:
            parsed_column = '_'.join(column.lower().split())

            if self.mapping.get(parsed_column):
                fields[column] = self.mapping[parsed_column]

        return fields

    def parse_row(self, row, fields):
        entry = {}

        for key, value in row.items():
            if fields.get(key):
                entry[fields[key]] = value

        if not entry.get('file'):
            entry['file'] = f'{entry["id"]}.jpg'

        return entry

    def parse_csv(self, file_path):
        entries = []

        with open(file_path, 'r', encoding='utf-8') as file_obj:
            reader = csv.DictReader(file_obj, delimiter=',')
            fields = self.parse_header(reader.fieldnames)

            if len(fields) == 0:
                return None

            for row in reader:
                entries.append(self.parse_row(row, fields))

        return entries

    def parse_json(self, file_path):
        entries = []

        with open(file_path, 'r', encoding='utf-8') as file_obj:
            for row in json.load(file_obj):
                fields, _ = self.parse_header(row.keys())

                if len(fields) > 0:
                    entries.append(self.parse_row(row, fields))

        if len(entries) == 0:
            return None

        return entries

    def parse_jsonl(self, file_path):
        entries = []

        with open(file_path, 'r', encoding='utf-8') as file_obj:
            for line in file_obj:
                row = json.loads(line)
                fields, _ = self.parse_header(row.keys())

                if len(fields) > 0:
                    entries.append(self.parse_row(row, fields))

        if len(entries) == 0:
            return None

        return entries

    def parse_metadata(self, file_path):
        if check_extension(file_path, extensions=['.csv']):
            return self.parse_csv(file_path)
        elif check_extension(file_path, extensions=['.json']):
            return self.parse_json(file_path)
        elif check_extension(file_path, extensions=['.jsonl']):
            return self.parse_jsonl(file_path)

    def parse_zip(self, file_path):
        entries = []

        try:
            file = zipfile.ZipFile(file_path, 'r')

            for name in file.namelist():
                if check_extension(name, extensions=[
                    '.gif',
                    '.png',
                    '.jpg',
                    '.jpeg',
                ]):
                    entries.append({
                        'path': name,
                        'name': Path(name).stem,
                    })
        except:
            pass

        if len(entries) == 0:
            return None

        return entries

    def parse_images(self, file_path):
        if check_extension(file_path, extensions=[
                '.zip',
                '.tar',
                '.tar.gz',
                '.tar.bz2',
                '.tar.xz',
            ]):
            return self.parse_zip(file_path)

    def merge(self, metadata_entries, image_entries):
        def path_sim(a, b):
            merged_paths = list(zip(a.parts[::-1], b.parts[::-1]))

            for i, x in enumerate(merged_paths):
                if x[0] != x[1]:
                    return i

            return len(merged_paths)

        entries = []

        for image_entry in image_entries:
            best_s, best_metadata = 0, None
            image_path = Path(image_entry['path'])

            for metadata_entry in metadata_entries:
                metadata_path = Path(metadata_entry['file'])
                s = path_sim(image_path, metadata_path)

                if s > best_s:
                    best_metadata = metadata_entry

            if best_metadata is None:
                continue

            entries.append({
                **best_metadata,
                **image_entry,
            })

        if len(entries) == 0:
            return None

        return entries

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        params = request.data

        if not params.get('name'):
            raise APIException('collection_name_is_required')

        collection_id = uuid.uuid4().hex
        collection_name = params['name']

        if len(collection_name) < 4:
            raise APIException('name_is_too_short')

        if len(collection_name) > 75:
            raise APIException('name_is_too_long')

        image_files = []

        for file in params.getlist('files'):
            if check_extension(file.name, extensions=[
                '.zip',
                '.tar',
                '.tar.gz',
                '.tar.bz2',
                '.tar.xz',
            ]):
                params['images'] = file
            elif check_extension(file.name, extensions=[
                '.csv',
                '.json',
                '.jsonl',
            ]):
                params['metadata'] = file
            elif check_extension(file.name, extensions=[
                '.gif',
                '.png',
                '.jpg',
                '.jpeg',
            ]):
                image_files.append(file)

        if not params.get('images'):
            if not image_files:
                raise APIException('image_file_is_required')

            params['images'] = io.BytesIO()

            with zipfile.ZipFile(params['images'], 'w') as file_obj:
                for file in image_files:
                    file_obj.writestr(file.name, file.read())

            params['images'].name = f'{collection_id}.zip'
            params['images'].size = params['images'].__sizeof__()

        if settings.DEBUG:
            output_dir = os.path.join(
                settings.UPLOAD_ROOT,
                collection_id[0:2],
                collection_id[2:4],
            )
        else:
            output_dir = os.path.join(
                settings.MEDIA_ROOT,
                collection_id[0:2],
                collection_id[2:4],
            )

        parsed_metadata = None

        if params.get('metadata'):
            metadata = download_file(
                output_name=collection_id,
                output_dir=output_dir,
                max_size=50 * 1024 * 1024,
                file=params['metadata'],
                extensions=(
                    '.csv',
                    '.json',
                    '.jsonl',
                ),
            )

            if metadata['status'] != 'ok':
                raise APIException(metadata['error']['type'])

            parsed_metadata = self.parse_metadata(metadata['path'])

            if parsed_metadata is None:
                raise APIException('no_valid_colnames_found')

        images = download_file(
            output_name=collection_id,
            output_dir=output_dir,
            max_size=50 * 1024 * 1024,
            file=params['images'],
            extensions=(
                '.zip',
                '.tar',
                '.tar.gz',
                '.tar.bz2',
                '.tar.xz',
            ),
        )

        if images['status'] != 'ok':
            raise APIException(images['error']['type'])

        parsed_images = self.parse_images(images['path'])

        if parsed_images is None:
            raise APIException('corrupt_archives_file')

        if parsed_metadata is not None:
            parsed_images = self.merge(
                parsed_metadata,
                parsed_images,
            )

            if parsed_images is None:
                raise APIException('no_matching_images_found')

        upload_collection.apply_async(
            (
                {
                    'collection_name': collection_name,
                    'collection_id': collection_id,
                    'image_path': str(images['path']),
                    'entries': list(map(unflat_dict, parsed_images)),
                    'user_id': request.user.id,
                },
            )
        )

        return Response()


@extend_schema(methods=['POST'], exclude=True)
class CollectionRemoveView(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        hash_id = request.data['params'].get('hash_id')

        if not hash_id:
            raise APIException('hash_id_is_required')

        collection = Collection.objects.get(hash_id=hash_id)
        resources = Resource.objects.filter(collection=collection)

        try:
            if resources.count():
                for resource in resources.values('hash_id'):
                    hash_id = resource['hash_id']

                    for resolution in settings.IMAGE_RESOLUTIONS:
                        suffix = resolution.get('suffix', '')

                        if settings.DEBUG:
                            file_path = os.path.join(
                                settings.UPLOAD_ROOT,
                                hash_id[0:2],
                                hash_id[2:4],
                                f'{hash_id}{suffix}.{settings.IMAGE_EXT}',
                            )
                        else:
                            file_path = os.path.join(
                                settings.MEDIA_ROOT,
                                hash_id[0:2],
                                hash_id[2:4],
                                f'{hash_id}{suffix}.{settings.IMAGE_EXT}',
                            )

                        if os.path.exists(file_path):
                            os.remove(file_path)

            collection.delete()

            return Response()
        except Exception as error:
            logger.error(traceback.format_exc())

        raise APIException('unknown_error')


@extend_schema(methods=['POST'], exclude=True)
class CollectionChangeView(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        params = request.data['params']

        if not params.get('hash_id'):
            raise APIException('hash_id_is_required')

        collection = Collection.objects.get(hash_id=params['hash_id'])

        if params.get('name'):
            collection_name = params['name']

            if len(collection_name) < 4:
                raise APIException('name_is_too_short')

            if len(collection_name) > 75:
                raise APIException('name_is_too_long')

            collection.name = collection_name

        if params.get('access'):
            collection_access = params['access']

            if collection_access.lower() == 'open':
                collection_access = 'O'
            elif collection_access.lower() == 'restricted':
                collection_access = 'R'

            try:
                collection.access = collection_access
            except:
                raise APIException('access_is_invalid')

        collection.save()

        return Response()
