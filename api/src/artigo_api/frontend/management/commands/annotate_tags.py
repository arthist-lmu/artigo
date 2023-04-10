import json
import requests

from tqdm import tqdm
from requests.exceptions import ConnectionError
from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from frontend.models import Tag


class WiktionarySearch:
    def __init__(self, tag):
        self.tag = tag

    def get(self, session, lang='en'):
        response = session.get(
            f'https://{lang}.wiktionary.org/w/api.php',
            params={
                'action': 'query',
                'list': 'search',
                'format': 'json',
                'srsearch': self.tag['name'],
            },
        )

        self.data = response.json()

    def check(self):
        if self.data.get('query', {}).get('search'):
            for page in self.data['query']['search']:
                if self.tag['name'].lower() in page['snippet'].lower():
                    tag = {
                        'name': page['title'],
                        'language': self.tag['language'],
                    }

                    return tag


class WiktionaryCategory:
    langs = {
        'de': 'german',
        'fr': 'french', 
        'en': 'english',
    }

    def __init__(self, tag):
        self.tag = tag

        self.color_term = False
        self.in_dictionary = False
        self.technical_term = False

    def get(self, session, lang='en'):
        titles = f'{self.tag["name"].lower()}'
        titles += f'|{self.tag["name"].capitalize()}'

        response = session.get(
            f'https://{lang}.wiktionary.org/w/api.php',
            params={
                'action': 'query',
                'prop': 'categories',
                'format': 'json',
                'titles': titles,
                'cllimit': 500,
            },
        )

        self.data = response.json()

    def check(self):
        if self.data.get('query', {}).get('pages'):
            for page in self.data['query']['pages'].values():
                for category in page.get('categories', []):
                    title = category.get('title', '').lower()
                    title = title.split(':', 1)[-1].strip()

                    if title.startswith((
                        self.tag['language'],
                        self.langs.get(self.tag['language']),
                    )):
                        self.in_dictionary = True

                        if 'colors' in title:
                            self.color_term = True
                        elif title.endswith('art'):
                            self.technical_term = True

                    if title.endswith('names'):
                        self.in_dictionary = True


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true')
        parser.add_argument('--continue', action='store_true')

    def handle(self, *args, **options):
        start_time = timezone.now()

        if options['reset']:
            tags = Tag.objects.exclude(in_dictionary__isnull=True)

            for tag in tqdm(tags.all().iterator()):
                tag.color_term = None
                tag.in_dictionary = None
                tag.technical_term = None
                tag.save()
        else:
            tags = Tag.objects

            if options['continue']:
                tags = tags.filter(in_dictionary__isnull=True)

            with requests.Session() as session:
                for tag in tqdm(tags.all().iterator()):
                    try:
                        category = WiktionaryCategory(tag.__dict__)

                        for lang in ('en', 'de'):
                            search = WiktionarySearch(tag.__dict__)
                            search.get(session, lang=lang)
                            query = search.check()

                            if query is not None:
                                category = WiktionaryCategory(query)
                                category.get(session, lang=lang)
                                category.check()

                            if category.in_dictionary:
                                break

                        tag.color_term = category.color_term
                        tag.in_dictionary = category.in_dictionary
                        tag.technical_term = category.technical_term
                        tag.save()
                    except ConnectionError:
                        continue

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Annotation took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
