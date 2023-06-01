import os
import json
import logging
import traceback

from django.db.models import Q
from django.utils import timezone
from django.core.management import BaseCommand, CommandError
from frontend.models import Resource, UserROI
from frontend.serializers import ResourceWithTaggingsSerializer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-f', '--format', choices=['jsonl'], default='jsonl')
        parser.add_argument('-o', '--output', type=str, default='/dump')
        parser.add_argument('--size', type=int, default=1000)

    def handle(self, *args, **options):
        start_time = timezone.now()

        objects = Resource.objects.filter(
                Q(collection__isnull=True)
                | Q(collection__access='O')
            ) \
            .exclude(hash_id__exact='') \
            .prefetch_related(
                'taggings',
                'rois',
            )

        output = options['output']

        if os.path.isdir(output):
            suffix = start_time.strftime('%Y%m%d%H%M%S')
            file_name = f"os-dump_{suffix}.{options['format']}"

            output = os.path.join(output, file_name)

        with open(output, 'w', encoding='utf-8') as file_obj:
            for i in range(0, objects.count(), options['size']):
                chunk = objects.all()[i:(i + options['size'])]
                chunk = ResourceWithTaggingsSerializer(chunk, many=True)

                if options['format'] == 'jsonl':
                    try:
                        for resource in chunk.data:
                            file_obj.write(f'{json.dumps(resource)}\n')
                    except Exception as error:
                        logger.error(traceback.format_exc())

        end_time = timezone.now()
        duration = end_time - start_time

        txt = f'Export took {duration.total_seconds()} seconds.'
        self.stdout.write(self.style.SUCCESS(txt))