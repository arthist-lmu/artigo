import logging

from django.conf import settings
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from dj_rest_auth.forms import AllAuthPasswordResetForm
from frontend.models import CustomUser

try:
    from allauth.account import app_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import (
        user_pk_to_url_str,
        user_username,
    )
    from allauth.utils import build_absolute_uri
except ImportError:
    raise ImportError('`allauth` needs to be installed.')

logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data['email']
        current_site = get_current_site(request)

        token_generator = kwargs.get(
            'token_generator',
            default_token_generator
        )

        for user in self.users:
            temp_key = token_generator.make_token(user)

            path = reverse(
                'password_reset_confirm',
                args=[user_pk_to_url_str(user), temp_key],
            )

            url = build_absolute_uri(request, path)

            # address locale-specific frontend path
            lang = request.data.get('lang', 'en')
            path = path.replace('auth/', f'{lang}/')
            frontend_url = f'{settings.FRONTEND_URL}{path}'

            context = {
                'current_site': current_site,
                'password_reset_frontend_url': frontend_url,
                'password_reset_url': url,
                'request': request,
                'user': user,
            }

            if app_settings.AUTHENTICATION_METHOD != \
                    app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)

            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )

        return self.cleaned_data['email']
