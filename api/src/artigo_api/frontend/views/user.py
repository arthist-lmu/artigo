import logging
import traceback

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
