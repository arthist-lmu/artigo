from datetime import datetime

from rest_framework import serializers, fields, request
from frontend.views import tag_service

# TODO: update fields according to model changes
from frontend.models import *
from rest_framework.relations import StringRelatedField, SlugRelatedField


class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'is_superuser']

  def create(self, validated_data):
    user_data = validated_data.pop('user')
    CustomUser.objects.create(**user_data)
    return user_data

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


class TagSerializer(serializers.ModelSerializer):

  class Meta:
    model = Tag
    fields = ('name', 'language')

  def create(self, validated_data):
    tag_data = validated_data.pop('tag')
    Tag.objects.create(**tag_data)
    return tag_data

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
  user = CustomUserSerializer(required=False, read_only=True)

  class Meta:
    model = Gamesession
    fields = ['id', 'user', 'gametype', 'created']

  def create(self, validated_data):
    gamesession_data = validated_data.pop('gamesession')
    Gamesession.objects.create(**gamesession_data)
    return gamesession_data

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class GameroundSerializer(serializers.ModelSerializer):
  gamesession = GamesessionSerializer(read_only=True)
  user = CustomUserSerializer(required=False, read_only=True)
  tags_to_compare = serializers.SerializerMethodField('get_tags_to_compare')

  class Meta:
    model = Gameround
    fields = ['id', 'user', 'gamesession', 'created', 'score', 'tags_to_compare']

  def get_tags_to_compare(self, round):
    taggings = round.tags
    return taggings

  def create(self, validated_data):
    gamesessions_data = validated_data.pop('gamesessions')
    gameround = Gameround.objects.create(**validated_data)
    for gamesession_data in gamesessions_data:
      Gameround.objects.create(gameround=gameround, **gamesession_data)
    return gameround

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class TaggingSerializer(serializers.ModelSerializer):
  # tag_id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),required=False,source='tag',write_only=False)
  tag = TagSerializer(required=False, write_only=False)
  resource_id = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all(),
                                                   required=True,
                                                   source='resource',
                                                   write_only=False)
  gameround_id = serializers.PrimaryKeyRelatedField(queryset=Gameround.objects.all(),
                                                    required=False,
                                                    source='gameround',
                                                    write_only=False)
  user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),
                                               required=False,
                                               source='user',
                                               write_only=False)

  class Meta:
    model = Tagging
    fields = ('id', 'user_id', 'gameround_id', 'resource_id', 'tag', 'created', 'score', 'origin')
    depth = 1

  def create(self, validated_data):
    """Create and return a new tagging"""

    tag_data = validated_data.pop('tag', None)
    if tag_data:
      tag = Tag.objects.get_or_create(**tag_data)[0]
      validated_data['tag'] = tag

    # tagging = Tagging.objects.create(**validated_data)

    tagging = Tagging(
      user=validated_data.get("user"),
      gameround=validated_data.get("gameround"),
      resource=validated_data.get("resource"),
      tag=validated_data.get("tag"),
      created=datetime.now(),
      score=validated_data.get("score"),
      origin=validated_data.get("origin")
    )

    # gameround_data = validated_data.pop('gameround', None)
    # if gameround_data:
    #   gameround = Gameround.objects.get_or_create(**gameround_data)[0]
    #   validated_data['gameround'] = gameround
    #
    # resource_data = validated_data.pop('resource', None)
    # if tag_data:
    #   resource = Resource.objects.get_or_create(**resource_data)[0]
    #   validated_data['resource'] = resource
    #
    # user_data = validated_data.pop('user', None)
    # if user_data:
    #   user = CustomUser.objects.get_or_create(**user_data)[0]
    #   validated_data['user'] = user

    tagging.save()

    return tagging

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class TaggingGetSerializer(serializers.ModelSerializer):
  """Tagging Serializer to be used only for GET request"""
  tag = StringRelatedField()
  resource = serializers.PrimaryKeyRelatedField(read_only=True) # StringRelatedField returns hash-id
  gameround = serializers.PrimaryKeyRelatedField(read_only=True)
  user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

  class Meta:
    model = Tagging
    fields = ('id', 'user', 'gameround', 'resource', 'tag', 'created', 'score', 'origin')

  def create(self, validated_data):
    """Create and return a new tagging"""
    # TODO: TEST a bit more, might work!
    tags_data = validated_data.pop('tag')
    resources_data = validated_data.pop('resource')
    gamerounds_data = validated_data.pop('gameround')
    users_data = validated_data.pop('user')

    tagging = Tagging.objects.create(tag=tags_data, resource=resources_data, gameround=gamerounds_data, user= users_data)
    return tagging

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class CombinationSerializer(serializers.ModelSerializer):
  tag_id = serializers.PrimaryKeyRelatedField(queryset=Tagging.objects.all(),
                                              required=False,
                                              source='tagging',
                                              write_only=False)
  resource_id = serializers.PrimaryKeyRelatedField(queryset=Resource.objects.all(),
                                                   required=True,
                                                   source='resource',
                                                   write_only=False)
  gameround_id = serializers.PrimaryKeyRelatedField(queryset=Gameround.objects.all(),
                                                    required=False,
                                                    source='gameround',
                                                    write_only=False)
  user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(),
                                               required=False,
                                               source='user',
                                               write_only=False)

  class Meta:
    model = Combination
    depth = 1
    fields = ('group_id', 'user_id', 'gameround_id', 'resource_id', 'tag_id', 'created', 'score', 'origin')

  def create(self, validated_data):
    combination = Combination(
      user=validated_data.get("user"),
      gameround=validated_data.get("gameround"),
      resource=validated_data.get("resource"),
      tag_id=validated_data.get("tag_id"),
      created=datetime.now(),
      score=validated_data.get("score"),
    )
    combination.save()
    return combination

  def to_representation(self, data):
    data = super().to_representation(data)
    return data


class TagCountSerializer(serializers.ModelSerializer):
  """Serializer with a count of a specific tag (over all resources)"""
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
    suggestions = res.tags
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
