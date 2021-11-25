# from frontend.models import *
from rest_framework import serializers

# TODO: update fields according to model changes
from frontend.models import *


class InstitutionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Institution
    fields = ('id', 'name', 'institution_url', 'resource_url')


# class WebPagesSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = WebPages
#     fields = ('id', 'about', 'url', 'language')


class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Location
    fields = ('id', 'name', 'country')


class ArtTechniqueSerializer(serializers.ModelSerializer):
  class Meta:
    model = ArtTechnique
    fields = ('id', 'name', 'language')


class ArtMovementSerializer(serializers.ModelSerializer):
  class Meta:
    model = ArtMovement
    fields = ('id', 'name', 'language')


class ArtStyleSerializer(serializers.ModelSerializer):
  class Meta:
    model = ArtStyle
    fields = ('id', 'name', 'language')


# class QuestionSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Question
#     fields = ('id', 'name', 'language')


class CreatorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Creator
    fields = ('id', 'name', 'born', 'died', 'nationality', 'locations', 'techniques')


class TitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Title
    fields = ('id', 'name', 'language', 'technique', 'style', 'movement')


class ResourceSerializer(serializers.ModelSerializer):
  creators = CreatorSerializer(many=True)
  titles = TitleSerializer(many=True)
  institution = InstitutionSerializer()

  class Meta:
    model = Resource
    fields = (
      'id', 'hash_id', 'titles', 'creators',
      'location', 'institution', 'origin',
      'enabled', 'media_type'
    )
    read_only_fields = (
      'titles', 'creators', 'institution',
    )

  def to_representation(self, data):
    data = super().to_representation(data)
    data['institution']['name'] = data['institution']['name'].title()

    return data


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ('id', 'name', 'language')

  def to_representation(self, data):
    data = super().to_representation(data)
    data['name'] = data['name'].lower()
    
    return data


class TaggingSerializer(serializers.ModelSerializer):
  tag = TagSerializer(read_only=True)

  class Meta:
    model = Tagging
    fields = ('id', 'tag')


class GametypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Gametype
    fields = ('id', 'rounds', 'round_duration')


# class CombinedTaggingSerializer(serializers.ModelSerializer):
#   combined_tag = TagSerializer(read_only=True)
#
#   class Meta:
#     model = CombinedTagging
#     fields = ('id', 'first_tag', 'second_tag')


class TagCountSerializer(serializers.ModelSerializer):
  id = serializers.ReadOnlyField(source='tag_id')
  name = serializers.ReadOnlyField(source='tag__name')
  language = serializers.ReadOnlyField(source='tag__language')
  count = serializers.IntegerField()

  class Meta:
    model = Tagging
    fields = ('id', 'name', 'language', 'count')

  def to_representation(self, data):
    data = super().to_representation(data)
    data['name'] = data['name'].lower()
    
    return data


class ResourceWithTaggingsSerializer(ResourceSerializer):
  tags = serializers.ReadOnlyField()

  class Meta(ResourceSerializer.Meta):
    fields = ResourceSerializer.Meta.fields + ('tags',)

  def to_representation(self, data):
    data = super().to_representation(data)
    data['tags'] = TagCountSerializer(data['tags'], many=True).data
    
    return data
