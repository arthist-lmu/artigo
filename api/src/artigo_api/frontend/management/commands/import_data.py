import os
import csv
import sys
import pytz
import uuid
import hashlib

from tqdm import tqdm
from frontend.models import *
from datetime import datetime
from django.db import connection
from django.apps import apps
from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from django.core.management.color import no_style
from frontend.utils import to_url, to_int

MODEL_MAPPING = {}


def to_score(x, default=0):
    x = to_int(x, default=None)

    return x if x else default


def to_datetime(x):
    if x:
        if '.' not in x: x += '.0'  # to proper date format

        x = datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f') \
            .replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

    return timezone.now()


class Create:
    def process(self):
        args = {'ignore_conflicts': True}

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as csv_file:
                data = csv.reader(csv_file)
                processed_rows = []
                columns = next(data)

                for row in tqdm(data, f'Import {self.name}', file=sys.stdout):
                    model = self.convert(dict(zip(columns, row)))

                    if model is not None:
                        processed_rows.append(model)

                    if len(processed_rows) > 5000:
                        try:
                            self.model.objects.bulk_create(processed_rows, **args)
                        except Exception as error:
                            print(error)

                        processed_rows = []

                if processed_rows:
                    try:
                        self.model.objects.bulk_create(processed_rows, **args)
                    except Exception as error:
                        print(error)
        else:
            sys.stdout(f'{self.file_path} does not exist.')


class CreateUser(Create):
    name = 'User'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'user.csv')
        self.model = CustomUser

    def convert(self, row):
        if not row.get('username'):
            row['username'] = uuid.uuid4().hex[:15]

        if not row.get('email'):
            row['email'] = f"{row['username']}@artigo.org"

        if not row.get('password'):
            password = uuid.uuid4().hex.encode('utf-8')
            row['password'] = hashlib.sha256(password).hexdigest()

        return self.model(
            id = to_int(row.get('id'), default=None),
            username = row.get('username'),
            email = row.get('email'),
            password = row.get('password'),
            first_name = row.get('first_name'),
            last_name = row.get('last_name'),
            date_joined = to_datetime(row.get('date_joined')),
            is_anonymous = row.get('is_anonymous') == 'True',
        )


class CreateSource(Create):
    name = 'Source'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'source.csv')
        self.model = Source

    def convert(self, row):
        return self.model(
            id = to_int(row.get('id'), default=None),
            name = row.get('name'),
            url = to_url(row.get('url'), default=''),
        )


class CreateCreator(Create):
    name = 'Creator'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'creator.csv')
        self.model = Creator

    def convert(self, row):
        return self.model(
            id = to_int(row.get('id'), default=None),
            name = row.get('name'),
        )


class CreateResource(Create):
    name = 'Resource'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'resource.csv')
        self.model = Resource

    def convert(self, row):
        return self.model(
            id = to_int(row.get('id'), default=None),
            hash_id = row.get('hash_id'),
            source_id = to_int(row.get('source_id'), default=None),
            created_start = to_int(row.get('created_start'), default=None),
            created_end = to_int(row.get('created_end'), default=None),
            location = row.get('location'),
            institution = row.get('institution'),
            origin = to_url(row.get('origin'), default=''),
            enabled = row.get('enabled'),
        )


class CreateTitle(Create):
    name = 'Title'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'title.csv')
        self.model = Title

    def convert(self, row):
        return self.model(
            id = to_int(row.get('id'), default=None),
            name = row.get('name'),
            language = row.get('language'),
        )


class CreateGamesession(Create):
    name = 'Gamesession'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'gamesession.csv')
        self.model = Gamesession

    def convert(self, row):
        model = self.model(
            id = to_int(row.get('id'), default=None),
            created = to_datetime(row.get('created')),
            user_id = to_int(row.get('user_id'), default=None),
            rounds = to_int(row.get('rounds'), default=None),
            round_duration = to_int(row.get('round_duration'), default=None),
        )

        if row.get('game_type'):
            if not row['game_type'] in MODEL_MAPPING:
                MODEL_MAPPING[row['game_type']], _ = GameType.objects \
                    .get_or_create(name=row['game_type'])
                MODEL_MAPPING[row['game_type']].save()

            model.game_type = MODEL_MAPPING[row['game_type']]

        return model


