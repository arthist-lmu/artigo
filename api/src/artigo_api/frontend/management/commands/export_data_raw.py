import os
import gzip
import logging
import warnings

from django.db import router
from django.apps import apps
from django.utils import timezone
from django.core import serializers
from django.core.management.base import CommandError
from django.core.management.commands.dumpdata import Command as BaseCommand
from django.core.management.utils import parse_apps_and_model_labels

try:
    import bz2

    has_bz2 = True
except ImportError:
    has_bz2 = False

try:
    import lzma

    has_lzma = True
except ImportError:
    has_lzma = False

logger = logging.getLogger(__name__)


class ProxyModelWarning(Warning):
    pass


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        def get_objects(count_only=False):
            '''
            Collate the objects to be serialized. If count_only is True, just
            count the number of objects to be serialized.
            '''
            if use_natural_foreign_keys:
                models = serializers.sort_dependencies(
                    app_list.items(), allow_cycles=True
                )
            else:
                # There is no need to sort dependencies when natural foreign
                # keys are not used.
                models = []

                for app_config, model_list in app_list.items():
                    if model_list is None:
                        models.extend(app_config.get_models())
                    else:
                        models.extend(model_list)

            for model in models:
                if model in excluded_models:
                    continue

                if model._meta.proxy and model._meta.proxy_for_model not in models:
                    warnings.warn(
                        '%s is a proxy model and won\'t be serialized.'
                        % model._meta.label,
                        category=ProxyModelWarning,
                    )

                if not model._meta.proxy and router.allow_migrate_model(using, model):
                    if use_base_manager:
                        objects = model._base_manager
                    else:
                        objects = model._default_manager

                    queryset = objects.using(using).order_by(model._meta.pk.name)

                    if primary_keys:
                        queryset = queryset.filter(pk__in=primary_keys)

                    if count_only:
                        yield queryset.order_by().count()
                    else:
                        if model.__name__ == 'CustomUser':
                            yield queryset, ('is_anonymous',)
                        else:
                            yield queryset, None


        start_time = timezone.now()

        format = options['format']
        indent = options['indent']
        using = options['database']
        excludes = options['exclude']
        output = options['output']
        show_traceback = options['traceback']
        use_natural_foreign_keys = options['use_natural_foreign_keys']
        use_natural_primary_keys = options['use_natural_primary_keys']
        use_base_manager = options['use_base_manager']
        pks = options['primary_keys']

        if os.path.isdir(output):
            suffix = start_time.strftime('%Y%m%d%H%M%S')
            file_name = f"os-dump-raw_{suffix}.{options['format']}"

            output = os.path.join(output, file_name)

        if pks:
            primary_keys = [pk.strip() for pk in pks.split(',')]
        else:
            primary_keys = []

        excluded_models, excluded_apps = parse_apps_and_model_labels(excludes)

        if not app_labels:
            if primary_keys:
                raise CommandError('You can only use --pks option with one model')

            app_list = dict.fromkeys(
                app_config
                for app_config in apps.get_app_configs()
                if app_config.models_module is not None
                and app_config not in excluded_apps
            )
        else:
            if len(app_labels) > 1 and primary_keys:
                raise CommandError('You can only use --pks option with one model')

            app_list = {}

            for label in app_labels:
                try:
                    app_label, model_label = label.split('.')

                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError as e:
                        raise CommandError(str(e))

                    if app_config.models_module is None or app_config in excluded_apps:
                        continue

                    try:
                        model = app_config.get_model(model_label)
                    except LookupError:
                        raise CommandError(
                            'Unknown model: %s.%s' % (app_label, model_label)
                        )

                    app_list_value = app_list.setdefault(app_config, [])

                    # We may have previously seen an 'all-models' request for
                    # this app (no model qualifier was given). In this case
                    # there is no need adding specific models to the list.
                    if app_list_value is not None and model not in app_list_value:
                        app_list_value.append(model)
                except ValueError:
                    if primary_keys:
                        raise CommandError(
                            'You can only use --pks option with one model'
                        )

                    # This is just an app - no model qualifier
                    app_label = label

                    try:
                        app_config = apps.get_app_config(app_label)
                    except LookupError as e:
                        raise CommandError(str(e))

                    if app_config.models_module is None or app_config in excluded_apps:
                        continue
                    app_list[app_config] = None

        # Check that the serialization format exists; this is a shortcut to
        # avoid collating all the objects and _then_ failing.
        if format not in serializers.get_public_serializer_formats():
            try:
                serializers.get_serializer(format)
            except serializers.SerializerDoesNotExist:
                pass

            raise CommandError('Unknown serialization format: %s' % format)

        try:
            self.stdout.ending = None
            progress_output = None
            object_count = 0

            # If dumpdata is outputting to stdout, there is no way to display progress
            if output and self.stdout.isatty() and options['verbosity'] > 0:
                progress_output = self.stdout
                object_count = sum(get_objects(count_only=True))

            if output:
                file_root, file_ext = os.path.splitext(output)
                compression_formats = {
                    '.bz2': (open, {}, file_root),
                    '.gz': (gzip.open, {}, output),
                    '.lzma': (open, {}, file_root),
                    '.xz': (open, {}, file_root),
                    '.zip': (open, {}, file_root),
                }

                if has_bz2:
                    compression_formats['.bz2'] = (bz2.open, {}, output)

                if has_lzma:
                    compression_formats['.lzma'] = (
                        lzma.open,
                        {'format': lzma.FORMAT_ALONE},
                        output,
                    )
                    compression_formats['.xz'] = (lzma.open, {}, output)

                try:
                    open_method, kwargs, file_path = compression_formats[file_ext]
                except KeyError:
                    open_method, kwargs, file_path = (open, {}, output)

                if file_path != output:
                    file_name = os.path.basename(file_path)
                    warnings.warn(
                        f'Unsupported file extension ({file_ext}). '
                        f'Fixtures saved in \'{file_name}\'.',
                        RuntimeWarning,
                    )

                stream = open_method(file_path, 'wt', **kwargs)
            else:
                stream = None

            try:
                for objects, fields in get_objects():
                    self.stdout.write(f'Processed fields: {fields}.')

                    serializers.serialize(
                        format,
                        objects,
                        indent=indent,
                        use_natural_foreign_keys=use_natural_foreign_keys,
                        use_natural_primary_keys=use_natural_primary_keys,
                        stream=stream or self.stdout,
                        # progress_output=progress_output,
                        # object_count=object_count,
                        fields=fields,
                    )
            finally:
                if stream:
                    stream.close()

            end_time = timezone.now()
            duration = end_time - start_time

            txt = f'Export took {duration.total_seconds()} seconds.'
            self.stdout.write(self.style.SUCCESS(txt))
        except Exception as e:
            self.stdout.write(f'Export failed with error: {e}.')

            if show_traceback:
                raise

            raise CommandError('Unable to serialize database: %s' % e)
