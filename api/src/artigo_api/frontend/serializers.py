from datetime import datetime

from rest_framework import serializers, fields, request
from frontend.views import tag_service

# TODO: update fields according to model changes
from frontend.models import *
from rest_framework.fields import ReadOnlyField
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
  creators = serializers.ReadOnlyField(source='creator.name')
  titles = serializers.ReadOnlyField(source='title.name')

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


class TagWithIdSerializer(serializers.ModelSerializer):

  class Meta:
    model = Tag
    fields = ('id', 'name', 'language')

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
    fields = ('id', 'user', 'gamesession', 'created', 'score', 'tags_to_compare')

  def get_tags_to_compare(self, round):
    taggings = round.tags
    # coordinated_gameround_tags_list = round.taggings.all().values_list("tag__name", flat=True)
    return taggings

  def get_field_names(self, *args, **kwargs):
    field_names = self.context.get('fields', None)
    if field_names:
      return field_names
    return super(GameroundSerializer, self).get_field_names(*args, **kwargs)

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
  tag = TagSerializer(required=False, write_only=False, many=False)
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

    user = None
    request = self.context.get("request")
    if request and hasattr(request, "user"):
      user = request.user

    resource = None
    # self means it refences post request instead of get
    request = self.context.get("request")
    if request and hasattr(request, "resource"):
      resource = request.query_params("resource")

    score = 0
    resource_id = validated_data.get("resource")
    # A previously played gameround for this resource is coordinated for Tag verification
    coordinated_gameround = Gameround.objects.all().filter(taggings__resource_id=resource_id).order_by("?").first()
    # list of tag_name from coordinated gameround
    coordinated_gameround_tags = coordinated_gameround.taggings.all().values_list("tag__name", flat=True)

    tag_data = validated_data.pop('tag', None)
    if tag_data:
      # tag = Tag.objects.get_or_create(**tag_data)[0]
      tag = Tag.objects.get_or_create(
        language=tag_data['language'],
        name=tag_data['name'].upper()
      )[0]
      validated_data['tag'] = tag
      if not Tag.objects.all().filter(name=tag.name).exists():
        score = 0
      elif Tag.objects.all().filter(name=tag.name).exists():
        score += 5
      if tag.name in coordinated_gameround_tags:
        score += 25

    tagging = Tagging(
      user=user,
      gameround=validated_data.get("gameround"),
      resource=validated_data.get("resource"),
      tag=validated_data.get("tag"),
      created=datetime.now(),
      score=score,
      origin=""
    )
    tagging.save()
    return tagging

  def to_representation(self, instance):
    rep = super().to_representation(instance)
    rep['tag'] = TagSerializer(instance.tag).data
    return rep


class TaggingGetSerializer(serializers.ModelSerializer):
  """Tagging Serializer to be used only for GET request"""
  tag = StringRelatedField()
  resource = serializers.PrimaryKeyRelatedField(read_only=True)
  gameround = serializers.PrimaryKeyRelatedField(read_only=True)
  user = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

  class Meta:
    model = Tagging
    fields = ('id', 'user', 'gameround', 'resource', 'tag', 'created', 'score', 'origin')

  def create(self, validated_data):
    """Create and return a new tagging"""
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
  tag_id = TagWithIdSerializer(many=True, required=False, write_only=False)
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
    fields = ('id', 'user_id', 'gameround_id', 'resource_id', 'tag_id', 'created', 'score')

  def create(self, validated_data):
    user = None
    request = self.context.get("request")
    if request and hasattr(request, "user"):
      user = request.user

    score = 0
    resource_id = validated_data.get("resource")
    # A previously played gameround for this resource is coordinated for Tag verification
    coordinated_gameround = Gameround.objects.all().filter(taggings__resource_id=resource_id).order_by("?").first()
    # TODO: Add extra condition for Combino
    tags_to_combine = resource_id.taggings.all().values_list("tag__name", flat=True)
    # list of tag_name from coordinated gameround
    coordinated_gameround_tags = coordinated_gameround.taggings.all().values_list("tag__name", flat=True)

    combination = Combination(
      user=user,
      gameround=validated_data.get("gameround"),
      resource=validated_data.get("resource"),
      created=datetime.now(),
      score=score
    )
    combination.save()

    tag_data = validated_data.pop('tag_id', None)
    for tag_item in tag_data:
      tag = Tag.objects.get_or_create(**tag_item)[0]
      combination.tag_id.add(tag)

      if combination.tag_id.count() == 2:
        return combination

  def update(self, combination, validated_data):
    resource_id = validated_data.get("resource")
    # A previously played gameround for this resource is coordinated for Tag verification
    coordinated_gameround = Gameround.objects.all().filter(taggings__resource_id=resource_id).order_by("?").first()
    # list of tag_name from coordinated gameround
    coordinated_gameround_tags = coordinated_gameround.taggings.all().values_list("tag__name", flat=True)
    # tags to combine by the user during a game round
    tags_to_combine = resource_id.taggings.all().values_list("tag__name", flat=True)

    if not Combination.objects.all().filter(tag_id=combination.tag_id).exists():
      combination.score = 0
    elif Combination.objects.all().filter(tag_id=combination.tag_id).exists():
      combination.score += 5
    if combination.tag_id in coordinated_gameround_tags:
      combination.score += 25

    return super().update(combination, validated_data)

  def to_representation(self, instance):
    rep = super().to_representation(instance)
    rep['tag_id'] = TagWithIdSerializer(instance.tag_id.all(), many=True).data
    return rep


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
  creators = StringRelatedField(many=True)
  titles = StringRelatedField(many=True)

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


