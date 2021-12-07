from .models import *
from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [f.name for f in model._meta.fields]
        super().__init__(model, admin_site)


@admin.register(Institution)
class InstitutionAdmin(CustomModelAdmin):
    pass


@admin.register(Creator)
class CreatorAdmin(CustomModelAdmin):
    pass


@admin.register(ArtTechnique)
class ArtTechniqueAdmin(CustomModelAdmin):
    pass


@admin.register(ArtMovement)
class ArtMovementAdmin(CustomModelAdmin):
    pass


@admin.register(ArtStyle)
class ArtStyleAdmin(CustomModelAdmin):
    pass


# @admin.register(WebPages)
# class WebPagesAdmin(CustomModelAdmin):
#     pass


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass
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


# @admin.register(Gamemode)
# class GamemodeAdmin(CustomModelAdmin):
#     pass


@admin.register(Tag)
class TagAdmin(CustomModelAdmin):
    pass


@admin.register(Tagging)
class TaggingAdmin(CustomModelAdmin):
    pass


# @admin.register(CombinedTagging)
# class CombinedTaggingAdmin(CustomModelAdmin):
#     pass


# @admin.register(ChosenOrder)
# class ChosenOrderAdmin(CustomModelAdmin):
#     pass


# TODO: see how similar it has to be to the Resource admin
# @admin.register(Question)
# class QuestionAdmin(CustomModelAdmin):
#     pass
