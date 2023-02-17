import os
import json
import logging
import traceback

from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from frontend.models import Resource
from frontend.serializers import ResourceWithTaggingsSerializer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--format', choices=['jsonl'], default='jsonl')
        parser.add_argument('-o', '--output', type=str, default='/dump')
        parser.add_argument('--size', type=int, default=1000)

    def handle(self, *args, **options):
        start_time = timezone.now()

        if os.path.isdir(options['output']):
            qs = Resource.objects.prefetch_related('taggings')

            dump_time = timezone.now().strftime('%Y%m%d%H%M%S')
            file_path = f"{options['output']}/os-dump_{dump_time}.{options['format']}"

            with open(file_path, 'w', encoding='utf-8') as file_obj:
                for i in range(0, qs.count(), options['size']):
                    chunk = qs.all()[i:(i + options['size'])]
                    chunk = ResourceWithTaggingsSerializer(chunk, many=True)

                    if options['format'] == 'jsonl':
                        try:
                            for resource in chunk.data:
                                file_obj.write(f"{json.dumps(resource)}\n")
                        except Exception as error:
                            logger.error(traceback.format_exc())
        else:
            raise CommandError('Output is not a directory.')

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Export took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
