import logging
import traceback

from itertools import groupby
from rest_framework import serializers
from django.conf import settings
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

        if hasattr(get_user_model(), 'n_rois'):
            fields.append('n_rois')

        if hasattr(get_user_model(), 'n_taggings'):
            fields.append('n_taggings')

        if hasattr(get_user_model(), 'n_annotations'):
            fields.append('n_annotations')

        if hasattr(get_user_model(), 'n_resources'):
            fields.append('n_resources')

        if hasattr(get_user_model(), 'n_collections'):
            fields.append('n_collections')

        if hasattr(get_user_model(), 'n_gamesessions'):
            fields.append('n_gamesessions')

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
            except DjangoValidationError as error:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(error)
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


class CollectionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionTitle
        fields = '__all__'


class CollectionCountSerializer(serializers.ModelSerializer):
    titles = CollectionTitleSerializer(many=True)
    resources = serializers.ReadOnlyField(source='resource_ids')
    count_taggings = serializers.IntegerField(required=False)
    count_roi_taggings = serializers.IntegerField(required=False)

    class Meta:
        model = Collection
        fields = (
            'hash_id',
            'titles',
            'access',
            'status',
            'progress',
            'created',
            'resources',
            'count_taggings',
            'count_roi_taggings',
        )

    def to_representation(self, data):
        data = super().to_representation(data)

        data['title'] = {x['language']: x['name'] for x in data['titles']}

        try:
            resource = Resource.objects.get(id=data['resources'][0])
            data['path'] = media_url_to_image(resource.hash_id)
        except:
            pass

        return data


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


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
        )


class ResourceSerializer(serializers.ModelSerializer):
    creators = CreatorSerializer(many=True, required=False)
    titles = TitleSerializer(many=True, required=False)
    source = SourceSerializer(required=False)

    class Meta:
        model = Resource
        fields = (
            'id',
            'collection_id',
            'hash_id',
            'titles',
            'creators',
            'location',
            'institution',
            'source',
        )

    def to_representation(self, data):
        data = super().to_representation(data)

        if data.get('source') is not None:
            data['source']['name'] = data['source']['name'].title()

        data['path'] = media_url_to_image(data['hash_id'])

        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

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
    tag_list = serializers.ReadOnlyField()
    roi_list = serializers.ReadOnlyField()

    class Meta(ResourceSerializer.Meta):
        fields = ResourceSerializer.Meta.fields
        fields += ('tag_list', 'roi_list',)

    def to_representation(self, data):
        data = super().to_representation(data)
        
        roi_list = {roi['tag_id']: roi for roi in data['roi_list']}
        data['tags'] = TagCountSerializer(data['tag_list'], many=True).data

        for tag in data['tags']:
            values = roi_list.get(tag['id'])

            if values:
                tag['regions'] = []

                for value in zip(
                    values['x'],
                    values['y'],
                    values['width'],
                    values['height'],
                ):
                    tag['regions'].append({
                        'x': value[0],
                        'y': value[1],
                        'width': value[2],
                        'height': value[3],
                    })

        data.pop('tag_list', None)
        data.pop('roi_list', None)
        
        data.pop('collection_id', None)

        return data


class UserTaggingCountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='user_id')
    username = serializers.ReadOnlyField(source='user__username')
    is_anonymous = serializers.ReadOnlyField(source='user__is_anonymous')
    sum_score = serializers.IntegerField()
    sum_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'is_anonymous',
            'sum_score',
            'sum_count',
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
    collection_id = serializers.ReadOnlyField(source='resource__collection_id')
    resource_id = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField(source='tag_id')
    name = serializers.ReadOnlyField(source='tag__name')
    score = serializers.ReadOnlyField()

    class Meta:
        model = UserTagging
        fields = (
            'collection_id',
            'resource_id',
            'id',
            'name',
            'score',
        )
        list_serializer_class = ResourceTagListSerializer


class SessionCountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='gamesession_id')
    created = serializers.ReadOnlyField(source='gamesession__created')
    resources = serializers.ReadOnlyField(source='resource_ids')
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

        try:
            resource = Resource.objects.get(id=data['resources'][0])
            data['path'] = media_url_to_image(resource.hash_id)
        except:
            pass

        return data
