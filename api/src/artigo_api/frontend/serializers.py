import logging

from itertools import groupby
from frontend.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

try:
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

UserModel = get_user_model()

logger = logging.getLogger(__name__)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        fields = []

        if hasattr(UserModel, 'email'):
            fields.append('email')

        if hasattr(UserModel, 'username'):
            fields.append('username')

        if hasattr(UserModel, 'first_name'):
            fields.append('first_name')

        if hasattr(UserModel, 'last_name'):
            fields.append('last_name')

        if hasattr(UserModel, 'date_joined'):
            fields.append('date_joined')

        if hasattr(UserModel, 'is_superuser'):
            fields.append('is_superuser')

        if hasattr(UserModel, 'is_anonymous'):
            fields.append('is_anonymous')

        model = UserModel
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
        model = UserTagging
        fields = ('id', 'tag')


class TagCountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    language = serializers.ReadOnlyField(source='tag__language')
    count = serializers.IntegerField()

    class Meta:
        model = UserTagging
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


class UserTaggingCountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user__username')
    count_taggings = serializers.IntegerField()
    count_gamerounds = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ('name', 'count_taggings', 'count_gamerounds')


class ResourceTagListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)
        groups = groupby(data, key=lambda x: x['resource_id'])

        return [
            {
                'resource_id': key,
                'tags': [self.to_dict(x) for x in group],
            }
            for key, group in groups
        ]

    @staticmethod
    def to_dict(values):
        values = dict(values)
        values.pop('resource_id', None)

        return values


class OpponentSerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    created_after = serializers.SerializerMethodField()

    class Meta:
        model = UserTagging
        fields = ('resource_id', 'id', 'name', 'created_after')
        list_serializer_class = ResourceTagListSerializer

    def get_created_after(self, obj):
        return obj['created_after'].total_seconds()


class TabooSerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')

    class Meta:
        model = UserTagging
        fields = ('resource_id', 'id', 'name')
        list_serializer_class = ResourceTagListSerializer


class SessionSerializer(serializers.ModelSerializer):
    resource_id = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField(source='count_tags')
    score = serializers.ReadOnlyField(source='sum_score')

    class Meta:
        model = UserTagging
        fields = ('resource_id', 'count', 'score')
        list_serializer_class = ResourceTagListSerializer
