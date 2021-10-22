import os
import json
import logging
import traceback

from frontend.serializers import ResourceWithTaggingsSerializer
from frontend.models import *
from django.db.models import Count
from django.utils import timezone
from django.core.management import BaseCommand, CommandError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--format', choices=['jsonl'])
        parser.add_argument('-o', '--output', type=str, default='/dump')

    def handle(self, *args, **options):
        start_time = timezone.now()

        if os.path.isdir(options['output']):
            if options['format'] == 'jsonl':
                qs = Resource.objects.prefetch_related('taggings')
                qs = ResourceWithTaggingsSerializer(qs.all(), many=True)

                dump_time = timezone.now().strftime('%Y%m%d%H%M%S')
                file_path = f"{options['output']}/os-dump_{dump_time}.jsonl"

                try:
                    with open(file_path, 'w', encoding='utf-8') as file_obj:
                        for resource in qs.data:
                            file_obj.write(json.dumps(resource) + '\n')
                except Exception as error:
                    logger.error(traceback.format_exc())
                    os.remove(file_path)
        else:
            raise CommandError('Output is not a directory.')

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Export took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))
