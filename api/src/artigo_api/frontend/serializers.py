import logging

from itertools import groupby
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import (
    UserDetailsSerializer,
    PasswordResetSerializer,
)
from dj_rest_auth.registration.serializers import RegisterSerializer
from frontend.models import *
from frontend.utils import (
    media_url_to_image,
    CustomAllAuthPasswordResetForm,
)

try:
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError('`allauth` needs to be installed.')

logger = logging.getLogger(__name__)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        fields = []

        if hasattr(get_user_model(), 'email'):
            fields.append('email')

        if hasattr(get_user_model(), 'username'):
            fields.append('username')

        if hasattr(get_user_model(), 'first_name'):
            fields.append('first_name')

        if hasattr(get_user_model(), 'last_name'):
            fields.append('last_name')

        if hasattr(get_user_model(), 'date_joined'):
            fields.append('date_joined')

        if hasattr(get_user_model(), 'is_superuser'):
            fields.append('is_superuser')

        if hasattr(get_user_model(), 'is_anonymous'):
            fields.append('is_anonymous')

        if hasattr(get_user_model(), 'taggings'):
            fields.append('taggings')

        if hasattr(get_user_model(), 'resources'):
            fields.append('resources')

        if hasattr(get_user_model(), 'game_sessions'):
            fields.append('game_sessions')

        model = get_user_model()
        fields = ('id', *fields)
        read_only_fields = ('email',)


class CustomRegisterSerializer(RegisterSerializer):
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)

        if request.data.get('is_staff'):
            user.is_staff = True

        if request.data.get('is_anonymous'):
            user.is_anonymous = True

        if self.cleaned_data.get('password1'):
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )

        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])

        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        self.reset_form = CustomAllAuthPasswordResetForm(data=self.initial_data)
        
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value


class ListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)

        return [dict(x) for x in data]


class ResourceTagListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)

        groups = groupby(data, key=lambda x: x['resource_id'])
        groups = dict((k, list(group)) for k, group in groups)

        resource_ids = self.context.get('ids', groups.keys())

        return [
            {
                'resource_id': resource_id,
                'tags': [
                    self.to_dict(x)
                    for x in groups.get(resource_id, [])
                ],
            }
            for resource_id in resource_ids
        ]

    @staticmethod
    def to_dict(values):
        values = dict(values)
        values.pop('resource_id', None)

        return values


class TagListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)

        groups = groupby(data, key=lambda x: x['name'])
        groups = dict((k, list(group)) for k, group in groups)

        tag_names = self.context.get('names', groups.keys())

        return [
            {
                'tag_name': tag_name,
                'data': [
                    self.to_dict(x)
                    for x in groups.get(tag_name, [])
                ],
            }
            for tag_name in tag_names
        ]

    @staticmethod
    def to_dict(values):
        values = dict(values)
        values.pop('name', None)

        return values


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'url',
        )


class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = (
            'id',
            'name',
        )


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'language',
        )


class ResourceSerializer(serializers.ModelSerializer):
    creators = CreatorSerializer(many=True)
    titles = TitleSerializer(many=True)
    source = SourceSerializer()

    class Meta:
        model = Resource
        fields = (
            'id',
            'hash_id',
            'titles',
            'creators',
            'location',
            'institution',
            'source',
        )
        read_only_fields = (
            'titles',
            'creators',
            'source',
        )

    def to_representation(self, data):
        data = super().to_representation(data)
        data['source']['name'] = data['source']['name'].title()

        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'language',
        )

    def to_representation(self, data):
        data = super().to_representation(data)
        data['name'] = data['name'].lower()

        return data


class TaggingSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)

    class Meta:
        model = UserTagging
        fields = (
            'id',
            'tag',
        )


class TagCountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    language = serializers.ReadOnlyField(source='tag__language')
    count = serializers.IntegerField()

    class Meta:
        model = UserTagging
        fields = (
            'id',
            'name',
            'language',
            'count',
        )

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


class UserTaggingCountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user__username')
    count_taggings = serializers.IntegerField()
    count_gamerounds = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = (
            'name',
            'count_taggings',
            'count_gamerounds',
        )


class OpponentTagSerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    created_after = serializers.SerializerMethodField()

    class Meta:
        model = UserTagging
        fields = (
            'resource_id',
            'id',
            'name',
            'created_after',
        )
        list_serializer_class = ResourceTagListSerializer

    def get_created_after(self, obj):
        return obj['created_after'].total_seconds()


class OpponentROISerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    x = serializers.ReadOnlyField()
    y = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    created_after = serializers.SerializerMethodField()

    class Meta:
        model = UserROI
        fields = (
            'resource_id',
            'id',
            'name',
            'x',
            'y',
            'width',
            'height',
            'created_after',
        )
        list_serializer_class = ResourceTagListSerializer

    def get_created_after(self, obj):
        return obj['created_after'].total_seconds()


class TabooTagSerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')

    class Meta:
        model = UserTagging
        fields = (
            'resource_id',
            'id',
            'name',
        )
        list_serializer_class = ResourceTagListSerializer


class TabooROISerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    x = serializers.ReadOnlyField()
    y = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()

    class Meta:
        model = UserROI
        fields = (
            'resource_id',
            'id',
            'name',
            'x',
            'y',
            'width',
            'height',
        )
        list_serializer_class = ResourceTagListSerializer


class TagROISerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    x = serializers.ReadOnlyField()
    y = serializers.ReadOnlyField()
    width = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()

    class Meta:
        model = UserROI
        fields = (
            'id',
            'name',
            'x',
            'y',
            'width',
            'height',
        )
        list_serializer_class = TagListSerializer


class SessionSerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    score = serializers.ReadOnlyField()

    class Meta:
        model = UserTagging
        fields = (
            'resource_id',
            'id',
            'name',
            'score',
        )
        list_serializer_class = ResourceTagListSerializer


class SessionCountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='gamesession_id')
    created = serializers.ReadOnlyField(source='gamesession__created')
    resources = serializers.ReadOnlyField()
    annotations = serializers.ReadOnlyField()

    class Meta:
        model = Gameround
        fields = (
            'id',
            'created',
            'resources',
            'annotations',
        )
        list_serializer_class = ListSerializer

    def to_representation(self, data):
        data = super().to_representation(data)

        resource_id = data.pop('resources')[0]
        data['path'] = media_url_to_image(resource_id)

        return data
