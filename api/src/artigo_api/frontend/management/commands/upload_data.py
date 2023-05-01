import os
import json
import zipfile
import logging
import requests

from datetime import datetime
from requests.exceptions import HTTPError
from django.conf import settings
from django.utils import timezone
from django.core.management import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Zenodo:
    url = 'https://zenodo.org/api/deposit/depositions'

    def __init__(self, query, access_token):
        self.params = {'access_token': access_token}

        self.deposition = self.get_deposition(query)
        self.draft_id = self.get_draft_id()

    def __repr__(self):
        return str(self.deposition['id'])

    def get_deposition(self, query):
        response = requests.get(
            self.url,
            params={
                'q': query,
                'sort': 'mostrecent',
                'size': 1,
                **self.params,
            },
        )
        response.raise_for_status()

        return response.json()[0]

    def get_draft_id(self):
        if self.deposition['links'].get('latest_draft'):
            url = self.deposition['links']['latest_draft']

            return url.rsplit('/', 1)[-1]

    def get_version(self, update=False):
        version = self.deposition['metadata']['version']

        if update:
            prefix, suffix = version.rsplit('.', 1)
            version = f'{prefix}.{int(suffix) + 1}'

        return version

    def new_version(self):
        response = requests.post(
            f'{self.url}/{self.deposition["id"]}/actions/newversion',
            params=self.params,
        )
        response.raise_for_status()

        self.deposition = response.json()
        self.draft_id = self.get_draft_id()

        response = requests.get(
            f'{self.url}/{self.draft_id}',
            params=self.params,
        )
        response.raise_for_status()

        data = response.json()
        data['metadata'] = {
            **data['metadata'],
            'version': self.get_version(update=True),
            'publication_date': datetime.today().strftime('%Y-%m-%d'),
        }

        response = requests.put(
            f'{self.url}/{self.draft_id}',
            params=self.params,
            json=data,
        )
        response.raise_for_status()

        self.deposition = response.json()

    def publish(self):
        response = requests.post(
            f'{self.url}/{self.deposition["id"]}/actions/publish',
            params=self.params,
        )
        response.raise_for_status()

        self.deposition = response.json()
        self.draft_id = self.get_draft_id()

    def delete_files(self, file_name=None):
        for file in self.deposition['files']:
            if file_name is None or file_name in file['filename']:
                response = requests.delete(
                    f'{self.url}/{self.deposition["id"]}/files/{file["id"]}',
                    params=self.params,
                )
                response.raise_for_status()

    def upload_file(self, data, file_path):
        url = self.deposition['links']['bucket']

        try:
            response = requests.put(
                f'{url}/{file_path}',
                params=self.params,
                data=data,
            )
            response.raise_for_status()
        except HTTPError:
            data = response.json()

            raise HTTPError(f'{response.status_code} Client Error: {data}')


def get_latest_dump(dump_folder, raw=False):
    dump_files = []

    for file in sorted(
        os.scandir(dump_folder),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    ):
        suffix = '-raw' if raw else ''

        if file.name.startswith(f'os-dump{suffix}_'):
            dump_files.append(file.name)

    return os.path.join(dump_folder, dump_files[0])


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--dump_input', type=str, default='/dump')
        parser.add_argument('--media_input', type=str, default='/media')
        parser.add_argument('--publish', action='store_true')

    def handle(self, *args, **options):
        start_time = timezone.now()

        if not os.path.isdir(options['dump_input']):
            raise CommandError('Dump input is not a directory.')

        if not os.path.isdir(options['media_input']):
            raise CommandError('Media input is not a directory.')

        dump_path = get_latest_dump(options['dump_input'], raw=False)
        media_path = os.path.join(options['dump_input'], 'media.zip')

        hash_ids = set()
        
        with open(dump_path, 'r') as file_obj:
            for line in file_obj:
                entry = json.loads(line)
                hash_ids.add(entry['hash_id'])
            
        with zipfile.ZipFile(media_path, mode='w') as archive:
            for path, _, files in os.walk(options['media_input']):
                for file in files:
                    if file.split('.', 1)[0] in hash_ids:
                        rel_path = os.path.relpath(path, options['media_input'])
                        
                        archive.write(
                            os.path.join(path, file),
                            os.path.join(rel_path, file),
                            compress_type=zipfile.ZIP_DEFLATED,
                        )

        if options['publish']:
            zenodo = Zenodo(
                query='ARTigo +Aggregated',
                access_token=settings.ZENODO_ACCESS_TOKEN,
            )

            zenodo.new_version()
            zenodo.delete_files()

            with open(dump_path, 'r') as file_obj:
                zenodo.upload_file(file_obj, 'data.jsonl')
                    
            with open(media_path, 'rb') as file_obj:
                zenodo.upload_file(file_obj, 'media.zip')

            zenodo.publish()

        dump_path = get_latest_dump(options['dump_input'], raw=True)

        if options['publish']:
            zenodo = Zenodo(
                query='ARTigo +Raw',
                access_token=settings.ZENODO_ACCESS_TOKEN,
            )

            zenodo.new_version()
            zenodo.delete_files()

            with open(dump_path, 'r', encoding='latin1') as file_obj:
                zenodo.upload_file(file_obj, 'data.jsonl')

            zenodo.publish()

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Upload took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
