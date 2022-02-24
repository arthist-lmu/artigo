import logging
import traceback

from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
from frontend.serializers import CustomUserDetailsSerializer

logger = logging.getLogger(__name__)


@extend_schema(methods=['GET', 'POST'], exclude=True)
class UserView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            raise APIException('not_authenticated')

        try:
            user = request.user

            return Response({
                'username': user.get_username(),
                'email': user.email,
                'date_joined': user.date_joined,
            })
        except Exception as e:
            logger.error(traceback.format_exc())

        raise APIException('unknown_error')

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }

        return Response(content)


class CustomLoginView(LoginView):
    '''
    Login user.
    '''


@extend_schema(methods=['GET'], exclude=True)
class CustomLogoutView(LogoutView):
    '''
    Logout user.
    '''


class CustomRegisterView(RegisterView):
    '''
    Register user.
    '''


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
