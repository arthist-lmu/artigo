import os
import re
import logging
import traceback

from collections import defaultdict
from django.utils import timezone
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-i', '--input', type=str, default='/dump')
        parser.add_argument('--limit', type=int, default=2)

    def handle(self, *args, **options):
        start_time = timezone.now()

        files = defaultdict(list)

        for file in sorted(
            os.scandir(options['input']),
            key=lambda file: file.stat().st_mtime,
            reverse=True,
        ):
            if file.name.startswith('os-dump'):
                file_path = os.path.join(options['input'], file.name)
                file_key = re.split('-|_', file.name)[-2]

                if len(files[file_key]) < options['limit']:
                    files[file_key].append(file_path)
                else:
                    os.remove(file_path)

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Delete took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
