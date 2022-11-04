from .models import *
from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [f.name for f in model._meta.fields]
        super().__init__(model, admin_site)


@admin.register(CustomUser)
class UserAdmin(CustomModelAdmin):
    pass

    
@admin.register(Source)
class SourceAdmin(CustomModelAdmin):
    pass


@admin.register(Creator)
class CreatorAdmin(CustomModelAdmin):
    pass


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    fields = [f.name for f in Resource._meta.fields]
    list_display = ['id', 'creator', 'title'] + fields[1:]

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
class GameroundAdmin(admin.ModelAdmin):
    fields = [f.name for f in Gameround._meta.fields]
    list_display = fields + ['suggester_type', 'score_type']

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
