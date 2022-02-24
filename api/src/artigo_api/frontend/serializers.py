from frontend.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import UserDetailsSerializer

UserModel = get_user_model()


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []

        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)

        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)

        if hasattr(UserModel, 'is_superuser'):
            extra_fields.append('is_superuser')

        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')

        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')

        if hasattr(UserModel, 'date_joined'):
            extra_fields.append('date_joined')

        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


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


class UserTaggingCountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user__username')
    count_taggings = serializers.IntegerField()
    count_gamerounds = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ('name', 'count_taggings', 'count_gamerounds')
