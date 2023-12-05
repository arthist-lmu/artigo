import os
import re
import sys
import uuid
import asyncio
import zipfile
import requests
import traceback

import xml.etree.ElementTree as ET

from django.conf import settings
from aiohttp import ClientSession
from tqdm import tqdm
from tqdm.asyncio import tqdm as atqdm
from frontend.tasks import upload_collection


class AsyncScraper:
    def __init__(self, urls, **kwargs):
        self.urls, self.store = set(urls), set()
        self.args, self.results = kwargs, []

        self.done = set()

        self.semaphore = asyncio.Semaphore(
            value=self.args.get('n', 10),
        )

    def run(self):
        self.n_iter = 0

        while self.urls and self.urls != self.store:
            self.urls -= self.done  
            self.store = self.urls
            self.n_iter += 1

            results = self.init_chunk()
            self.results.extend(results)

        return [x for x in self.results if x]

    def init_chunk(self):
        future = asyncio.ensure_future(self.run_chunk())
        loop = asyncio.get_event_loop()

        return loop.run_until_complete(future)

    async def run_chunk(self):
        tasks = []

        async with ClientSession() as session:
            for url in self.urls:
                task = self.bound_fetch(url, session)
                tasks.append(asyncio.ensure_future(task))

            self.urls = set()

            tasks = atqdm.as_completed(
                tasks, leave=False, disable=False,
                desc=f'Iteration {self.n_iter}',
            )

            return [await task for task in tasks]

    async def bound_fetch(self, url, session):
        async with self.semaphore:
           return await self.fetch(url, session)

    async def fetch(self, url, session):
        try:
            async with session.get(url) as response:
                html = await response.read()
                result = self.extract(url, html)
                self.done.add(url)

                return result
        except:
            traceback.print_exc()
            self.urls.add(url)


class BelvedereScraper(AsyncScraper):
    mapping = {
        'Object': 'file',
        'Title': 'title_name_de',
        'Creator': 'creator_name',
        'Location': 'location',
        'Publisher': 'institution',
        'IsShownAt': 'origin',
    }

    def extract(self, url, html):
        records = ET.fromstring(html)

        entries = []

        for record in records:
            entry = {}

            for child in record:
                if child.tag in self.mapping:
                    entry[self.mapping[child.tag]] = child.text
                elif child.tag == 'CreationDate':
                    try:
                        values = re.findall(r'[0-9]{4}', child.text)

                        entry['created_start'] = values[0]
                        entry['created_end'] = values[1]
                    except:
                        pass
                elif child.tag == 'Collection':
                    values = child.text.split('##')

                    if len(values) > 1:
                        entry['tags_name_de'] = values[0].strip().split(' | ')
                        entry['tags_name_en'] = values[1].strip().split(' | ')
                elif child.tag == 'ExpertTags':
                    if not entry.get('tags_name_de'):
                        entry['tags_name_de'] = []

                    tags = list(set(tag.text for tag in child))
                    entry['tags_name_de'].extend(tags)

            if entry:
                entries.append(entry)

        return entries


def download_images(entries, collection_id):
    output_dir = os.path.join(
        settings.MEDIA_ROOT,
        collection_id[0:2],
        collection_id[2:4],
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_path = os.path.join(output_dir, f'{collection_id}.zip')

    with zipfile.ZipFile(image_path, 'w') as file_obj:
        for entry in tqdm(entries):
            entry['path'] = f'{entry["file"].rsplit("/", 2)[1]}.jpg'
            file_path = os.path.join(output_dir, entry['path'])

            with open(file_path, 'wb') as img_obj:
                img_data = requests.get(entry['file']).content
                img_obj.write(img_data)

            file_obj.write(file_path, entry['path'])
            os.remove(file_path)

    return entries, image_path


def import_data(options):
    url = 'https://sammlung.belvedere.at/objects/xmlkultur?'
    url += 'filter=opencontentprogram%3Atrue&page={}'

    urls = [url.format(page) for page in range(1, 56)]

    entries = BelvedereScraper(urls, n=5).run()
    entries = [entry for x in entries for entry in x]

    collection_id = uuid.uuid4().hex
    collection_title = {
        'de': 'Österreichische Galerie Belvedere',
        'en': 'Austrian Gallery Belvedere',
    }

    entries, image_path = download_images(entries, collection_id)

    upload_collection.apply_async(
        (
            {
                'collection_title': collection_title,
                'collection_id': collection_id,
                'image_path': image_path,
                'entries': entries,
                'user_id': options['user_id'],
                'lang': options.get('lang', 'de'),
            },
        )
    )
