from django.urls import path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.views.generic import TemplateView, RedirectView
from drf_spectacular.views import (
    SpectacularAPIView as SchemaView,
    SpectacularRedocView as RedocView,
    SpectacularSwaggerView as SwaggerView,
)
from .views import *

urlpatterns = [
    path('game/', GameView.as_view(), name='game'),
    path('home/', HomeView.as_view(), name='home'),
    path('resource/', ResourceView.as_view(), name='resource'),
    path('reconcile/', ReconcileView.as_view(), name='reconcile'),
    path('reconcile/add/', ReconcileAddView.as_view(), name='reconcile_add'),
    path('reconcile/remove/', ReconcileRemoveView.as_view(), name='reconcile_remove'),
    path('search/', SearchView.as_view(), name='search'),
    path('session/', SessionView.as_view(), name='session'),
    path('sessions/', SessionsView.as_view(), name='sessions'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('schema/', SchemaView.as_view(), name='schema'),
    path('schema/swagger-ui/', SwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', RedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/registration/', RegisterView.as_view(), name='registration'),
    path('auth/user/', UserDetailsView.as_view(), name='user_details'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    re_path(
        r'auth/password/reset/confirm/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    re_path(
        r'auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        TemplateView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path('auth/password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('auth/', include('dj_rest_auth.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]
