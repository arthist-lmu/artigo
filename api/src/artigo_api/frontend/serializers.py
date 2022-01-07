# from frontend.models import *
from rest_framework import serializers

# TODO: update fields according to model changes
from frontend.models import *


class InstitutionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Institution
    fields = ['id', 'name', 'institution_url', 'resource_url']

  def to_representation(self, data):
    data = super().to_representation(data)
    data['name'] = data['name'].lower()

    return data


# class WebPagesSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = WebPages
#     fields = ('id', 'about', 'url', 'language')


class LocationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Location
    fields = ['id', 'name', 'country']


class ArtTechniqueSerializer(serializers.ModelSerializer):
  class Meta:
    model = ArtTechnique
    fields = ['id', 'name', 'language']


class ArtMovementSerializer(serializers.ModelSerializer):
  class Meta:
    model = ArtMovement
    fields = ['id', 'name', 'language']


class ArtStyleSerializer(serializers.ModelSerializer):
  class Meta:
    model = ArtStyle
    fields = ['id', 'name', 'language']


# class QuestionSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Question
#     fields = ('id', 'name', 'language')


class CreatorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Creator
    fields = ['id', 'name', 'born', 'died', 'nationality', 'locations', 'techniques']


class TitleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Title
    fields = ['id', 'name', 'language', 'technique', 'style', 'movement']


class ResourceSerializer(serializers.ModelSerializer):
  creators = CreatorSerializer(many=True)
  titles = TitleSerializer(many=True)
  # institution = InstitutionSerializer()

  class Meta:
    model = Resource
    fields = [
      'id', 'hash_id', 'titles', 'creators',
      'location', 'institution', 'origin',
      'enabled', 'media_type'
    ]
    read_only_fields = [
      'titles', 'creators', 'institution',
    ]

  def to_representation(self, data):
    data = super().to_representation(data)

    return data


class GameroundWithResourceSerializer(ResourceSerializer):
  # tags = serializers.ReadOnlyField()
  gameround = serializers.ReadOnlyField()

  class Meta(ResourceSerializer.Meta):
    fields = ResourceSerializer.Meta.fields + ['gameround'] # + ['tags']

  def to_representation(self, data):
    data = super().to_representation(data)
    data['gameround'] = GameroundSerializer(data['gameround']).data

    return data


class TagSerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=256)
  language = serializers.CharField(max_length=256)

  class Meta:
    model = Tag
    fields = ('__all__')

  def to_representation(self, data):
    data = super().to_representation(data)
    data['name'] = data['name'].lower()
    
    return data


class TabooTagSerializer(serializers.ModelSerializer):
  id = serializers.ReadOnlyField(source='tag_id')
  name = serializers.ReadOnlyField(source='tag__name')
  language = serializers.ReadOnlyField(source='tag__language')
  # TODO: Implement count
  count = serializers.IntegerField()

  class Meta:
    model = Tagging
    fields = ['id', 'name', 'language', 'count']

  def to_representation(self, data):
    data = super().to_representation(data)
    data['name'] = data['name'].lower()

    return data


class TaggingSerializer(serializers.ModelSerializer):
  tag = TagSerializer(read_only=True)

  class Meta:
    model = Tagging
    fields = ['id', 'tag', 'gameround', 'resource']

  def to_representation(self, data):
    data = super().to_representation(data)
    # data['tag'] = data['tag'].lower()

    return data


class GametypeSerializer(serializers.ModelSerializer):

  class Meta:
    model = Gametype
    fields = ['id', 'name', 'rounds', 'round_duration']

  def to_representation(self, data):
    data = super().to_representation(data)
    # data['id'] = data['id'].lower()

    return data


class GamesessionSerializer(serializers.ModelSerializer):
  gametype = GametypeSerializer(read_only=True)

  class Meta:
    model = Gamesession
    fields = ['id', 'user', 'gametype', 'created']

  def to_representation(self, data):
    data = super().to_representation(data)
    # data['id'] = data['id'].lower()

    return data


class GametypeWithGamesessionSerializer(serializers.ModelSerializer):
  gametypes = serializers.SerializerMethodField()

  class Meta:
    model = Gamesession
    fields = ['id', 'user', 'gametype', 'created']

  def get_gametype(self, obj):
    data = GametypeSerializer(obj.gametype.all(), many=True).data
    return data

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class GamesessionSerializer2(serializers.ModelSerializer):
  gametype = GametypeSerializer(read_only=True)

  class Meta:
    model = Gamesession
    fields = ['gametype', 'created']

  def to_representation(self, data):
    data = super().to_representation(data)
    # data['id'] = data['id'].lower()

    return data


class GamesessionWithGameroundSerializer(serializers.ModelSerializer):
  gametype = GametypeSerializer(read_only=True)
  gameround = serializers.ReadOnlyField(source='gameround')

  class Meta:
    model = Gamesession
    fields = ['id', 'user', 'gametype', 'created']

  def to_representation(self, data):
    data = super().to_representation(data)

    return data


class GameroundSerializer(serializers.ModelSerializer):
  gamesession = GamesessionSerializer(read_only=True)

  class Meta:
    model = Gameround
    fields = ['id', 'user', 'gamesession', 'created', 'score']

  def to_representation(self, data):
    data = super().to_representation(data)
    # data['id'] = data['id'].lower()

    return data


# class CombinedTaggingSerializer(serializers.ModelSerializer):
#   combined_tag = TagSerializer(read_only=True)
#
#   class Meta:
#     model = CombinedTagging
#     fields = ('id', 'first_tag', 'second_tag')


class TagCountSerializer(serializers.ModelSerializer):
  """Serializer with a count of a specific tag (over all resources)
  e.g. tag: baum; count: x
  """
  tag = TagSerializer(read_only=True)
  tag_count = serializers.SerializerMethodField('get_tag_count')

  class Meta:
    model = Tagging
    fields = ('id', 'tag', 'gameround', 'resource', 'tag_count')

  def get_tag_count(self, obj):
    # return obj.tag.all().count()
    tag_count = Tagging.objects.filter(tag=obj.tag).count()
    return tag_count

  def to_representation(self, data):
    data = super().to_representation(data)
    # data['tag'] = data['tag'].lower()
    
    return data


class ResourceWithTaggingsSerializer(ResourceSerializer):
  """Serializer used to send taggings to DB with Resource that got tagged with them"""
  taggings = TaggingSerializer(read_only=True)

  class Meta(ResourceSerializer.Meta):
    fields = ResourceSerializer.Meta.fields + ['taggings']

  def to_representation(self, data):
    data = super().to_representation(data)
    
    return data


class ResourceWithTagsSerializer(ResourceSerializer):
  """Serializer used to send tags to DB with Resource that got tagged with them"""
  tags = serializers.ReadOnlyField()

  class Meta(ResourceSerializer.Meta):
    fields = ResourceSerializer.Meta.fields + ['tags']

  def to_representation(self, data):
    data = super().to_representation(data)
    data['tags'] = TagCountSerializer(data['tags'], many=True).data

    return data
