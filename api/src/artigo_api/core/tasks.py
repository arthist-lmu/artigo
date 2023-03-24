import os
import json
import logging
import requests

from datetime import datetime
from celery import shared_task
from django.conf import settings
from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def export_data(folder='/dump'):
    call_command('export_data', format='jsonl', output=folder)


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

    def delete_file(self, file_name='data'):
        for file in self.deposition['files']:
            if file['filename'].startswith(file_name):
                response = requests.delete(
                    f'{self.url}/{self.deposition["id"]}/files/{file["id"]}',
                    params=self.params,
                )
                response.raise_for_status()

    def upload_file(self, data, file_name='data'):
        url = self.deposition['links']['bucket']

        response = requests.put(
            f'{url}/{file_name}.jsonl',
            params=self.params,
            data=data,
        )
        response.raise_for_status()

        return response.json()


@shared_task(ignore_result=True)
def upload_data(folder='/dump'):
    zenodo = Zenodo(
        query='ARTigo: Social Image Tagging',
        access_token=settings.ZENODO_ACCESS_TOKEN,
    )

    zenodo.new_version()
    zenodo.delete_file()

    for file in sorted(
        os.scandir(folder),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    ):
        if file.name.startswith('os-dump_'):
            file_path = os.path.join(folder, file.name)

            with open(file_path, 'r') as file_obj:
                zenodo.upload_file(file_obj)

            break

    zenodo.publish()
