from .models import *
from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [f.name for f in model._meta.fields]
        super().__init__(model, admin_site)


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
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('creators', 'titles')

        return qs

    def creator(self, obj):
        return list(obj.creators.all())

    def title(self, obj):
        return list(obj.titles.all())


@admin.register(Title)
class TitleAdmin(CustomModelAdmin):
    pass


@admin.register(Gametype)
class GametypeAdmin(CustomModelAdmin):
    pass


@admin.register(Gamesession)
class GamesessionAdmin(CustomModelAdmin):
    pass


@admin.register(Gameround)
class GameroundAdmin(CustomModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(CustomModelAdmin):
    pass


@admin.register(Tagging)
class TaggingAdmin(CustomModelAdmin):
    pass
