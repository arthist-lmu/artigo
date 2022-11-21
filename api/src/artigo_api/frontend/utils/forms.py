from django.conf import settings
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from dj_rest_auth.forms import AllAuthPasswordResetForm
from frontend.models import CustomUser


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
            frontend_url = f'{settings.FRONTEND_URL}/path'

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
