# from frontend.models import *
from rest_framework import serializers

# TODO: update fields according to model changes
from frontend.models import *


class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'is_superuser']

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class InstitutionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Institution
    fields = ['id', 'name', 'institution_url', 'resource_url']

  def to_representation(self, data):
    data = super().to_representation(data)
    data['name'] = data['name'].lower()

    return data


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
  gameround = serializers.ReadOnlyField()

  class Meta(ResourceSerializer.Meta):
    fields = ResourceSerializer.Meta.fields + ['gameround'] # + ['tags']

  def to_representation(self, data):
    data = super().to_representation(data)
    data['gameround'] = GameroundSerializer(data['gameround']).data

    return data


class TagSerializer(serializers.ModelSerializer):
  # name = serializers.CharField(max_length=256)
  # language = serializers.CharField(max_length=256)

  class Meta:
    model = Tag
    fields = ('id', 'name', 'language')

  def create(self, validated_data):
    return Tag.objects.create(**validated_data)

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class GametypeSerializer(serializers.ModelSerializer):

  class Meta:
    model = Gametype
    fields = ['id', 'name', 'rounds', 'round_duration']

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class GamesessionSerializer(serializers.ModelSerializer):
  gametype = GametypeSerializer(read_only=True)
  user = CustomUserSerializer(read_only=True)

  class Meta:
    model = Gamesession
    fields = ['id', 'user', 'gametype', 'created']

  def to_representation(self, data):
    data = super().to_representation(data)
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
    return data


class GameroundSerializer(serializers.ModelSerializer):
  gamesession = GamesessionSerializer(read_only=True)
  user = CustomUserSerializer(read_only=True)

  class Meta:
    model = Gameround
    fields = ['id', 'user', 'gamesession', 'created', 'score']

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class TaggingSerializer(serializers.ModelSerializer):
  tag = TagSerializer(read_only=True)
  resource = ResourceSerializer(read_only=True)
  gameround = GameroundSerializer(read_only=True)

  class Meta:
    model = Tagging
    fields = ('id', 'tag', 'gameround', 'created', 'score', 'resource')

  def create(self, validated_data):
    return Tagging.objects.create(**validated_data)

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


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
    tag_count = Tagging.objects.filter(tag=obj.tag).count()
    return tag_count

  def to_representation(self, data):
    data = super().to_representation(data)
    
    return data


class TabooTagSerializer(serializers.ModelSerializer):
  creators = CreatorSerializer(many=True)
  titles = TitleSerializer(many=True)
  taboo_tags = serializers.SerializerMethodField('get_taboo_tags')

  class Meta:
    model = Resource
    fields = ['id', 'hash_id', 'titles', 'creators', 'taboo_tags']
    read_only_fields = ['titles', 'creators', 'institution']

  def get_taboo_tags(self, res):
    """
    :param res:
    :return: A list of the ids of the validated Tags (not Taggings) per Resource
    """
    taboo_tags = res.tags

    return taboo_tags

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class SuggestionsSerializer(serializers.ModelSerializer):
  creators = CreatorSerializer(many=True)
  titles = TitleSerializer(many=True)
  suggestions = serializers.SerializerMethodField('get_suggestions')

  class Meta:
    model = Resource
    fields = ['id', 'hash_id', 'titles', 'creators', 'suggestions']
    read_only_fields = ['titles', 'creators', 'institution']

  def get_suggestions(self, res):
    """
    :param res:
    :return: A list of the ids of the validated Tags (not Taggings) per Resource
    """
    # TODO: Find out where suggestions come from and improve method
    suggestions = res.tags # returns the validated tags per resource
    # cleans up sugestions list
    # TODO: Review this
    # for suggestion in suggestions:
    return suggestions

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class CombinoTagsSerializer(serializers.ModelSerializer):
  """ Serializer that returns ids of tags to be combined with a Resource for Combino """
  creators = CreatorSerializer(many=True)
  titles = TitleSerializer(many=True)
  tags_to_combine = serializers.SerializerMethodField('get_tags_to_combine')

  class Meta:
    model = Resource
    fields = ('id', 'hash_id', 'titles', 'creators', 'tags_to_combine')
    read_only_fields = ('titles', 'creators', 'institution')

  def get_tags_to_combine(self, res):
    tags_to_combine = res.tags
    return tags_to_combine

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class ResourceWithTaggingsSerializer(ResourceSerializer):
  """Serializer used to send taggings to DB with Resource that got tagged with them"""
  taggings = TaggingSerializer(read_only=True)

  class Meta(ResourceSerializer.Meta):
    fields = ResourceSerializer.Meta.fields + ['taggings']

  def to_representation(self, data):
    data = super().to_representation(data)
    
    return data


class ResourceWithTabooTaggingsSerializer(ResourceSerializer):
  """Serializer used to send a resource with its taboo taggings to the user"""
  tags = serializers.ReadOnlyField()

  class Meta(ResourceSerializer.Meta):
    fields = ResourceSerializer.Meta.fields + ['tags']

  def to_representation(self, data):
    data = super().to_representation(data)
    data['tags'] = TagCountSerializer(data['tags'], many=True).data

    return data