class TabooTaggingSerializer(serializers.ModelSerializer):
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
    user = None
    request = self.context.get("request")
    if request and hasattr(request, "user"):
      user = request.user

    # resource = None
    # request = self.context.get("request")
    # if request and hasattr(request, "resource"):
    #   resource = request.resource

    score = 0
    resource_id = validated_data.get("resource")
    # A previously played gameround for this resource is coordinated for Tag verification
    coordinated_gameround = Gameround.objects.all().filter(taggings__resource_id=resource_id).order_by("?").first()
    # taboo tags to be compared with entered tags
    taboo_tags = resource_id.taggings.all().values_list("tag__name", flat=True)
    # list of tag_name from coordinated gameround
    coordinated_gameround_tags = coordinated_gameround.taggings.all().values_list("tag__name", flat=True)

    tag_data = validated_data.pop('tag', None)
    if tag_data:
      # tag = Tag.objects.get_or_create(**tag_data)[0]
      tag = Tag.objects.get_or_create(
        language=tag_data['language'],
        name=tag_data['name'].upper()
      )[0]
      validated_data['tag'] = tag
      if tag.name not in taboo_tags:
        if not Tag.objects.all().filter(name=tag.name).exists():
          score = 0
        elif Tag.objects.all().filter(name=tag.name).exists():
          score += 5
        if tag.name in coordinated_gameround_tags:
          score += 25

    tagging = Tagging(
      user=user,
      gameround=validated_data.get("gameround"),
      resource=validated_data.get("resource"),
      tag=validated_data.get("tag"),
      created=datetime.now(),
      score=score,
      origin=""
    )
    tagging.save()
    return tagging

  def to_representation(self, instance):
    rep = super().to_representation(instance)
    rep['tag'] = TagSerializer(instance.tag).data
    return rep


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


class TagATagTaggingSerializer(serializers.ModelSerializer):
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
  suggested = serializers.SerializerMethodField('get_suggestions')

  class Meta:
    model = Tagging
    fields = ('id', 'user_id', 'gameround_id', 'resource_id', 'tag', 'created', 'score', 'origin', 'suggested')
    depth = 1

  def get_suggestions(self, tagging):
    return tagging.resource.taggings.all().values_list("tag__name", flat=True)

  def create(self, validated_data):
    """Create and return a new tagging"""
    user = None
    request = self.context.get("request")
    if request and hasattr(request, "user"):
      user = request.user

    # resource = None
    # request = self.context.get("request")
    # if request and hasattr(request, "resource"):
    #   resource = request.resource

    score = 0
    resource_id = validated_data.get("resource")
    # A previously played gameround for this resource is coordinated for Tag verification
    coordinated_gameround = Gameround.objects.all().filter(taggings__resource_id=resource_id).order_by("?").first()
    # tags suggested for user to choose from to tag (Tag + Resource)
    tags_suggestions = resource_id.taggings.all().values_list("tag__name", flat=True)
    # list of tag_name from coordinated gameround
    coordinated_gameround_tags = coordinated_gameround.taggings.all().values_list("tag__name", flat=True)

    tag_data = validated_data.pop('tag', None)
    if tag_data:
      # tag = Tag.objects.get_or_create(**tag_data)[0]
      tag = Tag.objects.get_or_create(
        language=tag_data['language'],
        name=tag_data['name'].upper()
      )[0]
      validated_data['tag'] = tag
      # TODO: Figure out condition for Tag to be tagged!
      if not Tag.objects.all().filter(name=tag.name).exists():
        score = 0
      elif Tag.objects.all().filter(name=tag.name).exists():
        score += 5
      if tag.name in coordinated_gameround_tags:
        score += 25

    tagging = Tagging(
      user=user,
      gameround=validated_data.get("gameround"),
      resource=validated_data.get("resource"),
      tag=validated_data.get("tag"),
      created=datetime.now(),
      score=score,
      origin=""
    )
    tagging.save()
    return tagging

  def to_representation(self, instance):
    rep = super().to_representation(instance)
    rep['tag'] = TagSerializer(instance.tag).data
    return rep


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
