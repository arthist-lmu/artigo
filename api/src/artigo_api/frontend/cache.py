from django.core.cache import cache
from django.db.models import Count
from frontend.models import Resource, UserTagging


def name(func=None):
    def wrapper(*args, **kwargs):
        try:
            name = func.__func__.__qualname__
        except:
            name = func.__qualname__

        return func(*args, **kwargs, name=name)

    return wrapper


@name
def resource_count(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None:
        values = Resource.objects.latest('id').id

        cache.set(kwargs['name'], values, 60 * 60 * 24)

    return values


@name
def resource_tagging_count(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None:
        values = UserTagging.objects.values('resource') \
            .exclude(resource__hash_id__exact='') \
            .annotate(
                count_tags=Count('tag', distinct=True),
                count_taggings=Count('tag'),
            )

        cache.set(kwargs['name'], values, 60 * 60 * 24)

    return values


@name
def resource_roi_count(**kwargs):
    values = cache.get(kwargs['name'])

    if values is None:
        values = UserROI.objects.values('resource') \
            .exclude(resource__hash_id__exact='') \
            .annotate(
                count_tags=Count('tag', distinct=True),
                count_rois=Count('tag'),
            )

        cache.set(kwargs['name'], values, 60 * 60 * 24)

    return values
