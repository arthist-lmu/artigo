import os

from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from frontend.utils import reset_cursor
from .data import (
    import_data_legacy,
    import_data_belvedere,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--format', choices=['csv'], default='csv')
        parser.add_argument('--data', choices=['legacy', 'belvedere'])
        parser.add_argument('--input', type=str, default='/dump')
        parser.add_argument('--clean', action='store_true')
        parser.add_argument('--user_id', type=int, nargs='?')

    def handle(self, *args, **options):
        start_time = timezone.now()

        if not os.path.isdir(options['input']):
            raise CommandError('Input is not a directory.')

        if options['data'] == 'legacy':
            import_data_legacy(options)
        elif options['data'] == 'belvedere':
            import_data_belvedere(options)
        else:
            raise CommandError('Data must be set.')

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Import took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))

        reset_cursor()

        txt = 'Successfully reset AutoFields.'
        self.stdout.write(self.style.SUCCESS(txt))
