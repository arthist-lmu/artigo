import uuid
import logging
import traceback

from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
from dj_rest_auth.registration.views import RegisterView
from frontend.serializers import (
    CustomUserDetailsSerializer,
    CustomRegisterSerializer,
    CustomPasswordResetSerializer,
)
from frontend.models import (
    CustomUser,
    Gamesession,
    Gameround,
    UserTagging,
)


logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    '''
    Login user.
    '''

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        previous_user = request.user
        self.login()
        current_user = request.user

        if previous_user is not None and previous_user.is_anonymous:
            for x in previous_user._meta.related_objects:
                if x.related_model._meta.app_label == 'frontend':
                    try:
                        x.related_model.objects \
                            .filter(user=previous_user) \
                            .update(user=current_user)
                    except Exception as error:
                        logger.info(error)

            CustomUser.objects.filter(id=previous_user.id) \
                .delete()

        return self.get_response()


@extend_schema(methods=['GET'], exclude=True)
class CustomLogoutView(LogoutView):
    '''
    Logout user.
    '''


class CustomRegisterView(RegisterView):
    '''
    Register user.
    '''

    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('is_anonymous'):
            is_valid = False

            while not is_valid:
                request = self.create_anonymous(request)

                try:
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)

                    is_valid = True
                except:
                    pass
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(
                status=status.HTTP_204_NO_CONTENT,
                headers=headers,
            )

        return response

    def create_anonymous(self, request):
        username = uuid.uuid4().hex[:15]

        request.data['username'] = username
        request.data['email'] = f'{username}@artigo.org'
        request.data['password1'] = uuid.uuid4().hex
        request.data['password2'] = request.data['password1']

        return request


@extend_schema(methods=['GET', 'PUT', 'PATCH'], exclude=True)
class CustomUserDetailsView(UserDetailsView):
    '''
    View user details.
    '''

    serializer_class = CustomUserDetailsSerializer


@extend_schema(methods=['POST'], exclude=True)
class CustomPasswordResetView(PasswordResetView):
    '''
    Reset password.
    '''

    serializer_class = CustomPasswordResetSerializer


@extend_schema(methods=['POST'], exclude=True)
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    '''
    Confirm password reset.
    '''


@extend_schema(methods=['POST'], exclude=True)
class CustomPasswordChangeView(PasswordChangeView):
    '''
    Change password.
    '''
