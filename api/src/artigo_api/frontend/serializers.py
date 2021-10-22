from frontend.models import *
from rest_framework import serializers


class SourceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Source
    fields = ('id', 'name', 'url')


class CreatorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Creator
    fields = ('id', 'name')


class TitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Title
    fields = ('id', 'name', 'language')


class ResourceSerializer(serializers.ModelSerializer):
  creators = CreatorSerializer(many=True)
  titles = TitleSerializer(many=True)
  source = SourceSerializer()

  class Meta:
    model = Resource
    fields = (
      'id', 'hash_id', 'titles', 'creators',
      'location', 'institution', 'source',
    )
    read_only_fields = (
      'titles', 'creators', 'source',
    )

  def to_representation(self, data):
    data = super().to_representation(data)
    data['source']['name'] = data['source']['name'].title()

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
