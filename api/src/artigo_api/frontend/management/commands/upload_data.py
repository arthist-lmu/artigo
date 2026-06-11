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
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
        })

        self.deposition = self.get_deposition(query)
        self.draft_id = self.get_draft_id()

    def __repr__(self):
        return str(self.deposition['id'])

    def _raise_for_status(self, response):
        try:
            response.raise_for_status()
        except HTTPError as exc:
            try:
                details = response.json()
            except ValueError:
                details = response.text
            raise HTTPError(
                f"{response.status_code} error: {details}",
                response=response,
            ) from exc

    def _request(self, method, url, **kwargs):
        response = self.session.request(method, url, **kwargs)
        self._raise_for_status(response)
        return response

    def refresh(self):
        self.deposition = self._request(
            "GET",
            f"{self.url}/{self.deposition['id']}",
        ).json()
        self.draft_id = self.get_draft_id()
        return self.deposition

    def get_deposition(self, query):
        response = self._request(
            "GET",
            self.url,
            params={
                "q": query,
                "sort": "mostrecent",
                "size": 1,
            },
        )

        results = response.json()
        if not results:
            raise LookupError(f"No deposition found")

        return results[0]

    def get_draft_id(self):
        latest_draft = self.deposition.get("links", {}).get("latest_draft")
        if latest_draft:
            return latest_draft.rsplit("/", 1)[-1]
        return None

    def get_version(self, update=False):
        version = self.deposition.get("metadata", {}).get("version", "0.0.0")

        if update:
            prefix, suffix = version.rsplit(".", 1)
            version = f"{prefix}.{int(suffix) + 1}"

        return version

    def new_version(self):
        old_version = self.get_version(update=True)

        response = self._request(
            "POST",
            f"{self.url}/{self.deposition['id']}/actions/newversion",
        )

        original = response.json()
        latest_draft_url = original.get("links", {}).get("latest_draft")
        if not latest_draft_url:
            raise RuntimeError("Zenodo did not return links.latest_draft")

        draft = self._request("GET", latest_draft_url).json()
        draft_id = draft["id"]

        metadata = {
            **draft.get("metadata", {}),
            "version": old_version,
            "publication_date": date.today().isoformat(),
        }

        self.deposition = self._request(
            "PUT",
            f"{self.url}/{draft_id}",
            json={"metadata": metadata},
            headers={
                **self.session.headers,
                "Content-Type": "application/json",
            },
        ).json()

        self.draft_id = self.get_draft_id()
        return self.deposition



        response = requests.post(
            f'{self.url}/{self.deposition["id"]}/actions/newversion',
            params=self.params,
        )
        response.raise_for_status()

        version = self.get_version(update=True)
        publication_date = datetime.today().strftime('%Y-%m-%d')

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
            'version': version,
            'publication_date': publication_date,
        }

        for key in (
            'owner',
            'id',
            'submitted',
            'created',
            'state',
            'links',
            'title',
            'conceptrecid',
            'record_id',
            'conceptdoi',
            'modified',
        ):
            data.pop(key)

        response = requests.put(
            f'{self.url}/{self.draft_id}',
            params=self.params,
            json=data,
        )
        response.raise_for_status()

        self.deposition = response.json()

    def publish(self):
        response = self._request(
            "POST",
            f"{self.url}/{self.deposition['id']}/actions/publish",
        )

        self.deposition = response.json()
        self.draft_id = self.get_draft_id()
        return self.deposition

    def list_files(self):
        response = self._request(
            "GET",
            f"{self.url}/{self.deposition['id']}/files",
        )
        return response.json()

    def delete_files(self, file_name=None):
        for file in self.list_files():
            name = file.get("filename") or file.get("name")
            if file_name is None or file_name in name:
                file_id = file["id"]
                self._request(
                    "DELETE",
                    f"{self.url}/{self.deposition['id']}/files/{file_id}",
                )

        self.refresh()

    def upload_file(self, data, file_path):
        bucket_url = self.deposition.get("links", {}).get("bucket")
        if not bucket_url:
            raise RuntimeError()

        filename = str(file_path).replace("\\", "/").lstrip("/")

        response = self._request(
            "PUT",
            f"{bucket_url.rstrip('/')}/{filename}",
            data=data,
        )

        self.refresh()

        return response.json()


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
        parser.add_argument('--zenodo', choices=['prepare', 'publish'])

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

        if options['zenodo'] in ('prepare', 'publish'):
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

            if options['zenodo'] == 'publish':
                zenodo.publish()

        dump_path = get_latest_dump(options['dump_input'], raw=True)

        if options['zenodo'] in ('prepare', 'publish'):
            zenodo = Zenodo(
                query='ARTigo +Raw',
                access_token=settings.ZENODO_ACCESS_TOKEN,
            )

            zenodo.new_version()
            zenodo.delete_files()

            with open(dump_path, 'r', encoding='latin1') as file_obj:
                zenodo.upload_file(file_obj, 'data.jsonl')

            if options['zenodo'] == 'publish':
                zenodo.publish()

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Upload took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
