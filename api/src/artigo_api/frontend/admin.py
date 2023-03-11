import csv
import logging
import datetime

from .models import *
from django.http import HttpResponse
from django.contrib import admin

logger = logging.getLogger(__name__)


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        fields = [f.name for f in self.model._meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;' \
            + 'filename={}.csv'.format(self.model._meta)

        writer = csv.writer(response)
        writer.writerow(fields)

        for obj in queryset:
            row = []

            for field in fields:
                value = getattr(obj, field)

                if isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')

                row.append(value)

            writer.writerow(row)

        return response

    export_as_csv.short_description = 'Export selected'


class CustomModelAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ['export_as_csv']

    def __init__(self, model, admin_site):
        self.list_display = [f.name for f in model._meta.fields]
        super().__init__(model, admin_site)


@admin.register(CustomUser)
class UserAdmin(CustomModelAdmin):
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin, ExportCsvMixin):
    fields = [f.name for f in Collection._meta.fields]
    list_display = ['id', 'title'] + fields[1:]
    actions = ['export_as_csv']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .prefetch_related('titles')

        return qs

    def title(self, obj):
        return list(obj.titles.all())


@admin.register(CollectionTitle)
class CollectionTitleAdmin(CustomModelAdmin):
    pass

    
@admin.register(Source)
class SourceAdmin(CustomModelAdmin):
    pass


@admin.register(Creator)
class CreatorAdmin(CustomModelAdmin):
    pass


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin, ExportCsvMixin):
    fields = [f.name for f in Resource._meta.fields]
    list_display = ['id', 'creator', 'title'] + fields[1:]
    actions = ['export_as_csv']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .prefetch_related('creators', 'titles')

        return qs

    def creator(self, obj):
        return list(obj.creators.all())

    def title(self, obj):
        return list(obj.titles.all())


@admin.register(Title)
class TitleAdmin(CustomModelAdmin):
    pass


@admin.register(GameType)
class GameTypeAdmin(CustomModelAdmin):
    pass


@admin.register(OpponentType)
class OpponentTypeAdmin(CustomModelAdmin):
    pass


@admin.register(TabooType)
class TabooTypeAdmin(CustomModelAdmin):
    pass


@admin.register(SuggesterType)
class SuggesterTypeAdmin(CustomModelAdmin):
    pass


@admin.register(ScoreType)
class ScoreTypeAdmin(CustomModelAdmin):
    pass


@admin.register(Gamesession)
class GamesessionAdmin(CustomModelAdmin):
    pass


@admin.register(Gameround)
class GameroundAdmin(admin.ModelAdmin, ExportCsvMixin):
    fields = [f.name for f in Gameround._meta.fields]
    list_display = fields + ['suggester_type', 'score_type']
    actions = ['export_as_csv']

    def get_queryset(self, request):
        qs = super().get_queryset(request) \
            .prefetch_related('suggester_types') \
            .prefetch_related('score_types')

        return qs

    def suggester_type(self, obj):
        return list(obj.suggester_types.all())

    def score_type(self, obj):
        return list(obj.score_types.all())


@admin.register(GameroundParameter)
class GameroundParameterAdmin(CustomModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(CustomModelAdmin):
    pass


@admin.register(UserTagging)
class UserTaggingAdmin(CustomModelAdmin):
    pass


@admin.register(OpponentTagging)
class OpponentTaggingAdmin(CustomModelAdmin):
    pass


@admin.register(TabooTagging)
class TabooTaggingAdmin(CustomModelAdmin):
    pass


@admin.register(UserROI)
class UserROIAdmin(CustomModelAdmin):
    pass


@admin.register(OpponentROI)
class OpponentROIAdmin(CustomModelAdmin):
    pass


@admin.register(TabooROI)
class TabooROIAdmin(CustomModelAdmin):
    pass
