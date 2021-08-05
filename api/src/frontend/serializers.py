from frontend.models import *
from rest_framework import serializers


class CreatorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Creator
    fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Title
    fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Source
    fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
  creators = CreatorSerializer(read_only=True, many=True)
  titles = TitleSerializer(read_only=True, many=True)
  source = SourceSerializer(read_only=True)

  class Meta:
    model = Resource
    fields = (
      'id', 'hash_id', 'titles', 'creators',
      'location', 'institution', 'source',
    )

  def to_representation(self, data):
    data = super().to_representation(data)
    data['source']['name'] = data['source']['name'].title()

    return data


class TaggingSerializer(serializers.ModelSerializer):
  id = serializers.ReadOnlyField(source='tag_id')
  name = serializers.ReadOnlyField(source='tag__name')
  n = serializers.IntegerField()

  class Meta:
    model = Tagging
    fields = ('id', 'name', 'n')

  def to_representation(self, data):
    data = super().to_representation(data)
    data['name'] = data['name'].lower()
    
    return data