class CreateGameround(Create):
    name = 'Gameround'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'gameround.csv')
        self.model = Gameround

    def convert(self, row):
        model = self.model(
            id = to_int(row.get('id'), default=None),
            user_id = to_int(row.get('user_id'), default=None),
            gamesession_id = to_int(row.get('gamesession_id'), default=None),
            resource_id = to_int(row.get('resource_id'), default=None),
            created = to_datetime(row.get('created')),
            score = to_score(row.get('score')),
        )

        if row.get('opponent_type'):
            if not row['opponent_type'] in MODEL_MAPPING:
                MODEL_MAPPING[row['opponent_type']], _ = OpponentType.objects \
                    .get_or_create(name=row['opponent_type'])
                MODEL_MAPPING[row['opponent_type']].save()

            model.opponent_type = MODEL_MAPPING[row['opponent_type']]

        if row.get('taboo_type'):
            if not row['taboo_type'] in MODEL_MAPPING:
                MODEL_MAPPING[row['taboo_type']], _ = TabooType.objects \
                    .get_or_create(name=row['taboo_type'])
                MODEL_MAPPING[row['taboo_type']].save()

            model.taboo_type = MODEL_MAPPING[row['taboo_type']]

        return model


class CreateTag(Create):
    name = 'Tag'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'tag.csv')
        self.model = Tag

    def convert(self, row):
        return self.model(
            id = to_int(row.get('id'), default=None),
            name = row.get('name'),
            language = row.get('language'),
        )


class CreateTagging(Create):
    name = 'Tagging'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'tagging.csv')
        self.model = UserTagging

    def convert(self, row):
        return self.model(
            id = to_int(row.get('id'), default=None),
            created = to_datetime(row.get('created')),
            user_id = to_int(row.get('user_id'), default=None),
            gameround_id = to_int(row.get('gameround_id'), default=None),
            resource_id = to_int(row.get('resource_id'), default=None),
            tag_id = to_int(row.get('tag_id'), default=None),
            uploaded = not row.get('created'),
            score = to_score(row.get('score')),
        )


class CreateResourceTitle(Create):
    name = 'Resource title'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'title.csv')
        self.model = Resource.titles.through

    def convert(self, row):
        if row.get('resource_id'):
            return self.model(
                resource_id = to_int(row.get('resource_id'), default=None),
                title_id = to_int(row.get('id'), default=None),
            )


class CreateResourceCreator(Create):
    name = 'Resource creator'

    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'resource.csv')
        self.model = Resource.creators.through

    def convert(self, row):
        if row.get('creator_id'):
            return self.model(
                resource_id = to_int(row.get('id'), default=None),
                creator_id = to_int(row.get('creator_id'), default=None),
            )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--format', choices=['csv'], default='csv')
        parser.add_argument('--input', type=str, default='/dump')

    def handle(self, *args, **options):
        start_time = timezone.now()

        if not os.path.isdir(options['input']):
            raise CommandError('Input is not a directory.')

        if options['format'] == 'csv':
            CreateUser(options['input']).process()
            CreateSource(options['input']).process()
            CreateCreator(options['input']).process()
            CreateResource(options['input']).process()
            CreateTitle(options['input']).process()
            CreateGamesession(options['input']).process()
            CreateGameround(options['input']).process()
            CreateTag(options['input']).process()
            CreateTagging(options['input']).process()
            CreateResourceTitle(options['input']).process()
            CreateResourceCreator(options['input']).process()

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Import took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))

        configs = [apps.get_app_config(x) for x in ['frontend']]
        models = [list(config.get_models()) for config in configs]

        with connection.cursor() as cursor:
            for model in models:
                for sql in connection.ops.sequence_reset_sql(no_style(), model):
                    cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS('Successfully reset AutoFields.'))
