import os
import csv

from frontend.models import *
from datetime import datetime
from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def toInt(x):
    if isinstance(x, str):
        try:
            return int(float(x))
        except:
            pass

    return None


def toScore(x):
    x = toInt(x)

    if x:
        return x

    return 0


def isURL(x):
    try:
        validate = URLValidator()
        validate(x)

        return True
    except ValidationError:
        pass

    return False


def toURL(x):
    if isURL(x):
        return x

    return ''


def toDatetime(x):
    if x:
        if '.' not in x: x += '.0'
        frt = '%Y-%m-%d %H:%M:%S.%f'

        return datetime.strptime(x, frt)

    return timezone.now()


class Create:
    def process(self):
        args = {'ignore_conflicts': True}

        with open(self.file_path, 'r') as csv_file:
            data = csv.reader(csv_file)
            processed_rows = []
            columns = next(data)

            for row in data:
                obj = self.convert(dict(zip(columns, row)))

                if obj is not None:
                    processed_rows.append(obj)

                if len(processed_rows) > 5000:
                    self.obj.objects.bulk_create(processed_rows, **args)
                    processed_rows = []

            if processed_rows:
                self.obj.objects.bulk_create(processed_rows, **args)


class CreateUser(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'user.csv')
        self.obj = CustomUser

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            username = row.get('username'),
            email = row.get('email'),
            password = row.get('password'),
            first_name = row.get('first_name'),
            last_name = row.get('last_name'),
            date_joined = toDatetime(row.get('date_joined')),
        )


class CreateSource(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'source.csv')
        self.obj = Source

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            name = row.get('name'),
            url = toURL(row.get('url')),
        )


class CreateCreator(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'creator.csv')
        self.obj = Creator

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            name = row.get('name'),
        )


class CreateResource(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'resource.csv')
        self.obj = Resource

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            hash_id = row.get('hash_id'),
            source_id = toInt(row.get('source_id')),
            created_start = row.get('created_start'),
            created_end = row.get('created_end'),
            location = row.get('location'),
            institution = row.get('institution'),
            origin = toURL(row.get('origin')),
            enabled = row.get('enabled'),
        )


class CreateTitle(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'title.csv')
        self.obj = Title

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            name = row.get('name'),
            language = row.get('language'),
        )

        
class CreateGametype(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'gametype.csv')
        self.obj = Gametype

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            name = row.get('name'),
        )


class CreateOpponentType(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'opponent_type.csv')
        self.obj = OpponentType

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            name = row.get('name'),
        )


class CreateTabooType(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'taboo_type.csv')
        self.obj = TabooType

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            name = row.get('name'),
        )


class CreateGamesession(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'gamesession.csv')
        self.obj = Gamesession

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            gametype_id = toInt(row.get('gametype_id')),
            created = toDatetime(row.get('created')),
            user_id = toInt(row.get('user_id')),
            rounds = toInt(row.get('rounds')),
            round_duration = toInt(row.get('round_duration')),
        )


class CreateGameround(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'gameround.csv')
        self.obj = Gameround

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            user_id = toInt(row.get('user_id')),
            gamesession_id = toInt(row.get('gamesession_id')),
            resource_id=toInt(row.get('resource_id')),
            created = toDatetime(row.get('created')),
            score = toScore(row.get('score')),
            # opponent_type_id=toInt(row.get('opponent_type_id')),
            # taboo_type_id=toInt(row.get('taboo_type_id'))
        )


class CreateTag(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'tag.csv')
        self.obj = Tag

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            name = row.get('name'),
            language = row.get('language'),
        )


class CreateTagging(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'tagging.csv')
        self.obj = Tagging

    def convert(self, row):
        return self.obj(
            id = toInt(row.get('id')),
            created = toDatetime(row.get('created')),
            user_id = toInt(row.get('user_id')),
            gameround_id = toInt(row.get('gameround_id')),
            resource_id = toInt(row.get('resource_id')),
            tag_id = toInt(row.get('tag_id')),
            score = toScore(row.get('score')),
        )


class CreateResourceTitle(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'title.csv')
        self.obj = Resource.titles.through

    def convert(self, row):
        if row.get('resource_id'):
            return self.obj(
                resource_id = toInt(row.get('resource_id')),
                title_id = toInt(row.get('id')),
            )


class CreateResourceCreator(Create):
    def __init__(self, folder_path):
        self.file_path = os.path.join(folder_path, 'resource.csv')
        self.obj = Resource.creators.through

    def convert(self, row):
        if row.get('creator_id'):
            return self.obj(
                resource_id = toInt(row.get('id')),
                creator_id = toInt(row.get('creator_id')),
            )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--format', choices=['csv'])
        parser.add_argument('--input', type=str, default='/dump')

    def handle(self, *args, **options):
        start_time = timezone.now()

        if os.path.isdir(options['input']):
            if options['format'] == 'csv':
                CreateUser(options['input']).process()
                CreateSource(options['input']).process()
                CreateCreator(options['input']).process()
                CreateResource(options['input']).process()
                CreateTitle(options['input']).process()
                CreateGametype(options['input']).process()
                # CreateOpponentType(options['input']).process()
                # CreateTabooType(options['input']).process()
                CreateGamesession(options['input']).process()
                CreateGameround(options['input']).process()
                CreateTag(options['input']).process()
                CreateTagging(options['input']).process()

                CreateResourceTitle(options['input']).process()
                CreateResourceCreator(options['input']).process()
        else:
            raise CommandError('Input is not a directory.')

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Import took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
